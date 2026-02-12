from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional

# Matches: voice_group route101
VOICE_GROUP_RE = re.compile(r"^\s*voice_group\s+([A-Za-z0-9_]+)\s*$")

# Matches: voice_directsound 60, 0, DirectSoundWaveData_xxx, ...
VOICE_ENTRY_RE = re.compile(r"^\s*(voice_[A-Za-z0-9_]+)\b(.*)$")

# Matches: .include "sound/voicegroups/route101.inc"
INCLUDE_RE = re.compile(r'^\s*\.include\s+"([^"]+)"\s*$')


@dataclass
class VoiceEntry:
    index: int
    macro: str
    args: str
    type: str
    source_file: str


def classify_macro(macro: str) -> str:
    m = macro.lower()
    if "keysplit" in m:
        return "keysplits"
    if "drum" in m:
        return "drumset"
    if "directsound" in m:
        return "direct"
    if "programmable_wave" in m or "wave" in m:
        return "wave"
    if "square" in m:
        return "square"
    if "noise" in m:
        return "noise"
    return "unknown"


def read_text(path: Path) -> List[str]:
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def resolve_include(sound_dir: Path, include_path: str) -> Path:
    # include_path like 'sound/voicegroups/route101.inc'
    p = include_path
    if p.startswith("sound/"):
        p = p[len("sound/") :]
    return (sound_dir / p).resolve()


def collect_included_voicegroup_files(sound_dir: Path, voice_groups_inc: Path) -> List[Path]:
    files: List[Path] = []
    for line in read_text(voice_groups_inc):
        m = INCLUDE_RE.match(line)
        if not m:
            continue
        resolved = resolve_include(sound_dir, m.group(1))
        if resolved.exists():
            files.append(resolved)
    return files


def parse_voicegroups_from_file(path: Path) -> Dict[str, List[VoiceEntry]]:
    """
    Parses voice_group blocks in a single voicegroups/*.inc file.
    Returns mapping: group_name -> list of entries with indices.
    """
    lines = read_text(path)
    out: Dict[str, List[VoiceEntry]] = {}

    current_group: Optional[str] = None
    current_entries: List[VoiceEntry] = []
    idx = 0

    def flush():
        nonlocal current_group, current_entries, idx
        if current_group is not None:
            out[current_group] = current_entries
        current_group = None
        current_entries = []
        idx = 0

    for line in lines:
        # Skip pure comments
        stripped = line.strip()
        if stripped.startswith("@") or stripped.startswith(";"):
            continue

        g = VOICE_GROUP_RE.match(line)
        if g:
            flush()
            current_group = g.group(1)
            continue

        if current_group is None:
            continue

        if not stripped:
            continue

        e = VOICE_ENTRY_RE.match(line)
        if e:
            macro = e.group(1)
            args = e.group(2).strip()
            current_entries.append(
                VoiceEntry(
                    index=idx,
                    macro=macro,
                    args=args,
                    type=classify_macro(macro),
                    source_file=str(path),
                )
            )
            idx += 1

    flush()
    return out


def build_index(sound_dir: Path) -> Dict[str, List[dict]]:
    voice_groups_inc = sound_dir / "voice_groups.inc"
    if not voice_groups_inc.exists():
        raise FileNotFoundError(f"voice_groups.inc not found at: {voice_groups_inc}")

    files = collect_included_voicegroup_files(sound_dir, voice_groups_inc)
    if not files:
        raise RuntimeError(f"No .include entries resolved from: {voice_groups_inc}")

    merged: Dict[str, List[VoiceEntry]] = {}
    for f in files:
        parsed = parse_voicegroups_from_file(f)
        for group, entries in parsed.items():
            # Keep first definition if duplicates happen
            if group not in merged:
                merged[group] = entries

    return {k: [asdict(e) for e in v] for k, v in merged.items()}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sound-dir", required=True, help="Path to .../pokeemerald/sound")
    ap.add_argument("--out", default="voicegroups_index.json", help="Output JSON filename")
    args = ap.parse_args()

    sound_dir = Path(args.sound_dir).expanduser().resolve()
    index = build_index(sound_dir)

    out_path = Path(args.out).expanduser().resolve()
    out_path.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Wrote {len(index)} voicegroups to: {out_path}")


if __name__ == "__main__":
    main()
