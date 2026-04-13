#!/usr/bin/env python3
from items import Weapon, Potion, Scroll
from character_class import Character
from item_manager import ItemManager
"""main.py - Главная программа (ООП версия)"""

# 1. ИМПОРТЫ
from character_class import CharacterManager
from utils import save_to_file, load_from_file


# 2. КОНСТАНТЫ
TITLE = "=== CHARACTER DATABASE ==="


# 3. ФУНКЦИИ МЕНЮ
def show_menu():
    """Показать главное меню"""
    print("\n" + TITLE)
    print("1. Показать всех персонажей")
    print("2. Добавить персонажа")
    print("3. Удалить персонажа")
    print("4. Найти персонажа")
    print("5. Показать статистику")
    print("6. Показать все предметы")  # ← НОВОЕ!
    print("7. Сохранить в файл")
    print("8. Загрузить из файла")
    print("9. Выход")


# 4. ГЛАВНАЯ ФУНКЦИЯ
def main():
    """Главная функция программы"""
    
    # Создаём менеджер персонажей
    manager = CharacterManager()
    
    # Создаём менеджер предметов
    item_manager = ItemManager()
    
    # Загружаем предметы из JSON
    item_manager.load_from_json('weapons.json')
    
    # Загружаем данные при запуске
    data = load_from_file()
    if data:
        manager.from_dict(data)
        print("✅ Данные загружены")
    else:
        # Тестовые персонажи если пусто
        manager.add("Royals", 14, "Earth-Mage", 6100)
        manager.add("Zol", 13, "Critic", 9100)
        manager.add("Big Problem", 12, "Dodger", 8100)
        print("⚠️ Загружены тестовые персонажи")
    # ```Тестовый чар```    
    # test_char = manager.characters.get("player1")    
    # ... где-то после создания менеджера ...
    # ТЕСТ маны
# ТЕСТ СИСТЕМЫ СТАТОВ
    # ТЕСТ РАСЧЁТНЫХ HP/МАНЫ
    
    test_char = manager.characters.get("player1")
    if test_char:
        print("\n🧪 ТЕСТ DERIVED STATS:")
        print(f"Исходно: HP {test_char.health}/{test_char.max_health}, Mana {test_char.mana}/{test_char.max_mana}")
        
        test_char.level_up()  # +5 очков
        test_char.allocate_stat("endurance", 3)  # +30 к макс. HP
        test_char.allocate_stat("wisdom", 2)     # +16 к макс. маны
        
        print(f"После прокачки: HP {test_char.health}/{test_char.max_health}, Mana {test_char.mana}/{test_char.max_mana}")
        
        # Попытка "читернуть" должна быть невозможна
        # test_char.health = 9999  ← раскомментируй для проверки → выдаст AttributeError
    test_sword = Weapon("Ржавый клинок", 5, 50, 15)
    test_sword.equip(test_char)
    print(f"Урон с мечом: {test_char.damage}")  # Должно вырасти на 15
    test_sword.unequip(test_char)
    print(f"Урон без меча: {test_char.damage}")  # Вернётся к базовому
    test_char = manager.characters.get("player1")
    if test_char:
    # Создаём 3 свитка
        s1 = Scroll("Огненный шар", 0, 50, "damage", 80)
        s2 = Scroll("Исцеление", 0, 30, "heal", 60)
        s3 = Scroll("Ледяная стрела", 0, 40, "damage", 70)
    
    # 1. Добавляем в рюкзак
    test_char.scroll_inventory.add_scroll(s1)
    test_char.scroll_inventory.add_scroll(s2)
    test_char.scroll_inventory.show()
    
    # 2. Экипируем один
    test_char.scroll_inventory.equip_scroll(s1)
    test_char.scroll_inventory.show()
    
    # 3. Используем
    test_char.scroll_inventory.use_scroll(s1, test_char)
    test_char.scroll_inventory.show()
    
    # 4. Тест лимита (попробуй добавить 12 свитков)
    # Главный цикл программы
    while True:
        show_menu()
        choice = input("\nВыберите (1-8): ").strip()
        
        if choice == "1":
            manager.display_all()
        
        elif choice == "2":
            print("\n--- Добавление персонажа ---")
            name = input("Имя: ").strip() or "Noobie"
            level = int(input("Уровень: ") or "1")
            char_class = input("Класс: ").strip() or "Novice"
            health = int(input("Здоровье: ") or "100")
            mana = int(input("Мана: ") or "0")
            manager.add(name, level, char_class, health, mana)
        
        elif choice == "3":
            manager.display_all()
            search = input("Введите ID или имя для удаления: ").strip()
            manager.delete(search)
        
        elif choice == "4":
            search = input("Введите ID или имя для поиска: ").strip()
            manager.find(search)
        
        elif choice == "5":
            manager.show_statistics()
            
        elif choice == "6":  # ← НОВОЕ!
            item_manager.display_all()
            
        elif choice == "7":
            save_to_file(manager.to_dict())
            
        elif choice == "8":
            data = load_from_file()
            if data:
                manager.from_dict(data)
                
        elif choice == "9":  # ← Теперь это выход
            save_to_file(manager.to_dict())
            print("\n👋 До свидания!")
            break
        
        else:
            print("❌ Неверный выбор!")


# 5. ТОЧКА ВХОДА
if __name__ == "__main__":
    main()