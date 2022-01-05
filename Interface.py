import keyboard
import mouse
import ScreenScraper
import pytarkovdata


def start_polling_optimal_trader():
    """
    Starts the polling of the keyboard and mouse for ocr near the mouse
    Prints, to the console, the ocr text when alt+click is pressed
    """
    while True:
        print(poll_mouse_for_optimal_trader())


def poll_mouse_for_optimal_trader():
    """
    polls, once, the keyboard and mouse for ocr near the mouse
    Prints, to the console, the ocr text when alt+click is pressed
    """

    mouse.wait('left')
    if keyboard.is_pressed('t'):
        screenshot = ScreenScraper.get_screenshot_near_mouse()

        result = ScreenScraper.parse_click(screenshot)
        result = result.replace('\n', '')
        print(result)
        try:
            return pytarkovdata.get_optimal_trader_by_name(result)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    start_polling_optimal_trader()
