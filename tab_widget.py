from PyQt5.QtWidgets import QTabWidget

from tab_bar import TabBar


class TabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._tab_bar = TabBar(self)
        self.setTabBar(self._tab_bar)

        self._tab_manager = None
    
    def setTabManager(self, tab_manager):
        self._tab_manager = tab_manager
        self._tab_bar.setTabManager(self._tab_manager)