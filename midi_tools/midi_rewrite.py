from __future__ import annotations
from pathlib import Path
from typing import Dict, Optional

import mido


def apply_channel_voice_map(
    input_midi: Path,
    output_midi: Path,
    channel_to_voice: Dict[int, int],
    *,
    default_voice: Optional[int] = None,
    apply_to_all_program_changes: bool = True,
) -> None:
    """
    Rewrites Program Change messages so each channel uses the chosen voice index (0-127).

    - channel_to_voice: {channel(0-15): voice_index(0-127)}
    - default_voice: if set, any channel not in mapping but has program changes will be forced to this voice
    - apply_to_all_program_changes:
        True  -> rewrite every program_change encountered on that channel
        False -> rewrite only the first program_change per channel
    """
    mid = mido.MidiFile(input_midi)
    out = mido.MidiFile(ticks_per_beat=mid.ticks_per_beat)

    seen_first: set[tuple[int, int]] = set()  # (track_index, channel) is too strict; use channel only
    seen_channel: set[int] = set()

    for track in mid.tracks:
        new_track = mido.MidiTrack()
        for msg in track:
            if msg.type == "program_change" and hasattr(msg, "channel"):
                ch = int(msg.channel)

                if (not apply_to_all_program_changes) and (ch in seen_channel):
                    new_track.append(msg)
                    continue

                target = channel_to_voice.get(ch, default_voice)
                if target is not None:
                    if not (0 <= int(target) <= 127):
                        raise ValueError(f"voice index out of range for channel {ch}: {target} (must be 0-127)")
                    msg = msg.copy(program=int(target))
                    seen_channel.add(ch)

            new_track.append(msg)

        out.tracks.append(new_track)

    output_midi.parent.mkdir(parents=True, exist_ok=True)
    out.save(output_midi)
