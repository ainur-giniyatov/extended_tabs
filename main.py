import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget
from PyQt5.QtCore import Qt, QRect, pyqtSignal
from PyQt5.QtGui import QCursor

from tab_bar import TabBar
from tab_manager import TabManager

from main_window import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._tab_manager = TabManager(self)
        self.tabWidget.setTabManager(self._tab_manager)

        self.tabWidget.addTab(QWidget(), 'tab 1')
        self.tabWidget.addTab(QWidget(), 'tab 2')
        self.tabWidget.addTab(QWidget(), 'tab 3')
        self.tabWidget.addTab(QWidget(), 'tab 4')
        self.tabWidget.addTab(QWidget(), 'tab 5')

        self._torn_pages = []

    def _on_torn(self, index):
        widget = self.tabWidget.widget(index)
        self.tabWidget.removeTab(index)
        
        tab_w = QTabWidget()
        self._torn_pages.append(tab_w)
        tab_w.addTab(widget, 'new tab')
        tab_w.move(QCursor.pos())
        tab_w.show()


if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    exit(qapp.exec_())