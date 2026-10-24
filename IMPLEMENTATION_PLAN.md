# Implementation Plan: Vocal-to-Synth Lead Transcriber

Dedicated vocal-to-MIDI melody transcriber that turns singing, humming, whistling, and acapellas into clean, expressive monophonic MIDI melodies ready to drive synthesizers and virtual instruments.

---

## Deliverables Checklist

### v1.0.0 — Initial Release
- [x] **Core Vocal Transcriber**: `scripts/vocal_lead.py` leveraging Spotify Basic Pitch neural model. ✅ done in v1.0.0
- [x] **Breath & Plosive Rejection**: Elevated onset threshold (`0.60`) and frequency clamping (65 Hz - 1100 Hz). ✅ done in v1.0.0
- [x] **Monophonic Guarantee Filter**: Strict note overlap prevention preventing hanging notes on legato synthesizers. ✅ done in v1.0.0
- [x] **Vocal Pitch Bend Smoothing**: Moving-average filter removing jitter while preserving intentional slides and glissandos. ✅ done in v1.0.0
- [x] **Hard-Tune Quantizer Mode**: `--no-bends` option stripping all pitch bends for grid-rigid EDM/pop leads. ✅ done in v1.0.0
- [x] **Ableton Live & DAW Staging**: Direct staging in Ableton User Library (`Samples/Basic Pitch Leads`) with optional OSC dispatch. ✅ done in v1.0.0
- [x] **Tri-Platform Accessibility**: Canonical `.agents` installation linked to Claude, Grok, and Antigravity via NTFS junctions. ✅ done in v1.0.0
- [x] **Standard Documentation Suite**: `SKILL.md`, `HOW_TO_USE.txt`, `README.md`, `App Changes Tracker.html`, and `dev-notes-v1.0.0.md`. ✅ done in v1.0.0

---

## Roadmap & Future Enhancements

### v1.1.0 — Vocal Formant & Expression CC Mapping
- [ ] Map vocal dynamics (RMS amplitude) to MIDI CC 11 (Expression) or CC 1 (Mod Wheel).
- [ ] Map vocal vowel shifts (formants) to synth filter cutoff (CC 74).
- [ ] Key and scale snapping (quantize pitch bends to musical modes).

### v1.2.0 — Polyphonic Vocal Harmonies
- [ ] Multi-voice vocal transcription separating soprano, alto, tenor, and bass parts into distinct MIDI channels.
