# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chatV2.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.upper_frame = QtWidgets.QFrame(self.centralwidget)
        self.upper_frame.setGeometry(QtCore.QRect(10, 10, 781, 21))
        self.upper_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.upper_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.upper_frame.setObjectName("upper_frame")

        self.ip_addr_label = QtWidgets.QLabel(self.upper_frame)
        self.ip_addr_label.setGeometry(QtCore.QRect(10, 0, 91, 17))
        self.ip_addr_label.setObjectName("ip_addr_label")

        self.ip_addr_line = QtWidgets.QLineEdit(self.upper_frame)
        self.ip_addr_line.setGeometry(QtCore.QRect(110, 0, 181, 25))
        self.ip_addr_line.setObjectName("ip_addr_line")

        self.nick_label = QtWidgets.QLabel(self.upper_frame)
        self.nick_label.setGeometry(QtCore.QRect(460, 0, 67, 17))
        self.nick_label.setObjectName("nick_label")

        self.nick_line = QtWidgets.QLineEdit(self.upper_frame)
        self.nick_line.setGeometry(QtCore.QRect(540, 0, 221, 25))
        self.nick_line.setObjectName("nick_line")

        self.main_frame = QtWidgets.QFrame(self.centralwidget)
        self.main_frame.setGeometry(QtCore.QRect(10, 30, 781, 531))
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")

        self.main_chat_box = QtWidgets.QTextEdit(self.main_frame)
        self.main_chat_box.setGeometry(QtCore.QRect(10, 0, 761, 451))
        self.main_chat_box.setObjectName("main_chat_box")

        self.compose_msg_box = QtWidgets.QLineEdit(self.main_frame)
        self.compose_msg_box.setGeometry(QtCore.QRect(10, 460, 661, 61))
        self.compose_msg_box.setObjectName("compose_msg_box")

        self.send_button = QtWidgets.QPushButton(self.main_frame)
        self.send_button.setGeometry(QtCore.QRect(680, 460, 89, 61))
        self.send_button.setObjectName("send_button")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.ip_addr_label.setText(_translate("MainWindow", "IP Address:"))
        self.nick_label.setText(_translate("MainWindow", "Nick"))
        self.compose_msg_box.setText(_translate("MainWindow", "compose your message here"))
        self.send_button.setText(_translate("MainWindow", "Send"))

