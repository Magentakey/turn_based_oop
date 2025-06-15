#punya Gilang ini min
import random
from rafa import Player, Enemy
from juan import Skill, SpecialSkill, random_skills, random_special_skill
from ariq import Item
from jaydan import Shop

class GameManager:
    def __init__(self):
        # skill & item pools
        self.hero_skill_pool = []
        self.boss_skill_pool = []
        self.hero_special_skill_pool = []
        self.boss_special_skill_pool = []
        self.item_pool = []

        # gameplay state
        self.hero_pool = []
        self.player_team = []
        self.boss = None
        self.shop = None
        self.turn_number = 1
        self.running = True

    def init_skills_and_items(self):
        # Hero skill pool
        self.hero_skill_pool = [
            Skill("Fireball", 10, 100, "atk", "common", "Menembakkan bola api.", "single"),
            Skill("Heal", 15, -100, "healing", "common", "Menyembuhkan sekutu.", "single"),
            Skill("Slash", 5, 80, "atk", "common", "Serangan tebasan cepat.", "single"),
            Skill("Multi Heal", 20, -80, "healing", "uncommon", "Menyembuhkan semua sekutu.", "multi"),
            Skill("Thunder", 12, 90, "atk", "uncommon", "Serangan petir ke satu musuh.", "single"),
            Skill("War Cry", 10, 0, "buff", "rare", "Meningkatkan atk semua sekutu.", "multi"),
        ]

        # Boss skill pool
        self.boss_skill_pool = [
            Skill("Shadow Spike", 15, 110, "atk", "common", "Serangan bayangan menusuk.", "single"),
            Skill("Dark Heal", 20, -100, "healing", "common", "Menyembuhkan diri sendiri.", "single"),
            Skill("Corrupt Slash", 10, 85, "atk", "uncommon", "Serangan kegelapan.", "single"),
            Skill("Plague Burst", 25, 90, "atk", "rare", "Ledakan racun untuk semua musuh.", "multi"),
            Skill("Doom Chant", 20, 0, "buff", "epic", "Meningkatkan atk dan def boss.", "multi"),
        ]

        # Hero special skill pool
        self.hero_special_skill_pool = [
            SpecialSkill("Berserk", 25, 200, "atk", "epic", "Serangan brutal dengan risiko.", "single"),
            SpecialSkill("Divine Light", 30, -200, "healing", "legendary", "Menyembuhkan semua sekutu.", "multi"),
            SpecialSkill("Overcharge", 20, 0, "buff", "rare", "Meningkatkan MP dan serangan.", "multi"),
        ]

        # Boss special skill pool
        self.boss_special_skill_pool = [
            SpecialSkill("Void Collapse", 35, 220, "atk", "legendary", "Serangan besar dari dimensi gelap.", "multi"),
            SpecialSkill("Soul Drain", 30, 150, "atk", "epic", "Menguras HP dan menambah ke boss.", "single"),
            SpecialSkill("Hellfire Rain", 40, 180, "atk", "legendary", "Serangan api ke seluruh musuh.", "multi"),
        ]

        # Item pool
        self.item_pool = [
            Item("Iron Sword", "Pedang besi standar.", {"atk": 10}, 100),
            Item("Steel Armor", "Armor pelindung standar.", {"defense": 15}, 120),
            Item("HP Ring", "Cincin penambah HP.", {"max_hp": 100}, 150),
            Item("Mana Pendant", "Liontin penyimpan mana.", {"max_mp": 50}, 90),
            Item("Cursed Amulet", "Amulet terkutuk (atk naik, def turun).", {"atk": 20, "defense": -10}, 50),
            Item("Holy Charm", "Pesona suci pelindung.", {"defense": 25}, 80),
        ]

    def create_heroes_and_bosses(self):
        # Pilih beberapa nama untuk hero secara acak
        hero_names = ["Asep", "Lina", "Budi", "Tari", "Riko", "Joko", "Nina", "Dewi"]
        random.shuffle(hero_names)
        for name in hero_names[:5]:
            hero = Player(
                name,
                random.randint(400, 600),
                random.randint(80, 150),
                random.randint(35, 60),
                random.randint(20, 40)
            )
            hero.skills = random_skills(3, self.hero_skill_pool)
            hero.special_skill = random_special_skill(self.hero_special_skill_pool)
            self.hero_pool.append(hero)

        # Buat boss
        self.boss = Enemy("Lord Malgrim", 1500, 200, 70, 50)
        self.boss.skills = random_skills(3, self.boss_skill_pool)
        self.boss.special_skill = random_special_skill(self.boss_special_skill_pool)

    def choose_heroes(self):
        # Contoh pemilihan pertama 5 hero
        print("\n🔍 Pilih 5 hero dari daftar:")
        for i, hero in enumerate(self.hero_pool, start=1):
            print(f"{i}. {hero.name} | HP: {hero.max_hp}, MP: {hero.max_mp}, ATK: {hero.atk}, DEF: {hero.defense}")
        # Di sini kamu bisa ganti menjadi manual input jika diinginkan
        self.player_team = self.hero_pool[:5]
        print("\n✅ Hero yang dipilih:")
        for hero in self.player_team:
            print(f"- {hero.name}")

    def distribute_starting_items(self):
        print("\n🎁 Memberikan 3 item awal secara acak kepada hero:")
        for _ in range(3):
            hero = random.choice(self.player_team)
            item = random.choice(self.item_pool)
            if len(hero.equipped_items) < 5:
                hero.equip_item(item)
