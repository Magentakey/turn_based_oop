ALL_SKILLS = [
    Skill("Slash", 1.2, 5, "melee"),
    Skill("Double Shot", 0.8, 6, "range"),
    Skill("Fireball", 1.5, 8, "magic"),
    Skill("Blink", 0, 4, "dash"),
    Skill("Shield Bash", 1.0, 6, "melee"),
    Skill("Power Up", 0, 5, "buff"),      # menambah STR/INT/etc

    Skill("Arrow Barrage", 1.3, 10, "range"),
    Skill("Thunder Strike", 2.0, 12, "magic"),
    Skill("Heavy Smash", 1.8, 10, "melee"),
    Skill("Heal", -1.5, 8, "magic"),      # negatif: penyembuhan
]

CLASS_SKILL_POOL = {
    "warrior": ["Slash", "Shield Bash", "Heavy Smash", "Power Up"],
    "archer": ["Double Shot", "Arrow Barrage", "Blink", "Power Up"],
    "mage": ["Fireball", "Thunder Strike", "Heal", "Blink"],
    "tank": ["Shield Bash", "Heavy Smash", "Power Up"],
    "assassin": ["Slash", "Blink", "Double Shot", "Arrow Barrage"],
}
