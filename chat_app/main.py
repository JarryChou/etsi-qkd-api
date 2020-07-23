from PyQt5 import QtWidgets
import sys
import urllib3
from connect_window import ConnectWindow


# disables annoying warning that method is soon to be deprecated when performing TLS handshake with ETSI QKD server
urllib3.disable_warnings(urllib3.exceptions.SubjectAltNameWarning)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ConnectWindow()
    window.show()
    sys.exit(app.exec_())
