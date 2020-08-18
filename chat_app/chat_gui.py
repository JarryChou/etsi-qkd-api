# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chat_gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ChatWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(666, 511)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.main_frame = QtWidgets.QFrame(self.centralwidget)
        self.main_frame.setGeometry(QtCore.QRect(10, 60, 641, 401))
        self.main_frame.setAutoFillBackground(False)
        self.main_frame.setStyleSheet("selection-color: rgb(117, 80, 123);")
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")
        self.decrypted_chat_box = QtWidgets.QTextEdit(self.main_frame)
        self.decrypted_chat_box.setGeometry(QtCore.QRect(10, 30, 321, 301))
        self.decrypted_chat_box.setObjectName("decrypted_chat_box")
        self.compose_msg_box = QtWidgets.QLineEdit(self.main_frame)
        self.compose_msg_box.setGeometry(QtCore.QRect(10, 340, 521, 51))
        self.compose_msg_box.setText("")
        self.compose_msg_box.setObjectName("compose_msg_box")
        self.send_button = QtWidgets.QPushButton(self.main_frame)
        self.send_button.setGeometry(QtCore.QRect(530, 340, 101, 51))
        self.send_button.setObjectName("send_button")
        self.encrypted_chat_box = QtWidgets.QTextEdit(self.main_frame)
        self.encrypted_chat_box.setGeometry(QtCore.QRect(330, 30, 301, 301))
        self.encrypted_chat_box.setObjectName("encrypted_chat_box")
        self.label = QtWidgets.QLabel(self.main_frame)
        self.label.setGeometry(QtCore.QRect(120, 10, 111, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.main_frame)
        self.label_2.setGeometry(QtCore.QRect(440, 10, 111, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(230, 0, 241, 61))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(":/newPrefix/logo/logo.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 666, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SpeQtral Chat"))
        self.send_button.setText(_translate("MainWindow", "Send"))
        self.label.setText(_translate("MainWindow", "Decrypted Chat"))
        self.label_2.setText(_translate("MainWindow", "Encrypted Chat"))
