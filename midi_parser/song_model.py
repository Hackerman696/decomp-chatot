from dataclasses import dataclass, field
from typing import List


@dataclass
class Note:
    pitch: int
    velocity: int
    start: float
    duration: float


@dataclass
class Track:
    name: str
    midi_channel: int
    notes: List[Note] = field(default_factory=list)

    # GBA-related properties (editable in GUI)
    gba_instrument: str = "Piano"
    volume: int = 100       # 0–127
    reverb: int = 0         # 0–127
    pan: int = 64           # 0–127 (center)


@dataclass
class Song:
    title: str
    tempo: int
    tracks: List[Track] = field(default_factory=list)
