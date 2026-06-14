# hoyolab-monitor

A terminal-based real-time resource monitor for HoYoLab accounts. Tracks **Genshin Impact**, **Zenless Zone Zero**, and **Honkai: Star Rail** - resin, battery charge, expeditions, weekly challenges, and more. Refreshes on a configurable schedule with a live countdown progress bar.

## Features

**Genshin Impact**
- Resin and realm currency with fill timers
- Commissions, expeditions, parametric transformer
- Spiral Abyss, Imaginarium Theater, Stygian Onslaught

**Zenless Zone Zero**
- Battery charge, engagement, video store state
- Ridu Weekly, hollow zero, scratch card
- Shiyu Defense, Deadly Assault, Suibian Temple / auto-work

**Honkai: Star Rail**
- TB Power (current and reserved), daily training
- Simulated Universe, Echo of War, Bonus Synchronicity Points
- Memory of Chaos, Pure Fiction, Apocalyptic Shadow, Anomaly Arbitration

**General**
- Each game section is only fetched and shown if its UID is set in `.env`
- Sound alerts when resources hit 90 / 95 / 99% capacity
- Countdown progress bar between refreshes
- Loading spinner during data fetch
- Automatic update check on startup

---

## Requirements

- Python 3.10+
- pip

---

## Installation

### Windows (PowerShell)
```powershell
git clone https://github.com/sanioooook/hoyolab-monitor.git
cd hoyolab-monitor
.\setup.ps1
```

### Windows (cmd)
```cmd
git clone https://github.com/sanioooook/hoyolab-monitor.git
cd hoyolab-monitor
setup.bat
```

### Linux / macOS
```bash
git clone https://github.com/sanioooook/hoyolab-monitor.git
cd hoyolab-monitor
chmod +x setup.sh && ./setup.sh
```

Then open `.env` and fill in your credentials (see section below).

---

## Configuration

Copy `.env.example` to `.env` and edit it:

```env
# HoYoLab credentials (required)
HOYOLAB_LOGIN=your@email.com
HOYOLAB_PASSWORD=yourpassword

# Game UIDs - leave blank or remove the line to disable that game
GENSHIN_UID=
ZZZ_UID=
HSR_UID=

# Optional settings
LANG=en-us
DELAY_MINUTES=15
TWOCAPTCHA_API_KEY=
```

Your UID can be found in your HoYoLab profile or in-game.

---

## Usage

```bash
python main.py
```

---

## Updating

### If you cloned via git
```bash
git pull
pip install -r requirements.txt
```

### If you downloaded a zip
Download the latest archive from [Releases](https://github.com/sanioooook/hoyolab-monitor/releases) and extract it over your existing folder. Your `.env` file will not be overwritten - it is excluded by `.gitignore`.

On every startup the monitor silently checks GitHub for a newer release and prints a notification if one is available.

---

## Credits

This project is built on top of [**genshin.py**](https://github.com/seriaati/genshin.py), maintained by [**seriaati**](https://github.com/seriaati). The entire data layer of this monitor would not exist without that library - huge thanks for keeping an unofficial HoYoLab API wrapper alive and well.
