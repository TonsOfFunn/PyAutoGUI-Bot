# PyAutoGUI Bot Template

A minimal, reusable baseline for GUI automation projects using [PyAutoGUI](https://pyautogui.readthedocs.io/). Use this as a starting point for any image-based desktop automation.

## Setup

1. **Create a virtual environment** (recommended):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   source .venv/bin/activate   # macOS/Linux
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set your project root** in `pyautogui_bot_config.py`:

   ```python
   PROJECT_ROOT = Path(r"~\Documents\<project-name>").expanduser()
   ```

   Replace `<project-name>` with your project folder (e.g. `my-game-bot`). All image and log paths are derived from this single variable.

## Project layout

- **`pyautogui_bot_config.py`** — Single place for `PROJECT_ROOT`. Change this for each new project.
- **`pyautogui_bot_main.py`** — Entry point. Implement your automation flow in `main()`.
- **`pyautogui_bot_module.py`** — `PyautoGuiBot` class: image locate/click, waits, random range, file logging.
- **`pyautogui_bot_images.py`** — Dict of image paths (under `PROJECT_ROOT/images/`). Add keys and filenames for your screenshots.
- **`pyautogui_bot_logs.py`** — Dict of log file paths (under `PROJECT_ROOT/logs/`). Add keys for each log you write.
- **`pyautogui_bot_dependencies.py`** — Third-party and stdlib imports used by the bot module.

## Running

```bash
python pyautogui_bot_main.py
```

## Folder structure for your project

Create a folder for each project and put images and logs under it, e.g.:

```
Documents\
  <project-name>\
    images\
      button-ok.png
      menu-icon.png
    logs\
      logfile.log
```

Set `PROJECT_ROOT` in `pyautogui_bot_config.py` to that folder (e.g. `Path(r"~\Documents\my-bot").expanduser()`), then reference images and log files in `pyautogui_bot_images.py` and `pyautogui_bot_logs.py` by name only; paths are built from `PROJECT_ROOT`.

## Example usage in `main()`

```python
def main():
    bot = PyautoGuiBot()
    bot._find_image_once_and_click(images["descriptive-image-name"])
    bot._wait_seconds_random()
    bot._write_data_log(log_files["LOG_FILE"], "Step completed.")
```

See docstrings in `pyautogui_bot_module.py` for all bot methods (find once, find and click, search until found, continuous loops, etc.).
