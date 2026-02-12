import os
import json

CONFIG_PATH = os.path.expanduser("~/.pokemusicstudio_config.json")


def save_sound_path(path):
    data = {"sound_path": path}
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f)


def load_sound_path():
    if not os.path.exists(CONFIG_PATH):
        return None

    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)
        return data.get("sound_path")


def validate_sound_path(path):
    """
    Checks if path contains voice_groups.inc
    """
    vg_file = os.path.join(path, "voice_groups.inc")
    return os.path.exists(vg_file)
