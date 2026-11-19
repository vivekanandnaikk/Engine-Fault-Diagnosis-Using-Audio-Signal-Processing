"""Audio loading and normalization helpers."""

from pathlib import Path

import numpy as np
from scipy.io import wavfile


def to_mono(samples: np.ndarray) -> np.ndarray:
    """Convert mono or channel-last audio samples to a finite float mono signal.

    Integer PCM is scaled to approximately [-1, 1]. Floating-point samples are
    preserved. A two-dimensional array is treated as frames x channels.
    """
    data = np.asarray(samples)
    if data.ndim == 2:
        if data.shape[1] == 0:
            raise ValueError("Audio contains no channels")
        data = data.astype(np.float64).mean(axis=1)
    elif data.ndim != 1:
        raise ValueError("Audio must be a mono vector or frames-by-channels array")
    if data.size == 0:
        raise ValueError("Audio contains no samples")

    if np.issubdtype(data.dtype, np.integer):
        info = np.iinfo(data.dtype)
        if info.min < 0:
            data = data.astype(np.float64) / max(abs(info.min), info.max)
        else:
            midpoint = (info.max + 1) / 2
            data = (data.astype(np.float64) - midpoint) / midpoint
    else:
        data = data.astype(np.float64)

    if not np.all(np.isfinite(data)):
        raise ValueError("Audio contains NaN or infinite samples")
    return data


def load_audio(path: str | Path) -> tuple[np.ndarray, int]:
    """Read a WAV file and return normalized mono samples and sample rate."""
    audio_path = Path(path)
    if not audio_path.is_file():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    try:
        sample_rate, samples = wavfile.read(audio_path)
    except (OSError, ValueError) as exc:
        raise ValueError(f"Could not read WAV audio {audio_path}: {exc}") from exc
    if sample_rate <= 0:
        raise ValueError("Sample rate must be positive")
    return to_mono(samples), int(sample_rate)
