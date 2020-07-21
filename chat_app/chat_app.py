from PyQt5 import QtWidgets
from gui_class import Ui_MainWindow
import sys
import socket
from _thread import *
from AES_class import AESCipher
import base64
import requests
import urllib3

# disables annoying warning that method is soon to be deprecated when performing TLS handshake with ETSI QKD server
urllib3.disable_warnings(urllib3.exceptions.SubjectAltNameWarning)


def msg_box(title, data):
    w = QtWidgets.QWidget()
    QtWidgets.QMessageBox.information(w, title, data)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        # Set up the user interface from Designer.
        self.setupUi(self)

        # Add more functionality to UI elements. These are inherited from gui_class.py.
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

        self.start_server()

    def start_server(self):
        start_new_thread(self.server_socket, ())
        msg_box("Success", "Server Started Successfully")

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

            incoming_ip = str(addr[0])
            current_chat_ip = self.ip_addr_line.text()

            if incoming_ip != current_chat_ip:
                conn.close()
            else:
                data = conn.recv(4096)
                decrypted_msg = self.AES_obj.decrypt(data)
                self.main_chat_box.append(decrypted_msg)
                conn.close()
        s.close()

    def send_message(self):
        ip_address = self.ip_addr_line.text()

        nick = self.nick_line.text()
        nick = nick.replace("#>", "")
        raw_message = self.compose_msg_box.text()
        raw_message = raw_message.replace("#>", "")

        processed_message = nick + " #> " + raw_message

        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            c.connect((ip_address, 6190))
        except Exception as e:
            msg_box("Connection Refused", "Failed to connect to IP " + ip_address + ", error msg is " + str(e))
            return
        
        try:
            encrypted_msg = self.AES_obj.encrypt(processed_message)
            c.send(encrypted_msg)
            self.main_chat_box.append(processed_message)
        except Exception as e:
            msg_box("Failed to send", "Failed to send message, error msg is " + str(e))
            
        c.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
