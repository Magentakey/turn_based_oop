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
        pass

    def restore_mp(self):
        pass
    
    def is_alive(self):
        pass

# ==============================
# Skill dan Special Skill
# ==============================
class Skill:
    def __init__(self, name, mp_cost, power, type, rarity, description, target_type): #target_type ("single" / "multi")
        self.name = name
        self.mp_cost = mp_cost
        self.power = power
        self.type = type
        self.rarity = rarity
        self.description = description
        self.target_type = target_type

    def use(self, user, targets):
        pass

    def random_skills(self, amount):
        pass
    
    def random_special_skill(self, pool):
        pass


class SpecialSkill(Skill):
    def use(self, user, targets):
        pass

# ==============================
# Player Class (Hero Template)
# ==============================
class Player(Character):
    def __init__(self, name, max_hp, max_mp, atk, defense):
        super().__init__(name, max_hp, max_mp, atk, defense)
        self.gold = 0
        self.equipped_items = []  # Maks 5 item
        self.skills = []
        self.special_skill = None
        self.escaped = False  # Menandakan jika hero kabur (mati)

    def attack(self, target):
        pass

    def use_skill(self, skill, target):
        pass

    def use_special_skill(self, target):
        pass

    def equip_item(self, item):
        pass

    def sell_item(self, index):
        pass

    def retreat(self):
        self.escaped = True
        self.hp = 0

# ==============================
# Enemy (Boss Template)
# ==============================
class Enemy(Character):
    def __init__(self, name, max_hp, max_mp, atk, defense):
        super().__init__(name, max_hp, max_mp, atk, defense)
        self.skills = []
        self.special_skill = None

    def choose_action(self, players):
        pass

# ==============================
# Item Class
# ==============================
class Item:
    def __init__(self, name, description, stat_modifiers, price): # stat_modifiers(dict: {"atk": +5, "hp": -10})
        self.name = name
        self.description = description
        self.stat_modifiers = stat_modifiers
        self.price = price

    def apply_to(self, player):
        pass
    
    def remove_from(self, player):
        pass

# ==============================
# Shop Class
# ==============================
class Shop:
    def __init__(self, item_pool, stock):
        self.item_pool = item_pool
        self.current_stock = []

    def refresh_stock(self):
        pass

    def display_items(self):
        pass

    def buy(self, player, item):
        pass

