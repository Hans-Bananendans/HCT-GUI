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
    QCheckBox,
    QFrame,
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
    QSpacerItem,
    QSpinBox,
    QStackedWidget,
    QStatusBar,
    QToolBar,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

class TabGaussmeter(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Set up ui."""

        layout_0 = QHBoxLayout()

        layout_left = QVBoxLayout()

        group_readings = QGroupBox()
        group_readings.setTitle("Gaussmeter readings")

        group_recording = QGroupBox()
        group_recording.setTitle("Recording")

        group_plotoptions = QGroupBox()
        group_plotoptions.setTitle("Plot options")

        # Gaussmeter reading =================================================
        layout_readings = QGridLayout()

        # First row
        label00 = QLabel("B<sub>X / Y / Z</sub> (\u03bcT)")
        layout_readings.addWidget(label00, 0, 0)

        lcd0x = QLCDNumber()
        lcd0x.display(-1.0)
        lcd0x.setStyleSheet(
            """QLCDNumber {
                color: rgba(244, 67, 54, 255);
                background-color: rgba(244, 67, 54, 26);
                border-color: rgba(244, 67, 54, 77);
                }"""
        )
        layout_readings.addWidget(lcd0x, 0, 1)

        lcd0y = QLCDNumber()
        lcd0y.display(-2.0)
        lcd0y.setStyleSheet(
            """QLCDNumber {
                color: rgba(50, 255, 50, 255);
                background-color: rgba(50, 255, 50, 26);
                border-color: rgba(50, 255, 50, 77);
                }"""
        )
        layout_readings.addWidget(lcd0y, 0, 2)

        lcd0z = QLCDNumber()
        lcd0z.display(30.0)
        lcd0z.setStyleSheet(
            """QLCDNumber {
                color: rgba(0, 146, 255, 255);
                background-color: rgba(0, 146, 255, 26);
                border-color: rgba(0, 146, 255, 77);
                }"""
        )
        layout_readings.addWidget(lcd0z, 0, 3)

        label01 = QLabel("<span style='text-decoration:overline'>B</span> (\u03bcT)")
        layout_readings.addWidget(label01, 0, 4)

        lcd0t = QLCDNumber()
        lcd0t.display(-1000.1)
        layout_readings.addWidget(lcd0t, 0, 5)

        # Line
        hline_lcd0 = QFrame()
        hline_lcd0.setFrameShape(QFrame.HLine)
        hline_lcd0.setLineWidth(2)
        layout_readings.addWidget(hline_lcd0, 1, 0, 1, -1)

        # Second row
        label10 = QLabel("B - B<sub>EMF</sub> (\u03bcT)")
        layout_readings.addWidget(label10, 2, 0)

        lcd1x = QLCDNumber()
        lcd1x.display(-1.0)
        layout_readings.addWidget(lcd1x, 2, 1)

        lcd1y = QLCDNumber()
        lcd1y.display(-2.0)
        layout_readings.addWidget(lcd1y, 2, 2)

        lcd1z = QLCDNumber()
        lcd1z.display(30.0)
        layout_readings.addWidget(lcd1z, 2, 3)

        label11 = QLabel("""
        |<span style='text-decoration:overline'>B</span> - 
        <span style='text-decoration:overline'>B</span><sub>EMF</sub> | 
        (\u03bcT)""")
        layout_readings.addWidget(label11, 2, 4)

        lcd1t = QLCDNumber()
        lcd1t.display(-1000.1)
        layout_readings.addWidget(lcd1t, 2, 5)

        # # Spacer
        # vspacer = QToolButton()
        # vspacer.setSizePolicy(QSizePolicy.Policy.Preferred,
        #                       QSizePolicy.Policy.Expanding)
        # vspacer.setEnabled(False)
        # layout_readings.addWidget(vspacer, 2, 0)

        # Last row
        label30 = QLabel("B<sub>EMF</sub> (\u03bcT)")
        layout_readings.addWidget(label30, 4, 0)

        lcd3x = QLCDNumber()
        lcd3x.display(0.73)
        layout_readings.addWidget(lcd3x, 4, 1)

        lcd3y = QLCDNumber()
        lcd3y.display(19.19)
        layout_readings.addWidget(lcd3y, 4, 2)

        lcd3z = QLCDNumber()
        lcd3z.display(-45.46)
        layout_readings.addWidget(lcd3z, 4, 3)

        label31 = QLabel("|<span style='text-decoration:overline'>B</span><sub>EMF</sub>| (\u03bcT)")
        layout_readings.addWidget(label31, 4, 4)

        lcd3t = QLCDNumber()
        lcd3t.display(49.35)
        layout_readings.addWidget(lcd3t, 4, 5)

        # Integration
        for lcd in (lcd0x, lcd0y, lcd0z, lcd0t,
                    lcd1x, lcd1y, lcd1z, lcd1t,
                    lcd3x, lcd3y, lcd3z, lcd3t):
            lcd.setMinimumWidth(150)
            lcd.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
            lcd.setDigitCount(6)
            lcd.setSmallDecimalPoint(True)

        layout_readings.setRowMinimumHeight(2, 100)
        group_readings.setLayout(layout_readings)

        # Recording ==========================================================
        layout_recording = QVBoxLayout()
        layout_recording.addWidget(QLabel("layout_recording"))

        group_recording.setLayout(layout_recording)

        # Plot options ===================================================
        layout_plotoptions = QVBoxLayout()

        button_freeze = QPushButton("Freeze")
        button_freeze.setCheckable(True)

        check_x = QCheckBox("B_X")
        check_y = QCheckBox("B_Y")
        check_z = QCheckBox("B_Z")
        check_t = QCheckBox("B_tot")
        check_n = QCheckBox("B-B_EMF")

        spinbox_center = QSpinBox()
        spinbox_center.setRange(-1000, 1000)
        # spinbox_center.setPrefix("Vertical target")
        # spinbox_center.setSuffix("\u03bcT")

        spinbox_range = QSpinBox()
        spinbox_center.setRange(1, 1000)
        # spinbox_center.setPrefix("Vertical span")
        # spinbox_center.setSuffix("\u03bcT")

        check_autoscale = QCheckBox("Autoscale")

        spinbox_plotinterval = QSpinBox()
        spinbox_plotinterval.setRange(1, 600)
        # spinbox_plotinterval.setPrefix("Plotted interval")
        # spinbox_plotinterval.setSuffix("s")

        spinbox_updaterate = QSpinBox()
        spinbox_updaterate.setRange(1, 60)
        # spinbox_updaterate.setPrefix("Update rate")
        # spinbox_updaterate.setSuffix("S/s")

        for widget in (
                button_freeze, check_x, check_y, check_z, check_t,
                check_n, spinbox_center, spinbox_range, check_autoscale,
                spinbox_plotinterval, spinbox_updaterate):
            layout_plotoptions.addWidget(widget)

        group_plotoptions.setLayout(layout_plotoptions)

        # Plots ==============================================================

        plot_box_placeholder = QLabel("Plot Box")

        # Integration ========================================================

        layout_left.addWidget(group_readings)
        layout_left.addWidget(group_recording)

        layout_0.addLayout(layout_left)
        layout_0.addWidget(group_plotoptions)
        layout_0.addWidget(plot_box_placeholder)

        layout_0.addStretch(1)

        self.setLayout(layout_0)