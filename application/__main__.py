""" HCT GUI Framework

This project covers a GUI framework for the Helmholtz Cage Toolkit, written
in PySide6.
"""

__author__ = "Johan Monster"
__credits__ = ["Johan Monster"]
__license__ = "GPL"
__version__ = "0.0.1"


config = {
    "tab_dict": {
        0: {
            "name": "Tab 0",
            "checkable": True,
            "icon": ":gaussmeter"
        },
        1: {
            "name": "Tab 1",
            "checkable": True,
            "icon": ":box"
        },
        2: {
            "name": "Tab 2",
            "checkable": True,
            "icon": ":box"
        },
        3: {
            "name": "Tab 3",
            "checkable": True,
            "icon": ":box"
        },
        4: {
            "name": "Tab 4",
            "checkable": True,
            "icon": ":box"
        },
        5: {
            "name": "Tab 5",
            "checkable": True,
            "icon": ":box"
        },
        6: {
            "name": "Tab 6",
            "checkable": True,
            "icon": ":box"
        },
    },
    "default_tab": 0,
    "menubar": {

    },
}

# Imports
import sys
from PySide6.QtWidgets import QApplication
from qt_material import apply_stylesheet
from UI.main_window import MainWindow
import resources

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme="dark_teal.xml")
    window = MainWindow(config)
    window.show()
    app.exec()