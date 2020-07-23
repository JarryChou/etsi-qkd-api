from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
import socket
from msg_box import msg_box


class ChatWorker(QObject):

    encrypted_msg = pyqtSignal(bytes)

    @pyqtSlot()
    def chat_listening_server(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('', 6190))
            s.listen(1)
        except socket.error:
            msg_box("Socket Error !!", "Unable to setup local socket. Port in use")
            return

        while True:
            conn, addr = s.accept()
            _encrypted_msg = conn.recv(4096)
            self.encrypted_msg.emit(_encrypted_msg)
            conn.close()

        # no need to close socket as the server should remain listening until user closes the window manually
