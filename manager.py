from character import Character


class CharacterManager:
    """Менеджер для управления всеми персонажами"""

    def __init__(self):
        """Инициализация менеджера (пустая база)"""
        self.characters = {}

    def add(self, name, level, char_class, health, mana):
        """Добавить нового персонажа"""
        new_id = f"player{len(self.characters) + 1}"
        new_char = Character(name, level, char_class, health, mana)
        self.characters[new_id] = new_char
        print(f"\n✅ Персонаж {name} добавлен под ID: {new_id}")
        return new_id

    def delete(self, search_term):
        """Удалить персонажа по ID или имени"""
        found_id = None

        for char_id, char in self.characters.items():
            if search_term in char_id or search_term in char.name:
                found_id = char_id
                break

        if found_id:
            deleted = self.characters.pop(found_id)
            print(f"🗑️ Персонаж {deleted.name} удалён")
            return True
        else:
            print(f"❌ Персонаж '{search_term}' не найден")
            return False

    def find(self, search_term):
        """Найти персонажей по ID или имени"""
        found = []

        for char_id, char in self.characters.items():
            if search_term.lower() in char_id.lower() or search_term.lower() in char.name.lower():
                found.append((char_id, char))

        if found:
            print(f"\n✅ Найдено: {len(found)}")
            for char_id, char in found:
                print(f"\n--- {char.name} (ID: {char_id}) ---")
                char.display()
        else:
            print(f"❌ Персонаж '{search_term}' не найден")

        return found

    def display_all(self):
        """Показать всех персонажей"""
        print("\n" + "=" * 50)
        print("📋 ВСЕ ПЕРСОНАЖИ")
        print("=" * 50)

        if not self.characters:
            print("⚠️ База пуста!")
        else:
            for char_id, char in self.characters.items():
                print(f"\n   (ID: {char_id})")
                char.display()

        print("=" * 50)

    def show_statistics(self):
        """Показать статистику"""
        print("\n" + "=" * 50)
        print("📊 СТАТИСТИКА")
        print("=" * 50)

        if not self.characters:
            print("⚠️ Нет данных!")
            return

        max_level = 0
        max_name = ""
        min_health = float("inf")
        min_name = ""
        total_level = 0

        for char in self.characters.values():
            if char.level > max_level:
                max_level = char.level
                max_name = char.name
            if char.health < min_health:
                min_health = char.health
                min_name = char.name
            total_level += char.level

        count = len(self.characters)
        average = round(total_level / count, 2)

        print(f"\n📈 Всего персонажей: {count}")
        print(f"🏆 Макс. уровень:    {max_level} ({max_name})")
        print(f"📊 Средний уровень:  {average}")
        print(f"💚 Мин. здоровье:    {min_health} ({min_name})")
        print("=" * 50)

    def to_dict(self):
        """Преобразовать всех персонажей в словарь"""
        return {
            char_id: char.to_dict()
            for char_id, char in self.characters.items()
        }

    def from_dict(self, data):
        """Загрузить персонажей из словаря"""
        self.characters = {
            char_id: Character.from_dict(char_data)
            for char_id, char_data in data.items()
        }
