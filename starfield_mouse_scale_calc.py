import sys
import os
import subprocess
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, QHBoxLayout, QPlainTextEdit, QCheckBox, QSplashScreen)
from PySide6.QtGui import QClipboard, QFont, QPalette, QColor, QPainter, QFontMetrics, QFontDatabase, QPixmap, QIcon
from PySide6.QtCore import Qt, QTimer


class PatternWidget(QWidget):
    def __init__(self, color, parent=None):
        super().__init__(parent)
        self.color = color
        self.font = QFont("charfontv2")  # Set the font name
        self.font.setPixelSize(15)  # font size in pixels
        # OR
        #self.font.setPointSize(10)  # Set the desired font size in point size

        self.font.setBold(True)  # Make it bold.
        # Adjust the letter spacing
        self.font.setLetterSpacing(QFont.AbsoluteSpacing, -10)  # Decrease spacing by 1 pixel, default -1 
        # OR
        # self.font.setLetterSpacing(QFont.PercentageSpacing, 90)  # Decrease spacing to 90% of the original
       
        self.font.setStyleStrategy(QFont.NoAntialias) # No antialiasing
        # OR
        #self.font.setStyleStrategy(QFont.PreferAntialias) # Yes antialiasing
        self.setFont(self.font)  # Explicitly set the font for this widget

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.color)
        painter.setFont(self.font)  # Set the font to the painter
        font_metrics = QFontMetrics(self.font)  # Use the new font for metrics
        char_width = font_metrics.horizontalAdvance('░')
        num_chars = int(self.width() / char_width) + 1
        painter.drawText(self.rect(), '░' * num_chars)


