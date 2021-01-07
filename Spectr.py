import sys
import os
import wave
import time
import argparse

import librosa
import librosa.display
import pyaudio
import struct

from scipy.io import wavfile
import scipy.io.wavfile as wav
from scipy import signal
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LogNorm
from matplotlib.mlab import window_hanning,specgram

class Spectrogram:
    def __init__(self):
        self.fig = plt.figure()

        self.paudio = pyaudio.PyAudio()
        self.stream = None
        
        self.file_name = None
        self.file_path = None
        self.spectro = None

        self.sample = None
        self.sample_rate = None
        self.sample_time = None
        self.samples_per_frame = 10
        self.wave_file = None
        self.MODE = 'psd'

        self.CHUNK = 4096
        self.overlap = 512
        self.nfft = 1024


    def stream_wave(self):
        stream = self.paudio.open(format=self.paudio.get_format_from_width(self.wave_file.getsampwidth()),
                channels=self.wave_file.getnchannels(),
                rate=self.wave_file.getframerate(),
                output=True)
        return stream

    def get_data(self, stream):
        input_data = self.wave_file.readframes(self.CHUNK)
        stream.write(input_data)
        data = np.frombuffer(input_data, np.int16)
        return data

    def get_spectrogram(self, data):
        spectrum, freqs, t = specgram(data, 
            window=window_hanning,
            Fs=self.sample_rate,
            NFFT=self.nfft,
            noverlap=self.overlap)
        return spectrum, freqs, t

    def update_figure(self, n):
        data = self.get_data(self.stream)
        spectrum, freqs, t = self.get_spectrogram(data)
        im_data = self.im.get_array()
        if n < self.samples_per_frame:
            im_data = np.hstack((im_data,spectrum))
            self.im.set_array(im_data)
        else:
            keep_block = spectrum.shape[1]*(self.samples_per_frame - 1)
            im_data = np.delete(im_data,np.s_[:-keep_block],1)
            im_data = np.hstack((im_data,spectrum))
            self.im.set_array(im_data)
        return self.im,

    def start_playing_music(self, url):
        self.file_path = url
        self.sample, self.sample_rate = librosa.load(self.file_path)
        self.sample_time = np.arange(0, len(self.sample)) / self.sample_rate 
        self.wave_file = wave.open(self.file_path, 'rb')

        try:
            print("[Launching Streaming]")
            self.stream = self.stream_wave()
            spectrum, freqs, t = self.get_spectrogram(self.get_data(self.stream))

            extent = (t[0], t[-1] * self.samples_per_frame, freqs[-1], freqs[0])
            self.im = plt.imshow(spectrum,
                aspect="auto",
                extent = extent,
                interpolation="none",
                cmap = "viridis",
                norm = LogNorm(vmin=.01,vmax=1))
            plt.xlabel("Time (seconds)")
            plt.ylabel("Frequency (Hz)")
            plt.title("Streaming Spectrogram")
            plt.gca().invert_yaxis()
            plt.colorbar()
            anim = animation.FuncAnimation(self.fig,
                self.update_figure,
                blit = False,
                interval=1)
            plt.show()
            print()
            print("[Stopping Streaming]")
        except:
            self.stream.stop_stream()
            self.stream.close()
            self.wave_file.close()
            self.paudio.terminate()
            print("[Program Closed]")

class Parser:
    def createParser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('url')
        return parser

if "__main__" == __name__:
    parser = Parser().createParser()
    namespace = parser.parse_args(sys.argv[1:])
    spec = Spectrogram()
    spec.start_playing_music(namespace.url)