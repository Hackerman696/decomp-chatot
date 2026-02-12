from __future__ import annotations
from pathlib import Path
from typing import Dict, Optional

from midi_tools.midi_rewrite import apply_channel_voice_map
from preview_engine.preview_runner import run_preview


def prepare_preview_midi(
    source_midi: Path,
    output_midi: Path,
    channel_voice_map: Dict[int, int],
    *,
    default_voice: Optional[int] = None,
):
    """
    Basic pipeline:
    - Rewrite program changes per channel
    - Output mus_preview.mid
    """
    apply_channel_voice_map(
        source_midi,
        output_midi,
        channel_voice_map,
        default_voice=default_voice,
        apply_to_all_program_changes=True,
    )


def build_and_run_preview(
    repo_path: Path,
    midi_path: Path,
    voicegroup: str,
    *,
    mgba_path: Path,
    volume: int = 80,
    reverb: int = 50,
    priority: int = 0,
):
    run_preview(
        repo=repo_path,
        midi=midi_path,
        voicegroup=voicegroup,
        mgba=mgba_path,
        volume=volume,
        reverb=reverb,
        priority=priority,
    )
