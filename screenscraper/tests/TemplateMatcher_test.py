import unittest
from screenscraper.TemplateMatcher import TemplateMatcher as TemplateMatcher
import cv2


class TemplateMatcher_test(unittest.TestCase):
    def setUp(self):
        self.matcher = TemplateMatcher(r'C:\Users\zhao1\PycharmProjects\EFT-Loot-Optimizer\EfTIcons\uid', scale=4/3)
        # 4/3 scale is used for 1440p monitors as 1080p is the default for icon sizes
        # TODO: change to relative path

    def test_load(self):
        print(self.matcher.list_templates())

    def test_match_template(self):
        img = cv2.imread(r'C:\Users\zhao1\PycharmProjects\EFT-Loot-Optimizer\resources\test.jpg')
        result_rectangle = self.matcher.match_template(img, '5ca20abf86f77418567a43f2', self.matcher.templates_gray)
        cv2.rectangle(img, result_rectangle[0], result_rectangle[1], 255, 2)
        cv2.imshow('result', img)
        cv2.waitKey(0)

    def test_match(self):
        img = cv2.imread(r'C:\Users\zhao1\PycharmProjects\EFT-Loot-Optimizer\resources\test.jpg')
        self.matcher.match(img)


if __name__ == '__main__':
    unittest.main()
