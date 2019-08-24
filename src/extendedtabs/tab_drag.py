from PyQt5.QtCore import QObject, Qt, QEvent, QPoint
from PyQt5.QtGui import QGuiApplication, QCursor
from PyQt5.QtWidgets import QWidget, QLabel


class TabDrag(QObject):
    def __init__(self, manager):
        super().__init__()
        self._manager = manager
        ds = self._manager._dragging_state
        ds.detached_widget = ds.tab_widget.widget(ds.index)
        ds.detached_widget.setWindowTitle(ds.tab_widget.tabText(ds.index))
        self._dragging_img = self._make_draggin_image()

    def exec(self):
        QGuiApplication.instance().installEventFilter(self)
        result = False
        while QGuiApplication.mouseButtons() & Qt.LeftButton:
            QGuiApplication.processEvents()
            ds = self._manager._dragging_state
            tab_widget = ds.tab_widget
            loc_pos = tab_widget.mapFromGlobal(QCursor.pos())
            if not tab_widget.rect().contains(loc_pos):
                if tab_widget.indexOf(ds.detached_widget) >=0:
                    tab_widget.removeTab(ds.index)
                    result = True

        self._dragging_img.close()
        self._dragging_img = None
        QGuiApplication.instance().removeEventFilter(self)
        return result

    def eventFilter(self, obj, event):
        if self._dragging_img is not None and event.type() == QEvent.MouseMove:
            self._dragging_img.move(QCursor.pos() + QPoint(20, 20,))
        return event.type() in (QEvent.MouseMove, QEvent.MouseButtonPress, QEvent.MouseButtonRelease)

    def _make_draggin_image(self):
        dragging_image = QWidget(None, Qt.ToolTip)
        dragging_image.setAttribute(Qt.WA_DeleteOnClose)
        label = QLabel(':' + self._manager._dragging_state.detached_widget.windowTitle(), dragging_image)
        dragging_image.resize(50, 50)
        dragging_image.show()
        return dragging_image