class MouseScaleCalculator(QWidget):
    # Color Palette
    BACKGROUND_COLOR = "#2f4c79"
    BLUE_ACCENT = "#8091b2"
    TEXT_COLOR = "#f4f5f7"
    CRT_BLACK = "#1e1e1e"
    GOLD_ACCENT = "#d7ab61"
    ORANGE_ACCENT = "#e06236"
    RED_ACCENT = "#c82337"
    GREEN_ACCENT = "#d4ac64"

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Adding the banner lines at the top
        banner_colors = [self.RED_ACCENT, self.ORANGE_ACCENT, self.GOLD_ACCENT, self.BLUE_ACCENT]
        banner_layout = QVBoxLayout()
        banner_layout.setSpacing(0)  # Ensure no spacing between the lines
        banner_layout.setContentsMargins(0, 0, 0, 0)  # Set the margins to zero

        banner_container = QWidget(self)
        banner_container.setLayout(banner_layout)
        banner_container.setStyleSheet("background-color: #2f4c79;")  # Set the background color to off-white to act as the border

        for color in banner_colors:
            line_widget = PatternWidget(color, self)
            line_widget.setFixedHeight(10)
            banner_layout.addWidget(line_widget)

        layout.addWidget(banner_container)  # Add the container (with the banner inside) to the main layout

        # Title label for resolution
        title_label = QLabel("CHOOSE YOUR RESOLUTION: (dropdown select or type it in)", self)
        layout.addWidget(title_label)

        # Custom dropdown with arrows on both sides
        resolution_layout = QHBoxLayout()
        left_arrow_btn = QPushButton("▼", self)
        left_arrow_btn.clicked.connect(self.show_dropdown)
        left_arrow_btn.setMaximumWidth(30)
        left_arrow_btn.setStyleSheet(f"background-color: {self.GOLD_ACCENT}; color: {self.CRT_BLACK};")
        resolution_layout.addWidget(left_arrow_btn)

        self.resolutions_dropdown = QComboBox(self)
        self.resolutions_dropdown.setEditable(True)
        
        # Set the background color of the editable QComboBox
        combo_palette = self.resolutions_dropdown.palette()
        combo_palette.setColor(QPalette.Base, QColor(self.CRT_BLACK))
        self.resolutions_dropdown.setPalette(combo_palette)

        resolutions = [
            "1920x1080", "2560x1440", "3840x2160",
            "3440x1440", "3840x1600", "5120x1440",
            "5120x1600", "5120x2160"
        ]
        self.resolutions_dropdown.addItems(resolutions)
        self.resolutions_dropdown.setStyleSheet(f"color: {self.GOLD_ACCENT}; background-color: {self.CRT_BLACK};")
        resolution_layout.addWidget(self.resolutions_dropdown)

        right_arrow_btn = QPushButton("▼", self)
        right_arrow_btn.clicked.connect(self.show_dropdown)
        right_arrow_btn.setMaximumWidth(30)
        right_arrow_btn.setStyleSheet(f"background-color: {self.GOLD_ACCENT}; color: {self.CRT_BLACK};")
        resolution_layout.addWidget(right_arrow_btn)

        layout.addLayout(resolution_layout)

        # Input for fMouseHeadingXScale
        x_scale_layout = QHBoxLayout()
        x_scale_label = QLabel("fMouseHeadingXScale=:", self)
        self.x_scale_input = QLineEdit("0.021", self)
        self.x_scale_input.setStyleSheet(f"color: {self.GOLD_ACCENT}; background-color: {self.CRT_BLACK};")
        x_scale_layout.addWidget(x_scale_label)
        x_scale_layout.addWidget(self.x_scale_input)
        layout.addLayout(x_scale_layout)

        # Add the checkbox for disabling mouse acceleration
        self.disable_accel_checkbox = QCheckBox("Disable mouse acceleration", self)
        self.disable_accel_checkbox.setStyleSheet("""
    QCheckBox::indicator:checked {
        color: #d7ab61;
        background-color: #d7ab61;
    }
""")
        layout.addWidget(self.disable_accel_checkbox)
        # THE Calculate button
        self.calculate_btn = QPushButton("CALCULATE", self)
        self.calculate_btn.clicked.connect(self.calculate_scale)
        self.calculate_btn.setStyleSheet(f"background-color: {self.GOLD_ACCENT}; color: {self.CRT_BLACK}; font-weight: bold;")
        layout.addWidget(self.calculate_btn)

        # Output field (QLineEdit) to display the result
        self.output_field =QLineEdit(self)
        self.output_field.setReadOnly(True)  # Make it read-only so users can't modify the
        # content
        self.output_field.setStyleSheet(f"background-color: {self.CRT_BLACK}; color: {self.GOLD_ACCENT};")
        layout.addWidget(self.output_field)

        # Instructions title
        instructions_title_label = QLabel("Instructions:", self)
        layout.addWidget(instructions_title_label)

        # General instructions
        self.general_instructions_label = QLabel(
            "1) NAVIGATE TO: %USERPROFILE%\\Documents\\My Games\\Starfield\n"
            "2) OPEN OR CREATE StarfieldCustom.ini\n"
            "3) COPY AND PASTE THE BELOW OUTPUT INTO StarfieldCustom.ini AND SAVE:",
            self
        )
        layout.addWidget(self.general_instructions_label)

        # Mouse XY Scale Calculation Output in its own field
        #self.controls_output_label = QLabel("Mouse XY Scale Calculation Output:", self)
        #layout.addWidget(self.controls_output_label)
        self.controls_output = QPlainTextEdit(self)
        self.controls_output.setReadOnly(True)
        layout.addWidget(self.controls_output)

        # Adjusting the height of the controls_output widget
        font_metrics = self.controls_output.fontMetrics()
        lines = 5  # Number of lines in the controls_output widget
        line_spacing = font_metrics.lineSpacing()
        new_height = lines * line_spacing + (self.controls_output.contentsMargins().top() + self.controls_output.contentsMargins().bottom())
        self.controls_output.setFixedHeight(new_height)

        # Copy to Clipboard button
        self.copy_btn = QPushButton("COPY TO CLIPBOARD", self)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.copy_btn.setStyleSheet(f"background-color: {self.GOLD_ACCENT}; color: {self.CRT_BLACK}; font-weight: bold;")
        layout.addWidget(self.copy_btn)

        # Open Starfield config folder button
        self.open_folder_btn = QPushButton("OPEN STARFIELD CONFIG FOLDER (Windows)", self)
        self.open_folder_btn.clicked.connect(self.open_starfield_folder)
        self.open_folder_btn.setStyleSheet(f"background-color: {self.GOLD_ACCENT}; color: {self.CRT_BLACK}; font-weight: bold;")
        layout.addWidget(self.open_folder_btn)

        self.setLayout(layout)
        self.setWindowTitle("Starfield Mouse Scale Calculator")

    def calculate_scale(self):
        resolution = self.resolutions_dropdown.currentText()
        x_scale = float(self.x_scale_input.text())
        output_text = ""  # Initialize the output_text variable

        if "x" in resolution:
            x, y = map(int, resolution.split('x'))
            fMouseHeadingYScale = x_scale * (x / y)
            self.output_field.setText(f"fMouseHeadingYScale={fMouseHeadingYScale:.4f}")
            output_text = (
                f"[Controls]\n"
                f"fMouseHeadingXScale={x_scale:.4f}\n"
                f"fMouseHeadingYScale={fMouseHeadingYScale:.4f}"
            )
            # Check if the "Disable mouse acceleration" checkbox is checked
            if self.disable_accel_checkbox.isChecked():
                output_text += "\nbMouseAcceleration=0"
            
            self.controls_output.setPlainText(output_text)
        else:
            self.output_field.setText("Invalid resolution format!")

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.controls_output.toPlainText())

    def open_starfield_folder(self):
        path = os.path.expandvars("%USERPROFILE%\\Documents\\My Games\\Starfield")
        if os.path.exists(path):
            subprocess.Popen(f'explorer "{path}"')
        else:
            # Handle the case where the folder doesn't exist
            # For example, show a message to the user
            print("Starfield folder not found!")

    def show_dropdown(self):
        # Toggle the dropdown visibility
        if self.resolutions_dropdown.view().isVisible():
            self.resolutions_dropdown.hidePopup()
        else:
            self.resolutions_dropdown.showPopup()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load and display the splash screen
    if getattr(sys, 'frozen', False):
    # Running as a bundled executable
        base_path = sys._MEIPASS
    else:
    # Running as a normal script
        base_path = os.path.dirname(os.path.abspath(__file__))

    # Set window icon    
    icon_path = os.path.join(base_path, 'starcalcicon.ico')
    app.setWindowIcon(QIcon(icon_path))

    splash_path = os.path.join(base_path, 'starcalcsplash.png')
    splash_pix = QPixmap(splash_path)
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.show()

    # Load the custom font
    font_id = QFontDatabase.addApplicationFont("Monoid-Regular.ttf")
    font_families = QFontDatabase.applicationFontFamilies(font_id)
    if font_families:
        custom_font = QFont(font_families[0])  # Get the font family name
        custom_font.setPixelSize(12)  # font size in pixels
        # OR
        #custom_font.setPointSize(12)  # Set the desired font size

        #custom_font.setWeight(QFont.Normal)
        # OR
        #custom_font.setWeight(QFont.Bold)  # Make the font bolder

        #custom_font.setStyleStrategy(QFont.PreferAntialias)
        # OR
        #custom_font.setStyleStrategy(QFont.NoAntialias)  # Attempt to disable anti-aliasing
        #custom_font.setKerning(False) # Set font kerning, enable for pixel fonts
        #custom_font.setStretch(QFont.Unstretched) # Ensure font isn't stretched
        app.setFont(custom_font)  # Set the application-wide font

    # Setting the color scheme
    palette = QPalette()
    palette.setColor(QPalette.Window, MouseScaleCalculator.BACKGROUND_COLOR)
    palette.setColor(QPalette.WindowText, MouseScaleCalculator.TEXT_COLOR)
    palette.setColor(QPalette.Base, MouseScaleCalculator.CRT_BLACK)
    palette.setColor(QPalette.AlternateBase, MouseScaleCalculator.BACKGROUND_COLOR)
    palette.setColor(QPalette.Text, MouseScaleCalculator.GOLD_ACCENT)
    palette.setColor(QPalette.Button, MouseScaleCalculator.BACKGROUND_COLOR)
    palette.setColor(QPalette.ButtonText, MouseScaleCalculator.GOLD_ACCENT)
    palette.setColor(QPalette.Highlight, MouseScaleCalculator.ORANGE_ACCENT)
    palette.setColor(QPalette.HighlightedText, MouseScaleCalculator.TEXT_COLOR)
    app.setPalette(palette)

    def show_main_app():
        splash.close()
        window.show()

    # Delay the display of the main window in milliseconds, This was used so temporary files have a chance to unpack and so the splash screen can show
    QTimer.singleShot(4000, show_main_app)

    window = MouseScaleCalculator()
    sys.exit(app.exec())
