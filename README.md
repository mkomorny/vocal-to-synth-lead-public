# Vocal-to-Synth Lead Transcriber

> **Tri-Platform Agent Skill** for Claude Desktop / Code, Grok CLI, and Google Antigravity / Gemini.  
> Dedicated vocal-to-MIDI melody transcriber for singing, humming, whistling, and acapellas. Rejects breath noise, enforces monophonic melody lines, and smooths vocal pitch bends for instant synth lead playback in local files or Ableton Live.

---

## Overview

Human vocals are the most intuitive songwriting instrument—producers constantly hum hook ideas, whistle melodies, or sing guide riffs. However, standard audio-to-MIDI converters pick up breathing noise, register accidental polyphonic chords, and capture erratic vocal pitch jitter.

**`vocal-to-synth-lead`** is optimized specifically for the vocal acoustic profile:
1. **Breath & Lip-Smack Rejection**: Raised onset threshold (`0.60`) and frequency bounds (65 Hz - 1100 Hz / C2 to C6) eliminate breaths, pop plosives, and sub-rumble.
2. **Monophonic Guarantee**: Enforces clean single-voice note transitions, preventing double-stops so monophonic legato synth patches glide smoothly.
3. **Vibrato & Jitter Smoothing**: A moving-average filter removes throat tremor while preserving intentional glissandos and expressive slides.
4. **Hard-Tune Mode**: Option to strip pitch bends (`--no-bends`) for rigid, grid-quantized electronic dance leads.
5. **DAW Staging**: Automatically copies clips to the Ableton User Library (`Samples/Basic Pitch Leads`).

---

## CLI Usage

Run the converter standalone from the terminal:

```bash
# 1. Standard vocal melody transcription:
python scripts/vocal_lead.py "C:\Music\voice_memo.m4a"

# 2. Hard-tune / strip pitch bends for EDM/electronic lead:
python scripts/vocal_lead.py "C:\Music\vocal_riff.wav" --no-bends

# 3. Custom sensitivity tuning:
python scripts/vocal_lead.py "C:\Music\acapella.wav" --onset 0.70 --min-len 150

# 4. Stage for Ableton Live:
python scripts/vocal_lead.py "C:\Music\hook.wav" --mode daw --track-name "Vocal Hook Lead"
```

---

## Tri-Platform Architecture

Zero duplicate code across tools. Canonical source resides in `.agents`:
- **Canonical**: `C:\Users\<you>\.agents\skills\vocal-to-synth-lead`
- **Claude**: `C:\Users\<you>\.claude\skills\vocal-to-synth-lead` (NTFS Junction)
- **Grok**: `C:\Users\<you>\.grok\skills\vocal-to-synth-lead` (NTFS Junction)
- **Antigravity**: `C:\Users\<you>\.gemini\config\skills\vocal-to-synth-lead` (NTFS Junction)

---

## Documentation Suite

- [`HOW_TO_USE.txt`](file:///C:/Users/<you>/.agents/skills/vocal-to-synth-lead/HOW_TO_USE.txt): Standardized user guide and prompt templates.
- [`IMPLEMENTATION_PLAN.md`](file:///C:/Users/<you>/.agents/skills/vocal-to-synth-lead/IMPLEMENTATION_PLAN.md): Feature checklist and roadmap.
- [`App Changes Tracker.html`](file:///C:/Users/<you>/.agents/skills/vocal-to-synth-lead/App%20Changes%20Tracker.html): Interactive visual version log.
- [`SKILL.md`](file:///C:/Users/<you>/.agents/skills/vocal-to-synth-lead/SKILL.md): Agent system instructions and triggers.
