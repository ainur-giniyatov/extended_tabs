import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QTableWidget, QMenu, QLineEdit

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
        work_area.emptied.connect(new_window.close)
        work_area.tabContextMenuRequested.connect(self._parent_window._on_tab_context_menu_requested)
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
        self.work_area.tabContextMenuRequested.connect(self._on_tab_context_menu_requested)
        tab_widget = self.work_area._create_tab_widget(self.work_area)

        tab_widget.addTab(QLabel('cwgfwr'), '1')
        tab_widget.addTab(QTableWidget(), '2')
        tab_widget.addTab(QTableWidget(), '3')
        tab_widget.addTab(QTableWidget(), '4')

        self.actionTest.triggered.connect(self._on_test)
        self.actionAdd.triggered.connect(self._on_add)
        self.actionSubwindow.triggered.connect(self._on_add_subwindow)

        self.work_area.tabFocused.connect(self._on_tab_focused)

    def _on_test(self, state):
        print(len(self._tab_manager._tab_widgets))

    def _on_add(self, state):
        tab_widget = self.work_area.get_active_tab_widget()
        tab_widget.addTab(QLineEdit(), 'tab 5')

    def _on_add_subwindow(self, state):
        SecWinCreator(self, self._tab_manager).create()

    def _on_tab_context_menu_requested(self, twi, tbi, point):
        work_area = self.sender()
        assert isinstance(work_area, WorkArea)
        glob_point = work_area.mapToGlobal(point)
        menu = QMenu()
        menu.addAction('Split vertically', self._on_tab_split).setData([work_area, twi, tbi, Qt.Horizontal])
        menu.addAction('Split horizontally', self._on_tab_split).setData([work_area, twi, tbi, Qt.Vertical])
        menu.addSeparator()
        menu.addAction('Close', self._on_tab_close).setData([work_area, twi, tbi])
        menu.exec(glob_point)

    def _on_tab_split(self):
        action = self.sender()
        t = action.data()
        work_area, tab_widget_index, tab_index, orientation = t
        tab_widget = work_area.getTabWidget(tab_widget_index)
        tab = tab_widget.widget(tab_index)
        work_area.splitTab(tab, orientation)

    def _on_tab_close(self):
        action = self.sender()
        t = action.data()
        work_area, tab_widget_index, tab_index = t
        tab_widget = work_area.getTabWidget(tab_widget_index)
        tab_widget.removeTab(tab_index)

    def _on_tab_focused(self, tab_widget_index, tab_index):
        print(tab_widget_index, tab_index)


if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    exit(qapp.exec_())
