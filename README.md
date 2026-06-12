# Open-Audiodeleto

![Clippsly Banner](Banner.webp)

Public/open-source lightweight baseline.

This model detects audio patterns similar to known bypass uploads. It does not prove copyright infringement. It does not prove intent. It should not be used as the sole basis for enforcement.

## What It Does

This model produces a bypass-audio probability from audio-only features such as duration, RMS statistics, spectral statistics, tempo, silence ratio, and loudness-transition scores.

## What It Does Not Do

It does not prove copyright infringement. It does not prove intent. It should not be used for automatic bans, automatic account termination, or legal copyright conclusions. No automatic enforcement should rely only on this model.

## Run

```bash
python open_audiodeleto.py /path/to/audio.ogg
```

Example:

```bash
python open_audiodeleto.py audio.mp3
```

Example JSON:

```json
{
  "model": "Open-Audiodeleto",
  "version": "0.1-800",
  "file": "audio.mp3",
  "bypassProbability": 0.87,
  "riskLevel": "high",
  "recommendation": "review",
  "note": "This model detects audio patterns similar to known bypass uploads. It does not prove copyright infringement. It does not prove intent. It should not be used as the sole basis for enforcement."
}
```

## Metrics

Validation:

```json
{
  "accuracy": 0.7,
  "precision": 0.6875,
  "recall": 0.7333333333333333,
  "f1": 0.7096774193548387,
  "confusion_matrix": [
    [
      40,
      20
    ],
    [
      16,
      44
    ]
  ]
}
```

Test:

```json
{
  "accuracy": 0.7916666666666666,
  "precision": 0.7692307692307693,
  "recall": 0.8333333333333334,
  "f1": 0.8,
  "confusion_matrix": [
    [
      45,
      15
    ],
    [
      10,
      50
    ]
  ]
}
```

## Files

- `model.pkl`
- `metadata.json`
- `features.csv`
- `splits.csv`
- `results.json`
- `misclassified_files.csv`
- `invalid_files.csv`
- `open_audiodeleto.py`
- `requirements.txt`
