import stft
import scipy.io.wavfile as wav

fs, audio = wav.read("/home/askvortsov/labs/sounds_expl/test0/fo_no.wav")
specgram = stft.spectrogram(audio)
output = stft.ispectrogram(specgram)
wav.write('output.wav', fs, output)