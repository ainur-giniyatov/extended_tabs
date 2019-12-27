from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QSplitter, QTableWidget, QMenu, QTabBar, QLabel

from .tab_widget import TabWidget


class WorkArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._tab_manager = None
        self._vbox_layout = QVBoxLayout(self)
        self.setLayout(self._vbox_layout)

    def get_active_tab_widget(self):
        fw = self.focusWidget()

        if fw is None:
            fw = self._create_tab_widget(self)

        while not isinstance(fw, QTabWidget):
            fw = fw.parent()
            if fw == self:
                break

        if fw == self:
            fw = self._create_tab_widget(self)

        return fw

    def create_dumb(self):
        tab_widget = self._create_tab_widget(self)

        tab_widget.addTab(QLabel('cwgfwr'), '1')
        tab_widget.addTab(QTableWidget(), '2')
        tab_widget.addTab(QTableWidget(), '3')
        tab_widget.addTab(QTableWidget(), '4')

    def setTabManager(self, tab_manager):
        self._tab_manager = tab_manager

    def _create_tab_widget(self, parent):
        tab_widget = TabWidget(parent)

        tab_widget.setTabManager(self._tab_manager)

        if parent is self:
            self._vbox_layout.addWidget(tab_widget)

        tab_bar = tab_widget.tabBar()
        tab_bar.setContextMenuPolicy(Qt.CustomContextMenu)
        tab_bar.customContextMenuRequested.connect(self._on_context_menu_requested)

        tab_widget.setFocus()
        return tab_widget

    def _on_context_menu_requested(self, point):
        tab_bar = self.sender()
        assert isinstance(tab_bar, QTabBar)
        tab_index = tab_bar.tabAt(point)

        def _fe_v():
            self._on_split(tab_bar, tab_index, Qt.Horizontal)

        def _fe_h():
            self._on_split(tab_bar, tab_index, Qt.Vertical)

        def _fe_close():
            self._on_tab_close(tab_bar, tab_index)

        menu = QMenu()
        menu.addAction('split vertical', _fe_v)
        menu.addAction('split horizontal', _fe_h)
        menu.addSeparator()
        menu.addAction('close', _fe_close)
        menu.exec(tab_bar.mapToGlobal(point))

    def _on_split(self, tab_bar, tab_index, orientation):
        tab_widget = tab_bar.parent()
        assert isinstance(tab_widget, QTabWidget)
        tab_widgets_parent = tab_widget.parent()
        assert isinstance(tab_widgets_parent, (WorkArea, QSplitter))

        tab = tab_widget.widget(tab_index)
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

        if sizes is not None:
            tab_widgets_parent.setSizes(sizes)

    def _on_tab_close(self, tab_bar, tab_index):
        tab_widget = tab_bar.parent()
        assert isinstance(tab_widget, QTabWidget)
        tab = tab_widget.widget(tab_index)
        tab.deleteLater()
