#!/usr/bin/env python3
"""CLI for Open-Audiodeleto."""

from __future__ import annotations

import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
EXPERIMENT_DIR = REPO_ROOT / "experiments" / "first_pass_bypass_classifier"
if str(EXPERIMENT_DIR) not in sys.path:
    sys.path.insert(0, str(EXPERIMENT_DIR))

try:
    from train_bypass_classifier import FEATURE_COLUMNS, extract_features, joblib, pd, require_binary
except Exception as exc:
    print(json.dumps({"ok": False, "error": f"Could not load dependencies: {exc}"}))
    raise SystemExit(2)


RECOMMENDATIONS = {
    "low": "allow",
    "medium": "review",
    "high": "review",
    "critical": "review"
}
NOTE = "This model detects audio patterns similar to known bypass uploads. It does not prove copyright infringement. It does not prove intent. It should not be used as the sole basis for enforcement."


def risk_level(probability: float, thresholds: dict) -> str:
    if probability >= thresholds["critical"]:
        return "critical"
    if probability >= thresholds["high"]:
        return "high"
    if probability >= thresholds["medium"]:
        return "medium"
    return "low"


def fail(message: str, file_path: str | None = None, code: int = 1) -> None:
    payload = {"ok": False, "error": message}
    if file_path is not None:
        payload["file"] = file_path
    print(json.dumps(payload, ensure_ascii=False))
    raise SystemExit(code)


def main() -> None:
    if len(sys.argv) != 2:
        fail("Expected exactly one audio file path.", code=2)

    audio_path = Path(sys.argv[1]).expanduser()
    if not audio_path.exists() or not audio_path.is_file():
        fail("File missing.", str(audio_path), code=1)

    try:
        require_binary("ffmpeg")
        require_binary("ffprobe")
    except SystemExit:
        fail("ffmpeg and ffprobe are required.", str(audio_path), code=2)

    try:
        metadata = json.loads((SCRIPT_DIR / "metadata.json").read_text(encoding="utf-8"))
        model = joblib.load(SCRIPT_DIR / "model.pkl")
    except Exception as exc:
        fail(f"Could not load model files: {exc}", str(audio_path), code=2)

    try:
        features = extract_features(str(audio_path), sample_rate=22050, hop_length=512, n_fft=2048)
        row = pd.DataFrame([[features[column] for column in FEATURE_COLUMNS]], columns=FEATURE_COLUMNS)
        probability = float(model.predict_proba(row)[0][1])
    except Exception:
        fail("Could not decode audio file.", str(audio_path), code=1)

    level = risk_level(probability, metadata["riskThresholds"])
    payload = {
        "model": metadata["name"],
        "version": metadata["version"],
        "file": str(audio_path),
        "bypassProbability": round(probability, 6),
        "riskLevel": level,
        "recommendation": RECOMMENDATIONS[level],
        "note": NOTE,
    }
    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
