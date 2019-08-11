from PyQt5.QtWidgets import QTabBar, QApplication
from PyQt5.QtCore import Qt, QRect, pyqtSignal


class TabBar(QTabBar):

    def __init__(self, parent):
        super().__init__(parent)
        self._pressed = False
        self._away = False
        self._index = 0
        self._tab_manager = None
        self._proximity_rect = None
        self._detached = False
    
    def setTabManager(self, tab_manager):
        self._tab_manager = tab_manager

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._pressed = True
            self._index = self.tabAt(event.pos())
            self._proximity_rect = self.rect().adjusted(-10, -10, 10, 10)

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self._detached:
                self._tab_manager.drop_tab(event)
            self._pressed = False
            self._detached = False

        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self._pressed:
            self._away = not self._proximity_rect.contains(event.pos())
            if self._away:
                if not self._detached:
                    self._tab_manager.detach_tab(self._index, self.parent())
                    self._detached = True
            
                 