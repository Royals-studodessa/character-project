import json
from items import Weapon, Potion


class ItemManager:
    """Менеджер для управления предметами"""

    def __init__(self):
        """Инициализация менеджера (пустой инвентарь)"""
        self.items = {}

    def load_from_json(self, filename):
        """Загрузить предметы из JSON файла"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.items = {}
            for item_id, item_data in data.items():
                # Создаём правильный тип предмета
                if item_data.get('type') == 'weapon':
                    self.items[item_id] = Weapon(
                        name=item_data['name'],
                        weight=item_data['weight'],
                        value=item_data['value'],
                        damage_bonus=item_data['damage']
                    )
                elif item_data.get('type') == 'potion':
                    self.items[item_id] = Potion(
                        name=item_data['name'],
                        weight=item_data['weight'],
                        value=item_data['value'],
                        heal_amount=item_data['heal_amount']
                    )

            print(f"✅ Загружено {len(self.items)} предметов из {filename}")
            return True

        except FileNotFoundError:
            print(f"❌ Файл {filename} не найден!")
            return False
        except Exception as e:
            print(f"❌ Ошибка при загрузке: {e}")
            return False

    def display_all(self):
        """Показать все предметы"""
        print("\n" + "=" * 50)
        print("📦 ВСЕ ПРЕДМЕТЫ")
        print("=" * 50)

        if not self.items:
            print("⚠️ Инвентарь пуст!")
        else:
            for item_id, item in self.items.items():
                print(f"\n🔹 {item_id}: {item}")

        print("=" * 50)

    def get_item(self, item_id):
        """Получить предмет по ID"""
        return self.items.get(item_id)
