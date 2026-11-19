# Implementation status

This repository is a reconstructed reference project based on the author's recollection. It is not the original source code and has not been validated against original recordings.

## Available in this repository

- Python WAV loading with integer PCM normalization and stereo-to-mono conversion.
- Hann-windowed whole-recording FFT and single-sided magnitude spectrum calculations.
- RMS, zero-crossing rate, spectral centroid, bandwidth, 85% roll-off, dominant non-DC frequency, and MFCC mean/standard-deviation summaries.
- Python CLI commands for single-file analysis, two-file comparison, and dataset CSV extraction.
- MATLAB analysis function; MFCC output depends on MATLAB Audio Toolbox.
- Unit tests for signal handling and core feature calculations.

## Not supplied or established

- Original code, source history, motorcycle recordings, detailed labels, and acquisition metadata.
- Exact RPM/load, phone, sample-rate, recording-distance, or environment settings.
- Fault-specific thresholds, a trained classifier, a validated diagnostic protocol, or diagnostic accuracy.
- Real-time processing, adaptive LMS/RLS filters, or machine-learning methods.

## Verification

Run `pip install -e ".[dev]"` and `pytest` in a supported Python environment. No original dataset is provided, so results on real recordings must be collected and checked by the user. MATLAB execution has not been verified across MATLAB releases; MFCC availability depends on the Audio Toolbox installation.
