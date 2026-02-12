from PyQt6.QtWidgets import QApplication
from app.config.project_config import load_sound_path
from app.gui.setup_dialog import ask_for_sound_directory
from app.gba_mapper.voicegroup_parser import parse_voicegroups


def init_instruments(app):
    sound_path = load_sound_path()

    if not sound_path:
        sound_path = ask_for_sound_directory()

    if not sound_path:
        print("No valid sound path provided.")
        return []

    instruments = parse_voicegroups(sound_path)
    print(f"Loaded {len(instruments)} instruments.")
    return instruments


if __name__ == "__main__":
    app = QApplication([])

    instruments = init_instruments(app)

    # pass instruments to main window later
    app.exec()
