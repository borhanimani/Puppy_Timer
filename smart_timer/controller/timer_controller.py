from PySide6.QtCore import QObject, QTimer, Signal


class TimerController(QObject):
    timeChanged = Signal(int)
    workTimeFinished = Signal()
    timerFinished = Signal()
    stateChanged = Signal(str)

    def __init__(self):
        super().__init__()

        self.totalSeconds = 0
        self.workSeconds = 0
        self.restSeconds = 0
        self.remainingSeconds = 0

        self.working = False
        self.resting = False

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._tick)

    # ======================================================
    # CREATE
    # ======================================================

    def create(
        self,
        totalSeconds: int,
        restSeconds: int = 0,
    ):
        if totalSeconds <= 0:
            raise ValueError(
                "Timer duration must be greater than zero"
            )

        if restSeconds < 0:
            raise ValueError(
                "Rest duration cannot be negative"
            )

        if restSeconds >= totalSeconds:
            raise ValueError(
                "Rest must be less than total duration"
            )

        self.totalSeconds = totalSeconds
        self.restSeconds = restSeconds
        self.workSeconds = (
            totalSeconds - restSeconds
        )

        self.reset()

        self.stateChanged.emit("ready")

    # ======================================================
    # START
    # ======================================================

    def start(self):

        if self.totalSeconds <= 0:
            return False

        if self.working:
            return False

        # --------------------------------------------------
        # If timer is completely finished, start again
        # --------------------------------------------------

        if self.remainingSeconds <= 0:
            self.remainingSeconds = self.workSeconds
            self.resting = False

        self.working = True

        self.timeChanged.emit(
            self.remainingSeconds
        )

        self.stateChanged.emit("working")

        self.timer.start()

        return True

    # ======================================================
    # TICK
    # ======================================================

    def _tick(self):

        if not self.working:
            return

        self.remainingSeconds -= 1

        self.timeChanged.emit(
            self.remainingSeconds
        )

        # --------------------------------------------------
        # WORK FINISHED
        # --------------------------------------------------

        if self.remainingSeconds <= 0:

            if not self.resting:

                self.workTimeFinished.emit()

                if self.restSeconds > 0:

                    self.resting = True

                    self.remainingSeconds = (
                        self.restSeconds
                    )

                    self.stateChanged.emit(
                        "rest"
                    )

                    self.timeChanged.emit(
                        self.remainingSeconds
                    )

                else:

                    self.finish()

            # --------------------------------------------------
            # REST FINISHED
            # --------------------------------------------------

            else:

                self.finish()

    # ======================================================
    # FINISH
    # ======================================================

    def finish(self):

        self.timer.stop()

        self.working = False
        self.resting = False
        self.remainingSeconds = 0

        self.timeChanged.emit(0)

        self.timerFinished.emit()

        self.stateChanged.emit(
            "finished"
        )

    # ======================================================
    # STOP
    # ======================================================

    def stop(self):

        self.timer.stop()

        self.working = False
        self.resting = False

        self.remainingSeconds = self.workSeconds

        self.timeChanged.emit(
            self.remainingSeconds
        )

        self.stateChanged.emit(
            "stopped"
        )

    # ======================================================
    # RESET
    # ======================================================

    def reset(self):

        self.timer.stop()

        self.working = False
        self.resting = False

        self.remainingSeconds = (
            self.workSeconds
        )

        self.timeChanged.emit(
            self.remainingSeconds
        )

        self.stateChanged.emit(
            "ready"
        )

    # ======================================================
    # STATE
    # ======================================================

    def isRunning(self):
        return self.working

    def hasTimer(self):
        return self.totalSeconds > 0

