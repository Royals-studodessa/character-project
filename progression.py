# progression.py - Система прогрессии и классов

# === КОНФИГУРАЦИЯ ПРОГРЕССИИ ===

# Базовые скиллы для Newbie (уровни 0-4)
NEWBIE_SKILLS = {
    "basic_attack": {"name": "Базовая атака", "level_req": 0, "damage": 10},
    "basic_defense": {"name": "Базовая защита", "level_req": 1, "defense": 5},
    "first_aid": {"name": "Первая помощь", "level_req": 2, "heal": 20},
}

# Основные классы (выбор на уровне 4)
MAIN_CLASSES = {
    "Warrior": {
        "stat_requirements": {"strength": 8, "endurance": 8},
        "skills": {
            "power_strike": {"name": "Мощный удар", "level_req": 4, "damage": 25, "stat_req": {"strength": 10}},
            "shield_bash": {"name": "Удар щитом", "level_req": 5, "damage": 15, "stun_chance": 0.2},
            "war_cry": {"name": "Боевой клич", "level_req": 6, "buff": "attack_up"},
        },
        "subclasses": ["Tank", "Bruiser", "Dodger", "Crit"]
    },
    "Mage": {
        "stat_requirements": {"intelligence": 10, "wisdom": 8},
        "skills": {
            "fireball": {"name": "Огненный шар", "level_req": 4, "damage": 30, "mana_cost": 20},
            "ice_lance": {"name": "Ледяное копье", "level_req": 5, "damage": 20, "mana_cost": 15},
            "mana_shield": {"name": "Щит маны", "level_req": 6, "defense": 15},
        },
        "subclasses": ["Fire-Mage", "Water-Mage", "Earth-Mage", "Air-Mage"]
    },
    "Archer": {
        "stat_requirements": {"agility": 10, "intuition": 8},
        "skills": {
            "aimed_shot": {"name": "Прицельный выстрел", "level_req": 4, "damage": 28},
            "multi_shot": {"name": "Мульти-выстрел", "level_req": 5, "damage": 18, "hits": 2},
            "poison_arrow": {"name": "Отравленная стрела", "level_req": 6, "damage": 15, "dot": 5},
        },
        "subclasses": ["Sniper", "Ranger", "Assassin"]
    }
}

# Специализации (подклассы, выбор на уровне 10)
SUBCLASSES = {
    "Tank": {
        "stat_requirements": {"endurance": 15, "strength": 12},
        "required_skills": ["shield_bash"],
        "bonus_stats": {"endurance": 5, "strength": 2},
        "description": "Мастер защиты и контроля"
    },
    "Bruiser": {
        "stat_requirements": {"strength": 18, "endurance": 12},
        "required_skills": ["power_strike"],
        "bonus_stats": {"strength": 6, "endurance": 2},
        "description": "Тяжелый урон в ближнем бою"
    },
    "Dodger": {
        "stat_requirements": {"agility": 16, "intuition": 12},
        "required_skills": [],  # Можно добавить специфичные
        "bonus_stats": {"agility": 6, "intuition": 3},
        "description": "Уклонение и контратаки"
    },
    "Crit": {
        "stat_requirements": {"intuition": 18, "agility": 12},
        "required_skills": [],
        "bonus_stats": {"intuition": 7, "agility": 2},
        "description": "Критические удары"
    },
    "Fire-Mage": {
        "stat_requirements": {"intelligence": 18, "spirituality": 10},
        "required_skills": ["fireball"],
        "bonus_stats": {"intelligence": 6},
        "description": "Магия огня и разрушения"
    },
    "Air-Mage": {
        "stat_requirements": {"intelligence": 18, "spirituality": 10},
        "required_skills": ["fireball"],
        "bonus_stats": {"intelligence": 6},
        "description": "Магия огня и разрушения"
    },
    "Water-Mage": {
        "stat_requirements": {"intelligence": 18, "spirituality": 10},
        "required_skills": ["fireball"],
        "bonus_stats": {"intelligence": 6},
        "description": "Магия огня и разрушения"
    },
    "Earth-Mage": {
        "stat_requirements": {"intelligence": 18, "spirituality": 10},
        "required_skills": ["fireball"],
        "bonus_stats": {"intelligence": 6},
        "description": "Магия огня и разрушения"
    },
    # ... другие подклассы
}