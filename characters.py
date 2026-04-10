import utils


def display_characters(characters_dict):
    for key, char in characters_dict.items():
        print(f'🎯{char["name"]}')
        print(f'Level: {char["level"]}')
        print(f'Class: {char["class"]}')
        print(f'Health: {char["health"]}')
        print()


def add_character(characters_dict):
    print(f'Добавляем нового персонажа')

    new_id = f'player{len(characters_dict) + 1}'

    name = utils.get_string('Name: ', 'Noobie', 3)
    level = utils.get_number('Level: ', 0, 3)
    char_class = utils.get_string('Class: ', 'Noobie', 3)
    health = utils.get_number('Health: ', 100, 3)

    characters_dict[new_id] = {
        'name': name,
        'level': level,
        'class': char_class,
        'health': health
    }
    print(f"\n✅ Персонаж {name} добавлен!")


def del_character(characters_dict):
    print(f'Удаляем выбранного персонажа')
    display_characters(characters_dict)

    character = input('Введите Id или Name персонажа: ')

    # Сначала ищем персонажа
    found_id = None
    for id, char in characters_dict.items():
        if character in id or character in char['name']:
            found_id = id
            break

    # Удаляем после цикла
    if found_id:
        deleted_char = characters_dict.pop(found_id)
        print(f'Персонаж {deleted_char["name"]} был удален')
    else:
        print(f'Данный персонаж не найден')


def find_character(characters_dict):
    print('Выполняем поиск персонажа')
    character = input('Введите ID или Name персонажа: ').strip().lower()

    found_list = []  # ← Ищем всех совпадающих!

    for id, char in characters_dict.items():
        if character in id.lower() or character in char['name'].lower():
            found_list.append((id, char))  # ← Добавляем в список

    if not found_list:  # ← Если пусто
        print(f"❌ Персонаж '{character}' не найден!")
        return

    print(f"\n✅ Найдено: {len(found_list)}")
    for id, char in found_list:  # ← Показываем всех
        print(f"\n👤Имя: {char['name']}")
        print(f"   ID: {id}")
        print(f" ⭐Уровень: {char['level']}")
        print(f" ⚔️Класс: {char['class']}")
        print(f" ❤️Здоровье: {char['health']}")
        print("-" * 30)


def show_statistics(characters):
    """Выводит статистику по персонажам"""
    print("\n" + "=" * 50)
    print("📊 STATISTICS")
    print("=" * 50)

    if not characters:
        print("⚠️ Нет данных для статистики!")
        print("=" * 50)
        return

    # Считаем статистику
    max_level = 0
    max_name = ""
    min_health = float("inf")
    min_name = ""
    total_level = 0
    count = 0

    for key, char in characters.items():
        if char["level"] > max_level:
            max_level = char["level"]
            max_name = char["name"]

        if char["health"] < min_health:
            min_health = char["health"]
            min_name = char["name"]

        total_level += char["level"]
        count += 1

    average_level = round(total_level / count, 2)

    # Выводим
    print(f"\n📈 Total Characters:   {count}")
    print(f"🏆 Max Level:          {max_level} ({max_name})")
    print(f"📊 Average Level:      {average_level}")
    print(f"💚 Min Health:         {min_health} ({min_name})")
    print("=" * 50)
