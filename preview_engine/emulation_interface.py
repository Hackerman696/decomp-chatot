import mido
import tempfile
import os


def build_temp_midi(song):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mid")
    mid = mido.MidiFile()
    mid.ticks_per_beat = 480

    for track_data in song.tracks:
        track = mido.MidiTrack()
        mid.tracks.append(track)

        # Instrument (Program Change)
        track.append(mido.Message('program_change',
                                  program=track_data.gba_instrument.index,
                                  time=0))

        # Volume CC (7)
        track.append(mido.Message('control_change',
                                  control=7,
                                  value=track_data.volume,
                                  time=0))

        # Pan CC (10)
        track.append(mido.Message('control_change',
                                  control=10,
                                  value=track_data.pan,
                                  time=0))

        # Reverb CC (91)
        track.append(mido.Message('control_change',
                                  control=91,
                                  value=track_data.reverb,
                                  time=0))

        # Notes
        for note in track_data.notes:
            start_ticks = int(note.start * mid.ticks_per_beat)
            duration_ticks = int(note.duration * mid.ticks_per_beat)

            track.append(mido.Message('note_on',
                                      note=note.pitch,
                                      velocity=note.velocity,
                                      time=start_ticks))
            track.append(mido.Message('note_off',
                                      note=note.pitch,
                                      velocity=0,
                                      time=duration_ticks))

    mid.save(temp_file.name)
    return temp_file.name
import subprocess
import shutil


def build_song_in_project(temp_midi_path, project_root):
    dest = os.path.join(project_root, "sound/songs/temp_preview.mid")
    shutil.copy(temp_midi_path, dest)

    subprocess.run(["make", "-C", project_root], check=True)

    # assume built ROM
    return os.path.join(project_root, "pokeemerald.gba")
def launch_emulator(rom_path):
    subprocess.Popen(["mgba", rom_path])
