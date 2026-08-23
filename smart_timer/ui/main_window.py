from pathlib import Path

from PySide6.QtCore import (
    QSize,
    Qt,
    QPropertyAnimation,
    QEasingCurve,
    Property,
    QUrl,
)

from PySide6.QtGui import (
    QPainter,
    QColor,
    QIcon,
)

from PySide6.QtMultimedia import QSoundEffect

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QStackedWidget,
    QSpinBox,
    QSizePolicy,
)

from controller.timer_controller import TimerController



# ==========================================================
# SHARED TIMER
# ==========================================================

timer = TimerController()


# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ICON_DIR = BASE_DIR / "assets" / "icons"
SOUND_DIR = BASE_DIR / "assets" / "sounds"


def icon(name):
    path = ICON_DIR / name

    if path.exists():
        return QIcon(str(path))

    return QIcon()


# ==========================================================
# ASSISTANT CIRCLE
# ==========================================================

class AssistantCircle(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(160, 160)

        self.state = "idle"

        self._glow = 0.0

        self.animation = QPropertyAnimation(
            self,
            b"glow",
        )

        self.animation.setDuration(1200)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setLoopCount(-1)
        self.animation.setEasingCurve(
            QEasingCurve.InOutSine
        )

    def get_glow(self):
        return self._glow

    def set_glow(self, value):
        self._glow = value
        self.update()

    glow = Property(
        float,
        get_glow,
        set_glow,
    )

    def set_state(self, state):

        self.state = state

        if state in (
            "listening",
            "speaking",
            "thinking",
        ):
            self.animation.start()

        else:
            self.animation.stop()
            self._glow = 0.0

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        center = self.rect().center()

        # --------------------------------------------------
        # GLOW
        # --------------------------------------------------

        if self.state in (
            "listening",
            "speaking",
            "thinking",
        ):

            glow_size = (
                8 + int(self._glow * 12)
            )

            if self.state == "listening":
                glow_color = QColor(
                    108, 92, 231, 70
                )

            elif self.state == "speaking":
                glow_color = QColor(
                    244, 201, 93, 85
                )

            else:
                glow_color = QColor(
                    150, 130, 235, 60
                )

            painter.setPen(Qt.NoPen)
            painter.setBrush(glow_color)

            painter.drawEllipse(
                center.x()
                - 82
                - glow_size,

                center.y()
                - 82
                - glow_size,

                164
                + glow_size * 2,

                164
                + glow_size * 2,
            )

        # --------------------------------------------------
        # OUTER CIRCLE
        # --------------------------------------------------

        painter.setPen(Qt.NoPen)

        if self.state == "speaking":

            painter.setBrush(
                QColor(255, 248, 220)
            )

        elif self.state == "listening":

            painter.setBrush(
                QColor(238, 234, 253)
            )

        else:

            painter.setBrush(
                QColor(244, 241, 252)
            )

        painter.drawEllipse(
            5,
            5,
            150,
            150,
        )

        # --------------------------------------------------
        # INNER CIRCLE
        # --------------------------------------------------

        if self.state == "speaking":

            painter.setBrush(
                QColor(255, 246, 205)
            )

        elif self.state == "listening":

            painter.setBrush(
                QColor(226, 219, 250)
            )

        else:

            painter.setBrush(
                QColor(235, 230, 249)
            )

        painter.drawEllipse(
            18,
            18,
            124,
            124,
        )

        # --------------------------------------------------
        # TEXT
        # --------------------------------------------------

        painter.setPen(
            QColor(50, 43, 82)
        )

        font = painter.font()
        font.setPointSize(21)
        font.setBold(True)

        painter.setFont(font)

        if self.state == "speaking":

            text = "〰 〰"

        elif self.state == "listening":

            text = "Puppy"

        elif self.state == "thinking":

            text = "..."

        else:

            text = "Puppy"

        painter.drawText(
            self.rect(),
            Qt.AlignCenter,
            text,
        )


# ==========================================================
# MICROPHONE
# ==========================================================

class MicrophoneStatus(QFrame):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.muted = True

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            12,
            6,
            12,
            6,
        )

        layout.setSpacing(8)

        self.led = QLabel()
        self.led.setObjectName(
            "micLed"
        )

        self.status = QLabel("Muted")
        self.status.setObjectName(
            "micStatus"
        )

        self.button = QPushButton()

        self.button.setObjectName(
            "micButton"
        )

        self.button.setIcon(
            icon("mic-fill.svg")
        )

        self.button.setIconSize(
            QSize(14, 14)
        )

        self.button.setFixedSize(
            28,
            28,
        )

        self.button.setToolTip(
            "Toggle microphone"
        )

        self.button.clicked.connect(
            self.toggle
        )

        layout.addWidget(self.led)
        layout.addWidget(self.status)
        layout.addWidget(self.button)

        self.update_state()

    def toggle(self):

        self.muted = not self.muted

        self.update_state()

    def update_state(self):

        if self.muted:

            self.status.setText(
                "Muted"
            )

            self.led.setProperty(
                "status",
                "off",
            )

        else:

            self.status.setText(
                "Listening"
            )

            self.led.setProperty(
                "status",
                "on",
            )

        self.led.style().unpolish(
            self.led
        )

        self.led.style().polish(
            self.led
        )


