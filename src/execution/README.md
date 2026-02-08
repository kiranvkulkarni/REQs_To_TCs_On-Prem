# 📱 Test Execution Engine — uiautomator2 v2.0

## Overview

Executes generated Gherkin test cases on Android devices/emulators using **uiautomator2** with:

- 📸 **Screenshot capture on failure**
- 🎥 **Video recording of test execution**
- 🔄 **Test retry logic for flaky tests**
- 📱 **Parallel execution on multiple devices**

## Setup

1. Install uiautomator2:
   ```bash
   pip install uiautomator2
   ```

2. Connect Android devices/emulators via USB or ADB:
   ```bash
   adb devices
   ```

3. Initialize devices:
   ```bash
   python -m uiautomator2 init
   ```

4. Configure `config/settings.yaml`:
   - Set `app_package`, `app_activity`
   - Set `device_serials` for parallel execution
   - Set `screenshot_dir`, `video_dir`

## Running Tests

```bash
python src/execution/executor.py
```

## Features

### 📸 Screenshot Capture on Failure

- Automatically captures screenshot when a step fails.
- Saves to `data/screenshots/<scenario_name>/<step_name>.png`.

### 🎥 Video Recording

- Records test execution using `adb screenrecord`.
- Saves to `data/videos/<scenario_name>.mp4`.

### 🔄 Retry Logic

- Retries failed scenarios up to `retry_count` times.
- Delay between retries: `delay_seconds`.

### 📱 Parallel Execution

- Runs tests on multiple devices in parallel.
- Configure `device_serials` in `config/settings.yaml`.

## Extending

- Add new step mappings in `uiautomator2_adapter.py` → `_execute_step`.
- Add new report formats in `report_generator.py`.

## Troubleshooting

- Ensure devices are connected and `adb devices` shows them.
- Ensure app is installed on devices.
- Run `python -m uiautomator2 init` to install ATX agent.
- Check `data/logs/app.log` for errors.