import sys
import os
import wave
import time

import librosa
import librosa.display
import pyaudio
import struct

from PyQt5 import QtWidgets

from ui_app import Ui_MainWindow

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
        self.samples_per_frame = 100
        self.wave_file = None

        self.CHUNK = 8000
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
        arr2D, freqs, bins = specgram(data, 
            window=window_hanning,
            Fs=self.sample_rate,
            NFFT=self.nfft,
            noverlap=self.overlap)
        return arr2D, freqs, bins

    def update_figure(self, n):
        data = self.get_data(self.stream)
        arr2D,freqs,bins = self.get_spectrogram(data)
        im_data = self.im.get_array()
        if n < self.samples_per_frame:
            im_data = np.hstack((im_data,arr2D))
            self.im.set_array(im_data)
        else:
            keep_block = arr2D.shape[1]*(self.samples_per_frame - 1)
            im_data = np.delete(im_data,np.s_[:-keep_block],1)
            im_data = np.hstack((im_data,arr2D))
            self.im.set_array(im_data)
        return self.im,

    def start_playing_music(self):
        self.file_path = "/home/askvortsov/labs/sounds_expl/test0/song1.wav"
        self.sample, self.sample_rate = librosa.load(self.file_path)
        self.sample_time = np.arange(0, len(self.sample)) / self.sample_rate 
        self.wave_file = wave.open(self.file_path, 'rb')

        try:
            print("[Launching Streaming]")
            self.stream = self.stream_wave()
            arr2D,freqs,bins = specgram(self.get_data(self.stream),
                
                Fs = self.sample_rate,
                NFFT=self.nfft,
                noverlap=self.overlap)
            extent = (bins[0], bins[-1] * self.samples_per_frame, freqs[-1], freqs[0])
            self.im = plt.imshow(arr2D,
                aspect="auto",
                extent = extent,
                interpolation="none",
                cmap = "jet",
                norm = LogNorm(vmin=.01,vmax=1))
            plt.xlabel("Time (seconds)")
            plt.ylabel("Frequency (Hz)")
            plt.title("Streaming Spectrogram")
            plt.gca().invert_yaxis()
            plt.colorbar() #enable if you want to display a color bar
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


if "__main__" == __name__:
	am = Spectrogram()
	am.start_playing_music()