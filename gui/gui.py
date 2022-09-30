from typing import Union

from PyQt5 import Qt


class Gui(Qt.QWidget):
    def __init__(self,
                 size: Union[tuple[int, int], tuple[int, int, int, int]] = None,
                 title: str = None,
                 icon: str = None,
                 *args, **kwargs):
        if size is None: size = (800, 500)
        if title is None: title = "Gui"

        assert isinstance(size, tuple) and (len(size) in (2, 4)) and all([isinstance(s, int) for s in size]), \
            "size must be a tuple of 'int' of length 2 or 4"

        super(Gui, self).__init__(*args, **kwargs)
        sw, sh = self.screen().size().width(), self.screen().size().height()
        x, y = ((sw - size[0]) // 2, (sh - size[1]) // 4) if len(size) == 2 else size[2:]
        w, h = size[:2]
        self.setWindowTitle(title)
        self.setWindowIcon(Qt.QIcon(icon))
        self.setGeometry(x, y, w, h)
        self.setMinimumSize(w, h)
        cnt = Qt.QVBoxLayout()
        cnt.setContentsMargins(1, 1, 1, 1)
        self.setLayout(cnt)

        self.mainFrame = Qt.QFrame(self)
        self.mainFrame.setStyleSheet("background: red")
        layout = Qt.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.mainFrame.setLayout(layout)
        cnt.addWidget(self.mainFrame)
        # ui here
        layout.addWidget(self.canvas(), 1)
        layout.addWidget(self.dock())

    def canvas(self):
        canvas = Qt.QLabel(self.mainFrame)
        canvas.setStyleSheet("background: wheat")
        canvas.setMinimumWidth(500)
        canvas.setMaximumWidth(500)
        canvas.resizeEvent = lambda a0: canvas.setMaximumWidth(max(500, a0.size().height()))
        return canvas

    def dock(self):
        dock = Qt.QFrame(self.mainFrame)
        dock.setStyleSheet("background: blue")
        dock.setMinimumWidth(300)
        hBox = Qt.QHBoxLayout()
        dock.setLayout(hBox)
        tabs = Qt.QTabWidget(dock)
        tabs.setStyleSheet("background: lightblue")
        tabs.addTab(Qt.QLabel("t1"), "Primary")
        tabs.addTab(Qt.QLabel("t2"), "Secondary")
        hBox.addWidget(tabs)
        return dock


def main(*args, **kwargs):
    app = Qt.QApplication([])
    win = Gui(*args, **kwargs)
    win.show()
    win.activateWindow()
    app.exec_()
