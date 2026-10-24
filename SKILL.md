---
name: vocal-to-synth-lead
description: Dedicated vocal-to-MIDI lead melody transcriber for singing, humming, whistling, and acapellas. Rejects breath noise, enforces monophonic melody lines, and smooths vocal pitch bends for instant synth lead playback in local files or Ableton Live.
---

# Vocal-to-Synth Lead Transcriber

Converts vocal audio recordings (phone voice memos, studio acapellas, humming, whistling, or scatting) into clean, expressive monophonic MIDI melodies ready to drive synthesizers and virtual instruments.

## Vocal-Specific Optimizations

1. **Breath & Lip-Smack Rejection**: Automatically applies a raised onset threshold (`0.60`) and frequency clamping (65 Hz - 1100 Hz) to ignore intake breaths, plosives, and low-frequency rumble.
2. **Monophonic Guarantee**: Eliminates polyphonic artifacts or accidental double-notes so synthesizer patches (especially monophonic / legato synths) glide smoothly without hanging notes.
3. **Vibrato & Jitter Smoothing**: Natural singing contains throat tremors and breath fluctuations. The built-in moving-average filter removes jitter while preserving slides, glissandos, and expressive pitch bends.
4. **Hard-Tune Mode**: Option to strip pitch bends (`--no-bends`) for rigid, grid-quantized pop/dance leads.
5. **Local File & Ableton DAW Staging**: Saves `.mid` files directly on disk and copies them to the Ableton User Library (`User Library/Samples/Basic Pitch Leads`).

---

## Command Line Usage

### Local File Mode
```bash
# Transcribe singing/humming to a clean lead MIDI file:
python "C:\Users\<you>\.agents\skills\vocal-to-synth-lead\scripts\vocal_lead.py" "C:\Music\vocal_idea.wav"

# Hard-tune / zero pitch bends for rigid electronic lead:
python "C:\Users\<you>\.agents\skills\vocal-to-synth-lead\scripts\vocal_lead.py" "C:\Music\hook.mp3" --no-bends
```

### Ableton Live Mode
```bash
# Transcribe and stage for Ableton Live:
python "C:\Users\<you>\.agents\skills\vocal-to-synth-lead\scripts\vocal_lead.py" "C:\Music\acapella.wav" --mode daw --track-name "Synth Lead"
```
