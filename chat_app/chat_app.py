from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread
from chat_gui import Ui_MainWindow
from connect_gui import Ui_ConnectWindow
import sys
import socket
from AES_class import AESCipher
import base64
import requests
import urllib3
from chat_worker import ChatWorker
from connect_worker import ConnectWorker
from checker_worker import CheckerWorker
from msg_box import msg_box

# disables annoying warning that method is soon to be deprecated when performing TLS handshake with ETSI QKD server
urllib3.disable_warnings(urllib3.exceptions.SubjectAltNameWarning)


class ConnectWindow(QtWidgets.QMainWindow, Ui_ConnectWindow):

    def __init__(self):
        super(ConnectWindow, self).__init__()

        self.connect_worker = ConnectWorker()  # no parent!
        self.connect_thread = QThread()  # no parent!

        self.checker_worker = CheckerWorker()  # no parent!
        self.checker_thread = QThread()  # no parent!

        self.setupUi(self)

        self.connect_button.clicked.connect(self.connect_to)
        self.setup_connect_server()
        self.setup_checker_server()

    def check_usernames(self):
        while True:
            if self.sent_username is True and self.received_username is True:
                break
        self.main_window = MainWindow(self.other_ip_addr, self.your_username, self.other_username)
        self.main_window.show()

    def connect_to(self):

        while True:
            self.other_ip_addr = self.ip_addr.text()
            self.your_username = self.username.text()

            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                c.connect((self.other_ip_addr, 6180))
            except Exception as e:
                msg_box("Connection Refused", "Failed to connect to IP " + self.other_ip_addr + ", error msg is " + str(e))
                return

            try:
                c.send(self.your_username.encode())
            except Exception as e:
                msg_box("Failed to send", "Failed to send message, error msg is " + str(e))
                return

            c.close()
            self.checker_worker.sent_username = True
            return

    def setup_connect_server(self):

        self.connect_worker.other_ip_addr.connect(self.set_other_ip)
        self.connect_worker.other_username.connect(self.set_other_username)
        self.connect_worker.moveToThread(self.connect_thread)
        self.connect_thread.started.connect(self.connect_worker.connect_listening_server)
        self.connect_thread.finished.connect(app.exit)
        self.connect_thread.start()

    def setup_checker_server(self):

        self.checker_worker.start_main_window.connect(self.start_main_window)
        self.checker_worker.moveToThread(self.checker_thread)
        self.checker_thread.started.connect(self.checker_worker.check_to_start_main)
        self.checker_thread.finished.connect(app.exit)
        self.checker_thread.start()

    def set_other_ip(self, other_ip_addr):
        self.other_ip_addr = other_ip_addr

    def set_other_username(self, other_username):
        self.other_username = other_username
        self.checker_worker.received_username = True

    def start_main_window(self):
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
        self.chat_worker = ChatWorker()  # no parent!
        self.chat_thread = QThread()  # no parent!

        # Connect Worker`s signal to method to print message
        self.chat_worker.encrypted_msg.connect(self.print_msg)

        # Move the Worker object to the Thread object
        self.chat_worker.moveToThread(self.chat_thread)

        # Connect Thread started signal to Worker operational slot method
        self.chat_thread.started.connect(self.chat_worker.chat_listening_server)

        # Start the thread
        self.chat_thread.start()

    def print_msg(self, encrypted_msg):
        decrypted_msg = self.AES_obj.decrypt(encrypted_msg)
        self.decrypted_chat_box.append(self.other_username + " says:\n" + decrypted_msg + '\n')
        self.encrypted_chat_box.append(self.other_username + " says:\n" + encrypted_msg.decode() + '\n')

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
