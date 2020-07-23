from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread
import socket
from AES_class import AESCipher
import base64
import requests
from chat_worker import ChatWorker
from msg_box import msg_box
from chat_gui import Ui_ChatWindow


class ChatWindow(QtWidgets.QMainWindow, Ui_ChatWindow):
    """
    Inherits from GUI class chat_gui.py. The reason for inheritance is so that if changes need to be made to the UI from
    QT Designer 5, the new .py file it generates will not erase all of the networking functionality implemented here.
    """

    def __init__(self, other_ip_addr, your_username, other_username):
        super(ChatWindow, self).__init__()

        # Set up the user interface from Designer.
        self.setupUi(self)

        self.your_username = your_username
        self.other_username = other_username
        self.other_ip_addr = other_ip_addr

        # start chat server worker and thread
        self.chat_worker = ChatWorker()  # no parent!
        self.chat_thread = QThread()  # no parent!

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
            self.encrypted_chat_box.append(self.your_username + " says:\n" + encrypted_msg.decode() + '\n')
            self.decrypted_chat_box.append(self.your_username + " says:\n" + msg + '\n')
        except Exception as e:
            msg_box("Failed to send", "Failed to send message, error msg is " + str(e))

        c.close()