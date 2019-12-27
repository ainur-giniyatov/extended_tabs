import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

from src.extendedtabs import TabWidget
from src.extendedtabs.tab_manager import TabManager, ISecondaryWindowCreator

from main_window import Ui_MainWindow
from src.extendedtabs.work_area import WorkArea


class SecWinCreator(ISecondaryWindowCreator):
    def __init__(self, parent_window, tab_man):
        self._parent_window = parent_window
        self._tab_manager = tab_man

    def create(self):
        new_window = QMainWindow(self._parent_window)
        new_window.setAttribute(Qt.WA_DeleteOnClose)
        work_area = WorkArea(new_window)
        work_area.setTabManager(self._tab_manager)

        destination_tab_widget = work_area._create_tab_widget(work_area)
        # destination_tab_widget.setTabManager(self._tab_manager)

        # destination_tab_widget.setTabsClosable(True)

        new_window.setCentralWidget(work_area)
        new_window.show()
        return new_window, destination_tab_widget


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._tab_manager = TabManager(self)
        self._tab_manager.setSecondaryWindowCreator(SecWinCreator(self, self._tab_manager))

        self.work_area.setTabManager(self._tab_manager)
        self.work_area.create_dumb()

        self.actionTest.triggered.connect(self._on_test)
        self.actionAdd.triggered.connect(self._on_add)
        self.actionSubwindow.triggered.connect(self._on_add_subwindow)

    def _on_test(self, state):
        print(len(self._tab_manager._tab_widgets))

    def _on_add(self, state):
        tab_widget = self.work_area.get_active_tab_widget()
        tab_widget.addTab(QWidget(), 'tab 5')

    def _on_add_subwindow(self, state):
        SecWinCreator(self, self._tab_manager).create()


        
if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    exit(qapp.exec_())
