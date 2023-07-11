from PySide6.QtCore import QDir, QSize, Qt, Slot
from PySide6.QtGui import (
    QAction,
    QActionGroup,
    QFont,
    QIcon,
    QImage,
    QKeySequence,
    QPixmap,
)
from PySide6.QtWidgets import (
    QGraphicsView,
    QGroupBox,
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

import pyqtgraph as pg
import numpy as np
from . import tab_gaussmeter

# Test class for debugging purposes # TODO: Remove before production
class TestTab(QWidget):
    def __init__(self, tabname: str):
        super().__init__()
        layout_0 = QVBoxLayout()
        layout_0.addWidget(QLabel(tabname))
        self.setLayout(layout_0)


class MainWindow(QMainWindow):
    def __init__(self, config: dict) -> None:
        super().__init__()
        self.setup_ui(config)

    def setup_ui(self, config: dict) -> None:
        """
        Constructs the UI by placing all elements.
        """
        self.main_window = QMainWindow()
        self.resize(1600, 900)  # Default w x h dimensions
        self.setWindowIcon(QIcon(QPixmap(":program_icon")))
        self.setWindowTitle("Helmholtz Cage Toolkit")

        # Menubar
        menubar = self.create_menubar(config)
        self.setMenuBar(menubar)

        # Statusbar
        self.setStatusBar(QStatusBar())

        # CentralWidget
        self.tabcontainer = QStackedWidget()  # Important: this must be defined before calling create_tabbar()
        self.setCentralWidget(self.tabcontainer)

        # Tabbar
        tabbar = self.create_tabbar(config)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, tabbar)

    def create_menubar(self, config: dict):
        # TODO: Add menus
        # TODO: Autogenerate from config dict
        menubar = QMenuBar()

        menu_file = menubar.addMenu("&File")
        menu_view = menubar.addMenu("&View")
        menu_tools = menubar.addMenu("&Tools")
        menu_help = menubar.addMenu("&Help")

        # Menu bar - File menu
        # TODO: Add menu items, connect actions
        act_new_config = QAction(
            QIcon(QPixmap(":file")),
            "&New configuration", self)
        act_new_config.setStatusTip("Start a new configuration")
        # act_new_config.triggered.connect()
        act_new_config.setCheckable(False)
        act_new_config.setShortcut(QKeySequence("Ctrl+n"))

        act_open_config = QAction(
            QIcon(QPixmap(":folder")),
            "&Open configuration...", self)
        act_open_config.setStatusTip("Load a configuration from a file")
        # act_open_config.triggered.connect()
        act_open_config.setCheckable(False)
        act_open_config.setShortcut(QKeySequence("Ctrl+o"))

        act_saveas = QAction(text="Save as...", parent=self)
        act_saveas.setStatusTip("Save as...")
        # act_saveas.triggered.connect()
        act_saveas.setCheckable(False)

        act_save_config = QAction(
            QIcon(QPixmap(":save")),
            "&Save configuration", self)
        act_save_config.setStatusTip("Save this configuration to a file")
        # act_save_config.triggered.connect()
        act_save_config.setCheckable(False)
        act_save_config.setShortcut(QKeySequence("Ctrl+s"))

        act_settings = QAction(
            QIcon(QPixmap(":settings")),
            "Settings", self)
        act_settings.setStatusTip("View and edit program settings")
        # act_settings.triggered.connect()
        act_settings.setCheckable(False)

        act_quit = QAction(text="&Quit", parent=self)
        act_quit.setStatusTip("Save this configuration to a file")
        # act_quit.triggered.connect()
        act_quit.setCheckable(False)

        menu_file.addAction(act_new_config)
        menu_file.addAction(act_open_config)
        menu_file.addAction(act_saveas)
        menu_file.addAction(act_save_config)
        menu_file.addSeparator()
        menu_file.addAction(act_settings)
        menu_file.addSeparator()
        menu_file.addAction(act_quit)

        # Menu bar - View menu
        # TODO: Add menu items

        # Menu bar - Tools menu
        # TODO: Add menu items, connect actions
        act_screenshot = QAction(
            QIcon(QPixmap(":camera")),
            "Take a &Screenshot", self)
        act_screenshot.setStatusTip("Take a screenshot")
        # act_screenshot.triggered.connect()
        act_screenshot.setCheckable(False)
        # act_screenshot.setShortcut(QKeySequence("Ctrl+s"))

        menu_tools.addAction(act_screenshot)

        return menubar

    def create_tabbar(self, config: dict):
        """
        Creates the tabbar, a QToolBar that allows the user to navigate
         between the different tabs of the CentralWidget.

        Returns a QToolBar object
        """
        tabbar = QToolBar()
        tabbar.setMovable(False)
        tabbar.setIconSize(QSize(36, 36))

        # First create a new list:
        self.tabactions = []

        for i, attrs in config["tab_dict"].items():
            # Create a new action for each entry in tab_dict
            self.tabactions.append(
                QAction(
                    QIcon(QPixmap(attrs["icon"])),
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
            #  QStackedWidget object. # TODO: Replace with more useful generation
            if i == 0:
                self.tabcontainer.addWidget(tab_gaussmeter.TabGaussmeter())
            else:
                self.tabcontainer.addWidget(TestTab(attrs["name"]))

        # Cement the indexing by casting list into tuple
        self.tabactions = tuple(self.tabactions)

        # Set the default tab checked and visible upon startup
        self.tabactions[config["default_tab"]].setChecked(True)
        self.tabcontainer.setCurrentIndex(config["default_tab"])

        return tabbar

    @Slot()
    def change_tab(self) -> None:
        """
        Allows navigation of the various "tabs" of the CentralWidget, which
        are really just layered widgets in a QStackedWidget. Whenever a signal
        calls this function, change_tab() figures which tab action the signal
        originated from, set that tab action checked in the tabbar, set all
        others unchecked, and swap to the corresponding tab in the central
        widget.
        """
        # TODO: Currently the checked tabbar item can be clicked again, and be
        # TODO:  de-checked in this way. Fix it so that checked tabbar items
        # TODO:  cannot be unchecked manually.
        # Find the index of the tab action that sent the signal. This index
        # is identical to the index of the desired tab in the QStackedWidget.
        tab_index = self.tabactions.index(self.sender())

        # Set all tab actions unchecked, except for the one just clicked
        for action in self.tabactions:
            if action != self.tabactions[tab_index]:
                action.setChecked(False)

        # Tell the StackedWidget to display the tab with the desired index
        self.tabcontainer.setCurrentIndex(tab_index)

