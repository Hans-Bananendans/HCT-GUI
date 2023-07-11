#!/usr/bin/env python3

# Imports
import sys
from PySide6.QtCore import (
    QDir,
    QSize,
    Qt,
    Slot,
    QTimer,
)
from PySide6.QtGui import (
    QAction,
    QActionGroup,
    QColor,
    QFont,
    QIcon,
    QImage,
    QKeySequence,
    QPalette,
)
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsView,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLCDNumber,
    QMainWindow,
    QMenuBar,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QStackedWidget,
    QStatusBar,
    QToolBar,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from qt_material import apply_stylesheet
from time import time
from datasource_dummy import datasource_dummy
import numpy as np
import pyqtgraph as pg

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self._theme = "dark"

        # Event loop INFRASTRUCTURE ==========================================
        time0 = time()

        self.nsamples = 600
        self.update_rate = 150
        self.telemetry = [time(), 1.0, -12.0, 44.0]
        self.b_emf = [0.73, 19.19, -45.50]

        # Pre-allocate data structure
        self.data = []

        # Set a fake time history so the scrolling rate remains constant
        row0 = np.full(self.nsamples, time())
        past_correction = []
        for i in range(self.nsamples):
            past_correction.append(i*1/self.update_rate)
        row0 = (row0 - np.flip(np.array(past_correction))).round(1)

        self.data.append(row0)
        for i in range(1, 6):
            self.data.append(np.zeros(self.nsamples))


        self.lines = []
        # Add data to the plot
        for i in (1, 2, 3, 4, 5):
            line = self.plot_widget.plot(self.data[0], self.data[i], pen=(i, 5))
            self.lines.append(line)

        self.timer = QTimer()
        self.timer.setInterval(1000/self.update_rate)
        self.timer.timeout.connect(self.update_telemetry)
        self.timer.start()

    def setup_ui(self):
        """
        Constructs the UI by placing all elements.
        """
        self.main_window = QMainWindow()
        self.resize(800, 600)  # Default w x h dimensions

        self.number = 0

        menubar = QMenuBar()
        menubar.addMenu("Dummy Menu")

        tabbar = QToolBar("Tab bar")
        statusbar = QStatusBar()

        # Apply elements to MainWindow
        self.setMenuBar(menubar)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, tabbar)
        self.setStatusBar(statusbar)

        self.central_widget = QWidget()

        layout1 = QVBoxLayout()

        string = "Label - "+str(self.number)
        self.label_header = QLabel(string)
        self.label_0 = QLabel("0")
        self.label_1 = QLabel("0")
        self.label_2 = QLabel("0")
        self.label_3 = QLabel("0")
        self.label_4 = QLabel("0")
        self.label_5 = QLabel("0")

        for label in (self.label_header, self.label_0, self.label_1,
                      self.label_2, self.label_3, self.label_4, self.label_5):
            layout1.addWidget(label)
        self.central_widget.setLayout(layout1)

        self.button = QPushButton("Update!")
        self.button.pressed.connect(self.update_label)
        layout1.addWidget(self.button)

        self.plot_widget = pg.PlotWidget(title="Test Plot")
        layout1.addWidget(self.plot_widget)

        self.setCentralWidget(self.central_widget)


    def update_telemetry(self):
        # time0 = time()  # TODO Remove
        self.telemetry = datasource_dummy(self.telemetry, permutation=1)

        for i in range(len(self.data)):
            self.data[i][:-1] = self.data[i][1:]  # TODO: Investigate overhead

            if i in [0, 1, 2, 3]:
                self.data[i][-1] = self.telemetry[i]

            if i == 4:
                self.data[i][-1] = np.linalg.norm(
                    np.array((
                        self.telemetry[1],
                        self.telemetry[2],
                        self.telemetry[3]))
                )
            if i == 5:
                self.data[i][-1] = np.linalg.norm(
                    np.array((
                        self.telemetry[1]-self.b_emf[0],
                        self.telemetry[2]-self.b_emf[1],
                        self.telemetry[3]-self.b_emf[2]))
                )
        self.update_label()
        self.update_plot()

        # print("Updated in", time() - time0, "s")  # TODO: Remove


    def update_label(self):
        self.label_0.setText(str(round(self.data[0][-1], 0)))
        self.label_1.setText(str(round(self.data[1][-1], 2)))
        self.label_2.setText(str(round(self.data[2][-1], 2)))
        self.label_3.setText(str(round(self.data[3][-1], 2)))
        self.label_4.setText(str(round(self.data[4][-1], 2)))
        self.label_5.setText(str(round(self.data[5][-1], 2)))

    def update_plot(self):
        for i, line in enumerate(self.lines):
            line.setData(self.data[0], self.data[i+1])
            # self.plot_widget.setData(self.data[0], self.data[i])
            # self.plot_widget.get
        # print("update_plot() called")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme="dark_teal.xml")
    window = MainWindow()
    window.show()
    app.exec()
