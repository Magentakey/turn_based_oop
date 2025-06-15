import random

# ==============================
# Base Character Class
# ==============================
class Character:
    def __init__(self, name, max_hp, max_mp, atk, defense):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mp = max_mp
        self.mp = max_mp
        self.atk = atk
        self.defense = defense

    def take_damage(self, amount):
        if amount < 0:  # healing
            heal = -amount
            self.hp = min(self.max_hp, self.hp + heal)
            print(f"{self.name} healed for {heal} HP.")
        else:  # damage
            net = amount - self.defense
            net = net if net > 0 else 1
            self.hp = max(0, self.hp - net)
            print(f"{self.name} took {net} damage.")
        if self.hp == 0:
            print(f"{self.name} has fallen!")

    def restore_mp(self):
        self.mp = self.max_mp
        print(f"{self.name} restores MP to {self.mp}/{self.max_mp}.")

    def is_alive(self):
        return self.hp > 0

    def attack(self, target):
        print(f"{self.name} attacks {target.name} for {self.atk} power.")
        target.take_damage(self.atk)


# ==============================
# Skill & SpecialSkill Classes
# ==============================
class Skill:
    RARITY_WEIGHTS = {
        "common": 45,
        "uncommon": 25,
        "rare": 15,
        "epic": 10,
        "legendary": 5,
    }

    def __init__(self, name, mp_cost, power, type_, rarity, description, target_type):
        self.name = name
        self.mp_cost = mp_cost
        self.power = power
        self.type = type_         # "atk", "healing", "buff", "debuff"
        self.rarity = rarity
        self.description = description
        self.target_type = target_type  # "single", "multi", or "self"

    def use(self, user, targets):
        if user.mp < self.mp_cost:
            print(f"{user.name} does not have enough MP to use {self.name}.")
            return
        user.mp -= self.mp_cost
        print(f"{user.name} uses {self.name} ({self.mp_cost} MP).")
        for tgt in targets:
            if self.type == "atk":
                tgt.take_damage(self.power)
            elif self.type == "healing":
                tgt.take_damage(-self.power)
            elif self.type == "buff":
                amt = self.power if self.power > 0 else int(user.atk * 0.2)
                tgt.atk += amt
                print(f"{tgt.name}'s ATK increased by {amt}.")
            elif self.type == "debuff":
                amt = self.power if self.power > 0 else int(user.atk * 0.2)
                tgt.defense = max(0, tgt.defense - amt)
                print(f"{tgt.name}'s DEF decreased by {amt}.")
        print()

class SpecialSkill(Skill):
    # sama dengan Skill, bisa tambahkan efek khusus di sini
    pass


# ==============================
# Player (Hero) Class
# ==============================
class Player(Character):
    def __init__(self, name, max_hp, max_mp, atk, defense):
        super().__init__(name, max_hp, max_mp, atk, defense)
        self.gold = 0
        self.equipped_items = []
        self.skills = []
        self.special_skill = None
        self.escaped = False

    def use_skill(self, skill, targets):
        skill.use(self, targets)

    def use_special_skill(self, targets):
        if not self.special_skill:
            print(f"{self.name} has no special skill.")
            return
        self.special_skill.use(self, targets)

    def equip_item(self, item):
        if len(self.equipped_items) >= 5:
            print(f"{self.name} cannot equip more than 5 items.")
            return
        self.equipped_items.append(item)
        item.apply_to(self)
        print(f"{self.name} equips {item.name}.")

    def sell_item(self, index):
        if index < 0 or index >= len(self.equipped_items):
            print("Invalid item index.")
            return
        item = self.equipped_items.pop(index)
        item.remove_from(self)
        refund = int(item.price * 0.5)
        self.gold += refund
        print(f"{self.name} sold {item.name} for {refund} gold.")

    def retreat(self):
        self.escaped = True
        self.hp = 0
        print(f"{self.name} has retreated from battle!")


# ==============================
# Enemy (Boss) Class
# ==============================
class Enemy(Character):
    def __init__(self, name, max_hp, max_mp, atk, defense):
        super().__init__(name, max_hp, max_mp, atk, defense)
        self.skills = []
        self.special_skill = None

    def choose_action(self, players):
        if not self.is_alive():
            return
        choice = random.randint(1, 100)
        alive_targets = [p for p in players if p.is_alive()]
        if choice <= 30:
            tgt = random.choice(alive_targets)
            print(f"{self.name} chooses to attack.")
            self.attack(tgt)
        elif choice <= 80:
            skill = random.choice(self.skills)
            print(f"{self.name} tries to use skill {skill.name}.")
            if self.mp >= skill.mp_cost:
                if skill.target_type == "single":
                    skill.use(self, [random.choice(alive_targets)])
                elif skill.target_type == "multi":
                    skill.use(self, alive_targets)
                else:  # self
                    skill.use(self, [self])
            else:
                self.restore_mp()
        else:
            ss = self.special_skill
            print(f"{self.name} tries to use special skill {ss.name}.")
            if self.mp >= ss.mp_cost:
                if ss.target_type == "single":
                    ss.use(self, [random.choice(alive_targets)])
                elif ss.target_type == "multi":
                    ss.use(self, alive_targets)
                else:
                    ss.use(self, [self])
            else:
                self.restore_mp()


