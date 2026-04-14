# конструктор предметов

class Item:

    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value

    def __str__(self):
        return f"📦 {self.name} | Вес: {self.weight} | Цена: {self.value}"

    def display(self):
        print(f"Персонаж подобрал предмет {self.name}, вес предмета {self.weight}, цена предмета {self.value}")

    def to_dict(self):
        return {
            "name": self.name,
            "weight": self.weight,
            "value": self.value,
        }

    def apply_discount(self, percent):
        old_value = self.value
        new_value = old_value * (percent / 100)

        print(f" цена со скидкой будет {old_value - new_value}")


# --- МЕЧ ---
class Weapon(Item):
    def __init__(self, name, weight, value, damage_bonus):
        # super() вызывает __init__ от родителя (Item)
        super().__init__(name, weight, value)
        self.damage_bonus = damage_bonus  # Уникальное свойство оружия

    def use(self, target):
        print(f"⚔️ Ты ударил {target.name} мечом '{self.name}' на {self.damage_bonus} урона!")
        target.take_damage(self.damage_bonus)

    def equip(self, character):
        character._equip_damage_bonus += self.damage_bonus
        print(f"⚔️ Экипирован {self.name} (+{self.damage_bonus} урона)")

    def unequip(self, character):
        character._equip_damage_bonus -= self.damage_bonus
        print(f"🔄 Снят {self.name} (-{self.damage_bonus} урона)")


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
