import numpy as np
import cv2
import os


class TemplateMatcher(object):
    def __init__(self, path, threshold=0.70, scale=1.0):
        # templates is a dictionary of template names, extensions removed, and their corresponding images as np.array
        self.threshold = threshold
        self.templates: dict = _load_images(path)
        self.scale = scale
        self.templates_gray: dict = _templates_to_gray(self.templates, scale=self.scale)

        print("Loaded {} templates".format(len(self.templates)))

    def list_templates(self):
        return list(self.templates.keys())

    def match_template(self, image: np.array, template_name: str, template_gray: dict):
        """

        Args:
            image: an np.array of the image to match templates to
            template_name: the name of the template to match
            template_gray: a dict of template names and their corresponding grayscale images as np.arrays

        Returns:
            the top left and bottom right coordinates of the matched template

        """

        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        (tW, tH) = self.templates_gray[template_name].shape[::-1]
        # cv2.imshow("Template", self.templates_gray[template_name])
        # cv2.waitKey(0)
        result = cv2.matchTemplate(image, template_gray[template_name], cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val < self.threshold:
            return None

        top_left = max_loc
        bottom_right = (top_left[0] + tW, top_left[1] + tH)

        return top_left, bottom_right

    def match(self, image: np.array):
        """
        Given an image, match all templates and return their names and UIDs
        Args:
            image: an np.array of the image to match templates to
        """

        results = {}
        for template in self.templates_gray:
            result = self.match_template(image, template, self.templates_gray)
            if result is not None:
                cv2.rectangle(image, result[0], result[1], (0, 255, 0), 2)
                cv2.imshow("Matched", image)

        cv2.waitKey(0)


def _load_images(path):
    """
    Load all images from a directory

    Args:
        path: path to directory containing images
    """
    templates = {}
    for filename in os.listdir(path):
        image_as_array = cv2.imread(os.path.join(path, filename))
        if filename.endswith('.png'):
            filename = filename[:-4]
        templates[filename] = image_as_array
    return templates


def _templates_to_gray(templates, scale=1.0):
    """
    Convert all templates to grayscale

    Args:
        templates: dictionary of template names and images as np.array
        scale: scale factor to resize templates
    """

    templates_gray = {}
    for filename in templates:
        grayscale = cv2.cvtColor(templates[filename], cv2.COLOR_BGR2GRAY)

        templates_gray[filename] = cv2.resize(grayscale, None, fx=scale, fy=scale)
    return templates_gray
