from PyQt5.QtWidgets import QTabBar
from PyQt5.QtCore import Qt


class TabBar(QTabBar):

    def __init__(self, parent):
        super().__init__(parent)
        self._away = False
        self._tab_manager = None
        self.setContextMenuPolicy(Qt.CustomContextMenu)

    def setTabManager(self, tab_manager):
        self._tab_manager = tab_manager

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._tab_manager.left_pressed(event, self)

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._tab_manager.left_released(event, self)

        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if Qt.LeftButton & event.buttons():
            self._tab_manager.mouse_drag(event, self)
        else:
            super().mouseMoveEvent(event)