# ==========================================================
# TIMER CARD
# ==========================================================

class TimerCard(QFrame):

    def __init__(
        self,
        total_seconds,
        work_seconds,
        rest_seconds,
        delete_callback,
        parent=None,
    ):

        super().__init__(parent)

        self.setObjectName(
            "timerCard"
        )

        self.total_seconds = total_seconds
        self.work_seconds = work_seconds
        self.rest_seconds = rest_seconds

        self.work_sound_played = False
        self.finished_sound_played = False

        self.delete_callback = (
            delete_callback
        )

        # --------------------------------------------------
        # SOUNDS
        # --------------------------------------------------

        self.work_sound = QSoundEffect(
            self
        )

        self.finish_sound = QSoundEffect(
            self
        )

        work_sound_path = (
            SOUND_DIR / "ding.wav"
        )

        finish_sound_path = (
            SOUND_DIR / "complete.wav"
        )

        if work_sound_path.exists():

            self.work_sound.setSource(
                QUrl.fromLocalFile(
                    str(work_sound_path)
                )
            )

            self.work_sound.setVolume(
                0.7
            )

        if finish_sound_path.exists():

            self.finish_sound.setSource(
                QUrl.fromLocalFile(
                    str(finish_sound_path)
                )
            )

            self.finish_sound.setVolume(
                0.8
            )

        # --------------------------------------------------
        # LAYOUT
        # --------------------------------------------------

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            24,
            20,
            24,
            22,
        )

        layout.setSpacing(10)

        top = QHBoxLayout()

        title = QLabel(
            "Training Timer"
        )

        title.setObjectName(
            "timerTitle"
        )

        delete_button = QPushButton()

        delete_button.setObjectName(
            "deleteButton"
        )

        delete_button.setFixedSize(
            34,
            34,
        )

        delete_button.setIcon(
            icon("trash-fill.svg")
        )

        delete_button.setIconSize(
            delete_button.sizeHint()
        )

        delete_button.setToolTip(
            "Delete timer"
        )

        delete_button.clicked.connect(
            self.delete_timer
        )

        top.addWidget(title)
        top.addStretch()
        top.addWidget(delete_button)

        description = QLabel(
            f"{work_seconds}s work  •  "
            f"{rest_seconds}s rest"
        )

        description.setObjectName(
            "timerDescription"
        )

        description.setAlignment(
            Qt.AlignCenter
        )

        self.time_label = QLabel(
            self.format_time(
                total_seconds
            )
        )

        self.time_label.setObjectName(
            "cardTime"
        )

        self.time_label.setAlignment(
            Qt.AlignCenter
        )

        self.start_button = QPushButton(
            "Start Timer"
        )

        self.start_button.setObjectName(
            "primaryButton"
        )

        self.start_button.setIcon(
            icon("play-fill.svg")
        )

        self.start_button.clicked.connect(
            self.start_timer
        )

        layout.addLayout(top)
        layout.addWidget(description)
        layout.addSpacing(4)
        layout.addWidget(self.time_label)
        layout.addSpacing(4)
        layout.addWidget(
            self.start_button
        )

        # --------------------------------------------------
        # TIMER SIGNAL
        # --------------------------------------------------

        timer.timeChanged.connect(
            self.update_time
        )

    # ======================================================
    # START
    # ======================================================

    def start_timer(self):

        self.prepare_for_start()

        timer.start()

    def prepare_for_start(self):

        self.work_sound_played = False
        self.finished_sound_played = False

        self.start_button.setEnabled(
            False
        )

        self.start_button.setText(
            "Timer Running"
        )

    # ======================================================
    # VOICE START
    # ======================================================

    def start_from_voice(self):

        self.prepare_for_start()

    # ======================================================
    # TIME UPDATE
    # ======================================================

    def update_time(self, seconds):

        self.time_label.setText(
            self.format_time(seconds)
        )

        # --------------------------------------------------
        # WORK FINISHED
        # --------------------------------------------------

        if (
            seconds == self.rest_seconds
            and not self.work_sound_played
        ):

            self.work_sound_played = True

            if (
                self.work_sound
                .source()
                .isValid()
            ):

                self.work_sound.play()

        # --------------------------------------------------
        # FINISHED
        # --------------------------------------------------

        if (
            seconds == 0
            and not self.finished_sound_played
        ):

            self.finished_sound_played = True

            if (
                self.finish_sound
                .source()
                .isValid()
            ):

                self.finish_sound.play()

            self.start_button.setEnabled(
                True
            )

            self.start_button.setText(
                "Start Again"
            )

    # ======================================================
    # DELETE
    # ======================================================

    def delete_timer(self):

        if self.delete_callback:

            self.delete_callback(
                self
            )

    # ======================================================
    # FORMAT
    # ======================================================

    @staticmethod
    def format_time(seconds):

        minutes = seconds // 60

        seconds = seconds % 60

        return (
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )


