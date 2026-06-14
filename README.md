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

### First run - login

On the first run the script needs to authenticate with HoYoLab. There are two ways to do this.

---

#### Option 1: Email / password (automatic)

1. Fill in `HOYOLAB_LOGIN` and `HOYOLAB_PASSWORD` in `.env`
2. Run `python main.py`
3. A browser page may open with a CAPTCHA - solve it if it appears
4. A local page with an input field and a **Send** button will open
5. HoYoLab sends a one-time verification code to your email
6. Enter the code and click **Send**
7. Login is complete - credentials are saved to `cookies.txt` and reused on future runs

---

#### Option 2: Manual cookies from browser DevTools

If you want to skip the email flow, you can copy cookies directly from your browser.

1. Go to [hoyolab.com](https://www.hoyolab.com) and make sure you are logged in
2. Open DevTools (`F12`) and go to **Application > Cookies > https://www.hoyolab.com**
3. Create a file named `cookies.txt` in the project folder

You can use either format:

**JSON format:**
```json
{
  "ltoken_v2": "...",
  "ltuid_v2": "...",
  "ltmid_v2": "...",
  "account_id_v2": "...",
  "account_mid_v2": "...",
  "cookie_token_v2": "..."
}
```

**Cookie string format:**
```
ltoken_v2=...; ltuid_v2=...; ltmid_v2=...; account_id_v2=...; account_mid_v2=...; cookie_token_v2=...
```

Copy the values for these six keys from DevTools and paste them in. `HOYOLAB_LOGIN` and `HOYOLAB_PASSWORD` are not needed when using this method.

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
