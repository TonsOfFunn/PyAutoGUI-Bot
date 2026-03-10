# ===[ LIBRARIES ]===
"""
PyAutoGUI bot module.

Provides the PyautoGuiBot class for GUI automation using pyautogui: image-based
locate and click helpers, configurable waits, random ranges, and file logging.
Used with image path and log path config (e.g. pyautogui_bot_images, pyautogui_bot_logs).
"""
from pyautogui_bot_dependencies import (
    pyautogui, 
    random, 
    Fore, 
    Path, 
    datetime
    )


# ===[ CLASSES ]===
class PyautoGuiBot:
    def __init__(self):
        """
        Bot instance for GUI automation. Uses pyautogui via module import
        in its methods (image locate/click, waits, logging). No instance state required.
        """
        pass


    # ===[ PRIVATE ]===
    def __extract_filename_from_filepath(self, filepath: str) -> str:
        """
        Extract the filename from a given filepath.

        This method extracts the filename from the provided filepath, 
        converts it to uppercase, and replaces any dashes ('-') with spaces.

        Args:
            filepath (str): The full path to the file.

        Returns:
            str: The processed filename.

        Raises:
            Exception: Re-raised with added message if path processing fails.
        """
        try:
            filename = Path(filepath).stem
            return str(filename.upper().replace('-', ' '))
        
        except Exception as e:
            raise Exception(f'[!] Filename from filepath extraction failed: \n{e}')
    

    # ===[ PROTECTED ]===
    def _write_data_log(self, log_file: str, log_message: str='''Default message.'''):
        """
        Write custom log message to given log file on separate lines.

        Output to log file example. 
        
        [ year-month-day hours:minutes:seconds ] -> Custom log message.

        Args:
            log_file (str): The full path to the file.
            log_message (str): Any custom message provided.

        Returns:
            None.

        Raises:
            Exception: Re-raises the exception from the underlying file operation (e.g. FileNotFoundError, PermissionError).
        """
        try:
            with open(log_file, 'a') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f'[{timestamp}] -> {log_message}\n')
            
        except Exception as e:
            raise type(e)(f'[!] Unable to write log file: \n{e}') from e
        

    def _click_region(self, image_location, duration_range: tuple[float, float] = (0.57, 0.91)) -> None:
        """
        Click at a random point within the given image region with eased movement.

        Args:
            image_location: Bounding box (left, top, width, height) from pyautogui.locateOnScreen.
            duration_range (tuple[float, float]): (min, max) seconds for the mouse movement. Default (0.57, 0.91).

        Returns:
            None.
        """
        left, top, width, height = image_location
        x = random.randint(left, left + width)
        y = random.randint(top, top + height)
        pyautogui.click(x=x, y=y, duration=random.uniform(*duration_range), tween=pyautogui.easeOutQuad)


    def _wait_seconds(self, seconds: float = 10):
        """
        Use pyautogui.sleep() to wait for specified amount of time.

        Args:
            seconds (float): Amount of time in seconds. Default 10.

        Returns:
            None.

        Raises:
            None. On failure, prints an error message and does not raise.
        """
        try:
            pyautogui.sleep(seconds)
        
        except Exception as e:
            print(f'[!] Unable to wait: {e}')
    

    def _wait_seconds_random(self, time_start: float=1.56, time_stop: float=3.59):
        """
        Wait for a random duration between time_start and time_stop seconds.

        Args:
            time_start (float): Minimum wait time in seconds. Default 1.56.
            time_stop (float): Maximum wait time in seconds. Default 3.59.

        Returns:
            None. On failure, prints an error message and does not raise.
        """
        try:
            pyautogui.sleep(random.uniform(time_start, time_stop))
        
        except Exception as e:
            print(f'[!] Unable to wait randomly: \n{e}')

    
    def _random_range(self, minimum: int=5, maximum: int=7) -> int | None:
        """
        Return a random integer in the closed interval [minimum, maximum].

        Args:
            minimum (int): Lower bound (inclusive). Default 5.
            maximum (int): Upper bound (inclusive). Default 7.

        Returns:
            int: Random integer in [minimum, maximum], or None on error (error is printed).
        """
        try:
            return random.randint(minimum, maximum)
        
        except Exception as e:
            print(f'[!] Unable to return random range: {e}')
            return None


    def _find_image_once(self, filepath: str, confidence: float=0.9, grayscale: bool=False) -> bool:
        """
        Tries to locate the image on the screen once.

        Args:
            filepath (str): Full path to image file.
            confidence (float): Confidence level for image matching, range (0 - 1).
            grayscale (bool): False, image matching uses color. True, image matching uses grayscale.  

        Returns:
            bool: True if image was found; False if not found (ImageNotFoundException is caught and not propagated).

        Raises:
            No exceptions propagated; pyautogui.ImageNotFoundException is handled.
        """
        try:
            image_location = pyautogui.locateOnScreen(filepath, confidence=confidence, grayscale=grayscale)

            if image_location is not None:
                print(Fore.WHITE + f'[+] {self.__extract_filename_from_filepath(filepath)} image located...')
                return True
            
        except pyautogui.ImageNotFoundException:
            print(Fore.YELLOW + f'[-] {self.__extract_filename_from_filepath(filepath)} image not located, continuing...')
            return False


    def _find_image_once_and_click(self, filepath: str, confidence: float=0.9, grayscale: bool=False) -> bool:
        """
        Tries to locate the image on screen and click it once.

        Args:
            filepath (str): Full path to image file.
            confidence (float): Confidence level for image matching, range (0 - 1).
            grayscale (bool): False, image matching uses color. True, image matching uses grayscale. 

        Returns:
            bool: True if image was found and clicked; False if not found (ImageNotFoundException is caught and not propagated).

        Raises:
            No exceptions propagated; pyautogui.ImageNotFoundException is handled.
        """
        try:
            image_location = pyautogui.locateOnScreen(filepath, confidence=confidence, grayscale=grayscale)

            if image_location is not None:
                self._click_region(image_location)
                print(Fore.MAGENTA + f'[+] {self.__extract_filename_from_filepath(filepath)} image located, clicked...')
                return True
            
        except pyautogui.ImageNotFoundException:
            print(Fore.YELLOW + f'[-] {self.__extract_filename_from_filepath(filepath)} image not located, continuing...')
            return False


    def _find_images_once_and_click(self, *filepaths: str, confidence: float=0.9, grayscale: bool=False):
        """
        Locate multiple images on screen and click the first one found.

        Tries each filepath in order; on first match, clicks that region and returns.
        ImageNotFoundException is caught per attempt and not propagated.

        Args:
            *filepaths (str): Full paths to image files to try in order.
            confidence (float): Confidence for image matching (0–1). Default 0.9.
            grayscale (bool): Use grayscale matching if True. Default False.

        Returns:
            None.
        """
        for filepath in filepaths:
            try:
                image_location = pyautogui.locateOnScreen(filepath, confidence=confidence, grayscale=grayscale)

                if image_location is not None:
                    self._click_region(image_location)
                    print(Fore.MAGENTA + f'[+] {self.__extract_filename_from_filepath(filepath)} image located, clicked...')
                    # exit function on first image found
                    return
                
            except pyautogui.ImageNotFoundException:
                print(Fore.YELLOW + f'[-] {self.__extract_filename_from_filepath(filepath)} image not located, continuing...')


    def _find_image_continuously(self, filepath: str, confidence: float=0.9, grayscale: bool=False, sleep_time1: float=1):
        """
        Poll for the image repeatedly while it is present; exit when it is no longer found.

        Each failed attempt catches ImageNotFoundException. When the image disappears, the loop exits.

        Args:
            filepath (str): Full path to image file.
            confidence (float): Confidence for image matching (0–1). Default 0.9.
            grayscale (bool): Use grayscale matching if True. Default False.
            sleep_time1 (float): Seconds to sleep between detections when image is present. Default 1.

        Returns:
            None.
        """
        while True:
            try:
                image_location = pyautogui.locateOnScreen(filepath, confidence=confidence, grayscale=grayscale)

                if image_location is not None:
                    print(Fore.WHITE + f'[+] {self.__extract_filename_from_filepath(filepath)} image located, retrying...')
                    pyautogui.sleep(sleep_time1)
                
            except pyautogui.ImageNotFoundException:
                print(Fore.YELLOW + f'[-] {self.__extract_filename_from_filepath(filepath)} image not located, continuing...')
                # keep searching for image until it's not found
                break


    def _find_image_and_click_continuously(self, filepath: str, confidence: float=0.9, grayscale: bool=False, sleep_time1: float=1):
        """
        Find the image and click it repeatedly while it is present; exit when it is no longer found.

        Uses _click_region for each click. ImageNotFoundException is caught; when the image disappears, the loop exits.

        Args:
            filepath (str): Full path to image file.
            confidence (float): Confidence for image matching (0–1). Default 0.9.
            grayscale (bool): Use grayscale matching if True. Default False.
            sleep_time1 (float): Seconds to sleep after each click while image is present. Default 1.

        Returns:
            None.
        """
        while True:
            try:
                image_location = pyautogui.locateOnScreen(filepath, confidence=confidence, grayscale=grayscale)

                if image_location is not None:
                    self._click_region(image_location)
                    print(Fore.MAGENTA + f'[+] {self.__extract_filename_from_filepath(filepath)} image located, clicked...')
                    pyautogui.sleep(sleep_time1)
                    
            except pyautogui.ImageNotFoundException:
                print(Fore.YELLOW + f'[-] {self.__extract_filename_from_filepath(filepath)} image not located, continuing...')
                # keep searching for image and click until it's not found
                break


    def _find_image_and_click_wait_continuously(self, filepath: str, confidence: float=0.9, grayscale: bool=False, 
                                                sleep_time1: float=1, sleep_time2: float=3):
        """
        Find the image, click it, wait sleep_time1, click again, wait sleep_time2; repeat until image is not found.

        Uses _click_region for the first click; the second click is at the current position. Exits when the image is no longer found.

        Args:
            filepath (str): Full path to image file.
            confidence (float): Confidence for image matching (0–1). Default 0.9.
            grayscale (bool): Use grayscale matching if True. Default False.
            sleep_time1 (float): Seconds to wait after first click. Default 1.
            sleep_time2 (float): Seconds to wait after second click. Default 3.

        Returns:
            None.
        """
        while True:
            try:
                image_location = pyautogui.locateOnScreen(filepath, confidence=confidence, grayscale=grayscale)

                if image_location is not None:
                    self._click_region(image_location)
                    print(Fore.MAGENTA + f'[+] {self.__extract_filename_from_filepath(filepath)} image located, clicked...')
                    # wait, click, wait loop
                    pyautogui.sleep(sleep_time1)
                    pyautogui.click()
                    pyautogui.sleep(sleep_time2)
                
            except pyautogui.ImageNotFoundException:
                print(Fore.YELLOW + f'[-] {self.__extract_filename_from_filepath(filepath)} image not located, continuing...')
                # keep searching for image until is not found
                break


    def _search_image_until_found(self, filepath: str, confidence: float=0.9, grayscale: bool=False, sleep_time1: float=1):
        """
        Search for the image until it is found; sleep sleep_time1 between failed attempts.

        ImageNotFoundException is caught each attempt. Returns when the image is located.

        Args:
            filepath (str): Full path to image file.
            confidence (float): Confidence for image matching (0–1). Default 0.9.
            grayscale (bool): Use grayscale matching if True. Default False.
            sleep_time1 (float): Seconds to sleep between attempts when not found. Default 1.

        Returns:
            None.
        """
        while True:
            try:
                image_location = pyautogui.locateOnScreen(filepath, confidence=confidence, grayscale=grayscale)

                if image_location is not None:
                    print(Fore.WHITE + f'[+] {self.__extract_filename_from_filepath(filepath)} image located, continuing...')
                    # keep searching for image until it's found
                    break
                
            except pyautogui.ImageNotFoundException:
                print(Fore.YELLOW + f'[-] {self.__extract_filename_from_filepath(filepath)} image not located, retrying...')
                pyautogui.sleep(sleep_time1)


    def _search_image_until_found_and_click(self, filepath: str, confidence: float=0.9, grayscale: bool=False, sleep_time1: float=1):
        """
        Search for the image until it is found, then click it once via _click_region.

        Sleeps sleep_time1 between failed attempts. ImageNotFoundException is caught until the image is found.

        Args:
            filepath (str): Full path to image file.
            confidence (float): Confidence for image matching (0–1). Default 0.9.
            grayscale (bool): Use grayscale matching if True. Default False.
            sleep_time1 (float): Seconds to sleep between attempts when not found. Default 1.

        Returns:
            None.
        """
        while True:
            try:
                image_location = pyautogui.locateOnScreen(filepath, confidence=confidence, grayscale=grayscale)

                if image_location is not None:
                    self._click_region(image_location)
                    print(Fore.MAGENTA + f'[+] {self.__extract_filename_from_filepath(filepath)} image located, clicked...')
                    # keep searching for image until it's found and clicked
                    break
                
            except pyautogui.ImageNotFoundException:
                print(Fore.YELLOW + f'[-] {self.__extract_filename_from_filepath(filepath)} image not located, retrying...')
                pyautogui.sleep(sleep_time1)
