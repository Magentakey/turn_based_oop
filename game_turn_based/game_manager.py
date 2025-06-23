import random

# ==============================
# Base Character Class
# ==============================
class Character:
    def __init__(self, name, max_hp, max_mp, atk, defense, hero_class=None):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mp = max_mp
        self.mp = max_mp
        self.atk = atk
        self.defense = defense
        self.hero_class = hero_class  # ditambahkan atribut class
        self.type = None  # akan diisi dari rarity special skill

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
# Skill dan Special Skill
# ==============================
class Skill:
    def __init__(self, name, mp_cost, power, type, rarity, description, target_type):
        self.name = name
        self.mp_cost = mp_cost
        self.power = power
        self.type = type
        self.rarity = rarity
        self.description = description
        self.target_type = target_type

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
# Player Class (Hero Template)
# ==============================
class Player(Character):
    def __init__(self, name, max_hp, max_mp, atk, defense, hero_class=None):
        super().__init__(name, max_hp, max_mp, atk, defense, hero_class)
        self.gold = 0
        self.equipped_items = []
        self.skills = []
        self.special_skill = None
        self.escaped = False

    def attack_target(self, target):
        print(f"{self.name} uses basic attack on {target.name}")
        self.attack(target)

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

    def sell_item(self, index, shop=None):
        if index < 0 or index >= len(self.equipped_items):
            print("Invalid item index.")
            return
        item = self.equipped_items.pop(index)
        item.remove_from(self)
        refund = int(item.price * 0.5)
        self.gold += refund
        print(f"{self.name} sold {item.name} for {refund} gold.")

        if shop:
            shop.current_stock.append(item)
            
    def retreat(self):
        self.escaped = True
        self.hp = 0
        print(f"{self.name} has retreated from battle!")

# ==============================
# Enemy (Boss Template)
# ==============================
class Enemy(Character):
    def __init__(self, name, max_hp, max_mp, atk, defense, boss_class="Unknown"):
        super().__init__(name, max_hp, max_mp, atk, defense, hero_class=boss_class)
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
    def __init__(self, name, rarity, description, stat_modifiers, price):
        self.name = name
        self.rarity = rarity
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
    def __init__(self, item_pool):
        self.item_pool = item_pool
        self.current_stock = []

    def refresh_stock(self):
        # Ambil 9 item acak dari item_pool
        if len(self.item_pool) >= 9:
            self.current_stock = random.sample(self.item_pool, 9)
        else:
            self.current_stock = self.item_pool[:]

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
        
    def sell(self, player, item):
        if item not in player.equipped_items:
            print("Item not equipped by player.")
            return
        index = player.equipped_items.index(item)
        player.sell_item(index, self)



