from weakref import WeakSet

from PyQt5.QtCore import QObject, Qt, QPoint
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel
from PyQt5.QtGui import QCursor

from .tab_widget import TabWidget


class DraggingState:
    def __init__(self, tab_bar, index):
        # self.away = False
        self.tab_bar = tab_bar
        self.proximity_rect = tab_bar.rect().adjusted(-10, -10, 10, 10)
        self.index = index
        self.detached_widget = None
        self.dragging_image = None

    @property
    def tab_widget(self):
        return self.tab_bar.parent()


class TabManager(QObject):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self._main_window = main_window
        self._dragging_state = None

        self._tab_widgets = WeakSet()

    def _detach_tab(self):
        tab_widget = self._dragging_state.tab_widget
        self._dragging_state.detached_widget = tab_widget.widget(self._dragging_state.index)
        self._dragging_state.detached_widget.setWindowTitle(tab_widget.tabText(self._dragging_state.index))
        tab_widget.removeTab(self._dragging_state.index)

    def _drop_tab(self, pos):
        if self._dragging_state.detached_widget is not None:
            destination_tab_widget = self._get_tab_widget_under_mouse()
            if destination_tab_widget is None:
                new_window, destination_tab_widget = self.create_subwindow()
                new_window.move(QCursor.pos())
            
            index = destination_tab_widget.addTab(self._dragging_state.detached_widget, self._dragging_state.detached_widget.windowTitle())
            destination_tab_widget.setCurrentIndex(index)
            destination_tab_widget.activateWindow()

        self._dragging_state.detached_widget = None

    def _get_tab_widget_under_mouse(self):
        return next((widget for widget in self._tab_widgets if widget.underMouse()), None)

    def left_pressed(self, pos, tab_bar):
        self._dragging_state = DraggingState(tab_bar, tab_bar.tabAt(pos))
        
    def left_released(self, pos):
        if self._dragging_state is None:
            return
            
        self._drop_tab(pos)
        if self._dragging_state.dragging_image is not None:
            self._dragging_state.dragging_image.close()
        self._dragging_state = None

    def mouse_drag(self, pos):
        # self._dragging_state.away = not self._dragging_state.proximity_rect.contains(pos)
        if not self._dragging_state.proximity_rect.contains(pos):
            if not self._dragging_state.detached_widget:
                self._detach_tab()
                # if self._dragging_state.detached_widget:
                self._dragging_state.dragging_image = self._make_draggin_image()
        
        if self._dragging_state.dragging_image is not None:
            self._dragging_state.dragging_image.move(QCursor.pos() + QPoint(20, 20))
        
    def _make_draggin_image(self):
        dragging_image = QWidget(None, Qt.ToolTip)
        dragging_image.setAttribute(Qt.WA_DeleteOnClose)
        label = QLabel(self._dragging_state.detached_widget.windowTitle(), dragging_image)
        dragging_image.resize(50, 50)
        dragging_image.show()
        return dragging_image

    def create_subwindow(self):
        new_window = QMainWindow(self._main_window)
        new_window.setAttribute(Qt.WA_DeleteOnClose)
        destination_tab_widget = TabWidget(new_window)
        # destination_tab_widget.lastTabClosed.connect(new_window.close)
        # destination_tab_widget.setMovable(True)
        destination_tab_widget.setTabsClosable(True)
        destination_tab_widget.setTabManager(self, False)
        # destination_tab_widget.setMouseTracking(True)
        new_window.setCentralWidget(destination_tab_widget)
        new_window.show()
        return new_window, destination_tab_widget

    def memorizeTabWidget(self, tab_widget):
        self._tab_widgets.add(tab_widget)
