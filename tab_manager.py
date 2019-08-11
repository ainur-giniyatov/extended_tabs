from PyQt5.QtCore import QObject, Qt, QPoint
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel
from PyQt5.QtGui import QCursor

from tab_widget import TabWidget

class TabManager(QObject):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self._detached_widget = None
        self._main_window = main_window
        self._proximity_rect = None
        self._tab_bar = None
        self._away = False
        self._detached = False
        self._detached = False
        self._index = 0
        self._dragging_image = None

    def _detach_tab(self):
        if self._tab_bar.count() > 1:
            tab_widget = self._tab_bar.parent()
            self._detached_widget = tab_widget.widget(self._index)
            self._detached_widget.setWindowTitle(tab_widget.tabText(self._index))
            tab_widget.removeTab(self._index)
            self._detached = True

    def _drop_tab(self, pos):
        if self._detached:
            new_window = QMainWindow(self._main_window)
            
            new_tab_widget = TabWidget(new_window)
            new_tab_widget.setTabManager(self)
            new_window.setCentralWidget(new_tab_widget)
            new_tab_widget.addTab(self._detached_widget, self._detached_widget.windowTitle())

            new_window.show()
            new_window.move(QCursor.pos())

        self._detached = False
            
    def left_pressed(self, pos, tab_bar):
        self._tab_bar = tab_bar
        self._proximity_rect = tab_bar.rect().adjusted(-10, -10, 10, 10)
        
        self._index = self._tab_bar.tabAt(pos)
        
    def left_released(self, pos):
        self._drop_tab(pos)
        if self._dragging_image:
            self._dragging_image.close()
            self._dragging_image = None

    def mouse_drag(self, pos):
        self._away = not self._proximity_rect.contains(pos)
        if self._away:
            if not self._detached:
                self._detach_tab()
                if self._detached:
                    self._dragging_image = self._make_draggin_image()
        
        if self._dragging_image is not None:
            self._dragging_image.move(QCursor.pos() + QPoint(20, 20))
            
    def _make_draggin_image(self):
        dragging_image = QWidget(None, Qt.FramelessWindowHint)
        label = QLabel(self._detached_widget.windowTitle(), self._dragging_image)
        dragging_image.resize(50, 50)
        dragging_image.show()
        return dragging_image