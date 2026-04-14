# конструктор предметов

class Item:
    """Базовый класс для всех предметов"""
    def __init__(self, name, weight, value, slot="inventory", combat_props=None):
        self.name = name
        self.weight = weight
        self.value = value
        self.slot = slot  # Куда можно экипировать: "main_hand", "off_hand", "body" и т.д.
        self.combat_props = combat_props or {}  # {"is_shield": True, "stun_chance": 0.2}

    def __str__(self):
        return f"📦 {self.name} | Вес: {self.weight} | Цена: {self.value}"

    def display(self):
        print(f"📦 Предмет: {self.name}, Вес: {self.weight}, Цена: {self.value}")
        
    def to_dict(self):
        return {
            "name": self.name,
            "weight": self.weight,
            "value": self.value,
            "slot": self.slot,
            "combat_props": self.combat_props
        }

    def apply_discount(self, percent):
        old_value = self.value
        new_value = old_value * (percent / 100)
        print(f"💰 Цена со скидкой: {old_value - new_value}")


class Weapon(Item):
    """Класс оружия. Наследуется от Item"""
    def __init__(self, name, weight, value, damage_bonus, slot="main_hand", combat_props=None):
        # Передаём все аргументы родительскому классу
        super().__init__(name, weight, value, slot, combat_props)
        self.damage_bonus = damage_bonus  # Бонус к урону от этого оружия

    def use(self, target):
        print(f"⚔️ Ты ударил {target.name} мечом '{self.name}' на {self.damage_bonus} урона!")
        target.take_damage(self.damage_bonus)

    def equip(self, character):
        character._equip_damage_bonus += self.damage_bonus
        print(f"⚔️ Экипирован: {self.name} (+{self.damage_bonus} урона)")

    def unequip(self, character):
        character._equip_damage_bonus -= self.damage_bonus
        print(f"🔄 Снят: {self.name} (-{self.damage_bonus} урона)")


# --- ЗЕЛЬЕ ---
class Potion(Item):
    def __init__(self, name, weight, value, heal_amount):
        super().__init__(name, weight, value)
        self.heal_amount = heal_amount  # Уникальное свойство зелья

    def use(self, target):
        print(f"🧪 Ты выпил '{self.name}' и восстановил {self.heal_amount} HP!")
        target.heal(self.heal_amount)


class Scroll(Item):
    def __init__(self, name, weight, value, effect_type, power):
        super().__init__(name, weight, value)
        self.effect_type = effect_type  # "damage", "heal"
        self.power = power

    def use(self, target):
        if self.effect_type == "damage":
            print(f"🔥 Свиток '{self.name}' вспыхнул! Нанесено {self.power} урона.")
            target.take_damage(self.power)
        elif self.effect_type == "heal":
            print(f"✨ Свиток '{self.name}' засиял! Восстановлено {self.power} HP.")
            target.heal(self.power)


# Тест:
if __name__ == "__main__":
    sword = Item("Меч", 5, 100)
    sword.display()
    sword.apply_discount(10)
