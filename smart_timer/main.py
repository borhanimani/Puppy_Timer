import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from ui.main_window import MainWindow

BASE_DIR = Path(__file__).resolve().parent

ICON_PATH = (
    BASE_DIR
    / "assets"
    / "icons"
    / "puppy.png"
)


def main():

    app = QApplication(sys.argv)

    app.setWindowIcon(
        QIcon(
            str(ICON_PATH)
        )
    )

    with open("ui/style.qss", "r", encoding="utf-8") as file:
        app.setStyleSheet(file.read())


    window = MainWindow()

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()