import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QObject,pyqtSignal
import 爬虫.top250.findJob as findJop
import 爬虫.top250.showResult as showResult

class findJopFrame(QMainWindow,findJop.Ui_Dialog):
    def __init__(self):
        super(findJopFrame, self).__init__()
        self.setupUi(self)


class resultFrame(QMainWindow,showResult.Ui_Dialog):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setupUi(self)
    def SHOW(self):
        self.show()

if __name__=='__main__':
    app = QApplication(sys.argv)
    main = findJopFrame()
    main.show()
    result_frame = resultFrame()
    main.pushButton.clicked.connect(result_frame.SHOW)
    sys.exit(app.exec_())