from scipy.io import wavfile
import numpy as np

from engine_dsp.audio import load_audio


def test_load_wav_converts_stereo_to_mono(tmp_path):
    path = tmp_path / "sample.wav"
    wavfile.write(path, 16000, np.array([[1000, -1000], [2000, 0]], dtype=np.int16))
    samples, sample_rate = load_audio(path)
    assert sample_rate == 16000
    assert samples.shape == (2,)
    np.testing.assert_allclose(samples, [0.0, 1000 / 32768])
