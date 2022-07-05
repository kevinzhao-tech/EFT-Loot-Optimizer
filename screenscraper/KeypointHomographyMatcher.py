import cv2
import numpy as np

class KeypointHomographyMatcher:
    """
    Args:
        path: path to images to be matched
    """
    def __init__(self, object, path) -> None:
        self.object = object
        self.path = path

    def _load_images(self, path):
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