from PyQt5 import QtWidgets
from chat_gui import Ui_MainWindow
from connect_gui import Ui_ConnectWindow
import sys
import socket
import threading
from AES_class import AESCipher
import base64
import requests
import urllib3

# disables annoying warning that method is soon to be deprecated when performing TLS handshake with ETSI QKD server
urllib3.disable_warnings(urllib3.exceptions.SubjectAltNameWarning)


def msg_box(title, data):
    w = QtWidgets.QWidget()
    QtWidgets.QMessageBox.information(w, title, data)


class ConnectWindow(QtWidgets.QMainWindow, Ui_ConnectWindow):

    def __init__(self):
        super(ConnectWindow, self).__init__()

        self.sent_username = False
        self.received_username = False

        self.setupUi(self)

        self.connect_button.clicked.connect(self.connect_to)
        self.start_connect_server()
        self.checker_thread()

    def checker_thread(self):
        thread = threading.Thread(target=self.check_usernames, args=())
        thread.start()

    def check_usernames(self):
        while True:
            if self.sent_username is True and self.received_username is True:
                break
        self.main_window.show()

    def connect_to(self):

        while True:
            self.other_ip_addr = self.ip_addr.text()
            self.your_username = self.username.text()

            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                c.connect((self.other_ip_addr, 6180))
            except Exception as e:
                msg_box("Connection Refused",
                        "Failed to connect to IP " + self.other_ip_addr + ", error msg is " + str(e))
                continue

            try:
                c.send(self.your_username.encode())
            except Exception as e:
                msg_box("Failed to send", "Failed to send message, error msg is " + str(e))
                continue

            c.close()
            self.sent_username = True
            return

    def start_connect_server(self):
        thread = threading.Thread(target=self.server_socket, args=())
        thread.start()
        # msg_box("Success", "Server Started Successfully")

    def server_socket(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('', 6180))
            s.listen(1)
        except socket.error:
            msg_box("Socket Error !!", "Unable to setup local socket. Port in use")
            return

        while True:
            conn, addr = s.accept()

            incoming_ip = str(addr[0])
            current_ip = self.ip_addr.text()

            if incoming_ip != current_ip:
                conn.close()
            else:
                self.other_username = conn.recv(4096).decode()  # username of other user
                self.received_username = True
                conn.close()
                break
        s.close()

    def show_main_window(self):
        self.main_window = MainWindow(self.other_ip_addr, self.your_username, self.other_username)
        self.main_window.show()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Inherits from GUI class chat_gui.py. The reason for inheritance is so that if changes need to be made to the UI from
    QT Designer 5, the new .py file it generates will not erase all of the networking functionality implemented here.
    """

    def __init__(self, other_ip_addr, your_username, other_username):
        super(MainWindow, self).__init__()

        # Set up the user interface from Designer.
        self.setupUi(self)

        self.your_username = your_username
        self.other_username = other_username
        self.other_ip_addr = other_ip_addr

        # Add more functionality to UI elements. These are inherited from chat_gui.py.
        self.send_button.clicked.connect(self.send_message)

        # Retrieve a 256-bit qcrypto key as symmetric key for AES256 for this chat session from ETSI QKD API server
        URL = 'https://10.0.1.30/api/v1/keys/1/enc_keys'

        # AESCipher takes in a 32bytes (256bit) bytes object as private key
        PARAMS = {'number': 1, 'size': 256}

        # call GET request. include path to certificate file for TLS handshake to work
        r = requests.get(url=URL, params=PARAMS, verify='/etc/ssl/certs/certA.pem')
        key_container = r.json()
        key = key_container['keys'][0]['key']
        key = base64.b64decode(key)  # key is in base64 encoding (according to ETSI API), so decode to UTF8 bytes object
        self.AES_obj = AESCipher(key)

        self.start_chat_server()

    def start_chat_server(self):
        thread = threading.Thread(target=self.server_socket, args=())
        thread.start()
        # msg_box("Success", "Server Started Successfully")

    def server_socket(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('', 6190))
            s.listen(1)
        except socket.error:
            msg_box("Socket Error !!", "Unable to setup local socket. Port in use")
            return

        while True:
            conn, addr = s.accept()
            encrypted_msg = conn.recv(4096)
            decrypted_msg = self.AES_obj.decrypt(encrypted_msg)
            self.decrypted_chat_box.append(self.other_username + ": " + decrypted_msg)
            self.encrypted_chat_box.append(self.other_username + ": " + encrypted_msg.decode())
            conn.close()
        s.close()

    def send_message(self):
        msg = self.compose_msg_box.text()

        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            c.connect((self.other_ip_addr, 6190))
        except Exception as e:
            msg_box("Connection Refused", "Failed to connect to IP " + self.other_ip_addr + ", error msg is " + str(e))
            return

        try:
            encrypted_msg = self.AES_obj.encrypt(msg)
            c.send(encrypted_msg)
            self.encrypted_chat_box.append(self.your_username + ": " + encrypted_msg.decode())
            self.decrypted_chat_box.append(self.your_username + ": " + msg)
        except Exception as e:
            msg_box("Failed to send", "Failed to send message, error msg is " + str(e))

        c.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ConnectWindow()
    window.show()
    sys.exit(app.exec_())
