from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal

from .tab_bar import TabBar


class TabWidget(QTabWidget):
    lastTabClosed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._tab_bar = TabBar(self)
        self.setTabBar(self._tab_bar)
        self.tabCloseRequested.connect(self._on_tabCloseRequested)
        self._tab_manager = None

        self.setAcceptDrops(True)
    
    def setTabManager(self, tab_manager):
        self._tab_manager = tab_manager
        self._tab_bar.setTabManager(self._tab_manager)
        self._tab_manager.memorizeTabWidget(self)

    def _on_tabCloseRequested(self, index):
        widget = self.widget(index)
        self.removeTab(index)
        widget.close()

    def tabRemoved(self, index):
        if self.count() == 0:
            self.lastTabClosed.emit()

    # def dragEnterEvent(self, event):
    #     if event.mimeData().hasFormat('internal/tab'):
    #         event.acceptProposedAction()
    #
    # def dropEvent(self, event):
    #     print(event.mimeData().formats())
    #     tab = self._tab_manager._dragging_state.detached_widget
    #     self.addTab(tab, 'dd')