# ==============================
# GameManager Class
# ==============================
class GameManager:
    def __init__(self):
        self.skill_pool = []
        self.special_skill_pool = []
        self.item_pool = []
        self.hero_pool = []
        self.mobs_pool = []
        self.player_team = []
        self.boss = None
        self.shop = None
        # self.turn_number = 0
        self.round_number = 0  # satu putaran semua hero + boss
        # self.round_sequence = ["mobs", "mobs", "shop", "mobs", "boss"]
        self.round_sequence = ["mobs", "mobs", "shop", "mobs", "boss"]
        self.current_round_index = 0
        self.phase_round = self.round_sequence[self.current_round_index]
        self.running = True
        
    def new_round(self):
        self.round_number = 0
        return self.round_number
    def next_round(self):
        self.round_number += 1
        return self.round_number

    # def start_game(self):
    #     self.init_skills_and_items()
    #     self.create_heroes_and_bosses()
    #     self.choose_heroes()
    #     self.create_shop()
    #     self.distribute_starting_items()
    #     self.run_battle_turn()
    #     self.turn_number += 1

    #     while self.running:
    #         self.give_income()
    #         self.shop_phase()
    #         self.run_battle_turn()
    #         self.check_game_over()
    #         self.turn_number += 1

    def init_skills_and_items(self):
        self.hero_skill_pool = [
            Skill("Heal", 15, 100, "healing", "common", "Menyembuhkan sekutu.", "single"),
            Skill("Multi Heal", 20, 80, "healing", "uncommon", "Menyembuhkan semua sekutu.", "multi"),
            Skill("Thunder", 12, 90, "atk", "uncommon", "Serangan petir ke satu musuh.", "single"),
            Skill("War Cry", 10, 0, "buff", "rare", "Meningkatkan atk semua sekutu.", "multi"),
            Skill("Cry Cry", 10, 0, "debuff", "legendary", "Menurunkan defense semua musuh.", "multi"),

            # 🔥 Serangan
            Skill("Flame Strike", 8, 70, "atk", "common", "Serangan api cepat ke musuh.", "single"),
            Skill("Arrow Rain", 15, 60, "atk", "uncommon", "Hujan panah ke semua musuh.", "multi"),
            Skill("Smite", 18, 120, "atk", "rare", "Serangan suci ke satu target.", "single"),
            Skill("Nova Blast", 25, 100, "atk", "epic", "Ledakan energi ke semua musuh.", "multi"),

            # 💚 Penyembuhan
            Skill("Rejuvenate", 12, 80, "healing", "common", "Memulihkan satu sekutu.", "single"),
            Skill("Divine Light", 25, 120, "healing", "legendary", "Sinar penyembuh semua sekutu.", "multi"),

            # 🛡️ Buff
            Skill("Iron Skin", 10, 0, "buff", "uncommon", "Meningkatkan pertahanan satu sekutu.", "single"),
            Skill("Battle Shout", 14, 0, "buff", "rare", "Meningkatkan atk semua sekutu.", "multi"),
            Skill("Focus Mind", 12, 0, "buff", "uncommon", "Meningkatkan MP recovery diri.", "single"),

            # 💀 Debuff
            Skill("Weaken", 10, 0, "debuff", "uncommon", "Menurunkan atk musuh.", "single"),
            Skill("Corrupt Aura", 18, 0, "debuff", "rare", "Mengurangi atk & def semua musuh.", "multi"),
            # Skill("Piercing Shot", 10, 50, "atk", "uncommon", "Serangan menembus def musuh.", "single"),
            Skill("Dizzy Spell", 10, 0, "debuff", "rare", "Mengurangi akurasi semua musuh.", "multi"),
        ]

        self.mobs_skill_pool = [
            Skill("Claw", 5, 90, "atk", "common", "Serangan cakaran ke satu target.", "single"),
            Skill("Bite", 6, 85, "atk", "common", "Gigitan cepat ke musuh.", "single"),
            Skill("Scratch", 4, 95, "atk", "common", "Serangan cakaran ringan.", "single"),
            Skill("Growl", 5, 100, "debuff", "common", "Mengurangi atk semua musuh.", "multi"),
            Skill("Headbutt", 7, 80, "atk", "common", "Serangan kepala yang bisa membuat musuh pusing.", "single"),
            Skill("Poison Fang", 8, 80, "debuff", "uncommon", "Menggigit dan meracuni target.", "single"),
            Skill("Howl", 10, 0, "buff", "uncommon", "Meningkatkan atk semua sekutu.", "multi"),
            Skill("Frenzy", 12, 100, "atk", "uncommon", "Serangan brutal bertubi-tubi.", "single"),
            Skill("Ambush", 10, 90, "atk", "uncommon", "Serangan mendadak dari bayangan.", "single"),
            Skill("Tail Whip", 8, 100, "debuff", "uncommon", "Mengurangi defense musuh.", "single"),
            Skill("Shadow Claw", 15, 95, "atk", "rare", "Serangan gelap yang menakutkan.", "single"),
            Skill("Bloodlust", 12, 0, "buff", "rare", "Meningkatkan atk dan kecepatan pengguna.", "single"),
            Skill("Terror Roar", 10, 100, "debuff", "rare", "Mengurangi defense semua musuh.", "multi"),
            Skill("Rage Slash", 20, 100, "atk", "rare", "Tebasan kuat penuh amarah.", "single"),
            Skill("Dark Pulse", 18, 110, "atk", "rare", "Ledakan energi kegelapan yang kuat.", "multi")
        ]

        self.boss_skill_pool = [
            Skill("Shadow Spike", 15, 110, "atk", "common", "Serangan bayangan menusuk.", "single"),
            Skill("Dark Heal", 20, 100, "healing", "common", "Menyembuhkan diri sendiri.", "single"),
            Skill("Corrupt Slash", 10, 85, "atk", "uncommon", "Serangan kegelapan.", "single"),
            Skill("Plague Burst", 25, 90, "atk", "rare", "Ledakan racun untuk semua.", "multi"),
            Skill("Doom Chant", 20, 0, "buff", "epic", "Meningkatkan atk dan def musuh.", "multi"),
        ]

        self.hero_special_skill_pool = [
            SpecialSkill("Berserk", 25, 200, "atk", "common", "Serangan brutal, risiko damage balik.", "single"),
            SpecialSkill("Berserk", 25, 200, "atk", "uncommon", "Serangan brutal, risiko damage balik.", "single"),
            SpecialSkill("Special Cry", 25, 0, "debuff", "epic", "Teriakan yang melemahkan semua musuh.", "multi"),
            SpecialSkill("Divine Light", 30, 200, "healing", "legendary", "Menyembuhkan semua sekutu.", "multi"),
            SpecialSkill("Overcharge", 20, 0, "buff", "rare", "Meningkatkan MP dan serangan.", "multi"),

            # 🔥 Serangan
            SpecialSkill("Inferno Blade", 35, 250, "atk", "epic", "Serangan api yang membakar satu musuh.", "single"),
            SpecialSkill("Thunderstorm", 40, 200, "atk", "epic", "Petir menyambar semua musuh.", "multi"),
            SpecialSkill("Soul Breaker", 30, 220, "atk", "legendary", "Serangan sihir penghancur jiwa.", "single"),
            SpecialSkill("Celestial Wrath", 50, 260, "atk", "legendary", "Serangan surgawi ke semua musuh.", "multi"),

            # 💚 Healing
            SpecialSkill("Heaven's Grace", 35, 180, "healing", "epic", "Cahaya surgawi menyembuhkan semua.", "multi"),
            SpecialSkill("Last Hope", 25, 150, "healing", "rare", "Penyembuhan besar pada satu sekutu.", "single"),

            # 🛡️ Buff
            SpecialSkill("Battle Blessing", 20, 0, "buff", "epic", "Meningkatkan ATK dan DEF semua sekutu.", "multi"),
            SpecialSkill("Sacred Power", 18, 0, "buff", "rare", "Meningkatkan kekuatan diri sendiri.", "single"),

            # 💀 Debuff
            SpecialSkill("Void Curse", 30, 0, "debuff", "legendary", "Mengurangi semua stats musuh.", "multi"),
            SpecialSkill("Mind Shatter", 22, 0, "debuff", "epic", "Mengganggu konsentrasi target.", "single"),
        ]

        self.mobs_special_skill_pool = [
            SpecialSkill("Berserk", 25, 200, "atk", "epic", "Serangan brutal, risiko damage balik.", "single"),
            SpecialSkill("Meteor Smash", 35, 180, "atk", "epic", "Menjatuhkan meteor ke seluruh musuh.", "multi"),
            SpecialSkill("Earthquake", 30, 160, "atk", "epic", "Mengguncang tanah, menyerang semua musuh.", "multi"),
            SpecialSkill("Divine Light", 30, 200, "healing", "legendary", "Menyembuhkan semua sekutu.", "multi"),
            SpecialSkill("Overcharge", 20, 0, "buff", "rare", "Meningkatkan MP dan serangan.", "multi"),
            SpecialSkill("Ancient Shield", 25, 0, "buff", "epic", "Meningkatkan pertahanan tim secara drastis.", "multi"),
            SpecialSkill("Nightmare Gaze", 18, 100, "debuff", "epic", "Menurunkan atk dan def musuh.", "multi"),
            SpecialSkill("Void Pulse", 28, 140, "atk", "epic", "Serangan energi gelap dengan efek pengurasan MP.", "multi"),
            SpecialSkill("Soul Rend", 22, 180, "atk", "epic", "Serangan yang mengabaikan pertahanan target.", "single"),
        ]

        self.boss_special_skill_pool = [
            SpecialSkill("Void Collapse", 35, 220, "atk", "epic", "Serangan besar dari dimensi gelap.", "multi"),
            SpecialSkill("Soul Drain", 30, 150, "atk", "epic", "Menguras HP dan menambah ke boss.", "single"),
            SpecialSkill("Hellfire Rain", 40, 180, "atk", "epic", "Serangan api ke seluruh musuh.", "multi"),
        ]

        self.item_pool = [
            # 🗡️ Senjata & Serangan
            Item("Iron Sword", "common", "Pedang besi biasa.", {"atk": 10}, 100),
            Item("Steel Dagger", "common", "Dagger ringan dan cepat.", {"atk": 8}, 80),
            Item("Bronze Axe", "uncommon", "Kapak perunggu tajam.", {"atk": 15}, 120),
            Item("Iron Mace", "rare", "Gada besi berat.", {"atk": 25}, 150),
            # Item("Excalibur", "legendary", "op++.", {"atk": 99999}, 80),
            # Item("Excalibur", "legendary", "op++.", {"atk": 99999}, 80),
            # Item("Excalibur", "legendary", "op++.", {"atk": 99999}, 80),
            # Item("Excalibur", "legendary", "op++.", {"atk": 99999}, 80),
            # Item("Excalibur", "legendary", "op++.", {"atk": 99999}, 80),
            # Item("Excalibur", "legendary", "op++.", {"atk": 99999}, 80),
            # Item("Excalibur", "legendary", "op++.", {"atk": 99999}, 80),
            # Item("Excalibur", "legendary", "op++.", {"atk": 99999}, 80),
            # Item("Excalibur", "legendary", "op++.", {"atk": 99999}, 80),
            # Item("Excalibur", "legendary", "op++.", {"atk": 99999}, 80),

            # 🛡️ Armor & Defense
            Item("Leather Vest", "common", "Pelindung kulit ringan.", {"defense": 5}, 60),
            Item("Steel Armor", "uncommon", "Armor pelindung standar.", {"defense": 15}, 120),
            Item("Holy Charm", "rare", "Pesona suci yang meningkatkan pertahanan.", {"defense": 25}, 80),
            Item("Dragon Scale", "epic", "Pelindung dari sisik naga.", {"defense": 40}, 180),

            # ❤️ HP Boosters
            Item("HP Ring", "rare", "Cincin penambah HP.", {"max_hp": 100}, 150),
            # Item("Adams Apple", "rare", "Buah khuldi misterius.", {"max_hp": 99999}, 80),
            Item("Vital Pendant", "uncommon", "Menambah vitalitas.", {"max_hp": 50}, 100),
            Item("Blood Crystal", "epic", "Kristal merah penuh energi hidup.", {"max_hp": 150}, 200),

            # 🔷 MP Boosters
            Item("Mana Pendant", "epic", "Liontin penyimpan mana.", {"max_mp": 50}, 90),
            Item("Mystic Orb", "rare", "Bola energi penyimpan sihir.", {"max_mp": 80}, 120),
            Item("Spirit Talisman", "uncommon", "Jimat untuk penyihir muda.", {"max_mp": 30}, 70),

            # ☯️ Hybrid & Trade-off
            Item("Cursed Amulet", "legendary", "Menambah atk tapi mengurangi def.", {"atk": 20, "defense": -10}, 50),
            Item("Lucky Pendant", "legendary", "Berkah keberuntungan.", {"atk": 25, "defense": 25}, 80),
            Item("Dark Core", "epic", "Meningkatkan ATK besar tapi mengurangi HP.", {"atk": 40, "max_hp": -50}, 100),
            Item("Balance Shard", "rare", "Menyeimbangkan kekuatan.", {"atk": 10, "defense": 10}, 100),

            # 🌀 Utility / Unik
            # Item("Quick Boots", "uncommon", "Meningkatkan kecepatan (fungsi opsional).", {}, 90),
            # Item("Mirror Cloak", "legendary", "Mengurangi damage sihir (fungsi opsional).", {}, 120),
        ]


    def random_skills(self, amount, pool):
        return random.sample(pool, min(amount, len(pool)))

    def random_special_skill(self, pool):
        return random.choice(pool) if pool else None

    def create_heroes_and_bosses(self):
        self.hero_pool.clear()  # ← bersihkan hero sebelumnya
        self.boss = None        # ← reset boss lama kalau ada
        
        hero_names = [
            "Ardyn", "Lyra", "Kael", "Seraphine", "Thorne",
            "Elowen", "Draven", "Sylas", "Aurelia", "Fenric",
            "Kaida", "Gideon", "Liora", "Thalia", "Ezren",
            "Mirael", "Orion", "Riven", "Eira", "Lucan",
            "Cassian", "Nyra", "Bram", "Virel", "Rowan",
            "Isolde", "Alaric", "Zareth", "Kora", "Jarek",
            "Fael", "Ylva", "Torian", "Mireya", "Calen",
            "Selene", "Dorian", "Aziel", "Elandra", "Rhydan"
        ]
        hero_classes = ["Warrior", "Mage", "Archer", "Priest", "Rogue"]
        selected_names = random.sample(hero_names, 5)

        for name in selected_names:
            hero_class = random.choice(hero_classes)
            hero = Player(
                name,
                random.randint(400, 600),
                random.randint(80, 150),
                random.randint(35, 60),
                random.randint(20, 40),
                hero_class=hero_class
            )
            hero.skills = self.random_skills(3, self.hero_skill_pool)
            hero.special_skill = self.random_special_skill(self.hero_special_skill_pool)
            hero.type = hero.special_skill.rarity if hero.special_skill else "common"
            self.hero_pool.append(hero)

        boss = Enemy("Lord Zeus", 1500, 200, 70, 50, boss_class="god of Gods")
        boss.skills = self.random_skills(3, self.boss_skill_pool)
        boss.special_skill = self.random_special_skill(self.boss_special_skill_pool)
        boss.type = boss.special_skill.rarity if boss.special_skill else "common"
        self.boss = boss
        
    def create_heroes_op_and_bosses(self):
        self.hero_pool.clear()  # ← bersihkan hero sebelumnya
        self.boss = None        # ← reset boss lama kalau ada

        hero_names = [
            "admin", "admin", "admin", "admin", "admin",
            "admin", "admin", "admin", "admin", "admin",
            "admin", "admin", "admin", "admin", "admin",
            "admin", "admin", "admin", "admin", "admin",
            "admin", "admin", "admin", "admin", "admin",
            "admin", "admin", "admin", "admin", "admin",
            "admin", "admin", "admin", "admin", "admin",
            "admin", "admin", "admin", "admin", "admin"
        ]
        hero_classes = ["Warrior", "Mage", "Archer", "Priest", "Rogue"]
        selected_names = random.sample(hero_names, 5)

        for name in selected_names:
            hero_class = random.choice(hero_classes)
            hero = Player(
                name,
                99999,
                99999,
                99999,
                99999,
                hero_class=hero_class
            )
            hero.skills = self.random_skills(3, self.hero_skill_pool)
            hero.special_skill = self.random_special_skill(self.hero_special_skill_pool)
            hero.type = hero.special_skill.rarity if hero.special_skill else "common"
            self.hero_pool.append(hero)

        boss = Enemy("Lord Zeus", 1500, 200, 70, 50, boss_class="god of Gods")
        boss.skills = self.random_skills(3, self.boss_skill_pool)
        boss.special_skill = self.random_special_skill(self.boss_special_skill_pool)
        boss.type = boss.special_skill.rarity if boss.special_skill else "common"
        self.boss = boss
        
    def create_mobs(self):
        self.mobs_pool.clear()  # Reset mobs lama

        mob_names = ["Goblin", "Slime", "Werewolf", "Shadowling", "Skeleton", "Orc", "Wraith", "Bandit"]
        mob_classes = ["Brute", "Scout", "Cursed", "Undead", "Darkling"]
        num_mobs = random.randint(2, 5)
        selected_names = [random.choice(mob_names) for _ in range(num_mobs)]

        name_counter = {}

        for base_name in selected_names:
            # Hitung jumlah kemunculan nama
            count = name_counter.get(base_name, 0) + 1
            name_counter[base_name] = count

            # Tambahkan angka jika lebih dari satu
            name = f"{base_name}{count}" if count > 1 else base_name

            mob_class = random.choice(mob_classes)
            mob = Enemy(
                name,
                random.randint(300, 500),   # HP
                random.randint(50, 100),    # MP
                random.randint(30, 50),     # ATK
                random.randint(15, 35),     # DEF
                boss_class=mob_class
            )
            mob.skills = self.random_skills(2, self.mobs_skill_pool)
            mob.special_skill = self.random_special_skill(self.mobs_special_skill_pool)
            mob.type = mob.special_skill.rarity if mob.special_skill else "common"
            self.mobs_pool.append(mob)


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
        for hero in self.hero_pool:
          hero.gold += 255

    def shop_phase(self):
        pass

    def check_game_over(self):
        if not self.boss.is_alive():
            print(">>> Victory! Boss defeated.")
            self.running = False
        elif all(not h.is_alive() for h in self.player_team):
            print(">>> Game Over. All heroes have fallen.")
            self.running = False


    def display_team_status(self):
        pass
