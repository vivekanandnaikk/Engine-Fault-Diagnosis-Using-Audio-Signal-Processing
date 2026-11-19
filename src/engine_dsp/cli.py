"""Command-line interface for engine audio feature analysis."""

import argparse
import csv
import json
from pathlib import Path

from .audio import load_audio
from .comparison import compare_files
from .features import extract_features


def _analyze(path: Path) -> dict[str, float]:
    samples, sample_rate = load_audio(path)
    return extract_features(samples, sample_rate)


def main() -> None:
    parser = argparse.ArgumentParser(prog="engine-dsp", description="Exploratory motorcycle-engine audio feature analysis")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze_parser = subparsers.add_parser("analyze", help="extract descriptive features from one WAV file")
    analyze_parser.add_argument("audio", type=Path)

    compare_parser = subparsers.add_parser("compare", help="compare one normal and one faulty WAV recording")
    compare_parser.add_argument("normal", type=Path)
    compare_parser.add_argument("faulty", type=Path)

    dataset_parser = subparsers.add_parser("dataset", help="extract features for WAV files under normal/ and faulty/ folders")
    dataset_parser.add_argument("root", type=Path)
    dataset_parser.add_argument("--output", type=Path, default=Path("features.csv"), help="CSV output path (default: features.csv)")

    args = parser.parse_args()
    if args.command == "analyze":
        print(json.dumps({"file": str(args.audio), "features": _analyze(args.audio)}, indent=2))
    elif args.command == "compare":
        print(json.dumps(compare_files(args.normal, args.faulty), indent=2))
    else:
        rows = []
        for label in ("normal", "faulty"):
            folder = args.root / label
            if folder.exists():
                for audio_path in sorted(folder.rglob("*.wav")):
                    rows.append({"label": label, "file": str(audio_path), **_analyze(audio_path)})
        if not rows:
            parser.error(f"No WAV files found in {args.root}/normal or {args.root}/faulty")
        fieldnames = list(rows[0])
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Wrote {len(rows)} recording(s) to {args.output}")


if __name__ == "__main__":
    main()
