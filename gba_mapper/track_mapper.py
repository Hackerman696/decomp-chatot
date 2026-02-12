class TrackMapper:
    def __init__(self, song, instruments):
        self.song = song
        self.instruments = instruments  # list of Instrument objects

    def set_instrument(self, track_index, instrument_index):
        track = self.song.tracks[track_index]
        instrument = self.instruments[instrument_index]
        track.gba_instrument = instrument

    def set_volume(self, track_index, volume):
        self.song.tracks[track_index].volume = max(0, min(volume, 127))

    def set_reverb(self, track_index, reverb):
        self.song.tracks[track_index].reverb = max(0, min(reverb, 127))

    def set_pan(self, track_index, pan):
        self.song.tracks[track_index].pan = max(0, min(pan, 127))
