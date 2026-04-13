from skills import Skill

# --- СКИЛЛЫ ВОИНА (Танк/ДПС) ---
WARRIOR_SKILLS = {
    "shield_bash": Skill("Удар щитом", mana_cost=15, cooldown=2, damage=25),
    "war_cry": Skill("Боевой клич", mana_cost=20, cooldown=5, heal=50), # Лечит себя
    "execute": Skill("Казнь", mana_cost=30, cooldown=4, damage=100)
}

# --- СКИЛЛЫ МАГА (Стихии) ---
MAGE_SKILLS = {
    "fireball": Skill("Огненный шар", mana_cost=30, cooldown=3, damage=80),
    "ice_lance": Skill("Ледяное копье", mana_cost=15, cooldown=1, damage=30),
    "mana_shield": Skill("Щит маны", mana_cost=40, cooldown=6, damage=0) # Пока урон 0, потом добавим логику щита
}

# --- СКИЛЛЫ ЛУЧНИКА ---
ARCHER_SKILLS = {
    "aimed_shot": Skill("Прицельный выстрел", mana_cost=10, cooldown=2, damage=40),
    "rain_of_arrows": Skill("Дождь из стрел", mana_cost=40, cooldown=5, damage=90),
    "dodge_roll": Skill("Перекат", mana_cost=15, cooldown=3, damage=0) # Уклонение
}

# --- ОБЩАЯ БАЗА (удобно для поиска) ---
ALL_SKILLS = {
    **WARRIOR_SKILLS,
    **MAGE_SKILLS,
    **ARCHER_SKILLS
}