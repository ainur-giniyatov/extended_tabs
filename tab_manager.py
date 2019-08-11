from PyQt5.QtCore import QObject


class TabManager(QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self._detached_widget = None

    def detach_tab(self, index, tab_widget):
        self._detached_widget = tab_widget.widget(index)
        tab_widget.removeTab(index)
        print('detach')

    def drop_tab(self, pos):
        if self._detached_widget:
            self._detached_widget.setParent(None)
            self._detached_widget.show()