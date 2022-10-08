from typing import Union
from collections import namedtuple

from PyQt5 import Qt

from src import Warp, Noise, perlinGenerator

primarySettings = namedtuple("primarySettings", ["seed",
                                                 "frequency",
                                                 "waveLength",
                                                 "warp",
                                                 "range",
                                                 "octaves",
                                                 "persistence",
                                                 "lacunarity"])


class InputBox(Qt.QFrame):
    def __init__(self, *args,
                 label: str = None,
                 horiz: bool = False,
                 **kwargs):
        if label is None: label = ""
        self.label = label
        super(InputBox, self).__init__(*args, **kwargs)
        self.lay = Qt.QVBoxLayout() if not horiz else Qt.QHBoxLayout()
        self.setLayout(self.lay)
        self.lab = Qt.QLabel(self.label)
        self.lay.addWidget(self.lab, 0)

    def addInteger(self, _min: int = None, _max: int = None, default: int = None, onChange=None):
        x = Qt.QSpinBox()
        x.setMaximum(2 ** 16)
        x.setMinimum(-2 ** 16)
        if _min is not None: x.setMinimum(_min)
        if _max is not None: x.setMaximum(_max)
        if default is not None: x.setValue(default)
        if onChange is not None: x.valueChanged.connect(onChange)  # noqa
        self.lay.addWidget(x, 1)
        return x

    def addDouble(self, _min: float = None, _max: float = None, default: float = None, onChange=None,
                  decimals: float = None, step: float = None):
        x = Qt.QDoubleSpinBox()
        x.setMaximum(2 ** 32)
        x.setMinimum(-2 ** 32)
        if _min is not None: x.setMinimum(_min)
        if _max is not None: x.setMaximum(_max)
        if default is not None: x.setValue(default)
        if onChange is not None: x.valueChanged.connect(onChange)  # noqa
        if decimals is not None: x.setDecimals(0)
        if step is not None:
            x.setSingleStep(step)
        else:
            x.setSingleStep(10 ** -x.decimals())
        self.lay.addWidget(x, 1)
        return x

    def addSlider(self, _min: int = None, _max: int = None, default: int = None, onChange=None):
        x = Qt.QSlider(Qt.Qt.Horizontal)
        if _min is not None: x.setMinimum(_min)
        if _max is not None: x.setMaximum(_max)
        if default is not None: x.setValue(default)
        if onChange is not None: x.valueChanged.connect(onChange)  # noqa
        x.valueChanged.connect(lambda val: self.lab.setText(self.label + f": {val}"))  # noqa
        self.lab.setText(self.label + f": {x.value()}")
        self.lay.addWidget(x, 1)
        return x

    def addDrop(self, drops: tuple = None, default: int = None, onChange=None):
        if drops is None: drops = ("...",)
        x = Qt.QComboBox()
        x.addItems(drops)
        if default is not None: x.setCurrentIndex(default)
        if onChange is not None: x.currentIndexChanged.connect(onChange)  # noqa
        self.lay.addWidget(x)
        return x

    def addEnabledInp(self, label: str = None, default: bool = False, inp=None):
        if label is None: label = "Enable Input"
        x = Qt.QCheckBox(label)
        x.setChecked(default)
        x.toggled.connect(lambda val: inp.setDisabled(not val))  # noqa
        inp.setDisabled(not x.isChecked())
        self.lay.addWidget(x)
        return x


class ImgCanvas(Qt.QLabel):
    def __init__(self, *args,
                 size: tuple[int, int] = None,
                 **kwargs):
        if size is None: size = (500, 500)
        super(ImgCanvas, self).__init__(*args, **kwargs)
        self.setMinimumSize(*size)

    def resizeEvent(self, a0: "Qt.QResizeEvent") -> None:
        self.setMaximumWidth(max(self.minimumWidth(), a0.size().height()))


