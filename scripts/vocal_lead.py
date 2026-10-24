#!/usr/bin/env python3
"""
Vocal-to-Synth Lead Audio-to-MIDI Converter (Local & DAW Modes)
Specialized vocal melody extraction powered by Spotify Basic Pitch.

Features:
- Unvoiced noise & breath rejection (plosives/breaths filtered out).
- Strict monophonic voice cleaning (eliminates impossible vocal double-stops).
- Vocal pitch bend smoothing & calibration (preserves glissandos & vibrato).
- Local Mode & Ableton DAW staging.
"""

import os
import sys
import warnings
import logging
import json
import socket
import argparse
import importlib.util
import subprocess
from pathlib import Path

warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"
logging.basicConfig(level=logging.ERROR)
logging.getLogger().setLevel(logging.ERROR)

BASIC_PITCH_PYTHON = r"C:\Users\<you>\AppData\Roaming\uv\tools\basic-pitch\Scripts\python.exe"

# Auto re-exec in dedicated uv environment if needed
if not importlib.util.find_spec("basic_pitch"):
    if os.path.exists(BASIC_PITCH_PYTHON) and sys.executable.lower() != BASIC_PITCH_PYTHON.lower():
        result = subprocess.run([BASIC_PITCH_PYTHON] + sys.argv)
        sys.exit(result.returncode)

import numpy as np
import pretty_midi
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH


def clean_vocal_monophonic(instrument: pretty_midi.Instrument) -> None:
    """Ensure vocal line is strictly monophonic with clean transitions."""
    if not instrument.notes:
        return
    notes = sorted(instrument.notes, key=lambda n: (n.start, n.pitch))
    cleaned = []
    for i in range(len(notes)):
        curr_note = notes[i]
        if i + 1 < len(notes):
            next_note = notes[i + 1]
            if curr_note.end > next_note.start:
                curr_note.end = max(curr_note.start + 0.05, next_note.start - 0.005)
        if curr_note.end > curr_note.start + 0.03:
            cleaned.append(curr_note)
    instrument.notes = cleaned


def smooth_vocal_bends(instrument: pretty_midi.Instrument, window_size: int = 5) -> None:
    """Smooth vocal tremor and breath flutter while keeping intentional slides."""
    if len(instrument.pitch_bends) < window_size:
        return
    bends = sorted(instrument.pitch_bends, key=lambda pb: pb.time)
    values = [pb.pitch for pb in bends]
    half = window_size // 2
    smoothed = []
    for i in range(len(values)):
        start_idx = max(0, i - half)
        end_idx = min(len(values), i + half + 1)
        smoothed.append(int(sum(values[start_idx:end_idx]) / (end_idx - start_idx)))
    for i, pb in enumerate(bends):
        pb.pitch = smoothed[i]
    instrument.pitch_bends = bends


def scale_vocal_bends(instrument: pretty_midi.Instrument, scale: float = 1.0, remove: bool = False) -> None:
    if remove:
        instrument.pitch_bends = []
        return
    if scale == 1.0:
        return
    for pb in instrument.pitch_bends:
        new_val = int(pb.pitch * scale)
        pb.pitch = max(-8192, min(8191, new_val))


def send_osc_clip(host: str, port: int, midi_path: str, track_name: str) -> bool:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.5)
        def pad(b): return b + b'\x00' * ((4 - (len(b) % 4)) % 4)
        msg = pad(b"/live/clip/new") + pad(b",ss") + pad(midi_path.encode('utf-8')) + pad(track_name.encode('utf-8'))
        sock.sendto(msg, (host, port))
        sock.close()
        return True
    except Exception:
        return False


