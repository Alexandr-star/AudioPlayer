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
import matplotlib.animation as FuncAnimation

import Draw

# class animation(FuncAnimation):
#     '''
#     Класс имеющий возможность оперировать функциями анимации
#     на вход подается рисунок, ссылка на экземпляр линии функции, которые определяются как атрибуты.
#     В конструкторе объекта
#     '''
#     def __init__(self, fig, axes, plot_instance):
#         self.fig = fig
#         self.axes = axes
#         self.plot_instance = plot_instance
#         #Проверка объекта ссылки на линию
#         #self.check_is_it_plot_instance()
#         '''
#         animation - Подается рисунок, на котором анимируется объект, заем подается порядок изменения функции,
#         обеспечивающей перерисовку данных во времени, посредством (метод plot_animation)
#         init_func - начальный вариант функции
#         interval - Интервал через который вызывается метод (время в милисекундах мсек = 0.001 сек.)
#         '''
#         print(1)
#         FuncAnimation.__init__(self, self.fig, self.animate_my_plot, init_func=self.init_plot, frames=2,
#                                                  interval=800)


#     def animate_my_plot(self, i):
#         # Вывод тестовых данных
#         data_to_animate = set_test_data()
#         x, y = data_to_animate
#         #print(str(x)+'_список содержит данные для замены x из метода animate_my_plot')
#         self.plot_instance.set_data(x, y)
#         print(3)

#     def init_plot(self):
#         '''
#         Создаем начальное значение функции
#         '''
#         print(2)
#         self.plot_instance.set_data([], [])


#     def check_is_it_plot_instance(self):
#         #Проверка содержимого объекта
#         print(self.plot_instance)

class window(QtWidgets.QMainWindow):

    def __init__(self):
        super(window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.tempFiltredWidget = None
        self.tempWidget = None

        self.paudio = pyaudio.PyAudio()

        self.file_name = None
        self.file_path = None
        self.spectro = None

        self.sample = None
        self.sample_rate = None
        self.sample_time = None

        self.wave_file = None

        self.CHUNK = 1024

        self.initActionUI()

    def initActionUI(self):
        self.ui.actionOpen_WAV_file_2.triggered.connect(self.open_file)
        self.ui.actionExit.triggered.connect(self.exit)

        self.ui.startButton.clicked.connect(self.start_playing_music)

    def start_playing_music(self):
        self.file_path = "/home/askvortsov/labs/sounds_expl/test0/fo_no.wav"
        self.sample, self.sample_rate = librosa.load(self.file_path)
        self.sample_time = np.arange(0, len(self.sample)) / self.sample_rate 
        self.wave_file = wave.open(self.file_path, 'rb')

        S = np.abs(librosa.stft(self.sample))
        print(S)
        fig, ax = plt.subplots()
        # img = librosa.display.specshow(librosa.amplitude_to_db(S,
        #                                                ref=np.max),
        #                        y_axis='log', x_axis='time', ax=ax)
        # ax.set_title('Power spectrogram')
        # fig.colorbar(img, ax=ax, format="%+2.0f dB")
        # plt.show()
        D = S
        i = 0
        while len(D) > 0:
            D = S[i]
            amp = librosa.amplitude_to_db(D,
                                            ref=np.max)
            imp = librosa.display.specshow(amp,
                    y_axis='log', x_axis='time', ax=ax)
            i = i + 1;
        
        fig.colorbar(img, ax=ax, format="%+2.0f dB")
        plt.show()









    # stream = self.paudio.open(format=self.paudio.get_format_from_width(self.wave_file.getsampwidth()),
    #                                 channels=self.wave_file.getnchannels(),
    #                                 rate=self.wave_file.getframerate(),
    #                                 output=True,
    #                                 input=True)
        
    #     data = self.wave_file.readframes(self.CHUNK)
       
    #     while len(data) > 0:
    #         stream.write(data)
    #         data = self.wave_file.readframes(self.CHUNK)    
    

    def start_draw(self, *filt):
        self.ui.horizontalLayout.removeWidget(self.tempWidget)
        self.tempWidget = Draw.Spector(self.sample, self.sample_time, filt, parent=self)
        self.ui.horizontalLayout.addWidget(self.tempWidget)

    def callback(self, in_data, frame_count, time_info, status):
        data = self.wave_file.readframes(frame_count)
        return (data, pyaudio.paContinue)

    def open_file(self):
        options = QtWidgets.QFileDialog.Options()
        url = os.path.abspath(__file__)
        url = url.split('\\')
        url = url[:(len(url) - 3)]
        url = "\\".join(url)

        self.file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Open file", url, "WAV Files (*.wav)", options=options)
        self.ui.horizontalLayout.removeWidget(self.tempFiltredWidget)
        self.ui.horizontalLayout.removeWidget(self.tempWidget)

        if self.file_path:
            self.file_name = self.file_path.split("/")
            self.ui.sampleLabel.setText(self.file_name[-1])
            self.file_path = "/home/askvortsov/labs/sounds_expl/test0/wave.wav"
            self.sample, self.sample_rate = librosa.load(self.file_path)
            self.sample_time = np.arange(0, len(self.sample)) / self.sample_rate 
            self.wave_file = wave.open(self.file_path, 'rb')
            # self.sample_rate, self.sample = wav.read(self.file_path)
            # self.sample_time = self.sample.shape[0] / self.sample_rate


    


    def exit(self):
        stream.stop_stream()
        stream.close()
        self.wave_file.close()
        self.paudio.terminate()
        sys.exit(app.exec())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    application = window()
    application.setFixedSize(1050, 600)
    application.show()
    sys.exit(app.exec())