# Saarthi

Hinglish-first Chrome assistant with voice input, typed side-panel commands,
a draggable dog, browser actions, and Samsung SmartThings AC control.

## Current architecture

```text
Chrome extension (voice / side panel)
  → background.js
  → POST /browser/analyze (FastAPI)
  → JevService (TypeSafe intent understanding)
  → domain routing
      BROWSER → BrowserActionService → browser command → extension
      SMART_HOME / AC → ActionPlanner → PlanValidator
        → SmartHomeExecutor → ACController → SmartThingsClient → Samsung AC
```

Browser actions include opening supported websites, Google/YouTube/LeetCode
search, YouTube playback, opening a new tab, going back, and closing a tab.
Smart-home actions include power, temperature, mode, and fan speed changes,
compound plans, and polling to verify the resulting device state.
Other requests and unsupported smart devices are not executed.

## Run locally

Use Python 3.10 or newer. From the project root:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Before starting, configure these variables in your local `backend/.env`:
`TYPESAFE_API_KEY`, `SMARTTHINGS_TOKEN`, and `SMARTTHINGS_AC_DEVICE_ID`.
The backend requires all three during initialization. Keep credentials local;
`.env` files are ignored by Git.

In Chrome, open `chrome://extensions`, enable Developer mode, and load
`extension/` as an unpacked extension. Its background script calls the backend
at `http://127.0.0.1:8000/browser/analyze`.

## Existing manual checks

The `backend/test_*.py` files are manual integration scripts for current code,
not an isolated automated test suite. Run them from `backend/` only when you
intend to contact the external services. The AC controller and executor scripts
change the physical device state, including power and settings. The SmartThings
client script reads device information; the Jev script calls TypeSafe.
Do not run automatic test discovery over these scripts as a cleanup check.

## Local archive

`older_features/` is ignored by Git and preserves the previous assistant backend,
its local ML model and database, train/Python experiments, and Swift experiments.
Current backend code does not import this archive. Archived files retain their
original content and import paths for reference; they are not a second supported
application. The old `/analyze` route has been removed from the current backend.
