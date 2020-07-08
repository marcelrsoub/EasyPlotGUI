# -*- coding: utf-8 -*-
# @Author: Marcel Reis-Soubkovsky
# @Date:   2020-06-28 15:46:41
# @Last Modified by:   Marcel Reis-Soubkovsky
# @Last Modified time: 2020-07-08 18:04:03


from PySide2.QtWidgets import*
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Qt, QFile, QIODevice
from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtGui import QIcon
import sys

from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure
from matplotlib.widgets import Slider, Button, RadioButtons

import numpy as np
import random


class Mpl(QWidget):
    
    def __init__(self, parent = None):
        
        QWidget.__init__(self, parent)
        
        self.mpl_canvas = FigureCanvas(Figure(constrained_layout=True, facecolor='#f0f0f0'))
        
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.mpl_canvas)
        # vertical_layout.addWidget(NavigationToolbar(self.mpl_canvas, self))       #uncomment in order to have the matplotlib tools
        
        self.mpl_canvas.axes = self.mpl_canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)

# --------------------------------------
class EasyPlotGUI(QWidget):

    """Easy GUI with matplotlib
    """
    
    def __init__(self):

        self.window_title="EasyPlotGUI"
        self.ui_filepath="untitled.ui"
        self.icon_path=None

    def show_gui(self):
        app = QApplication([])
        
        QWidget.__init__(self)

        loader = QUiLoader()
        loader.registerCustomWidget(Mpl)
        # self.ui = loader.load(designer_file, self)
        ui_file = QFile(self.ui_filepath)
        if not ui_file.open(QIODevice.ReadOnly):
            print("Cannot open {}: {}".format(self.ui_filepath, ui_file.errorString()))
            sys.exit(-1)
        loader = QUiLoader()
        self.ui = loader.load(ui_file, None)
        ui_file.close()

        self.ax=self.ui.Mpl.mpl_canvas.axes
        self.canvas=self.ui.Mpl.mpl_canvas

        if not self.ui:
            print(loader.errorString())
            sys.exit(-1)

        self.update_interactivity()
        self.update_graph()

        self.setWindowTitle(self.window_title)

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.ui)
        self.setLayout(grid_layout)

        if self.icon_path!=None:
            self.setWindowIcon(QIcon(self.icon_path))
        
        self.show()
        app.exec_()

    def update_interactivity(self):
        # example, to be overwritten
        self.ui.pushButton_generate_random_signal.clicked.connect(self.update_graph)

    def update_graph(self):
        # example, to be overwritten
        y = np.random.rand(100)
        x = np.linspace(0,1,100)

        self.ax.clear()
        self.ax.plot(x, y, label="Random")
        self.ax.legend()
        self.ax.set_title('Random Values')
        self.canvas.draw()
        
if __name__ == "__main__":

    gui = EasyPlotGUI()
    gui.window_title="Window Title"
    gui.ui_filepath="untitled.ui"
    gui.icon_path="./logo.png"
    gui.show_gui()