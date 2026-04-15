# 1. ИМПОРТЫ
from manager import CharacterManager
from utils import save_to_file, load_from_file
from item_manager import ItemManager
from progression import SUBCLASSES, MAIN_CLASSES
from combats import CombatAction, CombatSession
import time
from items import Weapon
from character import Character
from battle_test import  run_auto_battle_test, run_mage_test, create_test_characters

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


def show_progression_menu(character):
    """Меню прогрессии персонажа"""
    while True:
        print("\n" + "=" * 50)
        print("📈 МЕНЮ ПРОГРЕССИИ")
        print("=" * 50)
        character.get_progression_info()

        print("\n1. Изучить новый навык")
        if character.level >= 4 and not character.main_class:
            print("2. Выбрать основной класс")
        if character.level >= 10 and not character.subclass:
            print("3. Выбрать специализацию")
        print("0. Назад")

        choice = input("\nВыберите: ").strip()

        if choice == "1":
            # Показываем доступные скиллы
            available_skills = []
            if character.main_class in MAIN_CLASSES:
                for skill_name, skill_data in MAIN_CLASSES[character.main_class]["skills"].items():
                    if skill_name not in character.learned_skills:
                        available_skills.append((skill_name, skill_data))

            if not available_skills:
                print("❌ Нет доступных навыков для изучения")
                continue

            print("\n📚 Доступные навыки:")
            for i, (name, data) in enumerate(available_skills, 1):
                print(f"  {i}. {data['name']} (уровень {data.get('level_req', 0)})")

            skill_choice = input("Выберите навык: ").strip()

        elif choice == "2" and character.level >= 4 and not character.main_class:
            print("\n🎯 Выберите основной класс:")
            for class_name, class_data in MAIN_CLASSES.items():
                print(f"  • {class_name} (Требования: {class_data['stat_requirements']})")

            class_choice = input("Введите название класса: ").strip()
            character.choose_main_class(class_choice)

        elif choice == "3" and character.level >= 10 and not character.subclass:
            available = character.get_available_subclasses()
            print("\n🎯 Выберите специализацию:")
            for sub in available:
                if sub in SUBCLASSES:
                    print(f"  • {sub}: {SUBCLASSES[sub]['description']}")

            sub_choice = input("Введите название: ").strip()
            character.choose_subclass(sub_choice)

        elif choice == "0":
            break


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
        # Тестовые персонажи начинают как Newbie
        manager.add("Royals", 3, "Newbie", 6100, 50)
        manager.add("Zol", 2, "Newbie", 9100, 50)
        manager.add("Big Problem", 1, "Newbie", 8100, 50)
        print("⚠️ Загружены тестовые персонажи (Newbie)")

        # ========================================
        # ТЕСТОВАЯ ПРОВЕРКА БОЕВОЙ СИСТЕМЫ
        # ========================================
    run_auto_battle_test(max_turns=10)
    

        # ========================================
        # КОНЕЦ ТЕСТА
        # ========================================

    while True:
        show_menu()
        choice = input("\nВыберите (1-9): ").strip()

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

        elif choice == "9":
            save_choice = input("\n💾 Сохранить прогресс перед выходом? (y/n): ").strip().lower()
            if save_choice in ('y', 'да'):
                save_to_file(manager.to_dict())
                print("✅ Прогресс сохранён.")
            else:
                print("⚠️ Прогресс не сохранён. Последние действия потеряны.")
            print("\n👋 До свидания!")
            break

        else:
            print("❌ Неверный выбор!")


# 5. ТОЧКА ВХОДА
if __name__ == "__main__":
    main()
