import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

from src.extendedtabs.tab_manager import TabManager

from main_window import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._tab_manager = TabManager(self, self)
        self.tabWidget.setTabManager(self._tab_manager)

        self.tabWidget.addTab(QWidget(), 'tab 1')
        self.tabWidget.addTab(QWidget(), 'tab 2')
        self.tabWidget.addTab(QWidget(), 'tab 3')
        self.tabWidget.addTab(QWidget(), 'tab 4')
        self.tabWidget.addTab(QWidget(), 'tab 5')

        self.actionTest.triggered.connect(self._on_test)
        self.actionAdd.triggered.connect(self._on_add)
        self.actionSubwindow.triggered.connect(self._on_add_subwindow)

    def _on_test(self, state):
        print(len(self._tab_manager._tab_widgets))

    def _on_add(self, state):
        self.tabWidget.addTab(QWidget(), 'tab 5')

    def _on_add_subwindow(self, state):
        self._tab_manager.create_subwindow()

        
if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    exit(qapp.exec_())