# ==============================
# Item Class
# ==============================
class Item:
    def __init__(self, name, description, stat_modifiers, price):
        self.name = name
        self.description = description
        self.stat_modifiers = stat_modifiers
        self.price = price

    def apply_to(self, player):
        for stat, mod in self.stat_modifiers.items():
            if stat == "max_hp":
                player.max_hp += mod
                player.hp = min(player.max_hp, player.hp + mod)
            elif stat == "hp":
                player.hp = min(player.max_hp, player.hp + mod)
            elif stat == "max_mp":
                player.max_mp += mod
                player.mp = min(player.max_mp, player.mp + mod)
            elif stat == "mp":
                player.mp = min(player.max_mp, player.mp + mod)
            elif stat == "atk":
                player.atk += mod
            elif stat == "defense":
                player.defense += mod

    def remove_from(self, player):
        for stat, mod in self.stat_modifiers.items():
            if stat == "max_hp":
                player.max_hp = max(1, player.max_hp - mod)
                player.hp = min(player.hp, player.max_hp)
            elif stat == "hp":
                player.hp = max(0, player.hp - mod)
            elif stat == "max_mp":
                player.max_mp = max(1, player.max_mp - mod)
                player.mp = min(player.mp, player.max_mp)
            elif stat == "mp":
                player.mp = max(0, player.mp - mod)
            elif stat == "atk":
                player.atk = max(0, player.atk - mod)
            elif stat == "defense":
                player.defense = max(0, player.defense - mod)


# ==============================
# Shop Class
# ==============================
class Shop:
    def __init__(self, item_pool, stock=10):
        self.item_pool = item_pool
        self.stock = stock
        self.current_stock = []

    def refresh_stock(self):
        count = min(self.stock, len(self.item_pool))
        self.current_stock = random.sample(self.item_pool, count)
        print(">> Shop stock refreshed.")

    def display_items(self):
        print("Available items:")
        for idx, itm in enumerate(self.current_stock):
            mods = ", ".join(f"{k}{v:+}" for k, v in itm.stat_modifiers.items())
            print(f" [{idx}] {itm.name} - {itm.price} gold ({mods})")

    def buy(self, player, index):
        if index < 0 or index >= len(self.current_stock):
            print("Invalid item choice.")
            return
        item = self.current_stock[index]
        if player.gold < item.price:
            print("Not enough gold!")
            return
        player.gold -= item.price
        player.equip_item(item)
        self.current_stock.pop(index)
        print(f"{player.name} bought {item.name} for {item.price} gold.\n")


