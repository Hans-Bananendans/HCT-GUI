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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self._theme = "dark"

        # Event loop INFRASTRUCTURE ==========================================
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_label)
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
        self.label = QLabel(string)
        layout1.addWidget(self.label)
        self.central_widget.setLayout(layout1)

        self.button = QPushButton("Update!")
        self.button.pressed.connect(self.update_label)
        layout1.addWidget(self.button)

        self.setCentralWidget(self.central_widget)


    def update_label(self):
        self.number += 1
        string = "Label - "+str(self.number)
        self.label.setText(string)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme="dark_teal.xml")
    window = MainWindow()
    window.show()
    app.exec()
