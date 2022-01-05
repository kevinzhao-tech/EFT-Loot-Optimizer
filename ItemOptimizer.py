from Item import Item
from PIL import Image
import pytesseract
import ScreenScraper

class ItemOptimizer:
    def __init__(self):
        self.inventory = []
        self.ground_items = []
    def optimize(self):

    def read_inventory(self):
        """ Reads the loot from the screen and adds it to the inventory """
        inventory_as_string = ScreenScraper.get_inventory()

    def add_item(self, item: Item):
        if self.inventory.len == 0:
            self.inventory.extend(item)
        else:
            for i in range(self.inventory.len):
                if self.inventory[i].get_pps() >= item.get_pps():
                    self.inventory.insert(i, item)

    def remove_item(self, item):
        self.inventory.remove(item)

    def list_inventory(self):
        """
        Returns the list of inventory items in ascending order of PPS
        Returns: a list of Item objects
        """
        return self.inventory.copy()


