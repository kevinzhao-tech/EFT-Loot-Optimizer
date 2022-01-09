from PIL import Image, ImageGrab
import pytesseract
import cv2
import numpy as np
import pyautogui

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

"""
A program to take screenshots of the screen and then use OCR to extract text from the image
"""

screenshot = ImageGrab.grab()
screenshot_width = screenshot.size[0]
screenshot_height = screenshot.size[1]


def get_screenshots() -> tuple:
    """
    Gets the screenshots of the the inventory and ground loot as np arrays
    Returns:
        tuple: (inventory, ground loot) images

    """
    # take a screenshot of the middle third of the screen (inventory)
    inventory_offset = screenshot_width / 10
    inventory_screenshot = screenshot.crop((screenshot_width / 4 + inventory_offset, 0, 2 * screenshot_width / 4 + inventory_offset, screenshot_height))

    # take a screenshot of the right third of the screen (ground loot)
    ground_offset = screenshot_width / 100
    ground_screenshot = screenshot.crop((2 * screenshot_width / 3 - ground_offset, 0, screenshot_width - ground_offset, screenshot_height))
    return np.array(inventory_screenshot), np.array(ground_screenshot)


def get_screenshot_near_mouse() -> np.array:
    """
    Gets a screenshot of the area near the mouse
    Returns:
        np array: screenshot of area near mouse
    """
    # get mouse position
    mouse_position = pyautogui.position()
    # get screenshot of area near mouse
    local_screenshot = ImageGrab.grab(bbox=(mouse_position[0] - 60, mouse_position[1] - 20, mouse_position[0] + 60, mouse_position[1] + 20))
    return np.array(local_screenshot)


def isolate_text(image) -> np.array:
    """
    Isolates the text from the image
    Args:
        image: image to be isolated

    Returns:
        np array: image with text isolated
    """
    # convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # apply thresholding to outlined text
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    # apply some dilation and erosion to join text
    kernel = np.ones((1, 1), np.uint8)
    thresh = cv2.dilate(thresh, kernel, iterations=1)
    thresh = cv2.erode(thresh, kernel, iterations=1)
    return thresh


def read_text(image) -> str:
    """
    Reads the text of an image
    Args:
        image: image to be read

    Returns:
        string: text of image
    """
    return pytesseract.image_to_string(image, lang='eng', config='--psm 12')


def parse_screen(screenshots: tuple) -> tuple:
    """
    Parses the screen and returns a the inventory and ground loot strings as a tuple
    Returns:
        tuple: (inventory, ground loot) strings
    """
    inventory_screenshot_thresh = isolate_text(screenshots[0])
    ground_screenshot_thresh = isolate_text(screenshots[1])
    inventory_text = read_text(inventory_screenshot_thresh)
    ground_text = read_text(ground_screenshot_thresh)
    # regex to remove new lines
    inventory_text = inventory_text.replace('\n', '')
    ground_text = ground_text.replace('\n', ' ')
    return inventory_text, ground_text


def parse_click(local_screenshot: np.array) -> str:
    """
    Parses the screen and returns the text of the area near the mouse
    Returns:
        string: text of area near mouse
    """
    screenshot_thresh = isolate_text(local_screenshot)
    text = read_text(screenshot_thresh)
    return text


def item_detection(image: np.array) -> np.array:
    """
    Using object detection, finds items in the image
    Args:
        image: an np-array

    Returns:
        np array: image with items outlined
    """
    objects_found = cv2.CascadClassifier()

