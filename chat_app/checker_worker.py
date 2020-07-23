from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class CheckerWorker(QObject):

    start_main_window = pyqtSignal(bool)
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.received_username = False
        self.sent_username = False

    @pyqtSlot()
    def check_to_start_main(self):
        while True:
            if self.sent_username is True and self.received_username is True:
                self.start_main_window.emit(True)
                break
        self.finished.emit()