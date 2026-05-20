# Contributing

## Helping implement new features

Some features require capturing device data before they can be implemented. If you're affected by one of those open issues and want to help, follow the steps below.

### What you'll be doing

You'll run a monitoring script that logs communication between the Dreame cloud and your device.

### Setup (one time)

You need Python 3.14 and Git. Python 3.14 is required — earlier versions are incompatible with Home Assistant 2026.3.1 and will fail when running `pip install -r tests/requirements.txt`.

```bash
git clone https://github.com/antondaubert/dreame-mower.git
cd dreame-mower
python3 -m venv .venv
.venv/bin/pip install -r tests/requirements.txt
```

### Step 1 – find your device ID

```bash
.venv/bin/python dev/list_devices.py
```

Enter your Dreame (or Mova) account email and password when prompted. You will also be asked for your region — choose the one matching your account (`eu`, `cn`, `us`, `ru`, or `sg`) — and your account type (`dreame` or `mova`). Note the numeric `did` value for your mower from the output.

### Step 2 – run the monitor

```bash
.venv/bin/python dev/realtime_monitor.py
```

Enter your email, password, region, and account type when prompted.

Now use the **Dreame app** to perform the action described in the issue (e.g. switch maps, start a zone mow). Do this a few times if you can. Let the monitor run for a couple of days or at least long enough to capture a few repetitions. Note: please ensure your computer doesn't go into sleep mode during this period.

Stop it with `Ctrl+C` when done. Logs are written to `dev/logs/<timestamp>/`.

### Step 3 – zip and attach

```bash
zip -r logs_capture.zip dev/logs/
```

Attach `logs_capture.zip` as a file to the GitHub issue.

### Alternative: one-shot device data snapshot

Some issues (e.g. missing map features like circular or rotated zones) require a snapshot of the device's stored configuration rather than a live event trace. For those, use `analyze_device_data.py` instead of — or in addition to — the realtime monitor.

```bash
.venv/bin/python dev/analyze_device_data.py
```

It accepts the same credential options as the monitor:

| Invocation | Credential source |
|---|---|
| `python dev/analyze_device_data.py` | Interactive prompts (default) |
| `python dev/analyze_device_data.py --launch-json` | `.vscode/launch.json` (dev shortcut) |
| `python dev/analyze_device_data.py --username you@example.com --device-id -123456789` | CLI flags (password still prompted securely) |

The tool fetches the full batch device data (`MAP.*`, `FBD_NTYPE.*`, `SETTINGS.*`, `SCHEDULE.*`, `OTA_INFO.*`) and prints a detailed analysis. It also saves raw JSON to `dev/logs/device_data_<timestamp>.json`. Attach that file to the issue.

---

That's it — thank you for helping!