# ==============================
# GameManager Class
# ==============================
class GameManager:
    def __init__(self):
        self.hero_skill_pool = []
        self.hero_special_skill_pool = []
        self.boss_skill_pool = []
        self.boss_special_skill_pool = []
        self.item_pool = []
        self.hero_pool = []
        self.player_team = []
        self.boss = None
        self.shop = None
        self.turn_number = 1
        self.running = True

    def init_skills_and_items(self):
        # Hero Skills
        self.hero_skill_pool = [
            Skill("Fireball", 10, 100, "atk",      "common",   "Bola api ke musuh.",             "single"),
            Skill("Heal",     12, -120, "healing","uncommon", "Menyembuhkan satu sekutu.",      "single"),
            Skill("Rally",    20,   0, "buff",    "rare",     "Meningkatkan ATK semua sekutu.", "multi"),
            Skill("Blizzard", 25,  80, "atk",      "epic",     "Serangan es area.",               "multi"),
            Skill("Barrier",  18,   0, "buff",    "uncommon", "Menambah DEF satu sekutu.",       "single"),
        ]
        # Hero Special Skills
        self.hero_special_skill_pool = [
            SpecialSkill("Dragon's Fury", 30, 200, "atk",     "epic",      "Serangan dahsyat ke satu musuh.", "single"),
            SpecialSkill("Phoenix Rise",  35, -200,"healing", "legendary", "Menyembuhkan semua sekutu besar-besaran.", "multi"),
        ]
        # Boss Skills
        self.boss_skill_pool = [
            Skill("Shadow Claw", 15, 150, "atk",   "rare",      "Cakar bayangan ke satu target.", "single"),
            Skill("Dark Shield", 20,   0, "buff",  "uncommon",  "Menambah DEF diri sendiri.",     "self"),
            Skill("Nightmare",   28,  90, "atk",   "epic",      "Serangan kegelapan area.",       "multi"),
        ]
        # Boss Special Skills
        self.boss_special_skill_pool = [
            SpecialSkill("Apocalypse", 40, 250, "atk", "legendary", "Serangan pamungkas area luas.", "multi"),
        ]
        # Items
        self.item_pool = [
            Item("Iron Sword",     "ATK +10",       {"atk": +10},     150),
            Item("Steel Shield",   "DEF +15",       {"defense": +15}, 200),
            Item("Healing Ring",   "HP +50",        {"hp": +50},      120),
            Item("Mana Amulet",    "MP +30",        {"max_mp": +30},  180),
            Item("Boots of Speed", "ATK +5, DEF +5",{"atk": +5, "defense": +5}, 220),
            Item("Titan Armor",    "HP +100, DEF +10",{"max_hp": +100,"defense": +10}, 300),
        ]

    def random_skills(self, amount, pool):
        weights = [Skill.RARITY_WEIGHTS[s.rarity] for s in pool]
        return random.choices(pool, weights=weights, k=amount)

    def random_special_skill(self, pool):
        weights = [Skill.RARITY_WEIGHTS[s.rarity] for s in pool]
        return random.choices(pool, weights=weights, k=1)[0]

    def create_heroes_and_bosses(self):
        names = ["Alya", "Raka", "Sita", "Rian", "Bima", "Nadia", "Dewi", "Jaya"]
        sel = random.sample(names, 5)
        for n in sel:
            h = Player(
                n,
                random.randint(450, 600),   # max_hp
                random.randint(80, 150),    # max_mp
                random.randint(30, 60),     # atk
                random.randint(15, 35)      # defense
            )
            h.skills = self.random_skills(3, self.hero_skill_pool)
            h.special_skill = self.random_special_skill(self.hero_special_skill_pool)
            self.hero_pool.append(h)

        self.boss = Enemy("Malphas the Conqueror", 2000, 250, 80, 60)
        self.boss.skills = self.random_skills(3, self.boss_skill_pool)
        self.boss.special_skill = self.random_special_skill(self.boss_special_skill_pool)

    def choose_heroes(self):
        self.player_team = list(self.hero_pool)

    def distribute_starting_items(self):
        for itm in random.sample(self.item_pool, 3):
            hero = random.choice(self.player_team)
            hero.equip_item(itm)

    def give_income(self):
        income = self.turn_number * 100
        print(f">> Turn {self.turn_number}: each hero gains {income} gold.")
        for h in self.player_team:
            if h.is_alive():
                h.gold += income
        print()

    def shop_phase(self):
        print(f"--- Shop Phase (Turn {self.turn_number}) ---")
        self.shop.refresh_stock()
        for h in self.player_team:
            if not h.is_alive():
                continue
            print(f"{h.name}: {h.gold} gold.")
            self.shop.display_items()
            buy = input(f"{h.name}, buy? (y/n) ").lower()
            if buy == "y":
                try:
                    idx = int(input("Choose item index: "))
                    self.shop.buy(h, idx)
                except:
                    print("Invalid input.")
        print()

    def run_battle_turn(self):
        print(f"=== Battle Turn {self.turn_number} ===")
        self.display_team_status()

        # Hero turns
        for h in self.player_team:
            if not h.is_alive():
                continue
            print(f"-- {h.name}'s turn --")
            print("1) Attack  2) Skill  3) Special  4) Restore MP  5) Retreat")
            cmd = input("Choose: ")
            if cmd == "1":
                h.attack(self.boss)
            elif cmd == "2":
                for i, sk in enumerate(h.skills):
                    print(f"[{i}] {sk.name} ({sk.mp_cost} MP)")
                idx = int(input("Skill index: "))
                sk = h.skills[idx]
                if sk.target_type == "single":
                    h.use_skill(sk, [self.boss])
                else:
                    h.use_skill(sk, [x for x in self.player_team if x.is_alive()])
            elif cmd == "3":
                ss = h.special_skill
                if ss.target_type == "single":
                    h.use_special_skill([self.boss])
                else:
                    h.use_special_skill([x for x in self.player_team if x.is_alive()])
            elif cmd == "4":
                h.restore_mp()
            elif cmd == "5":
                h.retreat()
            else:
                print("Invalid command.")

            if not self.boss.is_alive():
                break

        # Boss turn
        if self.boss.is_alive():
            print(f"-- {self.boss.name}'s turn --")
            self.boss.choose_action(self.player_team)

        print()
        self.display_team_status()
        print()

    def check_game_over(self):
        if not self.boss.is_alive():
            print(">>> Victory! Boss defeated.")
            self.running = False
        elif all(not h.is_alive() for h in self.player_team):
            print(">>> Game Over. All heroes have fallen.")
            self.running = False

    def display_team_status(self):
        print(f"{self.boss.name}: HP {self.boss.hp}/{self.boss.max_hp} | MP {self.boss.mp}/{self.boss.max_mp}")
        for h in self.player_team:
            status = "Alive" if h.is_alive() else "Dead"
            print(f"{h.name}: HP {h.hp}/{h.max_hp} | MP {h.mp}/{h.max_mp} | Gold {h.gold} | {status}")
        print()

    def start_game(self):
        self.init_skills_and_items()
        self.create_heroes_and_bosses()
        self.choose_heroes()
        self.shop = Shop(self.item_pool)
        self.shop.refresh_stock()
        self.distribute_starting_items()

        while self.running:
            self.run_battle_turn()
            self.check_game_over()
            if not self.running:
                break
            self.turn_number += 1
            self.give_income()
            self.shop_phase()


if __name__ == "__main__":
    gm = GameManager()
    gm.start_game()
