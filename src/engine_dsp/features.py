"""Descriptive time- and frequency-domain audio features."""

import numpy as np
from scipy.fft import rfft, rfftfreq
from scipy.signal.windows import hann


def extract_features(samples: np.ndarray, sample_rate: int, *, include_mfcc: bool = True) -> dict[str, float]:
    """Extract descriptive features from one mono audio signal.

    Spectral features use a Hann-windowed, whole-recording, single-sided FFT.
    This is a compact reference analysis, not a time-varying engine diagnostic.
    """
    x = np.asarray(samples, dtype=np.float64)
    if x.ndim != 1 or x.size == 0:
        raise ValueError("samples must be a non-empty mono vector")
    if sample_rate <= 0:
        raise ValueError("sample_rate must be positive")
    if not np.all(np.isfinite(x)):
        raise ValueError("samples must be finite")

    rms = float(np.sqrt(np.mean(np.square(x))))
    zcr = float(np.mean(np.signbit(x[1:]) != np.signbit(x[:-1]))) if x.size > 1 else 0.0

    windowed = x * hann(x.size, sym=False)
    spectrum = np.abs(rfft(windowed))
    frequencies = rfftfreq(x.size, d=1.0 / sample_rate)
    if spectrum.size > 1:
        spectrum[1:-1] *= 2.0 if x.size % 2 == 0 else 2.0
    positive = spectrum.copy()
    if positive.size:
        positive[0] = 0.0
    total = float(np.sum(positive))
    if total > 0.0:
        centroid = float(np.sum(frequencies * positive) / total)
        bandwidth = float(np.sqrt(np.sum(((frequencies - centroid) ** 2) * positive) / total))
        cumulative_power = np.cumsum(positive**2)
        rolloff_index = int(np.searchsorted(cumulative_power, 0.85 * cumulative_power[-1]))
        rolloff = float(frequencies[min(rolloff_index, frequencies.size - 1)])
        dominant = float(frequencies[1 + np.argmax(positive[1:])]) if positive.size > 1 else 0.0
    else:
        centroid = bandwidth = rolloff = dominant = 0.0

    result = {
        "rms": rms,
        "zero_crossing_rate": zcr,
        "spectral_centroid_hz": centroid,
        "spectral_bandwidth_hz": bandwidth,
        "spectral_rolloff_85_hz": rolloff,
        "dominant_frequency_hz": dominant,
    }

    if include_mfcc:
        try:
            import librosa
        except ImportError as exc:
            raise ImportError("MFCC extraction requires librosa; install it with `pip install librosa`.") from exc
        coeffs = librosa.feature.mfcc(y=x, sr=sample_rate, n_mfcc=13)
        for index, values in enumerate(coeffs, start=1):
            result[f"mfcc_{index:02d}_mean"] = float(np.mean(values))
            result[f"mfcc_{index:02d}_std"] = float(np.std(values))
    return result
