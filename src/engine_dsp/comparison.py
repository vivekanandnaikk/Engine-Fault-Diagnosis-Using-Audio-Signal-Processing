"""Feature comparison helpers."""

from pathlib import Path

from .audio import load_audio
from .features import extract_features


def compare_files(normal_path: str | Path, faulty_path: str | Path) -> dict[str, dict[str, float]]:
    """Extract features from two files and return values and faulty-minus-normal deltas."""
    normal_audio, normal_sr = load_audio(normal_path)
    faulty_audio, faulty_sr = load_audio(faulty_path)
    normal = extract_features(normal_audio, normal_sr)
    faulty = extract_features(faulty_audio, faulty_sr)
    shared = normal.keys() & faulty.keys()
    return {
        "normal": normal,
        "faulty": faulty,
        "difference_faulty_minus_normal": {key: faulty[key] - normal[key] for key in sorted(shared)},
    }
