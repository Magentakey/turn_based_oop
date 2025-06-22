SKILLS_BY_TYPE = {
    "archer":  ["RangeAttack", "Blink", "PiercingShot"],
    "mage":    ["Fireball", "Teleport", "Lightning"],
    "tank":    ["ShieldBash", "Taunt", "Fortify"],
}

def random_skill_for(hero_type):
    pool = SKILLS_BY_TYPE.get(hero_type, [])
    return random.choice(pool) if pool else None
