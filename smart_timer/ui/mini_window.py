from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QGraphicsDropShadowEffect,
)

from PySide6.QtCore import (
    Qt,
    QSize,
)

from PySide6.QtGui import (
    QPainter,
    QPainterPath,
    QColor,
    QPen,
    QIcon,
)

from pathlib import Path


# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ICON_DIR = BASE_DIR / "assets" / "icons"


# ==========================================================
# MINI WINDOW
# ==========================================================

class MiniWindow(QWidget):

    def __init__(
        self,
        main_window
    ):

        super().__init__()

        self.main_window = main_window

        self.active = False

        self.drag_position = None


        # ==================================================
        # WINDOW SETTINGS
        # ==================================================

        self.setFixedSize(
            220,
            150
        )

        self.setWindowFlags(
            Qt.Tool |
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground
        )


        # ==================================================
        # SHADOW
        # ==================================================

        shadow = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(
            25
        )

        shadow.setOffset(
            0,
            6
        )

        self.setGraphicsEffect(
            shadow
        )


        # ==================================================
        # LAYOUT
        # ==================================================

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            18,
            15,
            18,
            15
        )

        layout.setSpacing(
            8
        )


        # ==================================================
        # STATUS
        # ==================================================

        self.status = QLabel(
            "🟣 Puppy"
        )

        self.status.setAlignment(
            Qt.AlignCenter
        )


        # ==================================================
        # TIMER INFO
        # ==================================================

        self.timer_info = QLabel(
            ""
        )

        self.timer_info.setObjectName(
            "timerInfo"
        )

        self.timer_info.setAlignment(
            Qt.AlignCenter
        )


        # ==================================================
        # TIMER
        # ==================================================

        self.timer = QLabel(
            "--:--"
        )

        self.timer.setObjectName(
            "miniTimer"
        )

        self.timer.setAlignment(
            Qt.AlignCenter
        )


        layout.addWidget(
            self.status
        )

        layout.addWidget(
            self.timer_info
        )

        layout.addWidget(
            self.timer
        )


        # ==================================================
        # OPEN MAIN WINDOW BUTTON
        # ==================================================

        self.open_button = QPushButton(
            self
        )

        self.open_button.setObjectName(
            "windowButton"
        )

        self.open_button.setIcon(
            self.icon(
                "box-arrow-in-up-right.svg"
            )
        )

        self.open_button.setIconSize(
            QSize(
                14,
                14
            )
        )

        self.open_button.setFixedSize(
            28,
            28
        )

        self.open_button.setFocusPolicy(
            Qt.NoFocus
        )

        self.open_button.setCursor(
            Qt.PointingHandCursor
        )

        self.open_button.clicked.connect(
            self.show_main
        )


        # ==================================================
        # STYLE
        # ==================================================

        self.setStyleSheet(
            """

            /* ---------------------------------------------
               GENERAL LABEL
               --------------------------------------------- */

            QLabel {

                color: #322B52;
                font-size: 16px;
                font-weight: bold;

            }


            /* ---------------------------------------------
               TIMER
               --------------------------------------------- */

            QLabel#miniTimer {

                color: #5D50C9;
                font-size: 32px;
                font-weight: 700;

            }


            /* ---------------------------------------------
               TIMER INFO
               --------------------------------------------- */

            QLabel#timerInfo {

                color: #928EA1;
                font-size: 10px;
                font-weight: normal;

            }


            /* ---------------------------------------------
               OPEN BUTTON
               --------------------------------------------- */

            QPushButton#windowButton {

                background: #EEEAFE;
                color: #5D50C9;

                border: none;
                border-radius: 8px;

                padding: 0px;

            }


            QPushButton#windowButton:hover {

                background: #E4DFFA;

            }


            QPushButton#windowButton:pressed {

                background: #D9D2F4;

            }

            """
        )


        # ==================================================
        # INITIAL BUTTON POSITION
        # ==================================================

        self.position_button()


    # ======================================================
    # ICON
    # ======================================================

    def icon(
        self,
        name
    ):

        path = ICON_DIR / name

        if path.exists():

            return QIcon(
                str(path)
            )

        return QIcon()


    # ======================================================
    # POSITION BUTTON
    # ======================================================

    def position_button(self):

        self.open_button.move(
            self.width()
            - self.open_button.width()
            - 15,

            self.height()
            - self.open_button.height()
            - 15
        )

        self.open_button.raise_()


    # ======================================================
    # TIMER INFO
    # ======================================================

    def set_timer_info(
        self,
        work,
        rest
    ):

        self.timer_info.setText(
            f"Focus {work}s  •  Rest {rest}s"
        )


    # ======================================================
    # UPDATE STATUS
    # ======================================================

    def set_status(
        self,
        text
    ):

        self.status.setText(
            text
        )


    # ======================================================
    # ACTIVE STATE
    # ======================================================

    def set_active(
        self,
        value
    ):

        self.active = value

        if value:

            self.status.setText(
                "🟢 Puppy Listening"
            )

        else:

            self.status.setText(
                "🟣 Puppy"
            )

        self.update()


    # ======================================================
    # UPDATE TIMER
    # ======================================================

    def set_timer(
        self,
        text
    ):

        self.timer.setText(
            text
        )


    # ======================================================
    # RETURN MAIN WINDOW
    # ======================================================

    def show_main(self):

        self.hide()

        self.main_window.show()

        self.main_window.activateWindow()


    # ======================================================
    # PAINT
    # ======================================================

    def paintEvent(
        self,
        event
    ):

        painter = QPainter(
            self
        )

        painter.setRenderHint(
            QPainter.Antialiasing
        )


        # --------------------------------------------------
        # ROUNDED RECTANGLE
        # --------------------------------------------------

        path = QPainterPath()

        path.addRoundedRect(
            5,
            5,
            self.width() - 10,
            self.height() - 10,
            18,
            18
        )


        # --------------------------------------------------
        # BACKGROUND
        # --------------------------------------------------

        if self.active:

            background = QColor(
                225,
                255,
                235
            )

        else:

            background = QColor(
                255,
                255,
                255
            )


        painter.fillPath(
            path,
            background
        )


        # --------------------------------------------------
        # ACTIVE LINE
        # --------------------------------------------------

        if self.active:

            pen = QPen(
                QColor(
                    60,
                    200,
                    120
                )
            )

            pen.setWidth(
                5
            )

            painter.setPen(
                pen
            )

            painter.drawLine(
                25,
                self.height() - 8,
                self.width() - 25,
                self.height() - 8
            )


    # ======================================================
    # MOVE WINDOW
    # ======================================================

    def mousePressEvent(
        self,
        event
    ):

        if event.button() == Qt.LeftButton:

            self.drag_position = (
                event.globalPosition().toPoint()
                -
                self.frameGeometry().topLeft()
            )

        super().mousePressEvent(
            event
        )


    def mouseMoveEvent(
        self,
        event
    ):

        if (
            event.buttons()
            ==
            Qt.LeftButton
            and
            self.drag_position is not None
        ):

            self.move(
                event.globalPosition().toPoint()
                -
                self.drag_position
            )

        super().mouseMoveEvent(
            event
        )


    # ======================================================
    # RESIZE
    # ======================================================

    def resizeEvent(
        self,
        event
    ):

        self.position_button()

        super().resizeEvent(
            event
        )