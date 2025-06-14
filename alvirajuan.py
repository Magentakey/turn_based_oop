class Skill:
    def __init__(self, name, mp_cost, power, skill_type, rarity, description, target_type):
        self.name = name
        self.mp_cost = mp_cost
        self.power = power
        self.skill_type = skill_type  # "atk", "healing", "stun", "buff", "debuff"
        self.rarity = rarity  # "common", "uncommon", "rare", "epic", "legendary"
        self.description = description
        self.target_type = target_type  # "single" atau "multi"

    def use(self, user, targets):
        if user.mp < self.mp_cost:
            print(f"{user.name} tidak cukup MP untuk menggunakan {self.name}.")
            return

        user.mp -= self.mp_cost

        # Single target atau multi target
        if self.target_type == "single":
            targets = [targets]

        for target in targets:
            if self.skill_type == "atk":
                damage = max(1, self.power + user.atk - target.defense)
                target.take_damage(damage)
                print(f"{target.name} menerima {damage} damage dari {self.name}.")

            elif self.skill_type == "healing":
                heal = abs(self.power)
                target.hp = min(target.max_hp, target.hp + heal)
                print(f"{target.name} disembuhkan {heal} HP oleh {self.name}.")

            elif self.skill_type == "stun":
                target.stunned = True
                print(f"{target.name} terkena stun oleh {self.name}.")

            elif self.skill_type == "buff":
                target.atk += self.power
                print(f"{target.name} mendapat buff ATK +{self.power} dari {self.name}.")

            elif self.skill_type == "debuff":
                target.defense = max(0, target.defense - self.power)
                print(f"{target.name} terkena debuff DEF -{self.power} dari {self.name}.")


class SpecialSkill(Skill):
    def __init__(self, name, mp_cost, power, skill_type, rarity, description, target_type):
        super().__init__(name, mp_cost, power, skill_type, rarity, description, target_type)

    def use(self, user, targets):
        print(f"{user.name} menggunakan Special Skill: {self.name}!")
        super().use(user, targets)