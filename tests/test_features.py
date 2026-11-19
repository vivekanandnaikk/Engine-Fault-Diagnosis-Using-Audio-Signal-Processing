import numpy as np
import pytest

from engine_dsp.audio import to_mono
from engine_dsp.features import extract_features


def test_integer_stereo_is_normalized_and_averaged():
    stereo = np.array([[32767, 0], [-32768, 0]], dtype=np.int16)
    mono = to_mono(stereo)
    assert mono.shape == (2,)
    assert mono[0] == pytest.approx(32767 / 32768 / 2)
    assert mono[1] == pytest.approx(-0.5)


def test_float_audio_is_preserved():
    samples = np.array([0.25, -0.5], dtype=np.float32)
    np.testing.assert_allclose(to_mono(samples), samples)


def test_features_include_expected_descriptors_without_mfcc():
    sr = 8000
    time = np.arange(sr) / sr
    tone = np.sin(2 * np.pi * 440 * time)
    result = extract_features(tone, sr, include_mfcc=False)
    assert result["rms"] == pytest.approx(1 / np.sqrt(2), rel=1e-3)
    assert result["dominant_frequency_hz"] == pytest.approx(440, abs=1)
    assert result["spectral_centroid_hz"] > 0
    assert 0 <= result["zero_crossing_rate"] <= 1
    assert result["spectral_rolloff_85_hz"] > 0


def test_silence_has_zero_spectral_features():
    result = extract_features(np.zeros(128), 8000, include_mfcc=False)
    assert result["dominant_frequency_hz"] == 0
    assert result["spectral_centroid_hz"] == 0
    assert result["spectral_bandwidth_hz"] == 0
    assert result["spectral_rolloff_85_hz"] == 0


def test_invalid_inputs_are_rejected():
    with pytest.raises(ValueError):
        extract_features(np.array([]), 8000, include_mfcc=False)
    with pytest.raises(ValueError):
        extract_features(np.ones(8), 0, include_mfcc=False)
    with pytest.raises(ValueError):
        to_mono(np.array([[1.0, np.nan]]))
