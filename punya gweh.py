import random

# Character, Player, Enemy Class #

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
        damage_taken = max(0, amount - self.defense)
        self.hp -= damage_taken
        print(f"{self.name} menerima {damage_taken} damage.")
        if self.hp <= 0:
            self.hp = 0
            print(f"{self.name} telah gugur.")

    def restore_mp(self):
        restore_amount = int(self.max_mp * 0.3)
        self.mp = min(self.max_mp, self.mp + restore_amount)
        print(f"{self.name} memulihkan {restore_amount} MP.")

    def is_alive(self):
        return self.hp > 0

class Player(Character):
    def __init__(self, name, max_hp, max_mp, atk, defense):
        super().__init__(name, max_hp, max_mp, atk, defense)
        self.gold = 0
        self.equipped_items = []    # Maksimal 5 item
        self.skills = []            # List[Skill]
        self.special_skill = None   # SpecialSkill
        self.escaped = False        # Retreat flag

    def attack(self, target):
        if self.is_alive() and not self.escaped:
            print(f"{self.name} menyerang {target.name}!")
            target.take_damage(self.atk)

    def use_skill(self, skill, targets):
        if skill in self.skills:
            skill.use(self, targets)
        else:
            print(f"{self.name} tidak memiliki skill itu!")

    def use_special_skill(self, targets):
        if self.special_skill:
            self.special_skill.use(self, targets)
        else:
            print(f"{self.name} tidak memiliki special skill!")

    def equip_item(self, item):
        if len(self.equipped_items) >= 5:
            print(f"{self.name} tidak bisa membawa lebih dari 5 item!")
            return
        item.apply_to(self)
        self.equipped_items.append(item)
        print(f"{self.name} melengkapi item {item.name}.")

    def sell_item(self, index):
        if 0 <= index < len(self.equipped_items):
            item = self.equipped_items.pop(index)
            item.remove_from(self)
            self.gold += item.price // 2
            print(f"{self.name} menjual {item.name} seharga {item.price // 2} gold.")

    def retreat(self):
        self.escaped = True
        self.hp = 0
        print(f"{self.name} retreat dan dianggap gugur.")

class Enemy(Character):
    def __init__(self, name, max_hp, max_mp, atk, defense):
        super().__init__(name, max_hp, max_mp, atk, defense)
        self.skills = []            # List[Skill]
        self.special_skill = None   # SpecialSkill

    def attack(self, target):
        print(f"{self.name} menyerang {target.name}!")
        target.take_damage(self.atk)

    def choose_action(self, players):
        living = [p for p in players if p.is_alive() and not p.escaped]
        if not living:
            return

        roll = random.randint(1, 100)
        if self.mp < 10:
            self.restore_mp()
            return

        if roll <= 30:
            # Serang biasa
            target = random.choice(living)
            self.attack(target)

        elif roll <= 80:
            # Gunakan skill biasa
            sk = random.choice(self.skills)
            if sk.target_type == "single":
                targets = [random.choice(living)]
            else:
                targets = living
            print(f"{self.name} menggunakan skill {sk.name}!")
            sk.use(self, targets)

        else:
            # Gunakan special skill
            if self.special_skill:
                if self.special_skill.target_type == "single":
                    targets = [random.choice(living)]
                else:
                    targets = living
                print(f"{self.name} menggunakan SPECIAL SKILL {self.special_skill.name}!")
                self.special_skill.use(self, targets)

#  Skill & SpecialSkill    #

class Skill:
    def __init__(self, name, mp_cost, power, type, rarity, description, target_type):
        self.name = name
        self.mp_cost = mp_cost
        self.power = power
        self.type = type              # "atk","healing","buff","debuff"
        self.rarity = rarity          # "common","uncommon","rare","epic","legendary"
        self.description = description
        self.target_type = target_type# "single"/"multi"

    def use(self, user, targets):
        if user.mp < self.mp_cost:
            print(f"{user.name} tidak cukup MP untuk {self.name}!")
            return
        user.mp -= self.mp_cost

        # Bungkus single target
        if not isinstance(targets, list):
            targets = [targets]

        for t in targets:
            if self.type == "atk":
                print(f"{user.name} menyerang {t.name} dengan {self.name}.")
                t.take_damage(self.power)
            elif self.type == "healing":
                heal = abs(self.power)
                t.hp = min(t.max_hp, t.hp + heal)
                print(f"{user.name} menyembuhkan {t.name} +{heal} HP.")
            elif self.type == "buff":
                t.atk += 10; t.defense += 5
                print(f"{user.name} memberi buff ke {t.name}.")
            elif self.type == "debuff":
                t.atk = max(0, t.atk - 10)
                t.defense = max(0, t.defense - 5)
                print(f"{user.name} melemahkan {t.name}.")

class SpecialSkill(Skill):
    def use(self, user, targets):
        print(f"{user.name} mengaktifkan SPECIAL SKILL {self.name}!")
        super().use(user, targets)

def random_skills(n, pool):
    rar = ["common"]*45 + ["uncommon"]*25 + ["rare"]*15 + ["epic"]*10 + ["legendary"]*5
    sel = []
    while len(sel) < n:
        r = random.choice(rar)
        c = [s for s in pool if s.rarity == r]
        if c:
            sel.append(random.choice(c))
    return sel

def random_special_skill(pool):
    rar = ["common"]*45 + ["uncommon"]*25 + ["rare"]*15 + ["epic"]*10 + ["legendary"]*5
    while True:
        r = random.choice(rar)
        c = [s for s in pool if s.rarity == r]
        if c:
            return random.choice(c)

#  Item System   #