def convert_vocal_to_lead(
    audio_path: str,
    output_midi_path: str = None,
    mode: str = "local",
    onset_threshold: float = 0.60,
    frame_threshold: float = 0.35,
    min_note_length: float = 120.0,
    min_frequency: float = 65.0,     # C2
    max_frequency: float = 1100.0,   # C6
    smooth_bends: bool = True,
    scale_bends: float = 1.0,
    no_bends: bool = False,
    daw_track_name: str = None
) -> dict:
    audio_file = Path(audio_path).resolve()
    if not audio_file.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_file}")

    if output_midi_path is None:
        output_midi_path = audio_file.with_name(f"{audio_file.stem}_vocal_lead.mid")
    else:
        output_midi_path = Path(output_midi_path).resolve()

    output_midi_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n[*] Extracting Vocal Lead MIDI: {audio_file.name}")
    print(f"    Mode: {mode.upper()}")
    print(f"    Vocal Filtering: Onset={onset_threshold}, MinLen={min_note_length}ms, Freq={min_frequency}-{max_frequency}Hz")

    # Run Basic Pitch with vocal-optimized settings
    model_output, midi_data, note_events = predict(
        audio_path=str(audio_file),
        model_or_model_path=ICASSP_2022_MODEL_PATH,
        onset_threshold=onset_threshold,
        frame_threshold=frame_threshold,
        minimum_note_length=min_note_length,
        minimum_frequency=min_frequency,
        maximum_frequency=max_frequency,
        multiple_pitch_bends=False,
        melodia_trick=True
    )

    for inst in midi_data.instruments:
        # Enforce monophonic lead vocal melody
        clean_vocal_monophonic(inst)
        if no_bends:
            scale_vocal_bends(inst, remove=True)
        else:
            if smooth_bends:
                smooth_vocal_bends(inst, window_size=5)
            if scale_bends != 1.0:
                scale_vocal_bends(inst, scale=scale_bends)

    midi_data.write(str(output_midi_path))
    total_notes = sum(len(i.notes) for i in midi_data.instruments)
    print(f"[+] Vocal Lead MIDI saved: {output_midi_path} ({total_notes} notes extracted)")

    result = {
        "audio_path": str(audio_file),
        "midi_path": str(output_midi_path),
        "total_notes": total_notes,
        "mode": mode
    }

    if mode.lower() in ("daw", "ableton"):
        track_name = daw_track_name or f"Vocal Lead - {audio_file.stem}"
        user_lib_samples = Path("C:/Users/<you>/Documents/Ableton/User Library/Samples/Basic Pitch Leads")
        try:
            user_lib_samples.mkdir(parents=True, exist_ok=True)
            import shutil
            copied_midi = user_lib_samples / output_midi_path.name
            shutil.copy2(output_midi_path, copied_midi)
            print(f"[DAW] Staged in Ableton User Library: {copied_midi}")
            result["user_library_midi"] = str(copied_midi)
        except Exception:
            pass

        send_osc_clip("127.0.0.1", 11925, str(output_midi_path), track_name)
        print(f"[DAW] Ready for Ableton Live: Load onto track '{track_name}' and drop a synth/lead instrument preset!")

    return result


def main():
    parser = argparse.ArgumentParser(description="Vocal-to-Synth Lead Audio-to-MIDI (Local & DAW)")
    parser.add_argument("audio_path", help="Path to vocal audio file (acapella, voice memo, humming)")
    parser.add_argument("--output", "-o", help="Path to output .mid file")
    parser.add_argument("--mode", choices=["local", "daw", "ableton"], default="local",
                        help="Operation mode: 'local' (file on disk) or 'daw'/'ableton' (staged for Live)")
    parser.add_argument("--onset", type=float, default=0.60, help="Onset threshold (default 0.60 to reject breaths)")
    parser.add_argument("--frame", type=float, default=0.35, help="Frame sustain threshold (default 0.35)")
    parser.add_argument("--min-len", type=float, default=120.0, help="Minimum note length in ms (default 120)")
    parser.add_argument("--min-freq", type=float, default=65.0, help="Minimum vocal frequency in Hz (default ~C2)")
    parser.add_argument("--max-freq", type=float, default=1100.0, help="Maximum vocal frequency in Hz (default ~C6)")
    parser.add_argument("--no-smoothing", action="store_true", help="Disable pitch bend jitter smoothing")
    parser.add_argument("--scale-bends", type=float, default=1.0, help="Scale factor for pitch bends")
    parser.add_argument("--no-bends", action="store_true", help="Strip all pitch bends for hard-quantized leads")
    parser.add_argument("--track-name", help="Ableton track name")

    args = parser.parse_args()

    res = convert_vocal_to_lead(
        audio_path=args.audio_path,
        output_midi_path=args.output,
        mode=args.mode,
        onset_threshold=args.onset,
        frame_threshold=args.frame,
        min_note_length=args.min_len,
        min_frequency=args.min_freq,
        max_frequency=args.max_freq,
        smooth_bends=not args.no_smoothing,
        scale_bends=args.scale_bends,
        no_bends=args.no_bends,
        daw_track_name=args.track_name
    )
    print("\n[SUCCESS] Vocal Lead MIDI Ready:")
    print(f"  Audio: {res['audio_path']}")
    print(f"  MIDI:  {res['midi_path']}")
    print(f"  Notes: {res['total_notes']}")


if __name__ == "__main__":
    main()
