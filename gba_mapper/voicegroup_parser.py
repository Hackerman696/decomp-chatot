import os
import re


class Instrument:
    def __init__(self, name, source_file, index):
        self.name = name
        self.source_file = source_file
        self.index = index

    def __str__(self):
        return f"{self.name} ({self.source_file} entry {self.index})"


def parse_voicegroups(root_path):
    """
    root_path = path to pokeemerald/sound directory
    """
    vg_file = os.path.join(root_path, "voice_groups.inc")

    include_pattern = re.compile(r'\.include\s+"([^"]+)"')
    instruments = []

    with open(vg_file, "r") as f:
        content = f.readlines()

    includes = []
    for line in content:
        match = include_pattern.search(line)
        if match:
            includes.append(match.group(1))

    for inc in includes:
        full_path = os.path.join(root_path, "..", inc)

        if not os.path.exists(full_path):
            continue

        filename = os.path.basename(inc)
        instruments += parse_instrument_file(full_path, filename)

    return instruments


def parse_instrument_file(filepath, label):
    instruments = []
    entry_index = 0

    with open(filepath, "r") as f:
        for line in f:
            if line.strip().startswith("voice_"):
                instruments.append(
                    Instrument(
                        name=f"{label}",
                        source_file=label,
                        index=entry_index
                    )
                )
                entry_index += 1

    return instruments
