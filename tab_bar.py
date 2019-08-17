from PyQt5.QtWidgets import QTabBar, QApplication
from PyQt5.QtCore import Qt, QRect, pyqtSignal


class TabBar(QTabBar):

    def __init__(self, parent):
        super().__init__(parent)
        self._pressed = False
        self._away = False
        self._tab_manager = None
    
    def setTabManager(self, tab_manager):
        self._tab_manager = tab_manager

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._pressed = True
            self._tab_manager.left_pressed(event.pos(), self)

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._tab_manager.left_released(event.pos())
            self._pressed = False

        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self._pressed:
            self._tab_manager.mouse_drag(event.pos(), event)
        else:
            super().mouseMoveEvent(event)
            
                 