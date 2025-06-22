class Item:
    def __init__(self, name, slot, modifiers, price, tier=1):
        self.name = name
        self.slot = slot            # "weapon", "armor", "accessory"
        self.modifiers = modifiers  # dict, ex: {"atk": 10}
        self.price = price
        self.tier = tier


ITEMS = [
    Item("Short Sword", "weapon", {"atk": 8}, price=50, tier=1),
    Item("Long Bow", "weapon", {"atk": 6, "agi": 3}, price=65, tier=1),
    Item("Mage Staff", "weapon", {"int": 10}, price=70, tier=1),
    Item("Steel Armor", "armor", {"def": 12}, price=60, tier=1),
    Item("Vital Ring", "accessory", {"hp": 50}, price=50, tier=1),

    Item("Enchanted Sword", "weapon", {"atk": 18, "agi": 5}, price=120, tier=2),
    Item("Battle Robe", "armor", {"def": 8, "int": 12}, price=110, tier=2),
    Item("Power Amulet", "accessory", {"str": 6, "hp": 30}, price=100, tier=2),

    Item("Mythic Halberd", "weapon", {"atk": 35}, price=200, tier=3),
    Item("Dragon Plate", "armor", {"def": 30, "hp": 100}, price=220, tier=3),
    Item("Archangel's Charm", "accessory", {"int": 20, "agi": 10}, price=210, tier=3),
]
