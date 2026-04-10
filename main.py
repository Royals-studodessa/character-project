import utils
from characters import (
    display_characters,
    add_character,
    del_character,
    find_character,
    show_statistics
)


# Загружаем данные при запуске
characters = utils.load_from_file()

# Если пусто — добавляем тестовых персонажей
if not characters:
    characters = {
        "player1": {"name": "Royals", "level": 14, "class": "Earth-Mage", "health": 6100},
        "player2": {"name": "Zol", "level": 13, "class": "Critic", "health": 9100},
        "player3": {"name": "Big Problem", "level": 12, "class": "Dodger", "health": 8100}
    }
    print("⚠️ Загружены тестовые персонажи")


# 2. Создайте функцию display_characters()


while True:
    print("\n=== МЕНЮ ===")
    print("1. Показать всех персонажей")
    print("2. Добавить персонажа")
    print("3. Удалить персонажа")
    print("4. Найти персонажа")
    print("5. Показать статистику")
    print("6. Сохранить в файл")  # ← Новый пункт!
    print("7. Загрузить из файла")  # ← Новый пункт!
    print("8. Выход")

    choice = input("Выберите (1-8): ")  # ← Исправлено!

    if choice == "1":
        display_characters(characters)
    elif choice == "2":
        add_character(characters)
    elif choice == "3":
        del_character(characters)
    elif choice == "4":
        find_character(characters)
    elif choice == "5":
        show_statistics(characters)
    elif choice == "6":
        utils.save_to_file(characters)  # ← Вызов функции!
    elif choice == "7":
        characters = utils.load_from_file()  # ← Загрузка!
    elif choice == "8":
        # Автосохранение при выходе
        utils.save_to_file(characters)
        print("Выход совершен!")
        break
    else:
        print("Неверный выбор!")


