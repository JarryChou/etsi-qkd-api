from PyQt5 import QtCore, QtGui, QtWidgets
from gui_class import Ui_MainWindow
import sys, socket
from _thread import *
# from Crypto.Cipher import AES
from AES_class import AESCipher
import sys
sys.path.insert(1,'/home/alvin/PycharmProjects/etsi-qkd-api')
from project.kme import KME
import base64

def msg_box(title, data):
    w = QtWidgets.QWidget()
    QtWidgets.QMessageBox.information(w, title, data)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):


    def __init__(self):
        super(MainWindow, self).__init__()

        # Set up the user interface from Designer.
        self.setupUi(self)

        # Add more functionality to UI elements
        self.send_button.clicked.connect(self.send_message)

        # Retrieve a 256-bit qcrypto key as symmetric key for AES256 for this chat session
        KME_obj = KME('/home/alvin/PycharmProjects/etsi-qkd-api/key_files')
        key_container = KME_obj.get_key(1, 256)
        key = key_container['keys'][0]['key']
        key = base64.b64decode(key)
        self.AES_obj = AESCipher(key)

        self.start_server()

    def start_server(self):
        start_new_thread(self.server_socket, ())
        msg_box("Success", "Server Started Succesfully")

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
        rmessage = self.compose_msg_box.text()
        rmessage = rmessage.replace("#>", "")

        rmsg = nick + " #> " + rmessage

        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            c.connect((ip_address, 6190))
        except Exception as e:
            msg_box("Connection Refused", "Failed to connect to IP " + ip_address + ", error msg is " + str(e))
            return
        
        try:
            encrypted_msg = self.AES_obj.encrypt(rmsg)
            c.send(encrypted_msg)
            self.main_chat_box.append(rmsg)
        except Exception as e:
            msg_box("Failed to send", "Failed to send message, error msg is "+ str(e))
            
        c.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())