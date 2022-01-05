import unittest
import ScreenScraper
import cv2
from PIL import Image


class TestScreenScraper(unittest.TestCase):
    def test_get_screenshots(self):
        results = ScreenScraper.get_screenshots()
        cv2.imshow('test', results[0])
        cv2.waitKey(0)
        cv2.imshow('test', results[1])
        cv2.waitKey(0)

    def test_isolate_text(self):
        cv2.imshow('test results', ScreenScraper.isolate_text(ScreenScraper.get_screenshots()[0]))
        cv2.waitKey()
        cv2.imshow('test results', ScreenScraper.isolate_text(ScreenScraper.get_screenshots()[1]))
        cv2.waitKey()

    def test_parse_screen(self):
        print(ScreenScraper.parse_screen(ScreenScraper.get_screenshots()))

