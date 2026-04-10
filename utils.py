import json


def save_to_file(characters_dict, filename="characters.json"):
    """Сохраняет словарь персонажей в JSON файл"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(characters_dict, f, ensure_ascii=False, indent=4)
        print(f"✅ Данные сохранены в {filename}")
    except IOError as e:
        print(f"❌ Ошибка сохранения: {e}")


def load_from_file(filename="characters.json"):
    """Загружает словарь персонажей из JSON файла"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"✅ Данные загружены из {filename}")
        return data
    except FileNotFoundError:
        print("⚠️ Файл не найден, начинаем с пустой базы")
        return {}
    except json.JSONDecodeError:
        print("⚠️ Ошибка чтения файла, начинаем с пустой базы")
        return {}


def get_number(prompt, default=0, max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        try:
            return int(input(prompt))
        except ValueError:
            if attempt == 1:
                print("❌ Это не число! Попробуйте ещё раз:")
            elif attempt == 2:
                print("❌ Снова ошибка! Последняя попытка:")
            else:
                print(f"⚠️ Лимит исчерпан! Значение Будет: {default}")

    return default


def get_string(prompt, default="", max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        value = input(prompt)

        if value.strip():  # Если не пустая строка
            print(f'✅ Результат: {value}')
            return value.strip()

        # Если пустая — показываем ошибку
        if attempt == 1:
            print("❌ Пустая строка! Попробуйте ещё раз:")
        elif attempt == 2:
            print("❌ Снова ошибка! Последняя попытка:")
        else:
            print(f"⚠️ Лимит исчерпан! Значение будет: {default}")

    return default
