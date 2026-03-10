# ===[ CONFIG ]===
"""
Single place to set the project name / root for this automation project.
Used by pyautogui_bot_images and pyautogui_bot_logs for image and log paths.
"""
from pathlib import Path

# Change this for each new project (folder under which images/ and logs/ live).
PROJECT_ROOT = Path(r"~\Documents\<project-name>").expanduser()

