from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread
from connect_gui import Ui_ConnectWindow
import socket
from connect_worker import ConnectWorker
from checker_worker import CheckerWorker
from msg_box import msg_box
from chat_window import ChatWindow
import configparser


class ConnectWindow(QtWidgets.QMainWindow, Ui_ConnectWindow):

    def __init__(self):
        super(ConnectWindow, self).__init__()

        config = configparser.ConfigParser()
        config.read("port_config.ini")
        default_section = config['DEFAULT']

        self.connect_port = default_section.getint('connect_port')

        self.connect_worker = ConnectWorker(self.connect_port)  # no parent!
        self.connect_thread = QThread()  # no parent!

        self.checker_worker = CheckerWorker()  # no parent!
        self.checker_thread = QThread()  # no parent!

        self.setupUi(self)

        self.connect_button.clicked.connect(self.connect_to)
        self.setup_connect_server()
        self.setup_checker_server()



    def connect_to(self):

        while True:
            self.other_ip_addr = self.ip_addr.text()
            self.your_username = self.username.text()

            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                c.connect((self.other_ip_addr, self.connect_port))
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
        # self.connect_thread.finished.connect(app.exit)
        self.connect_thread.start()

    def setup_checker_server(self):

        self.checker_worker.start_chat_window.connect(self.start_chat_window)
        self.checker_worker.moveToThread(self.checker_thread)
        self.checker_thread.started.connect(self.checker_worker.check_to_start_main)
        # self.checker_thread.finished.connect(app.exit)
        self.checker_thread.start()

    def set_other_ip(self, other_ip_addr):
        self.other_ip_addr = other_ip_addr

    def set_other_username(self, other_username):
        self.other_username = other_username
        self.checker_worker.received_username = True

    def start_chat_window(self):
        self.chat_window = ChatWindow(self.other_ip_addr, self.your_username, self.other_username)
        self.chat_window.show()
