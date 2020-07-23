from PyQt5 import QtWidgets


def msg_box(title, data):
    w = QtWidgets.QWidget()
    QtWidgets.QMessageBox.information(w, title, data)