# ==========================================================
# ADD TIMER VIEW
# ==========================================================

class AddTimerView(QWidget):

    def __init__(
        self,
        save_callback,
        back_callback,
    ):

        super().__init__()

        self.save_callback = (
            save_callback
        )

        self.back_callback = (
            back_callback
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            50,
            35,
            50,
            35,
        )

        layout.setSpacing(18)

        # --------------------------------------------------
        # BACK
        # --------------------------------------------------

        back_button = QPushButton()

        back_button.setObjectName(
            "backButton"
        )

        back_button.setIcon(
            icon("arrow-left.svg")
        )

        back_button.setText(
            "  Back"
        )

        back_button.clicked.connect(
            self.back_callback
        )

        # --------------------------------------------------
        # TITLE
        # --------------------------------------------------

        title = QLabel(
            "Create a timer"
        )

        title.setObjectName(
            "pageTitle"
        )

        subtitle = QLabel(
            "Set up your training session."
        )

        subtitle.setObjectName(
            "pageSubtitle"
        )

        # --------------------------------------------------
        # WORK
        # --------------------------------------------------

        work_label = QLabel(
            "Work duration"
        )

        self.work_input = QSpinBox()

        self.work_input.setRange(
            1,
            3600,
        )

        self.work_input.setValue(
            45
        )

        self.work_input.setSuffix(
            " sec"
        )

        # --------------------------------------------------
        # REST
        # --------------------------------------------------

        rest_label = QLabel(
            "Rest duration"
        )

        self.rest_input = QSpinBox()

        self.rest_input.setRange(
            0,
            3600,
        )

        self.rest_input.setValue(
            15
        )

        self.rest_input.setSuffix(
            " sec"
        )

        # --------------------------------------------------
        # SAVE
        # --------------------------------------------------

        save_button = QPushButton(
            "Save Timer"
        )

        save_button.setObjectName(
            "primaryButton"
        )

        save_button.setIcon(
            icon("check-lg.svg")
        )

        save_button.clicked.connect(
            self.save
        )

        # --------------------------------------------------
        # LAYOUT
        # --------------------------------------------------

        layout.addWidget(
            back_button
        )

        layout.addSpacing(12)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addSpacing(12)

        layout.addWidget(
            work_label
        )

        layout.addWidget(
            self.work_input
        )

        layout.addWidget(
            rest_label
        )

        layout.addWidget(
            self.rest_input
        )

        layout.addStretch()

        layout.addWidget(
            save_button
        )

    def save(self):

        work = self.work_input.value()
        rest = self.rest_input.value()

        total = work + rest

        timer.create(
            total,
            rest,
        )

        self.save_callback(
            total,
            work,
            rest,
        )


