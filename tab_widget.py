from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal

from tab_bar import TabBar


class TabWidget(QTabWidget):
    lastTabClosed = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self._tab_bar = TabBar(self)
        self.setTabBar(self._tab_bar)
        self.is_main_tab = False
        self.tabCloseRequested.connect(self._on_tabCloseRequested)
        self._tab_manager = None
    
    def setTabManager(self, tab_manager, is_main_tab=True):
        self._tab_manager = tab_manager
        self._tab_bar.setTabManager(self._tab_manager)
        self.is_main_tab = is_main_tab
        self._tab_manager.memorizeTabWidget(self)

    def _on_tabCloseRequested(self, index):
        widget = self.widget(index)
        self.removeTab(index)
        # print(widget.close())

    def tabRemoved(self, index):
        if self.count() == 0:
            self.lastTabClosed.emit()

        
