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
    QToolButton,
)

from ui.mini_window import MiniWindow
from controller.timer_controller import TimerController
from controller.timer_voice_contoller import TimerVoiceController
from controller.wake_word_controller import WakeWordController
from assets.sound_lib_paths import *


# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
ICON_DIR = BASE_DIR / "assets" / "icons"


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

        self.setFixedSize(
            160,
            160,
        )

        self.state = "idle"

        self.glow_color = QColor(
            150,
            130,
            235,
            60,
        )

        self._glow = 0.0

        self.animation = QPropertyAnimation(
            self,
            b"glow",
        )

        self.animation.setDuration(
            1200,
        )

        self.animation.setStartValue(
            0.0,
        )

        self.animation.setEndValue(
            1.0,
        )

        self.animation.setLoopCount(
            -1,
        )

        self.animation.setEasingCurve(
            QEasingCurve.InOutSine,
        )

    def set_glow_color(self, color):

        self.glow_color = color
        self.update()

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

            if self.animation.state() != QPropertyAnimation.Running:
                self.animation.start()

        else:

            self.animation.stop()
            self._glow = 0.0

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing,
        )

        if self.state in (
            "listening",
            "speaking",
            "thinking",
        ):

            painter.setPen(
                Qt.NoPen,
            )

            painter.setBrush(
                self.glow_color,
            )

            painter.drawEllipse(
                0,
                0,
                160,
                160,
            )

            if self.state == "speaking":

                painter.setBrush(
                    QColor(
                        255,
                        248,
                        220,
                    )
                )

            elif self.state == "listening":

                painter.setBrush(
                    QColor(
                        238,
                        234,
                        253,
                    )
                )

            else:

                painter.setBrush(
                    QColor(
                        244,
                        241,
                        252,
                    )
                )

            painter.drawEllipse(
                5,
                5,
                150,
                150,
            )

        if self.state == "speaking":

            painter.setBrush(
                QColor(
                    255,
                    246,
                    205,
                )
            )

        elif self.state == "listening":

            painter.setBrush(
                QColor(
                    226,
                    219,
                    250,
                )
            )

        else:

            painter.setBrush(
                QColor(
                    235,
                    230,
                    249,
                )
            )

        painter.drawEllipse(
            18,
            18,
            124,
            124,
        )

        painter.setPen(
            QColor(
                50,
                43,
                82,
            )
        )

        font = painter.font()

        font.setPointSize(
            21,
        )

        font.setBold(
            True,
        )

        painter.setFont(
            font,
        )

        if self.state == "speaking":

            text = "〰 〰"

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

    def __init__(
        self,
        toggle_callback,
        parent=None,
    ):

        super().__init__(parent)

        self.muted = True
        self.toggle_callback = toggle_callback

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            12,
            6,
            12,
            6,
        )

        layout.setSpacing(
            8,
        )

        self.led = QLabel()

        self.led.setObjectName(
            "micLed",
        )

        self.status = QLabel(
            "Muted",
        )

        self.status.setObjectName(
            "micStatus",
        )

        self.button = QPushButton()

        self.button.setObjectName(
            "micButton",
        )

        self.button.setIcon(
            icon(
                "mic-fill.svg",
            )
        )

        self.button.setIconSize(
            QSize(
                14,
                14,
            )
        )

        self.button.setFixedSize(
            28,
            28,
        )

        self.button.setToolTip(
            "Toggle microphone",
        )

        self.button.clicked.connect(
            self.toggle_callback,
        )

        layout.addWidget(
            self.led,
        )

        layout.addWidget(
            self.status,
        )

        layout.addWidget(
            self.button,
        )

        self.update_state()

    def set_muted(self, muted):

        self.muted = muted
        self.update_state()

    def update_state(self):

        if self.muted:

            self.status.setText(
                "Muted",
            )

            self.led.setProperty(
                "status",
                "off",
            )

        else:

            self.status.setText(
                "Listening",
            )

            self.led.setProperty(
                "status",
                "on",
            )

        self.led.style().unpolish(
            self.led,
        )

        self.led.style().polish(
            self.led,
        )


# ==========================================================
# TIMER CARD
# ==========================================================

