# ===[ LIBRARIES ]===
from pyautogui_bot_module import PyautoGuiBot
from pyautogui_bot_images import images_dict
from pyautogui_bot_logs import log_files_dict
from pyautogui_bot_dependencies import init, Fore, pyautogui


# ===[ INITIALIZATIONS ]===
init(autoreset=True)
# global pause between pyautogui actions
pyautogui.PAUSE = 1


# ===[ VARIABLES ]===
images = images_dict
log_files = log_files_dict


# ===[ MAIN ]===
def main():
    bot = PyautoGuiBot()
    pass


# ===[ __MAIN__ ]===
if __name__ == '__main__':
    main()
