from functools import partial
from weakref import WeakSet
from typing import Callable

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication

from .work_area import WorkArea
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
    workAreaAdded = pyqtSignal(int)
    workAreaRemoved = pyqtSignal(int)

    tabAdded = pyqtSignal(int, int)
    tabRemoved = pyqtSignal(int, int)

    def __init__(self, parent):
        super().__init__(parent)
        self._dragging_state = None
        self._secondary_window_creator = None

        self._tab_widgets = WeakSet()
        self._work_areas = []

    def setSecondaryWindowCreator(self, secondary_window_creator):
        assert isinstance(secondary_window_creator, ISecondaryWindowCreator)
        self._secondary_window_creator = secondary_window_creator

    def createSecondaryWindow(self):
        return self._secondary_window_creator.create()

    def _drop_tab(self):
        detached_tab = self._dragging_state.detached_tab
        if detached_tab is not None:
            destination_tab_widget = self._get_tab_widget_under_mouse()
            if destination_tab_widget is None:
                new_window, destination_tab_widget = self.createSecondaryWindow()
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
            tb = tb.parent() if isinstance(tb.parent, Callable) else None

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

    @property
    def tab_widgets(self):
        return [*self._tab_widgets]

    @property
    def work_areas(self):
        return self._work_areas

    def _add_wa(self, work_area):
        self._work_areas.append(work_area)
        self.workAreaAdded.emit(len(self._work_areas) - 1)
        work_area.destroyed.connect(partial(self._on_wa_destroyed, work_area))
        work_area.tabInserted.connect(self._on_tab_inserted)
        work_area.tabRemoved.connect(self._on_tab_removed)

    def _on_wa_destroyed(self, work_area, obj):
        assert isinstance(work_area, WorkArea)
        self._del_wa(work_area)

    def _del_wa(self, work_area):
        assert work_area in self._work_areas
        self._work_areas.remove(work_area)
        self.workAreaRemoved.emit(len(self._work_areas))

    def _on_tab_inserted(self, tab_widget_index, tab_index):
        wa = self.sender()
        assert isinstance(wa, WorkArea)
        tab_widget = wa.getTabWidget(tab_widget_index)
        tab = tab_widget.widget(tab_index)
        all_tabs = [tw.widget(i) for wa in self._work_areas for tw in wa._tab_widgets for i in range(0, tw.count())]
        self.tabAdded.emit(self._work_areas.index(wa), all_tabs.index(tab))

    def _on_tab_removed(self, tab_widget_index, tab_index):
        wa = self.sender()
        assert isinstance(wa, WorkArea)

        print(tab_widget_index, tab_index)
