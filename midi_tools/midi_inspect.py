from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set, Tuple

import mido


@dataclass
class ChannelInfo:
    channel: int
    programs: Set[int] = field(default_factory=set)   # Program Change values 0-127
    has_notes: bool = False
    note_count: int = 0


@dataclass
class MidiSummary:
    path: Path
    ticks_per_beat: int
    channels: Dict[int, ChannelInfo]  # key = 0-15
    used_channels: List[int]
    uses_percussion_channel_9: bool


def inspect_midi(path: Path) -> MidiSummary:
    mid = mido.MidiFile(path)
    channels: Dict[int, ChannelInfo] = {ch: ChannelInfo(channel=ch) for ch in range(16)}

    for track in mid.tracks:
        for msg in track:
            if not hasattr(msg, "channel"):
                continue
            ch = int(msg.channel)
            ci = channels[ch]

            if msg.type == "program_change":
                ci.programs.add(int(msg.program))

            # Note usage detection
            if msg.type in ("note_on", "note_off"):
                ci.has_notes = True
                if msg.type == "note_on" and int(msg.velocity) > 0:
                    ci.note_count += 1

    used = [ch for ch, ci in channels.items() if ci.has_notes or ci.programs]
    return MidiSummary(
        path=Path(path),
        ticks_per_beat=int(mid.ticks_per_beat),
        channels=channels,
        used_channels=used,
        uses_percussion_channel_9=(9 in used),
    )


if __name__ == "__main__":
    import sys, json
    p = Path(sys.argv[1])
    s = inspect_midi(p)

    out = {
        "path": str(s.path),
        "ticks_per_beat": s.ticks_per_beat,
        "used_channels": s.used_channels,
        "uses_percussion_channel_9": s.uses_percussion_channel_9,
        "channels": {
            str(ch): {
                "programs": sorted(list(ci.programs)),
                "has_notes": ci.has_notes,
                "note_count": ci.note_count,
            }
            for ch, ci in s.channels.items()
            if ch in s.used_channels
        },
    }
    print(json.dumps(out, indent=2))
