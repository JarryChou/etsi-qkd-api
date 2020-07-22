# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect_gui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ConnectWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(486, 324)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(20, 20, 431, 241))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.ip_addr = QtWidgets.QLineEdit(self.frame)
        self.ip_addr.setGeometry(QtCore.QRect(30, 40, 371, 25))
        self.ip_addr.setObjectName("ip_addr")
        self.username = QtWidgets.QLineEdit(self.frame)
        self.username.setGeometry(QtCore.QRect(30, 120, 371, 25))
        self.username.setObjectName("username")
        self.ip_label = QtWidgets.QLabel(self.frame)
        self.ip_label.setGeometry(QtCore.QRect(30, 20, 261, 17))
        self.ip_label.setObjectName("ip_label")
        self.username_label = QtWidgets.QLabel(self.frame)
        self.username_label.setGeometry(QtCore.QRect(30, 100, 71, 17))
        self.username_label.setObjectName("username_label")
        self.connect_button = QtWidgets.QPushButton(self.frame)
        self.connect_button.setGeometry(QtCore.QRect(150, 160, 131, 61))
        self.connect_button.setObjectName("connect_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 486, 22))
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
        self.ip_label.setText(_translate("MainWindow", "IP Address to connect to"))
        self.username_label.setText(_translate("MainWindow", "Username"))
        self.connect_button.setText(_translate("MainWindow", "Connect"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

