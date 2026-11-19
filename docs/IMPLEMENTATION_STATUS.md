# Implementation status

This repository implements a digital-signal-processing workflow for analyzing motorcycle engine audio and comparing descriptive features for normal and faulty recordings.

## Included

- Python WAV loading with integer PCM normalization and stereo-to-mono conversion.
- Hann-windowed FFT with a single-sided magnitude spectrum.
- RMS, zero-crossing rate, spectral centroid, bandwidth, 85% roll-off, dominant frequency, and MFCC summaries.
- Python CLI commands for single-file analysis, two-file comparison, and dataset CSV extraction.
- MATLAB analysis function; MFCC output depends on MATLAB Audio Toolbox.
- Unit tests for audio conversion and core feature calculations.

## Not included

- Original recordings or recording metadata are not distributed in this repository.
- A trained or validated fault classifier is not implemented.
- Diagnostic thresholds, fault-type labels, or accuracy claims are not included.
- LMS/RLS adaptive filtering and real-time acquisition are future work.

## Verification

Run `pip install -e ".[dev]"` and `pytest` in a supported Python environment. MATLAB execution and Audio Toolbox MFCC behavior should be verified in the target MATLAB installation.
