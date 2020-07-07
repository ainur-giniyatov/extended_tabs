from qtpy.QtWidgets import QTabWidget
from qtpy.QtCore import Signal, Slot

from .tab_bar import TabBar


class TabWidget(QTabWidget):
    lastTabClosed = Signal()
    tabInsertedSig = Signal(int)
    tabRemovedSig = Signal(int)

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

    def addTab(self, widget, *__args):
        widget.windowTitleChanged.connect(self._on_window_title_changed)
        return super().addTab(widget, *__args)

    @Slot(str)
    def _on_window_title_changed(self, new_title):
        widget = self.sender()
        self.setTabText(self.indexOf(widget), new_title)
