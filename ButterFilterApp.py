import sys
import os

from PyQt5 import QtWidgets

from ui_app import Ui_MainWindow

from scipy.io import wavfile


class window(QtWidgets.QMainWindow):

    def __init__(self):
        super(window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.tempFiltredWidget = None
        self.tempWidget = None

        self.file_name = None
        self.filtredSepmle = None

        self.sample = None
        self.sample_rate = None
        self.sample_time = None

        self.wp = 0
        self.ws = 0
        self.max = 0
        self.min = 0
        self.samplingFrequency = 8000.00

        self.initActionUI()

    def initActionUI(self):
        self.ui.actionOpen_WAV_file_2.triggered.connect(self.open_file)
        self.ui.actionExit.triggered.connect(self.exit)

    def open_file(self):
        options = QtWidgets.QFileDialog.Options()
        url = os.path.abspath(__file__)
        url = url.split('\\')
        url = url[:(len(url) - 3)]
        url = "\\".join(url)
        print(url)


        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Open file", url, "WAV Files (*.wav)", options=options)

        if file_path:
            self.file_name = file_path.split("/")
            self.ui.sampleLabel.setText(self.file_name[-1])
            print(file_path)
            self.sample_rate, self.sample = wavfile.read(file_path)
            self.sample_time = self.sample.shape[0] / self.sample_rate
            print(self.sample_rate)
            print(self.sample.shape[0])

            print(self.sample)

            self.start_draw()

    def exit(self):
        sys.exit(app.exec())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    application = window()
    application.setFixedSize(1050, 600)
    application.show()
    sys.exit(app.exec())