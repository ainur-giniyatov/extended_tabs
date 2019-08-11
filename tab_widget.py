from PyQt5.QtWidgets import QTabWidget

from tab_bar import TabBar


class TabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._tab_bar = TabBar(self)
        self.setTabBar(self._tab_bar)
        self.is_main_tab = False

        self._tab_manager = None
    
    def setTabManager(self, tab_manager, is_main_tab=True):
        self._tab_manager = tab_manager
        self._tab_bar.setTabManager(self._tab_manager)
        self.is_main_tab = is_main_tab
