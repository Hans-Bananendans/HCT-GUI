#!/usr/bin/env python3

# Imports
import sys
from PySide6.QtCore import (
    QDir,
    QSize,
    Qt,
    Slot,
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

class TestTab1(QWidget):
    def __init__(self):
        super().__init__()
        layout_0 = QVBoxLayout()
        layout_0.addWidget(QLabel("This is TEST TAB 1"))
        self.setLayout(layout_0)


class TestTab2(QWidget):
    def __init__(self):
        super().__init__()
        layout_0 = QVBoxLayout()
        layout_0.addWidget(QLabel("This is TEST TAB 2"))
        self.setLayout(layout_0)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self._theme = "dark"

    def setup_ui(self):
        """
        Constructs the UI by placing all elements.
        """
        self.main_window = QMainWindow()
        self.resize(800, 600)  # Default w x h dimensions

        menubar = QMenuBar()
        self.tabcontainer = QStackedWidget()
        tabbar = QToolBar("Tab bar")
        statusbar = QStatusBar()

        menubar.addMenu("Dummy Menu")

        # Apply elements to MainWindow
        self.setMenuBar(menubar)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, tabbar)
        self.setStatusBar(statusbar)
        self.setCentralWidget(self.tabcontainer)

        # Add tab swapping actions in tuple, so they are indexed.
        self.tabactions = (
            QAction("Tab 1", self, checkable=True),
            QAction("Tab 2", self, checkable=True),
        )
        tabbar.addAction(self.tabactions[0])
        tabbar.addAction(self.tabactions[1])
        self.tabactions[0].setChecked(True)  # Default

        self.tabactions[0].triggered.connect(self.change_tab)
        self.tabactions[1].triggered.connect(self.change_tab)

        tab_1 = TestTab1()
        self.tabcontainer.addWidget(tab_1)

        tab_2 = TestTab2()
        self.tabcontainer.addWidget(tab_2)
        self.tabcontainer.setCurrentIndex(0)

    @Slot()
    def change_tab(self) -> None:
        time0 = time()
        """
        Finds index of tab and displays it using
            stack_widget.setCurrentIndex(index)
        """
        tab_index = self.tabactions.index(self.sender())

        for action in self.tabactions:
            if action != self.tabactions[tab_index]:
                action.setChecked(False)

        self.tabcontainer.setCurrentIndex(tab_index)
        print("Swapped to tab", tab_index)
        print("Time: ", time()-time0)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme="dark_teal.xml")
    window = MainWindow()
    # window = QLabel("Hello, this is a shit UI!")
    window.show()
    app.exec()