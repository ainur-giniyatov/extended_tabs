# from functools import partial

from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QVariant, pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QSplitter, QTabBar

from .tab_widget import TabWidget


class WorkArea(QWidget):
    emptied = pyqtSignal()
    tabContextMenuRequested = pyqtSignal(int, int, QPoint)
    tabInserted = pyqtSignal(int, int)
    tabRemoved = pyqtSignal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._tab_manager = None
        self._vbox_layout = QVBoxLayout(self)
        self._vbox_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._vbox_layout)

        self._last_activated_tab_widget = None
        self._tab_widgets = []

        self._data = None
        self._focused_page: QWidget = None

    def destroy(self, destroyWindow=True, destroySubWindows=True):
        super().destroy(destroyWindow, destroySubWindows)
        self._tab_manager._del_wa(self)

    def get_active_tab_widget(self):
        if self._last_activated_tab_widget is None:
            self._last_activated_tab_widget = self._create_tab_widget(self)

        return self._last_activated_tab_widget

    def getTabWidget(self, index):
        return self._tab_widgets[index]

    def setTabManager(self, tab_manager):
        self._tab_manager = tab_manager
        self._tab_manager._add_wa(self)

    def setData(self, data):
        self._data = QVariant(data)

    def data(self):
        return self._data

    def _create_tab_widget(self, parent):
        tab_widget = TabWidget(parent)
        self._tab_widgets.append(tab_widget)
        tab_widget.setMovable(True)
        tab_widget.currentChanged.connect(self._on_current_tab_changed)
        tab_widget.tabBarClicked.connect(self._on_current_tab_changed)
        tab_widget.lastTabClosed.connect(self._on_last_tab_close)
        tab_widget.setTabManager(self._tab_manager)

        if parent is self:
            self._vbox_layout.addWidget(tab_widget)

        tab_bar = tab_widget.tabBar()
        tab_bar.setContextMenuPolicy(Qt.CustomContextMenu)
        tab_bar.customContextMenuRequested.connect(self._on_context_menu_requested)

        tab_widget.setFocus()

        tab_widget.tabInsertedSig.connect(self._on_tab_inserted)
        tab_widget.tabRemovedSig.connect(self._on_tab_removed)

        return tab_widget

    @pyqtSlot(int)
    def _on_tab_inserted(self, tab_index):
        tab_widget = self.sender()
        tab_widget_index = self._tab_widgets.index(tab_widget)
        self.tabInserted.emit(tab_widget_index, tab_index)

    @pyqtSlot(int)
    def _on_tab_removed(self, tab_index):
        tab_widget = self.sender()
        tab_widget_index = self._tab_widgets.index(tab_widget)
        self.tabRemoved.emit(tab_widget_index, tab_index)

    @pyqtSlot(int)
    def _on_current_tab_changed(self, tab_index):
        tab_widget = self.sender()
        assert isinstance(tab_widget, TabWidget)
        self._last_activated_tab_widget = tab_widget
        self._set_focused_page(tab_widget.widget(tab_index))

        for tw in self._tab_widgets:
            tw.tabBar().setStyleSheet('')

        tab_bar = tab_widget.tabBar()
        tab_bar.setStyleSheet('QTabBar::tab:selected{background: qlineargradient(x1: 0, y1: 0.85, x2: 0, y2: 1, stop: 0 white, stop: 1 blue)}')


    def _set_focused_page(self, widget: QWidget):
        assert widget is not None
        self._focused_page = widget
        self._focused_page.setFocus()

    def _on_context_menu_requested(self, point):
        tab_bar = self.sender()
        assert isinstance(tab_bar, QTabBar)
        tab_index = tab_bar.tabAt(point)
        tab_widget = tab_bar.parent()
        assert isinstance(tab_widget, TabWidget)

        tab_widget_index = self._tab_widgets.index(tab_widget)
        self.tabContextMenuRequested.emit(tab_widget_index, tab_index, tab_bar.mapTo(self, point))

    def splitTab(self, tab, orientation):
        tab_widget = tab.parent().parent()

        if tab_widget.count() <= 1:
            return

        assert isinstance(tab_widget, QTabWidget)
        tab_widgets_parent = tab_widget.parent()
        assert isinstance(tab_widgets_parent, (WorkArea, QSplitter))

        tab_index = tab_widget.indexOf(tab)
        tab_text = tab_widget.tabText(tab_index)
        tab_widget.removeTab(tab_index)

        splitter = QSplitter(orientation, tab_widgets_parent)
        splitter.setChildrenCollapsible(False)
        splitter.setHandleWidth(2)

        sizes = None
        if tab_widgets_parent == self:
            self._vbox_layout.addWidget(splitter)
        else:
            i = tab_widgets_parent.indexOf(tab_widget)
            sizes = tab_widgets_parent.sizes()
            tab_widgets_parent.insertWidget(i, splitter)

        splitter.addWidget(tab_widget)
        new_tab_widget = self._create_tab_widget(splitter)
        splitter.addWidget(new_tab_widget)
        new_tab_widget.addTab(tab, tab_text)

        assert splitter.count() == 2
        splitter.setSizes([10, 10])
        if sizes is not None:
            tab_widgets_parent.setSizes(sizes)

    def _on_last_tab_close(self):
        tab_widget = self.sender()
        assert isinstance(tab_widget, QTabWidget)
        self._last_tab_closed(tab_widget)

    def _last_tab_closed(self, tab_widget):
        if isinstance(tab_widget.parent(), QSplitter):
            splitter = tab_widget.parent()
            tab_widget_index = splitter.indexOf(tab_widget)
            if tab_widget_index == 0:
                second_tab_widget = splitter.widget(1)
            elif tab_widget_index == 1:
                second_tab_widget = splitter.widget(0)
            else:
                assert False

            assert isinstance(second_tab_widget, (TabWidget, QSplitter))
            second_tab_widget.setParent(None)
            p = splitter.parent()
            splitter.deleteLater()
            del splitter

            if isinstance(p, QSplitter):
                p.addWidget(second_tab_widget)
            elif isinstance(p, WorkArea):
                second_tab_widget.setParent(p)
                p.layout().addWidget(second_tab_widget)

            self._tab_widgets.remove(tab_widget)
            self._last_activated_tab_widget = second_tab_widget

        else:
            self._last_activated_tab_widget = tab_widget
            self.emptied.emit()
