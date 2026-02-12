import mido
from .song_model import Song, Track, Note


def load_midi_file(filepath: str) -> Song:
    mid = mido.MidiFile(filepath)

    song = Song(
        title=filepath.split("/")[-1],
        tempo=120
    )

    ticks_per_beat = mid.ticks_per_beat

    for i, midi_track in enumerate(mid.tracks):
        track = Track(name=midi_track.name or f"Track {i}", midi_channel=0)

        time = 0
        active_notes = {}

        for msg in midi_track:
            time += msg.time

            if msg.type == 'set_tempo':
                song.tempo = mido.tempo2bpm(msg.tempo)

            if msg.type == 'note_on' and msg.velocity > 0:
                active_notes[msg.note] = (time, msg.velocity)

            elif msg.type in ['note_off', 'note_on'] and msg.note in active_notes:
                start_time, velocity = active_notes.pop(msg.note)
                duration = time - start_time

                note = Note(
                    pitch=msg.note,
                    velocity=velocity,
                    start=start_time / ticks_per_beat,
                    duration=duration / ticks_per_beat
                )
                track.notes.append(note)

        if track.notes:
            song.tracks.append(track)

    return song
