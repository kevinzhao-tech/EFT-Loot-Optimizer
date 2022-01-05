class Item:
    def __init__(self, name, uid, price, inventory_position, slots):
        self.name = name
        self.uid = uid
        self.price = price
        self.slots = slots
        self.inventory_position = inventory_position
        self.pps = price / slots

    def get_pps(self):
        return self.pps