# ==========================================================
# MAIN WINDOW
# ==========================================================

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Puppy"
        )

        self.resize(
            960,
            670,
        )

        self.setMinimumSize(
            820,
            560,
        )

        self.timer_exists = False

        # --------------------------------------------------
        # COMMAND HANDLER
        # --------------------------------------------------

        self.timer_handler = (
            TimerCommandHandler(timer)
        )

        self.current_timer_card = None

        # --------------------------------------------------
        # UI
        # --------------------------------------------------

        self.setup_ui()

    # ======================================================
    # SETUP
    # ======================================================

    def setup_ui(self):

        self.stack = QStackedWidget()

        self.setCentralWidget(
            self.stack
        )

        self.main_view = (
            self.create_main_view()
        )

        self.add_view = AddTimerView(
            self.save_timer,
            self.show_main,
        )

        self.stack.addWidget(
            self.main_view
        )

        self.stack.addWidget(
            self.add_view
        )

    # ======================================================
    # MAIN VIEW
    # ======================================================

    def create_main_view(self):

        page = QWidget()

        layout = QVBoxLayout(page)

        layout.setContentsMargins(
            36,
            24,
            36,
            22,
        )

        layout.setSpacing(14)

        # --------------------------------------------------
        # HEADER
        # --------------------------------------------------

        header = QHBoxLayout()

        brand = QLabel(
            "Puppy"
        )

        brand.setObjectName(
            "brand"
        )

        subtitle = QLabel(
            "Focus • Move • Breathe"
        )

        subtitle.setObjectName(
            "brandSubtitle"
        )

        brand_box = QVBoxLayout()

        brand_box.setSpacing(0)

        brand_box.addWidget(
            brand
        )

        brand_box.addWidget(
            subtitle
        )

        header.addLayout(
            brand_box
        )

        header.addStretch()

        self.microphone = (
            MicrophoneStatus()
        )

        header.addWidget(
            self.microphone
        )

        layout.addLayout(
            header
        )

        # --------------------------------------------------
        # TIMER HEADER
        # --------------------------------------------------

        timer_header = QHBoxLayout()

        timer_title = QLabel(
            "Your timer"
        )

        timer_title.setObjectName(
            "sectionTitle"
        )

        self.add_button = QPushButton(
            "Add timer"
        )

        self.add_button.setObjectName(
            "secondaryButton"
        )

        self.add_button.setIcon(
            icon("plus-lg.svg")
        )

        self.add_button.clicked.connect(
            self.show_add
        )

        timer_header.addWidget(
            timer_title
        )

        timer_header.addStretch()

        timer_header.addWidget(
            self.add_button
        )

        layout.addLayout(
            timer_header
        )

        # --------------------------------------------------
        # TIMER CONTAINER
        # --------------------------------------------------

        self.timer_container = (
            QVBoxLayout()
        )

        self.timer_container.setSpacing(
            10
        )

        layout.addLayout(
            self.timer_container
        )

        # --------------------------------------------------
        # EMPTY STATE
        # --------------------------------------------------

        self.empty_label = QLabel(
            "No timer yet\n\n"
            "Create a timer for your next session."
        )

        self.empty_label.setObjectName(
            "emptyState"
        )

        self.empty_label.setAlignment(
            Qt.AlignCenter
        )

        self.empty_label.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed,
        )

        self.timer_container.addWidget(
            self.empty_label
        )

        # --------------------------------------------------
        # ASSISTANT
        # --------------------------------------------------

        layout.addStretch(1)

        assistant_title = QLabel(
            "Ask Puppy"
        )

        assistant_title.setObjectName(
            "assistantTitle"
        )

        assistant_title.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            assistant_title
        )

        self.assistant = (
            AssistantCircle()
        )

        assistant_container = (
            QHBoxLayout()
        )

        assistant_container.addStretch()

        assistant_container.addWidget(
            self.assistant
        )

        assistant_container.addStretch()

        layout.addLayout(
            assistant_container
        )

        hint = QLabel(
            'Say "Hey Puppy" to get started'
        )

        hint.setObjectName(
            "assistantHint"
        )

        hint.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            hint
        )

        return page

    # ======================================================
    # NAVIGATION
    # ======================================================

    def show_add(self):

        if self.timer_exists:
            return

        self.stack.setCurrentWidget(
            self.add_view
        )

    def show_main(self):

        self.stack.setCurrentWidget(
            self.main_view
        )

    # ======================================================
    # SAVE TIMER
    # ======================================================

    def save_timer(
        self,
        total,
        work,
        rest,
    ):

        if self.timer_exists:
            return

        card = TimerCard(
            total,
            work,
            rest,
            self.delete_timer,
        )

        self.current_timer_card = card

        self.timer_container.addWidget(
            card
        )

        self.empty_label.hide()

        self.timer_exists = True

        self.add_button.setEnabled(
            False
        )

        self.show_main()

    # ======================================================
    # VOICE SET TIMER
    # ======================================================

    def create_voice_timer(
        self,
        command,
    ):

        if self.timer_exists:
            return

        if command.work_seconds is None:
            return

        work = command.work_seconds
        rest = command.rest_seconds

        total = work + rest

        # TimerController
        self.timer_handler.handle(
            command
        )

        # UI
        self.save_timer(
            total,
            work,
            rest,
        )

    # ======================================================
    # VOICE COMMAND
    # ======================================================

    def handle_voice_command(
        self,
        command,
    ):

        # ----------------------------------------------
        # SET TIMER
        # ----------------------------------------------

        if command.command == CommandType.SET_TIMER:

            self.create_voice_timer(
                command
            )

            return

        # ----------------------------------------------
        # START / STOP / RESET
        # ----------------------------------------------

        handled = (
            self.timer_handler.handle(
                command
            )
        )

        if not handled:
            return

        # ----------------------------------------------
        # UI START STATE
        # ----------------------------------------------

        if (
            command.command
            == CommandType.START_TIMER
        ):

            if self.current_timer_card:

                self.current_timer_card.start_from_voice()

        # ----------------------------------------------
        # UI STOP / RESET
        # ----------------------------------------------

        elif (
            command.command
            in (
                CommandType.STOP_TIMER,
                CommandType.RESET_TIMER,
            )
        ):

            if self.current_timer_card:

                self.current_timer_card.start_button.setEnabled(
                    True
                )

                self.current_timer_card.start_button.setText(
                    "Start Timer"
                )

    # ======================================================
    # DELETE
    # ======================================================

    def delete_timer(
        self,
        card,
    ):

        self.timer_container.removeWidget(
            card
        )

        card.deleteLater()

        self.current_timer_card = None

        self.timer_exists = False

        self.empty_label.show()

        self.add_button.setEnabled(
            True
        )

        self.show_main()

    # ======================================================
    # ASSISTANT STATES
    # ======================================================

    def demo_listening(self):
        self.assistant.set_state(
            "listening"
        )

    def demo_speaking(self):
        self.assistant.set_state(
            "speaking"
        )

    def demo_thinking(self):
        self.assistant.set_state(
            "thinking"
        )

    def demo_idle(self):
        self.assistant.set_state(
            "idle"
        )