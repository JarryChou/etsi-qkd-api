from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import socket
from msg_box import msg_box


class ConnectWorker(QObject):

    other_username = pyqtSignal(str)
    other_ip_addr = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, connect_port):
        super().__init__()
        self.connect_port = connect_port

    @pyqtSlot()
    def connect_listening_server(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('', self.connect_port))
            s.listen(1)

        except socket.error:
            msg_box("Socket Error !!", "Unable to setup local socket. Port in use")
            return

        while True:
            conn, addr = s.accept()
            _other_ip_addr = str(addr[0])
            _other_username = conn.recv(4096).decode()  # username of other user
            self.other_ip_addr.emit(_other_ip_addr)
            self.other_username.emit(_other_username)
            conn.close()
            break

        s.close()
        self.finished.emit()
