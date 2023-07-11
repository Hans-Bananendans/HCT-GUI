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

config = {"tab_dict":
    {
        0: {
            "name": "Tab 0",
            "checkable": True,
            "icon": "settings.svg"
        },
        1: {
            "name": "Tab 1",
            "checkable": True,
            "icon": "thingy.svg"
        },
        2: {
            "name": "Tab 2",
            "checkable": True,
            "icon": "thingy.svg"
        },
        3: {
            "name": "Tab 3",
            "checkable": True,
            "icon": "thingy.svg"
        },
        4: {
            "name": "Tab 4",
            "checkable": True,
            "icon": "thingy.svg"
        },
        5: {
            "name": "Tab 5",
            "checkable": True,
            "icon": "thingy.svg"
        },
        6: {
            "name": "Tab 6",
            "checkable": True,
            "icon": "thingy.svg"
        },
    }
}


class TestTab(QWidget):
    def __init__(self, tabname: str):
        super().__init__()
        layout_0 = QVBoxLayout()
        layout_0.addWidget(QLabel(tabname))
        self.setLayout(layout_0)


class MainWindow(QMainWindow):
    def __init__(self, config: dict):
        super().__init__()
        self.setup_ui(config)
        self._theme = "dark"

    def setup_ui(self, tab_dict: dict, default_tab=0):
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

        # AUTO-ADD TAB INFRASTRUCTURE ========================================

        # Add tab swapping actions in list, so they are indexed.
        # First create a new list:
        self.tabactions = []

        for i, attrs in config["tab_dict"].items():
            # Create a new action for each entry in tab_dict
            self.tabactions.append(
                QAction(
                    # QIcon(iconpath+str(TestTab(attrs["icon"]),
                    attrs["name"],
                    self,
                    checkable=attrs["checkable"]
                )
            )
            # Connect each created item to the change_tab() function
            self.tabactions[i].triggered.connect(self.change_tab)
            # Connect the action to the tabbar, so they are visible on the UI
            tabbar.addAction(self.tabactions[i])

            # Artificially create a TestTab for each entry and add to the
            #  QStackedWidget object.
            self.tabcontainer.addWidget(TestTab(attrs["name"]))

        # Cement the indexing by casting list into tuple
        self.tabactions = tuple(self.tabactions)

        # Set the default tab checked and visible upon startup
        self.tabactions[default_tab].setChecked(True)
        self.tabcontainer.setCurrentIndex(default_tab)

    @Slot()
    def change_tab(self) -> None:
        """
        Finds index of tab and displays it using
            stack_widget.setCurrentIndex(index)
        """
        # Find the index of the tab action that sent the signal. This index
        # is identical to the index of the desired tab in the QStackedWidget.
        tab_index = self.tabactions.index(self.sender())

        # Set all tab actions unchecked, except for the one just clicked
        for action in self.tabactions:
            if action != self.tabactions[tab_index]:
                action.setChecked(False)

        # Tell the StackedWidget to display the tab with the desired index
        self.tabcontainer.setCurrentIndex(tab_index)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme="dark_teal.xml")
    window = MainWindow(config)
    # window = QLabel("Hello, this is a shit UI!")
    window.show()
    app.exec()