class Character:
    def __init__(self, name, level, health):
        self.name = name
        self.health = health
        self.level = level

    def display(self):
        print(f"🎯 {self.name}")
        print(f"   Level:  {self.level}")
        print(f"   Health: {self.health}")

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        print(f"💥 {self.name} получил {damage} урона, осталось {self.health} жизни.")


# Тест в конце файла:
if __name__ == "__main__":
    print("=== ТЕСТ CHARACTER ===\n")

    # 1. Создание персонажа
    hero = Character("Royals", 14, 100)
    print("1. Персонаж создан:")
    hero.display()

    # 2. Тест урона
    print("\n2. Тест урона:")
    hero.take_damage(30)
    hero.take_damage(80)  # Должно остаться 0, не -10!

    print("\n=== ТЕСТ ЗАВЕРШЁН ===")