class Gui(Qt.QWidget):
    def __init__(self, *args,
                 size: Union[tuple[int, int], tuple[int, int, int, int]] = None,
                 title: str = None,
                 icon: str = None,
                 **kwargs):
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
        # --- ui here ---
        canvas = self.canvas()
        dock = self.dock()
        # ---------------
        layout.addWidget(canvas, 1)
        layout.addWidget(dock)

    def canvas(self):
        canvas = ImgCanvas(self.mainFrame, size=(self.minimumHeight(),) * 2)
        canvas.setStyleSheet("background: wheat")
        # --- ui here ---
        # ---------------
        return canvas

    def dock(self):
        dock = Qt.QFrame()
        dock.setStyleSheet("background: blue")
        dock.setMinimumWidth(self.minimumWidth() - self.minimumHeight())
        hBox = Qt.QHBoxLayout()
        dock.setLayout(hBox)
        # --- ui here ---
        tabs = Qt.QTabWidget(dock)
        tabs.setStyleSheet("background: lightblue")
        tabs.addTab(self.tabPrimary(
            lambda noise: print(perlinGenerator(noise, (0, 128, 128 * 4), (0, 128, 128 * 4))[0].shape)
        ), "Primary")
        tabs.addTab(self.tabSecondary(), "Secondary")
        # ---------------
        hBox.addWidget(tabs)
        return dock

    @staticmethod
    def tabPrimary(onChange):
        def change():
            label.setText(str(noise))
            onChange(noise)

        def onWarp(val):
            if warps[val][1].__func__ == Warp.polynomial:
                warps_polynomial.setVisible(True)
                noise.setWarp(Warp.polynomial(warps_polynomial.value()))
            else:
                warps_polynomial.setVisible(False)
                noise.setWarp(warps[val][1]())
            change()

        settings = primarySettings._make([None, 8, 128, Warp.improved(), (0, 1), 8, .5, 2])
        Noise.__chunked__ = [True, 2]
        noise = Noise(
            seed=settings.seed,
            frequency=settings.frequency,
            waveLength=settings.waveLength,
            warp=settings.warp,
            _range=settings.range,
            octaves=settings.octaves,
            lacunarity=settings.lacunarity,
            persistence=settings.persistence,
        )

        tp_area = Qt.QScrollArea()
        tp_area.setWidgetResizable(True)
        tp = Qt.QFrame()
        tp_layout = Qt.QVBoxLayout()
        tp.setLayout(tp_layout)
        # --- ui here ---
        label = Qt.QLabel(str(noise))
        label.setWordWrap(True)
        tp_layout.addWidget(label)

        seed_inp = InputBox(label="Seed")
        seed_inp.addEnabledInp(inp=seed_inp.addDouble(0, decimals=0, default=noise.seed,
                                                      onChange=lambda val: noise.setSeed(int(val))
                                                                           or change()))
        tp_layout.addWidget(seed_inp)

        frequency_inp = InputBox(label="Frequency")
        frequency_inp.addInteger(2, default=settings.frequency,
                                 onChange=lambda val: noise.setFrequency(val)
                                                      or change())
        tp_layout.addWidget(frequency_inp)

        waveLength_inp = InputBox(label="Wave Length")
        waveLength_inp.addDouble(1, default=settings.waveLength, step=settings.waveLength,
                                 onChange=lambda val: noise.setWaveLength(val)
                                                      or change())
        tp_layout.addWidget(waveLength_inp)

        warp_inp = InputBox(label="Warp")
        warps = [(k, v) for k, v in Warp.__dict__.items() if isinstance(v, staticmethod)]
        warp_inp.addDrop(tuple([k.capitalize() for k, v in warps]), default=0, onChange=onWarp)
        warps_polynomial = warp_inp.addInteger(1, default=4,
                                               onChange=lambda val: noise.setWarp(Warp.polynomial(val))
                                                                    or change())
        warps_polynomial.setVisible(False)
        tp_layout.addWidget(warp_inp)

        range_inp = InputBox(label="Range")
        x1 = range_inp.addDouble(default=settings.range[0],
                                 onChange=lambda val: x2.setMinimum(val + 10 ** -x1.decimals())
                                                      or noise.setRange((x1.value(), x2.value()))
                                                      or change())
        x2 = range_inp.addDouble(x1.value() + 10 ** -x1.decimals(), default=settings.range[1],
                                 onChange=lambda val: noise.setRange((x1.value(), x2.value()))
                                                      or change())
        tp_layout.addWidget(range_inp)

        octaves_inp = InputBox(label="Octaves")
        octaves_inp.addSlider(1, 8, default=settings.octaves,
                              onChange=lambda val: noise.setOctaves(val)
                                                   or change())
        tp_layout.addWidget(octaves_inp)

        persistence_inp = InputBox(label="Persistence")
        persistence_inp.addDouble(0.01, 1, default=settings.persistence,
                                  onChange=lambda val: noise.setPersistence(val)
                                                       or change())
        tp_layout.addWidget(persistence_inp)

        lacunarity_inp = InputBox(label="Lacunarity")
        lacunarity_inp.addInteger(1, default=settings.lacunarity,
                                  onChange=lambda val: noise.setLacunarity(val)
                                                       or change())
        tp_layout.addWidget(lacunarity_inp)
        # ---------------
        tp_layout.addStretch(1)
        tp_area.setWidget(tp)
        return tp_area

    @staticmethod
    def tabSecondary():
        ts = Qt.QFrame()
        return ts


def main(*args, **kwargs):
    app = Qt.QApplication([])
    win = Gui(*args, **kwargs)
    win.show()
    win.activateWindow()
    app.exec_()
