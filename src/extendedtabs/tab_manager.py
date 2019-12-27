from weakref import WeakSet

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication

from .tab_widget import TabWidget
from .tab_drag import TabDrag


class ISecondaryWindowCreator:
    def create(self):
        raise NotImplementedError


class DraggingState:
    def __init__(self, tab_bar, tab_indx):
        self.tab_bar = tab_bar
        self.tab_index = tab_indx
        self.proximity_rect = tab_bar.rect().adjusted(-10, -10, 10, 10)
        self.detached_tab = None
        self.dragging_image = None
        self.dragging_pixmap = None

    @property
    def tab_widget(self):
        return self.tab_bar.parent()


class TabManager(QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self._dragging_state = None
        self._secondary_window_creator = None

        self._tab_widgets = WeakSet()

    def setSecondaryWindowCreator(self, secondary_window_creator):
        assert isinstance(secondary_window_creator, ISecondaryWindowCreator)
        self._secondary_window_creator = secondary_window_creator

    def _drop_tab(self):
        detached_tab = self._dragging_state.detached_tab
        if detached_tab is not None:
            destination_tab_widget = self._get_tab_widget_under_mouse()
            if destination_tab_widget is None:
                new_window, destination_tab_widget = self._secondary_window_creator.create()
                new_window.move(QCursor.pos())

            source_tab_widget = detached_tab.parent().parent()
            assert isinstance(source_tab_widget, TabWidget)
            index = destination_tab_widget.addTab(detached_tab, detached_tab.windowTitle())
            destination_tab_widget.setCurrentIndex(index)
            destination_tab_widget.activateWindow()

        self._dragging_state.detached_tab = None

    def _get_tab_widget_under_mouse(self):
        tb = QApplication.widgetAt(QCursor.pos())
        while tb not in [None, *self._tab_widgets]:
            tb = tb.parent()

        return tb

    def left_pressed(self, event, tab_bar):
        self._dragging_state = DraggingState(tab_bar, tab_bar.tabAt(event.pos()))
        
    def left_released(self, event, tab_bar):
        if self._dragging_state is None:
            return

        self._dragging_state = None

    def mouse_drag(self, event, tab_bar):
        if self._dragging_state.tab_bar is tab_bar and not self._dragging_state.proximity_rect.contains(event.pos()):
            drag = TabDrag(self)
            if drag.exec():
                self._drop_tab()

    def memorizeTabWidget(self, tab_widget):
        self._tab_widgets.add(tab_widget)
