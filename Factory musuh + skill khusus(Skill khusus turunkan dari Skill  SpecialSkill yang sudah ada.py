import random

class Wolf(Enemy):
    def __init__(self):
        super().__init__("Wolf", hp=120, atk=18, typ="beast")
        self.skills = [ClawSwipe(), HowlBuff()]

class Lizardman(Enemy):
    ...

ENEMY_POOL = [Wolf, Lizardman, Goblin]

def _random_enemy(self):
    return random.choice(ENEMY_POOL)()
