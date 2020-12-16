from PyQt5.QtWidgets import QSizePolicy
import ui_app
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import random

class Spector(FigureCanvas):
    def __init__(self, sample, time,  *filtr, parent=None, width=400, height=600, dpi=70, drawFunc=None):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.draw(sample, time, filtr)


    def draw(self, sample, time, filtr):
        print("Time", sample.shape[0])
        t = np.linspace(0, time, sample.shape[0], False)
        canvasSignal = self.figure.add_subplot(2, 1, 1)
        canvasSignal.plot(t, sample, 'g', linewidth=0.5)
        canvasSignal.set_title('Signal')
        #canvasSignal.set_ylabel("x")
        canvasSignal.set_xlabel('Time [seconds]')
        canvasSignal.grid(which='both', axis='both')
        if (len(filtr[0]) != 0):
            canvasSignal.set_xlabel('')
            filtr_sample = filtr[0]
            filtr_sample = filtr_sample[0]
            canvasAFR = self.figure.add_subplot(2, 1, 2)
            canvasAFR.set_title('Filter signal')
            #canvasAFR.set_ylabel('x')
            canvasAFR.set_xlabel('Time [seconds]')
            canvasAFR.plot(t, filtr_sample, 'r', linewidth=0.5)
            canvasAFR.grid(which='both', axis='both')

