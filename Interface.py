import keyboard
import mouse
import ScreenScraper


def start_polling():
    """
    Starts the polling of the keyboard and mouse for ocr near the mouse
    Prints, to the console, the ocr text when alt+click is pressed
    """
    while True:
        mouse.wait('left')
        if keyboard.is_pressed('alt'):
            screenshot = ScreenScraper.get_screenshot_near_mouse()

            result = ScreenScraper.parse_click(screenshot)
            print(result)


if __name__ == '__main__':
    start_polling()
