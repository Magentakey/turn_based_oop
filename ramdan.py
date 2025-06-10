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
            self.run_battle_turn()
            self.check_game_over()
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
      print(f"\n--- Turn {self.turn_number} ---\n")
      self.display_team_status()

      # Giliran Hero
      for hero in self.player_team:
        if not hero.is_alive() or hero.escaped:
          continue

        print(f"\nGiliran {hero.name}")
        print("1. Attack")
        print("2. Use Skill")
        print("3. Use Special Skill")
        print("4. Restore MP")
        print("5. Retreat")

        choice = input("Pilih aksi: ")

        if choice == "1":
          hero.attack(self.boss)

        elif choice == "2":
          if not hero.skills:
            print("Tidak ada skill.")
            continue
          print("Skill:")
          
          for i, skill in enumerate(hero.skills):
            print(f"{i+1}. {skill.name} (MP: {skill.mp_cost})")
          
          idx = int(input("Pilih skill: ")) - 1
          if 0 <= idx < len(hero.skills):
            hero.use_skill(hero.skills[idx], self.boss)

        elif choice == "3":
          hero.use_special_skill(self.boss)

        elif choice == "4":
          hero.restore_mp()

        elif choice == "5":
          hero.retreat()
          print(f"{hero.name} telah retreat!")

      # Giliran Boss
      if self.boss.is_alive():
        self.boss.choose_action([h for h in self.player_team if h.is_alive() and not h.escaped])

    def give_income(self):
      income = 100 * self.turn_number
      for hero in self.player_team:
        hero.gold += income
        print(f"{hero.name} menerima {income} gold. Total: {hero.gold}")

    def shop_phase(self):
        pass

    def check_game_over(self):
      all_escaped_or_dead = all(not hero.is_alive() or hero.escaped for hero in self.player_team)
      boss_dead = not self.boss.is_alive()

      if all_escaped_or_dead:
        print("\nSemua hero telah mati atau retreat. Game Over.")
        self.running = False
      elif boss_dead:
        print("\nBoss telah dikalahkan! Kemenangan!")
        self.running = False

    def display_team_status(self):
      print("\n--- Status Tim ---")
      for hero in self.player_team:
        status = "Escaped" if hero.escaped else ("Alive" if hero.is_alive() else "Dead")
        print(f"{hero.name}: HP {hero.hp}/{hero.max_hp}, MP {hero.mp}/{hero.max_mp}, Gold: {hero.gold}, Status: {status}")
        print(f"  Items: {[item.name for item in hero.equipped_items]}")