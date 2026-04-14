class StatusEffect:

    def __init__(self, name: str, duration: int, effect_type: str, value: float):

        self.name = name
        self.duration = duration
        self.effect_type = effect_type
        self.value = value

    def tick(self, target):

        # 1. Уменьшаем счетчик ходов
        self.duration -= 1

        # 2. Если эффект типа 'damage' (как кровотечение)
        if self.effect_type == "damage":
            # Формула: Макс. здоровье цели * (значение / 100)
            # value = 2.5 (проценты) -> делим на 100 получаем 0.025
            damage_amount = int(target.max_health * (self.value / 100))

            print(f"💧 {target.name} истекает кровью: -{damage_amount} HP ({self.duration} ходов осталось)")
            target.take_damage(damage_amount)

        # 3. Если эффект 'control' (оглушение), урон не наносим, просто логируем
        elif self.effect_type == "control":
            print(f"😵 {target.name} оглушен! ({self.duration} ходов осталось)")

        # 4. Возвращаем True, если эффект еще активен, False — если он закончился
        return self.duration > 0
