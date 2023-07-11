#!/usr/bin/env python3

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QMenuBar
)
from PySide6.QtCore import (
    Qt, QTimer
)
from PySide6.QtGui import QGuiApplication
import sys
from qt_material import apply_stylesheet
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
import numpy as np
from datasource_dummy import datasource_dummy
from time import time


class GaussmeterPlot(pg.PlotItem):
    def __init__(self,
                 parent=None,
                 name=None,
                 labels=None,
                 title='Speed (m/s)',
                 viewBox=None,
                 axisItems=None,
                 enableMenu=True,
                 **kargs):
        super().__init__(parent, name, labels, title, viewBox, axisItems, enableMenu, **kargs)
        nparams = 6     # TODO: Remove hardcoding
        self.nsamples = 100  # TODO: Remove hardcoding

        self.b_emf = [0.73, 19.19, -45.50]  # TODO: Remove hardcoding
        self.telemetry = [time(), 1.0, -12.0, 44.0]  # TODO: Remove hardcoding
        self.show = [True, True, True, False, False]  # TODO: Remove hardcoding
        self.data = []
        for i in range(nparams):
            self.data.append(np.zeros(self.nsamples))

    def update(self, telemetry):

        self.telemetry = datasource_dummy(self.telemetry, permutation=0.1)

        for i in range(len(self.data)):
            self.data[i][:-1] = self.data[i][1:]  # TODO: Investigate overhead

            if i in [0, 1, 2, 3]:
                self.data[i][-1] = telemetry[i]

            if i == 4:
                self.data[i][-1] = np.linalg.norm(
                    np.array(
                        telemetry[1],
                        telemetry[2],
                        telemetry[3])
                )
            if i == 5:
                self.data[i][-1] = np.linalg.norm(
                    np.array(
                        telemetry[1]-self.b_emf[0],
                        telemetry[2]-self.b_emf[1],
                        telemetry[3]-self.b_emf[2])
                )


class GaussmeterPlotTest:
    def __init__(self):
        nparams = 6     # TODO: Remove hardcoding
        self.nsamples = 100  # TODO: Remove hardcoding

        self.b_emf = [0.73, 19.19, -45.50]  # TODO: Remove hardcoding
        self.telemetry = [time(), 1.0, -12.0, 44.0]  # TODO: Remove hardcoding
        self.show = [True, True, True, False, False]  # TODO: Remove hardcoding
        self.data = []
        for i in range(nparams):
            self.data.append(np.zeros(self.nsamples))

    def update(self, telemetry):

        self.telemetry = datasource_dummy(self.telemetry, permutation=0.1)

        for i in range(len(self.data)):
            self.data[i][:-1] = self.data[i][1:]  # TODO: Investigate overhead

            if i in [0, 1, 2, 3]:
                self.data[i][-1] = telemetry[i]

            if i == 4:
                self.data[i][-1] = np.linalg.norm(
                    np.array((
                        telemetry[1],
                        telemetry[2],
                        telemetry[3]))
                )
            if i == 5:
                self.data[i][-1] = np.linalg.norm(
                    np.array((
                        telemetry[1]-self.b_emf[0],
                        telemetry[2]-self.b_emf[1],
                        telemetry[3]-self.b_emf[2]))
                )
        print("Updated", self.telemetry)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self._theme = "dark"

        # TEST CODE
        self.testclass = GaussmeterPlotTest()

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update())
        self.timer.start()

    def setup_ui(self):
        """
        Constructs the UI by placing all elements.
        """
        self.main_window = QMainWindow()
        self.resize(1200, 960)  # Default w x h dimensions

        menubar = QMenuBar()
        self.gaussmeterplot = GaussmeterPlot()
        tabbar = QToolBar("Tab bar")
        statusbar = QStatusBar()

        menubar.addMenu("Dummy Menu")

        # Apply elements to MainWindow
        self.setMenuBar(menubar)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, tabbar)
        self.setStatusBar(statusbar)
        self.setCentralWidget(self.gaussmeterplot)


    def update(self):
        self.testclass.update(self.testclass.telemetry)
        print("Update() called")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme="dark_teal.xml")
    window = MainWindow()
    window.show()
    app.exec()