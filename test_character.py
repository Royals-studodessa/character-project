#!/usr/bin/env python3
# test_character.py - Тест класса Character

from character_class import Character

print("=== ТЕСТ КЛАССА CHARACTER ===\n")

# Создание персонажей
print("1. Создание персонажей:")
hero1 = Character("Royals", 14, "Earth-Mage", 6100)
hero2 = Character("Zol", 13, "Critic", 9100)

print(f"   ✅ {hero1.name} создан")
print(f"   ✅ {hero2.name} создан\n")

# Отображение
print("2. Информация о персонажах:")
print("\n--- Персонаж 1 ---")
hero1.display()

print("\n--- Персонаж 2 ---")
hero2.display()

# Тест боя
print("\n3. Тест боя:")
hero1.take_damage(500)
hero2.heal(1000)

# Преобразование в словарь
print("\n4. Преобразование в словарь:")
hero1_dict = hero1.to_dict()
print(f"   Словарь: {hero1_dict}")

# Создание из словаря
print("\n5. Создание из словаря:")
hero3 = Character.from_dict(hero1_dict)
print(f"   ✅ {hero3.name} создан из словаря")
hero3.display()

print("\n=== ТЕСТ ЗАВЕРШЁН ===")