class TimerCard(QFrame):

    def __init__(
        self,
        timer_controller,
        total_seconds,
        work_seconds,
        rest_seconds,
        delete_callback,
        parent=None,
    ):

        super().__init__(parent)

        self.setObjectName(
            "timerCard",
        )

        self.timer_controller = timer_controller

        self.total_seconds = total_seconds
        self.work_seconds = work_seconds
        self.rest_seconds = rest_seconds

        self.work_sound_played = False
        self.finished_sound_played = False

        self.delete_callback = delete_callback

        # --------------------------------------------------
        # SOUNDS
        # --------------------------------------------------

        self.work_sound = QSoundEffect(self)
        self.finish_sound = QSoundEffect(self)

        work_sound_path = WAV_WORK_SOUND
        finish_sound_path = WAV_FINISH_SOUND

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

        layout.setSpacing(
            10,
        )

        top = QHBoxLayout()

        title = QLabel(
            "Training Timer",
        )

        title.setObjectName(
            "timerTitle",
        )

        delete_button = QPushButton()

        delete_button.setObjectName(
            "deleteButton",
        )

        delete_button.setFixedSize(
            34,
            34,
        )

        delete_button.setIcon(
            icon(
                "trash-fill.svg",
            )
        )

        delete_button.setToolTip(
            "Delete timer",
        )

        delete_button.clicked.connect(
            self.delete_timer,
        )

        top.addWidget(
            title,
        )

        top.addStretch()

        top.addWidget(
            delete_button,
        )

        description = QLabel(
            f"{work_seconds}s focus  •  "
            f"{rest_seconds}s rest"
        )

        description.setObjectName(
            "timerDescription",
        )

        description.setAlignment(
            Qt.AlignCenter,
        )

        self.time_label = QLabel(
            self.format_time(
                total_seconds,
            )
        )

        self.time_label.setObjectName(
            "cardTime",
        )

        self.time_label.setAlignment(
            Qt.AlignCenter,
        )

        self.start_button = QPushButton(
            "Start Timer",
        )

        self.start_button.setObjectName(
            "primaryButton",
        )

        self.start_button.setIcon(
            icon(
                "play-fill.svg",
            )
        )

        self.start_button.clicked.connect(
            self.start_timer,
        )

        layout.addLayout(
            top,
        )

        layout.addWidget(
            description,
        )

        layout.addSpacing(
            4,
        )

        layout.addWidget(
            self.time_label,
        )

        layout.addSpacing(
            4,
        )

        layout.addWidget(
            self.start_button,
        )

        # --------------------------------------------------
        # TIMER SIGNALS
        # --------------------------------------------------

        self.timer_controller.timeChanged.connect(
            self.update_time,
        )

        self.timer_controller.timerFinished.connect(
            self.timer_finished,
        )

    # ======================================================
    # PREPARE START
    # ======================================================

    def prepare_for_start(self):

        self.work_sound_played = False
        self.finished_sound_played = False

        self.start_button.setEnabled(
            False,
        )

        self.start_button.setText(
            "Timer Running",
        )

    # ======================================================
    # MOUSE START
    # ======================================================

    def start_timer(self):

        if self.timer_controller.start():

            self.prepare_for_start()

    # ======================================================
    # VOICE START
    # ======================================================

    def start_from_voice(self):

        if self.timer_controller.start():

            self.prepare_for_start()

    # ======================================================
    # UPDATE TIME
    # ======================================================

    def update_time(self, seconds):

        self.time_label.setText(
            self.format_time(
                seconds,
            )
        )

        if (
            seconds == self.rest_seconds
            and not self.work_sound_played
            and self.rest_seconds > 0
        ):

            self.work_sound_played = True

            if self.work_sound.source().isValid():

                self.work_sound.play()

    # ======================================================
    # TIMER FINISHED
    # ======================================================

    def timer_finished(self):

        if not self.finished_sound_played:

            self.finished_sound_played = True

            if self.finish_sound.source().isValid():

                self.finish_sound.play()

        self.time_label.setText(
            self.format_time(
                self.total_seconds,
            )
        )

        self.start_button.setEnabled(
            True,
        )

        self.start_button.setText(
            "Start Again",
        )

    # ======================================================
    # DELETE
    # ======================================================

    def delete_timer(self):

        if self.delete_callback:

            self.delete_callback(
                self,
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

        self.save_callback = save_callback
        self.back_callback = back_callback

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            50,
            35,
            50,
            35,
        )

        layout.setSpacing(
            18,
        )

        # --------------------------------------------------
        # BACK
        # --------------------------------------------------

        back_button = QPushButton()

        back_button.setObjectName(
            "backButton",
        )

        back_button.setIcon(
            icon(
                "arrow-left.svg",
            )
        )

        back_button.setText(
            "  Back",
        )

        back_button.clicked.connect(
            self.back_callback,
        )

        # --------------------------------------------------
        # TITLE
        # --------------------------------------------------

        title = QLabel(
            "Create a timer",
        )

        title.setObjectName(
            "pageTitle",
        )

        subtitle = QLabel(
            "Set up your training session.",
        )

        subtitle.setObjectName(
            "pageSubtitle",
        )

        # --------------------------------------------------
        # WORK
        # --------------------------------------------------

        work_label = QLabel(
            "Focus duration",
        )

        self.work_input = QSpinBox()

        self.work_input.setRange(
            1,
            3600,
        )

        self.work_input.setValue(
            45,
        )

        self.work_input.setSuffix(
            " sec",
        )

        # --------------------------------------------------
        # REST
        # --------------------------------------------------

        rest_label = QLabel(
            "Rest duration",
        )

        self.rest_input = QSpinBox()

        self.rest_input.setRange(
            0,
            3600,
        )

        self.rest_input.setValue(
            15,
        )

        self.rest_input.setSuffix(
            " sec",
        )

        # --------------------------------------------------
        # SAVE
        # --------------------------------------------------

        save_button = QPushButton(
            "Save Timer",
        )

        save_button.setObjectName(
            "primaryButton",
        )

        save_button.setIcon(
            icon(
                "check-lg.svg",
            )
        )

        save_button.clicked.connect(
            self.save,
        )

        # --------------------------------------------------
        # LAYOUT
        # --------------------------------------------------

        layout.addWidget(
            back_button,
        )

        layout.addSpacing(
            12,
        )

        layout.addWidget(
            title,
        )

        layout.addWidget(
            subtitle,
        )

        layout.addSpacing(
            12,
        )

        layout.addWidget(
            work_label,
        )

        layout.addWidget(
            self.work_input,
        )

        layout.addWidget(
            rest_label,
        )

        layout.addWidget(
            self.rest_input,
        )

        layout.addStretch()

        layout.addWidget(
            save_button,
        )

    def save(self):

        work = self.work_input.value()
        rest = self.rest_input.value()

        total = work + rest

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
            "Puppy Timer",
        )

        self.resize(
            960,
            730,
        )

        self.setMinimumSize(
            820,
            560,
        )

        # ==================================================
        # TIMER CONTROLLER
        # ==================================================

        self.timer_controller = TimerController()

        # ==================================================
        # VOICE CONTROLLERS
        # ==================================================

        self.timer_voice_controller = TimerVoiceController(
            self
        )

        self.timer_voice_controller.createTimerSignal.connect(
            self.create_ui_timer
        )

        self.timer_voice_controller.startTimerSignal.connect(
            self.start_ui_timer
        )

        self.timer_voice_controller.deleteTimerSignal.connect(
            self.delete_timer_from_voice
        )

        self.timer_voice_controller.voiceFailedSignal.connect(
            self.show_voice_error
        )

        self.timer_voice_controller.voiceSuccessSignal.connect(
            self.clear_voice_message
        )

        self.wake_word_controller = WakeWordController(
            self.on_wake_word_detected
        )

        # ==================================================
        # TIMER STATE
        # ==================================================

        self.timer_exists = False
        self.current_timer_card = None
        self.initial_timer_seconds = 0

        # ==================================================
        # UI
        # ==================================================

        self.setup_ui()

        # ==================================================
        # MINI WINDOW
        # ==================================================

        self.mini_window = MiniWindow(
            self
        )

        # ==================================================
        # TIMER SIGNAL
        # ==================================================

        self.timer_controller.timeChanged.connect(
            self.update_mini_timer
        )

        # ==================================================
        # WAKE WORD SOUND
        # ==================================================

        self.wake_sound = QSoundEffect(
            self
        )

        wake_path = WAV_AI_SOUND

        if wake_path.exists():

            self.wake_sound.setSource(
                QUrl.fromLocalFile(
                    str(wake_path)
                )
            )

            self.wake_sound.setVolume(
                0.8
            )

        # ==================================================
        # VOICE ACTION SOUND
        # ==================================================

        self.voice_action_sound = QSoundEffect(
            self
        )

        voice_action_path = WAV_AI_SOUND

        if voice_action_path.exists():

            self.voice_action_sound.setSource(
                QUrl.fromLocalFile(
                    str(voice_action_path)
                )
            )

            self.voice_action_sound.setVolume(
                0.8
            )

    # ======================================================
    # VOICE ACTION SOUND
    # ======================================================

    def play_voice_action_sound(self):

        if self.voice_action_sound.source().isValid():

            self.voice_action_sound.play()

    # ======================================================
    # UPDATE MINI TIMER
    # ======================================================

    def update_mini_timer(self, seconds):

        if seconds > 0:

            display_seconds = seconds

        elif (
            seconds == 0
            and self.timer_exists
        ):

            display_seconds = (
                self.initial_timer_seconds
            )

        else:

            display_seconds = 0

        minutes = display_seconds // 60
        sec = display_seconds % 60

        text = (
            f"{minutes:02d}:"
            f"{sec:02d}"
        )

        self.mini_window.set_timer(
            text
        )

    # ======================================================
    # SHOW MINI WINDOW
    # ======================================================

    def show_mini_window(self):

        self.mini_window.show()
        self.hide()

    # ======================================================
    # SHOW VOICE ERROR
    # ======================================================

    def show_voice_error(self):

        self.assistant_message.setText(
            "Sorry, I didn't understand"
        )

        self.assistant_message.show()

    def clear_voice_message(self):

        self.assistant_message.hide()

    # ======================================================
    # SETUP UI
    # ======================================================

    def setup_ui(self):

        self.stack = QStackedWidget()

        self.setCentralWidget(
            self.stack
        )

        self.main_view = self.create_main_view()

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

        layout = QVBoxLayout(
            page
        )

        layout.setContentsMargins(
            36,
            24,
            36,
            22,
        )

        layout.setSpacing(
            14,
        )

        # --------------------------------------------------
        # HEADER
        # --------------------------------------------------

        header = QHBoxLayout()

        brand = QLabel(
            "Puppy Timer"
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

        brand_box.setSpacing(
            0
        )

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

        self.mini_button = QToolButton()

        self.mini_button.setObjectName(
            "windowButton"
        )

        self.mini_button.setIcon(
            icon(
                "box-arrow-up-right.svg"
            )
        )

        self.mini_button.setIconSize(
            QSize(
                18,
                18,
            )
        )

        self.mini_button.setFixedSize(
            34,
            34,
        )

        self.mini_button.clicked.connect(
            self.show_mini_window
        )

        # --------------------------------------------------
        # MICROPHONE
        # --------------------------------------------------

        self.microphone = MicrophoneStatus(
            self.toggle_microphone
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
            icon(
                "plus-lg.svg"
            )
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

        self.timer_container = QVBoxLayout()

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

        layout.addStretch(
            1
        )

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

        self.assistant = AssistantCircle()

        assistant_container = QHBoxLayout()

        assistant_container.addStretch()

        assistant_container.addWidget(
            self.assistant
        )

        assistant_container.addStretch()

        layout.addLayout(
            assistant_container
        )

        # --------------------------------------------------
        # ASSISTANT MESSAGE
        # --------------------------------------------------

        self.assistant_message = QLabel(
            "Sorry, I didn't understand"
        )

        font = self.assistant_message.font()

        font.setPointSize(
            13
        )

        self.assistant_message.setFont(
            font
        )

        self.assistant_message.setStyleSheet(
            """
            color: #555555;
            """
        )

        self.assistant_message.setObjectName(
            "assistantMessage"
        )

        self.assistant_message.setAlignment(
            Qt.AlignCenter
        )

        self.assistant_message.hide()

        layout.addWidget(
            self.assistant_message
        )

        # --------------------------------------------------
        # HINT
        # --------------------------------------------------

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

        # --------------------------------------------------
        # MINI BUTTON
        # --------------------------------------------------

        window_button_layout = QHBoxLayout()

        window_button_layout.addStretch()

        window_button_layout.addWidget(
            self.mini_button
        )

        layout.addLayout(
            window_button_layout
        )

        return page

    # ======================================================
    # SHOW ADD
    # ======================================================

    def show_add(self):

        if self.timer_exists:
            return

        self.stack.setCurrentWidget(
            self.add_view
        )

    # ======================================================
    # SHOW MAIN
    # ======================================================

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

        self.initial_timer_seconds = total

        try:

            self.timer_controller.create(
                total,
                rest,
            )

        except ValueError as error:

            print(
                "Timer creation error:",
                error,
            )

            return

        card = TimerCard(
            self.timer_controller,
            total,
            work,
            rest,
            self.delete_timer,
        )

        self.current_timer_card = card

        self.update_mini_timer(
            total
        )

        self.mini_window.set_timer_info(
            work,
            rest,
        )

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
    # CREATE TIMER - VOICE
    # ======================================================

    def create_ui_timer(
        self,
        total,
        rest,
    ):

        if self.timer_exists:
            return

        self.play_voice_action_sound()

        work = total - rest

        self.save_timer(
            total,
            work,
            rest,
        )

    # ======================================================
    # START TIMER - VOICE
    # ======================================================

    def start_ui_timer(self):

        if not self.current_timer_card:

            print(
                "VOICE: No timer exists."
            )

            return

        self.play_voice_action_sound()

        self.current_timer_card.start_from_voice()

    # ======================================================
    # MICROPHONE TOGGLE
    # ======================================================

    def toggle_microphone(self):

        if self.microphone.muted:

            self.enable_microphone()

        else:

            self.disable_microphone()

    # ======================================================
    # MICROPHONE ON
    # ======================================================

    def enable_microphone(self):

        print(
            "MICROPHONE >>> ON"
        )

        self.microphone.set_muted(
            False
        )

        self.assistant.set_glow_color(
            QColor(
                150,
                130,
                235,
                60,
            )
        )

        self.assistant.set_state(
            "listening"
        )

        self.mini_window.set_status(
            "🟣 Listening"
        )

        self.wake_word_controller.load_assistant()

    # ======================================================
    # WAKE WORD DETECTED
    # ======================================================

    def on_wake_word_detected(self):

        print(
            "MAIN WINDOW >>> WAKE WORD DETECTED"
        )

        self.mini_window.set_active(
            True
        )

        if self.wake_sound.source().isValid():

            self.wake_sound.play()

        self.assistant.set_glow_color(
            QColor(
                60,
                230,
                120,
                150,
            )
        )

        self.wake_word_controller.stop_wake_word()

        self.assistant.set_state(
            "listening"
        )

        self.clear_voice_message()

        self.timer_voice_controller.load_assistant()

    # ======================================================
    # MICROPHONE OFF
    # ======================================================

    def disable_microphone(self):

        print(
            "MICROPHONE >>> OFF"
        )

        self.mini_window.set_active(
            False
        )

        self.mini_window.set_status(
            "⚪ Sleep"
        )

        self.wake_word_controller.stop_wake_word()

        self.timer_voice_controller.stop_assistant()

        self.microphone.set_muted(
            True
        )

        self.assistant.set_glow_color(
            QColor(
                150,
                130,
                235,
                60,
            )
        )

        self.assistant.set_state(
            "idle"
        )

    # ======================================================
    # DELETE TIMER - VOICE
    # ======================================================

    def delete_timer_from_voice(self):

        if self.current_timer_card:

            self.play_voice_action_sound()

            self.delete_timer(
                self.current_timer_card
            )

        else:

            print(
                "VOICE: No timer to delete"
            )

    # ======================================================
    # DELETE TIMER
    # ======================================================

    def delete_timer(
        self,
        card,
    ):

        self.timer_controller.stop()

        self.timer_controller.reset()

        self.timer_container.removeWidget(
            card
        )

        card.deleteLater()

        self.current_timer_card = None
        self.timer_exists = False
        self.initial_timer_seconds = 0

        self.mini_window.set_timer(
            "--:--"
        )

        self.mini_window.set_timer_info(
            "",
            ""
        )

        self.empty_label.show()

        self.add_button.setEnabled(
            True
        )

        self.show_main()

    # ======================================================
    # ASSISTANT DEMO
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

    # ======================================================
    # CLOSE
    # ======================================================

    def closeEvent(self, event):

        print(
            "MAIN WINDOW >>> CLOSING"
        )

        self.wake_word_controller.stop_wake_word()

        self.timer_voice_controller.stop_assistant()

        self.timer_controller.stop()

        event.accept()