# class_profiles.py
CLASS_PROFILES = {
    "Mage": {
        "max_block_zones": 0,
        "allowed_weapons": ["staff_2h"],
        "slots": {"main_hand": True, "off_hand": False},
        "zones": {"unguarded": 1.0, "guarded": 0.0},
        "block_penetration": 1.0,  # 100%
        "damage_mult": 1.0,
        "passive": "spells_ignore_block",
        "stat_synergy": {"intelligence": 1.5, "spirituality": 0.8}
    },
    "Tank": {
        "max_block_zones": 2,
        "allowed_weapons": ["sword_1h", "club_1h", "shield"],
        "slots": {"main_hand": True, "off_hand": True},
        "zones": {"unguarded": 0.4, "guarded": 0.6},
        "block_penetration": 0.0,
        "damage_mult": 1.0,
        "passive": "shield_bash",
        "stat_synergy": {"endurance": 1.2, "strength": 1.0}
    },
    "Dodger": {
        "max_block_zones": 2,
        "allowed_weapons": ["knife_1h"],
        "slots": {"main_hand": True, "off_hand": True},
        "zones": {"unguarded": 0.7, "guarded": 0.3},
        "block_penetration": 0.0,
        "damage_mult": 0.9,
        "passive": "bleed_chance_05",
        "stat_synergy": {"agility": 1.3, "intuition": 0.7}
    },
    "Bruiser": {
        "max_block_zones": 1,
        "allowed_weapons": ["axe_2h", "club_2h"],
        "slots": {"main_hand": True, "off_hand": False},
        "zones": {"unguarded": 0.5, "guarded": 0.5},
        "block_penetration": 0.0,
        "damage_mult": 1.25,
        "passive": "heavy_hits",
        "stat_synergy": {"strength": 1.4, "endurance": 0.8}
    },
    "Crit": {
        "max_block_zones": 2,
        "allowed_weapons": ["sword_1h"],
        "slots": {"main_hand": True, "off_hand": True},
        "zones": {"unguarded": 0.6, "guarded": 0.4},
        "block_penetration": 0.5,
        "damage_mult": 1.0,
        "passive": "crit_penetrates_block",
        "stat_synergy": {"intuition": 1.2, "agility": 1.0}
    },
    "Archer": {
        "max_block_zones": 1,
        "allowed_weapons": ["bow_2h", "crossbow_2h"],
        "slots": {"main_hand": True, "off_hand": False},
        "zones": {"unguarded": 1.0, "guarded": 0.0},
        "block_penetration": 0.5,
        "damage_mult": 0.95,
        "passive": "ranged_pierce",
        "stat_synergy": {"agility": 1.1, "intuition": 0.9}
    }
}