# ==============================
# GameManager Class
# ==============================
class GameManager:
    def __init__(self):
        self.skill_pool = []
        self.special_skill_pool = []
        self.item_pool = []
        self.hero_pool = []
        self.player_team = []
        self.boss = None
        self.shop = None
        self.turn_number = 1
        self.running = True

    def start_game(self):
        self.init_skills_and_items()
        self.create_heroes_and_bosses()
        self.choose_heroes()
        self.create_shop()
        self.distribute_starting_items()
        self.run_battle_turn()
        self.turn_number += 1

        while self.running:
            self.give_income()
            self.shop_phase()
            self.check_game_over()
            self.run_battle_turn()
            self.turn_number += 1

    def init_skills_and_items(self):
        # Skill Pool khusus Hero
        self.hero_skill_pool = [
            Skill("Fireball", 10, 100, "atk", "common", "Menembakkan bola api.", "single"),
            Skill("Heal", 15, -100, "healing", "common", "Menyembuhkan sekutu.", "single"),
            Skill("Slash", 5, 80, "atk", "common", "Serangan tebasan cepat.", "single"),
            Skill("Multi Heal", 20, -80, "healing", "uncommon", "Menyembuhkan semua sekutu.", "multi"),
            Skill("Thunder", 12, 90, "atk", "uncommon", "Serangan petir ke satu musuh.", "single"),
            Skill("War Cry", 10, 0, "buff", "rare", "Meningkatkan atk semua sekutu.", "multi"),
        ]

        # Skill Pool khusus Boss (tidak ada yang sama)
        self.boss_skill_pool = [
            Skill("Shadow Spike", 15, 110, "atk", "common", "Serangan bayangan menusuk.", "single"),
            Skill("Dark Heal", 20, -100, "healing", "common", "Menyembuhkan diri sendiri.", "single"),
            Skill("Corrupt Slash", 10, 85, "atk", "uncommon", "Serangan kegelapan.", "single"),
            Skill("Plague Burst", 25, 90, "atk", "rare", "Ledakan racun untuk semua.", "multi"),
            Skill("Doom Chant", 20, 0, "buff", "epic", "Meningkatkan atk dan def musuh.", "multi"),
        ]

        # Special Skill Pool khusus Hero
        self.hero_special_skill_pool = [
            SpecialSkill("Berserk", 25, 200, "atk", "epic", "Serangan brutal, risiko damage balik.", "single"),
            SpecialSkill("Divine Light", 30, -200, "healing", "legendary", "Menyembuhkan semua sekutu.", "multi"),
            SpecialSkill("Overcharge", 20, 0, "buff", "rare", "Meningkatkan MP dan serangan.", "multi"),
        ]

        # Special Skill Pool khusus Boss
        self.boss_special_skill_pool = [
            SpecialSkill("Void Collapse", 35, 220, "atk", "legendary", "Serangan besar dari dimensi gelap.", "multi"),
            SpecialSkill("Soul Drain", 30, 150, "atk", "epic", "Menguras HP dan menambah ke boss.", "single"),
            SpecialSkill("Hellfire Rain", 40, 180, "atk", "legendary", "Serangan api ke seluruh musuh.", "multi"),
        ]

        # Item Pool (bisa untuk hero saja)
        self.item_pool = [
            Item("Iron Sword", "Pedang besi biasa.", {"atk": 10}, 100),
            Item("Steel Armor", "Armor pelindung standar.", {"defense": 15}, 120),
            Item("HP Ring", "Cincin penambah HP.", {"max_hp": 100}, 150),
            Item("Mana Pendant", "Liontin penyimpan mana.", {"max_mp": 50}, 90),
            Item("Cursed Amulet", "Amulet terkutuk menambah atk tapi mengurangi def.", {"atk": 20, "defense": -10}, 50),
            Item("Holy Charm", "Pesona suci yang meningkatkan pertahanan.", {"defense": 25}, 80),
        ]

    def create_heroes_and_bosses(self):
        hero_names = ["Asep", "Lina", "Budi", "Tari", "Riko", "Joko", "Nina", "Dewi"]
        selected_names = random.sample(hero_names, 5)

        for name in selected_names:
            #random stats
            hero = Player(
                name,
                random.randint(400, 600),
                random.randint(80, 150),
                random.randint(35, 60),
                random.randint(20, 40)
            )
            hero.skills = self.random_skills(3, self.hero_skill_pool)
            hero.special_skill = self.random_special_skill(self.hero_special_skill_pool)
            self.hero_pool.append(hero)

        # Buat boss
        boss = Enemy("Lord Malgrim", 1500, 200, 70, 50)
        boss.skills = self.random_skills(3, self.boss_skill_pool)
        boss.special_skill = self.random_special_skill(self.boss_special_skill_pool)
        self.boss = boss

    def choose_heroes(self):
        pass

    def create_shop(self):
        self.shop = Shop(self.item_pool)
        self.shop.refresh_stock()

    def distribute_starting_items(self):
        pass

    def run_battle_turn(self):
        pass

    def give_income(self):
        pass

    def shop_phase(self):
        print("\n--- SHOP PHASE ---")
        self.shop.refresh_stock()

        for player in self.player_team:
            while True:
                print(f"\n{player.name} - Gold: {player.gold}")
                self.shop.display_items()
                choice = input("Pilih item yang ingin dibeli (1-10, atau 0 untuk skip): ")

                if not choice.isdigit():
                    print("Input tidak valid.")
                    continue

                choice = int(choice)
                if choice == 0:
                    break

                self.shop.buy(player, choice - 1)

                lanjut = input("Beli item lagi? (y/n): ").lower()
                if lanjut != 'y':
                    break

    def check_game_over(self):
        pass

    def display_team_status(self):
        pass
