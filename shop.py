import random

class Shop:
    def __init__(self, item_pool):
        self.item_pool = item_pool
        self.stock = []

    def refresh_stock(self):
        self.stock = random.sample(self.item_pool, min(10, len(self.item_pool)))

    def display_items(self):
        print("\n=== SHOP STOCK ===")
        for i, item in enumerate(self.stock):
            print(f"{i+1}. {item.name} | ATK: {item.attack_bonus}, DEF: {item.defense_bonus}, HP: {item.health_bonus} | Harga: {item.price} gold")
        print("==================")

    def buy(self, player, item_index):
        if item_index < 0 or item_index >= len(self.stock):
            print("Pilihan tidak valid.")
            return

        item = self.stock[item_index]
        if player.gold < item.price:
            print(f"{player.name} tidak punya cukup gold!")
            return

        if len(player.equipped_items) >= 5:
            print(f"{player.name} tidak bisa membawa lebih dari 5 item!")
            return

        player.gold -= item.price
        player.equip_item(item)
        print(f"{player.name} membeli {item.name}!")
