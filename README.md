# Auto Senpai

[![Build Status](https://github.com/ServOMorph/Auto_Senpai/actions/workflows/python-app.yml/badge.svg)](https://github.com/ServOMorph/Auto_Senpai/actions)

Automation bot made for **[senpai-stream](https://senpai-stream.com)** that detects ads on screen and automatically clicks through reward sequences using image recognition.

## What it does

Monitors the **left half of the screen** for an ad (`pub.png`). When detected, it automatically:

1. Clicks the ad
2. Waits 2s → clicks **Gagner**
3. Waits 1s → clicks **Valider**
4. Waits 2s → clicks **Continuer**

A fullscreen red overlay flashes on screen to notify you each time the sequence triggers.

## Requirements

- Python 3.9+
- Windows (uses pyautogui + tkinter)

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Run the main bot
python pub_clicker.py

# Test image detection (shows overlay when prochaine_vue.png is found)
python test_detect.py
```

Stop with `Ctrl+C`.

## Setup — add your own images

Put your template images in the `IMAGES/` folder:

| File | Role |
|------|------|
| `pub.png` | Ad to detect (searched in left half only) |
| `gagner.png` | "Claim reward" button |
| `valider.png` | "Validate" button |
| `continuer.png` | "Continue" button |

To capture a template: take a screenshot and crop tightly around the button/image you want to detect.

## Configuration

In `pub_clicker.py`, adjust at the top:

```python
CONFIDENCE = 0.8  # Detection threshold (0.0–1.0). Lower = more tolerant.
```

## How it works

Uses `pyautogui` + `pillow` + `opencv` for pixel-level template matching with configurable confidence. The screen is split in half for the initial ad detection to avoid false positives on the right side.

## Author

Made by **ServOMorph**
