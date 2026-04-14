class Skill:
    """Базовый класс для любого умения"""

    def __init__(self, name, mana_cost, cooldown_turns, damage=0, heal=0):
        self.name = name
        self.mana_cost = mana_cost
        self.cooldown_turns = cooldown_turns
        self.damage = damage
        self.heal = heal

    def can_use(self, character):
        """Проверяет, можно ли использовать (мана + кулдаун)"""
        if character.mana < self.mana_cost:
            print(f"❌ Недостаточно маны для {self.name} (нужно {self.mana_cost})")
            return False

        if not character.cooldowns.is_ready(self.name):
            print(f"❌ {self.name} ещё не готово!")
            character.cooldowns.show()
            return False

        return True

    def use(self, character, target):
        """Использовать навык"""
        if not self.can_use(character):
            return False

        # 1. Списываем ману (нужно добавить метод списания маны в Character)
        character.spend_mana(self.mana_cost)

        # 2. Применяем эффект
        if self.damage > 0:
            print(f"🔥 {self.name}: Удар на {self.damage} урона!")
            target.take_damage(self.damage)

        if self.heal > 0:
            print(f"✨ {self.name}: Лечение на {self.heal} HP!")
            target.heal(self.heal)

        # 3. Запускаем кулдаун
        character.cooldowns.start(self.name, self.cooldown_turns)
        return True
