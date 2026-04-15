"""
Тесты для боевой системы
Запуск: python battle_test.py
"""

import random
from character import Character
from combats import CombatSession
from items import Weapon


def create_test_characters():
    """Создаёт тестовых персонажей"""
    dodger = Character("Quick", 10, "Dodger", 400, 100)
    tank = Character("Shield", 10, "Tank", 450, 100)
    
    # Экипировка для Dodger (2 ножа)
    dodger.equipment["main_hand"] = Weapon(
        "Нож 1", 1, 10, 20, 
        combat_props={"weapon_type": "dagger", "bleed_chance": 0.1}
    )
    dodger.equipment["off_hand"] = Weapon(
        "Нож 2", 1, 10, 20, 
        combat_props={"weapon_type": "dagger", "bleed_chance": 0.1}
    )
    
    # Экипировка для Tank (меч + щит)
    tank.equipment["main_hand"] = Weapon("Дубина", 4, 30, 25)
    tank.equipment["off_hand"] = Weapon(
        "Щит", 3, 30, 0, 
        slot="off_hand", 
        combat_props={"is_shield": True, "stun_chance": 0.3}
    )
    
    return dodger, tank


def run_auto_battle_test(max_turns=15):
    """Запускает автоматический тест боя"""
    print("\n" + "="*60)
    print("🎮 АВТОМАТИЧЕСКИЙ ТЕСТ БОЕВОЙ СИСТЕМЫ")
    print("="*60)
    
    p1, p2 = create_test_characters()
    session = CombatSession(p1, p2, timeout_sec=1)
    
    print(f"⚔️ {p1.name} ({p1.char_class}) vs {p2.name} ({p2.char_class})")
    print(f"HP: {p1._current_health}/{p1.max_health} | {p2._current_health}/{p2.max_health}")
    
    # Запускаем авто-бой
    turn = 1
    while session.is_active and turn <= max_turns:
        print(f"\n{'─'*15} ХОД {turn} {'─'*15}")
        
        # Авто-генерация действий
        zones = ["head", "torso", "legs", "waist"]
        for name, player in session.players.items():
            if player.is_alive:
                # Получаем статы экипировки
                eq_stats = player.get_equipment_stats()
                num_attacks = eq_stats["num_attacks"]
                
                # Генерируем НЕСКОЛЬКО зон атаки (по количеству оружия)
                atk_zones = [random.choice(zones) for _ in range(num_attacks)]
                blk_zone = random.choice(zones)
                
                session.submit_action(
                    player_name=name,
                    action_type="attack",
                    attack_zones=atk_zones,  # ← Теперь СПИСОК из 1 или 2 зон
                    block_zones=[blk_zone],
                    skills=[]
                )
        
        # Разрешаем ход
        session.resolve_turn()
        
        if not session.is_active:
            break
        turn += 1
    
    if session.is_active:
        print("\n⏱️ Превышен лимит ходов. Бой прерван.")
    
    print("\n" + "="*60)
    print("✅ ТЕСТ ЗАВЕРШЁН")
    print("="*60 + "\n")
    
    return session


def run_mage_test():
    """Тест боя с магом"""
    print("\n" + "="*60)
    print("🔮 ТЕСТ: Маг vs Воин")
    print("="*60)
    
    from skills_db import ALL_SKILLS
    
    mage = Character("Fire-Mage", 10, "Mage", 400, 100)
    warrior = Character("Tank", 10, "Tank", 400, 100)
    
    # Настраиваем мага
    mage._current_mana = 100
    mage._stats["intelligence"] = 15
    mage._stats["wisdom"] = 12
    
    # Даём посох
    staff = Weapon(
        "Огненный посох", 5, 100, 0,
        slot="main_hand",
        combat_props={"magic_bonus": 20}
    )
    mage.equipment["main_hand"] = staff
    
    session = CombatSession(mage, warrior, timeout_sec=1)
    
    # Маг кастует файербол
    session.submit_action(
        player_name=mage.name,
        action_type="skill_only",
        attack_zones=[],
        block_zones=[],
        skills=[],
        skill_name="fireball"
    )
    
    # Воин атакует
    session.submit_action(
        player_name=warrior.name,
        action_type="attack",
        attack_zones=["head"],
        block_zones=["head"],
        skills=[]
    )
    
    session.resolve_turn()
    
    print("\n✅ ТЕСТ МАГА ЗАВЕРШЁН\n")
    return session


# Если файл запускается напрямую
if __name__ == "__main__":
    print("\n🧪 ЗАПУСК ТЕСТОВ БОЕВОЙ СИСТЕМЫ")
    print("="*60)
    
    # Выбор теста
    print("\nВыберите тест:")
    print("1. Авто-бой (Dodger vs Tank)")
    print("2. Маг vs Воин")
    
    choice = input("\nВведите номер (1 или 2): ").strip()
    
    if choice == "1":
        run_auto_battle_test()
    elif choice == "2":
        run_mage_test()
    else:
        print("❌ Неверный выбор. Запускаю авто-бой по умолчанию.")
        run_auto_battle_test()