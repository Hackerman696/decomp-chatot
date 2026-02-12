from PyQt6.QtWidgets import (
    QTableWidget, QTableWidgetItem,
    QComboBox, QSlider
)
from PyQt6.QtCore import Qt


class TrackTable(QTableWidget):
    def __init__(self, song, instruments, mapper):
        super().__init__()
        self.song = song
        self.instruments = instruments
        self.mapper = mapper

        self.setColumnCount(5)
        self.setHorizontalHeaderLabels([
            "Track", "Instrument", "Volume", "Reverb", "Pan"
        ])

        self.populate()

    def populate(self):
        self.setRowCount(len(self.song.tracks))

        for i, track in enumerate(self.song.tracks):
            self.setItem(i, 0, QTableWidgetItem(track.name))

            # Instrument dropdown
            combo = QComboBox()
            for inst in self.instruments:
                combo.addItem(str(inst))
            combo.currentIndexChanged.connect(
                lambda idx, row=i: self.mapper.set_instrument(row, idx)
            )
            self.setCellWidget(i, 1, combo)

            # Volume slider
            vol_slider = self.make_slider(
                track.volume,
                lambda val, row=i: self.mapper.set_volume(row, val)
            )
            self.setCellWidget(i, 2, vol_slider)

            # Reverb slider
            rev_slider = self.make_slider(
                track.reverb,
                lambda val, row=i: self.mapper.set_reverb(row, val)
            )
            self.setCellWidget(i, 3, rev_slider)

            # Pan slider
            pan_slider = self.make_slider(
                track.pan,
                lambda val, row=i: self.mapper.set_pan(row, val)
            )
            self.setCellWidget(i, 4, pan_slider)

    def make_slider(self, value, callback):
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 127)
        slider.setValue(value)
        slider.valueChanged.connect(callback)
        return slider
