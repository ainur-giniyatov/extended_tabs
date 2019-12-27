from PyQt5.QtCore import QObject, Qt, QEvent, QPoint
from PyQt5.QtGui import QGuiApplication, QCursor
from PyQt5.QtWidgets import QLabel


class TabDrag(QObject):
    def __init__(self, manager):
        super().__init__()
        self._manager = manager
        ds = self._manager._dragging_state
        ds.detached_tab = ds.tab_widget.widget(ds.tab_index)
        ds.detached_tab.setWindowTitle(ds.tab_widget.tabText(ds.tab_index))
        ds.dragging_pixmap = ds.detached_tab.grab()

        self._thumb_widg = self._make_thumb_widg()

    def exec(self):
        QGuiApplication.instance().installEventFilter(self)
        result = False
        ds = self._manager._dragging_state
        tab_widget = ds.tab_widget
        while QGuiApplication.mouseButtons() & Qt.LeftButton:
            QGuiApplication.processEvents()
            loc_pos = tab_widget.mapFromGlobal(QCursor.pos())
            if not tab_widget.rect().contains(loc_pos):
                if tab_widget.indexOf(ds.detached_tab) >= 0:
                    result = True
            else:
                result = False

        self._thumb_widg.close()
        self._thumb_widg = None
        QGuiApplication.instance().removeEventFilter(self)
        return result

    def eventFilter(self, obj, event):
        if self._thumb_widg is not None and event.type() == QEvent.MouseMove:
            self._thumb_widg.move(QCursor.pos() + QPoint(10, 10,))
        return event.type() in (QEvent.MouseMove, QEvent.MouseButtonPress, QEvent.MouseButtonRelease)

    def _make_thumb_widg(self):
        label = QLabel(None)
        label.setWindowFlags(Qt.ToolTip)
        label.setWindowOpacity(0.6)
        label.setAttribute(Qt.WA_DeleteOnClose)
        label.setScaledContents(True)

        pix = self._manager._dragging_state.dragging_pixmap
        label.setPixmap(pix)

        label.resize(pix.size().scaled(150, 150, Qt.KeepAspectRatio))
        label.show()
        return label
