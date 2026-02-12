from PyQt6.QtWidgets import QFileDialog, QMessageBox
from app.config.project_config import save_sound_path, validate_sound_path


def ask_for_sound_directory(parent=None):
    folder = QFileDialog.getExistingDirectory(
        parent,
        "Select the pokeemerald sound folder (contains voice_groups.inc)"
    )

    if not folder:
        return None

    if not validate_sound_path(folder):
        QMessageBox.critical(parent, "Invalid Folder",
                             "voice_groups.inc not found in this directory.")
        return None

    save_sound_path(folder)
    return folder
