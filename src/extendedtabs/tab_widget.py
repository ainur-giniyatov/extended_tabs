from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal

from .tab_bar import TabBar


class TabWidget(QTabWidget):
    lastTabClosed = pyqtSignal()
    tabInsertedSig = pyqtSignal(int)
    tabRemovedSig = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._tab_bar = TabBar(self)
        self.setTabBar(self._tab_bar)

        self._tab_manager = None

        self.setAcceptDrops(True)
    
    def setTabManager(self, tab_manager):
        self._tab_manager = tab_manager
        self._tab_bar.setTabManager(self._tab_manager)
        self._tab_manager.memorizeTabWidget(self)

    def tabInserted(self, index):
        super().tabInserted(index)
        self.tabInsertedSig.emit(index)

    def tabRemoved(self, index):
        super().tabRemoved(index)
        self.tabRemovedSig.emit(index)
        if self.count() == 0:
            self.lastTabClosed.emit()