class Item:
    def __init__(self, name, description, stat_modifiers, price):
        self.name = name
        self.description = description
        self.stat_modifiers = stat_modifiers
        self.price = price

    def apply_to(self, player):
        for k, v in self.stat_modifiers.items():
            if hasattr(player, k):
                setattr(player, k, getattr(player, k) + v)

    def remove_from(self, player):
        for k, v in self.stat_modifiers.items():
            if hasattr(player, k):
                setattr(player, k, getattr(player, k) - v)

#  Shop System   #

class Shop:
    def __init__(self, item_pool):
        self.item_pool = item_pool
        self.current_stock = []

    def refresh_stock(self):
        self.current_stock = random.sample(self.item_pool, min(10, len(self.item_pool)))

    def display_items(self):
        print("\n🛒 Toko menjual:")
        for i, itm in enumerate(self.current_stock, start=1):
            print(f"{i}. {itm.name} - {itm.price} gold - {itm.stat_modifiers}")

    def buy(self, player, index):
        if index < 0 or index >= len(self.current_stock):
            print("Pilihan invalid.")
            return
        itm = self.current_stock[index]
        if player.gold < itm.price:
            print("Gold tidak cukup.")
            return
        if len(player.equipped_items) >= 5:
            print("Inventory penuh.")
            return
        player.gold -= itm.price
        player.equip_item(itm)
        print(f"{player.name} membeli {itm.name} seharga {itm.price} gold.")

#  GameManager Full   #

class GameManager:
    def __init__(self):
        self.hero_pool = []
        self.player_team = []
        self.boss = None
        self.shop = None
        self.turn_number = 1
        self.running = True

    def init_skills_and_items(self):
        # Skill Hero
        self.hero_skill_pool = [
            Skill("Fireball", 10, 100, "atk", "common", "Bola api", "single"),
            Skill("Heal", 15, -100, "healing", "common", "Penyembuh", "single"),
            Skill("Slash", 5, 80, "atk", "common", "Tebas", "single"),
        ]
        self.hero_special_skill_pool = [
            SpecialSkill("Divine Light", 30, -200, "healing", "legendary", "Heal massal", "multi")
        ]
        # Skill Boss
        self.boss_skill_pool = [
            Skill("Corrupt Slash", 15, 120, "atk", "rare", "Serang kegelapan", "single")
        ]
        self.boss_special_skill_pool = [
            SpecialSkill("Void Collapse", 40, 220, "atk", "legendary", "Ledakan dimensi", "multi")
        ]
        # Items
        self.item_pool = [
            Item("Iron Sword", "Pedang besi", {"atk": 10}, 100),
            Item("Steel Armor", "Armor baja", {"defense": 15}, 120),
        ]

    def create_heroes_and_bosses(self):
        names = ["Asep", "Lina", "Budi", "Tari", "Riko"]
        for nm in names:
            h = Player(nm, 500, 100, 50, 20)
            h.skills = random_skills(2, self.hero_skill_pool)
            h.special_skill = random_special_skill(self.hero_special_skill_pool)
            self.hero_pool.append(h)
        self.boss = Enemy("Lord Malgrim", 1500, 200, 70, 50)
        self.boss.skills = random_skills(1, self.boss_skill_pool)
        self.boss.special_skill = random_special_skill(self.boss_special_skill_pool)

    def choose_heroes(self):
        print("\n🔍 Memilih 5 hero pertama:")
        self.player_team = self.hero_pool[:5]
        for h in self.player_team:
            print(f"- {h.name}")

    def distribute_starting_items(self):
        print("\n🎁 Memberi 3 item awal:")
        for _ in range(3):
            h = random.choice(self.player_team)
            itm = random.choice(self.item_pool)
            if len(h.equipped_items) < 5:
                h.equip_item(itm)

    def run_battle_turn(self):
        print(f"\n===== TURN {self.turn_number} =====")
        # Hero phase
        for h in self.player_team:
            if h.is_alive() and not h.escaped:
                h.attack(self.boss)
        # Boss phase
        if self.boss.is_alive():
            self.boss.choose_action(self.player_team)
        self.display_team_status()

    def give_income(self):
        for h in self.player_team:
            h.gold += self.turn_number * 100

    def check_game_over(self):
        if not self.boss.is_alive():
            print("\n🎉 Kamu menang!")
            self.running = False
        elif all(not h.is_alive() or h.escaped for h in self.player_team):
            print("\n💀 Semua hero kalah.")
            self.running = False

    def display_team_status(self):
        print("\n📊 STATUS TIM:")
        for h in self.player_team:
            status = "Hidup" if h.is_alive() else "KO"
            if h.escaped:
                status = "Retreat"
            print(f"{h.name}: HP {h.hp}/{h.max_hp} | MP {h.mp}/{h.max_mp} | Gold {h.gold} | {status}")
        print(f"Boss {self.boss.name}: HP {self.boss.hp}/{self.boss.max_hp} | MP {self.boss.mp}/{self.boss.max_mp}")

    def start_game(self):
        self.init_skills_and_items()
        self.create_heroes_and_bosses()
        self.choose_heroes()
        self.shop = Shop(self.item_pool)
        self.shop.refresh_stock()
        self.distribute_starting_items()

        # Turn pertama
        self.run_battle_turn()

        # Loop berikutnya
        while self.running:
            self.give_income()
            self.shop.refresh_stock()
            self.shop.display_items()
            for h in self.player_team:
                choice = input(f"{h.name} mau beli? (y/n): ").lower()
                if choice == 'y':
                    try:
                        idx = int(input("Pilih nomor item: ")) - 1
                        self.shop.buy(h, idx)
                    except:
                        print("Input invalid.")
            self.run_battle_turn()
            self.check_game_over()
            self.turn_number += 1

if __name__ == "__main__":
    gm = GameManager()
    gm.start_game()
