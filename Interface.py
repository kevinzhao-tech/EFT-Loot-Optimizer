import keyboard
import mouse
import screenscraper.ScreenScraper as ScreenScraper
import pytarkovdata
from Item import Item


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
        screenshot = ScreenScraper.get_screenshot_tooltip()

        result = ScreenScraper.parse_click(screenshot)
        result = result.replace('\n', '')
        print(result)
        try:
            item = Item(pytarkovdata.get_uid(result))
            return item.get_optimal_trader()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    start_polling_optimal_trader()
