



from app.gui.track_table import TrackTable
from app.gba_mapper.track_mapper import TrackMapper

mapper = TrackMapper(song, instruments)
table = TrackTable(song, instruments, mapper)
layout.addWidget(table)
