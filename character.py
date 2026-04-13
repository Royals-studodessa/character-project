from systems import ScrollInventory, CooldownTracker
import time
# character.py - Классы для управления персонажами
BASE_STATS = {
    "strength": 10,       # Физ. урон, грузоподъёмность
    "agility": 10,        # Шанс блока, скорость атаки
    "intuition": 8,       # Шанс крита, поиск слабых мест
    "endurance": 10,      # Макс. HP, сопротивление физ. урону
    "intelligence": 8,    # Макс. мана, маг. урон
    "wisdom": 8,          # Регенерация маны, длительность эффектов
    "spirituality": 8     # Сопротивление магии, эффективность лечения
}

class Character:
    """Класс одного персонажа"""
    
    def __init__(self, name, level, char_class, health, mana):
        self.name = name
        self._level = level
        self.char_class = char_class
        self._stats = BASE_STATS.copy()
        self.stat_points = 0  # Свободные очки для распределения
        self.base_damage = 5
        self._equip_damage_bonus = 0  # ← Сумма урона от всей экипировки
        self.scroll_inventory = ScrollInventory(max_slots=10)
        self._current_health = min(health, self.max_health)
        self._current_mana = min(mana, self.max_mana)
        self.cooldowns = CooldownTracker()
        self.last_activity_time = time.time()  # ← Запоминаем время создания/загрузки
   
        # --- РАСЧЁТНЫЕ МАКСИМУМЫ ---
    @property
    def max_health(self):
        base = 100
        level_bonus = self.level * 20        # +20 HP за каждый уровень
        endurance_bonus = self._stats.get("endurance", 0) * 10
        equip_bonus = getattr(self, "_equip_health_bonus", 0)
        return base + level_bonus + endurance_bonus + equip_bonus

    @property
    def max_mana(self):
        base = 50
        level_bonus = self.level * 15        # +15 маны за каждый уровень
        wisdom_bonus = self._stats.get("wisdom", 0) * 8
        equip_bonus = getattr(self, "_equip_mana_bonus", 0)
        return base + level_bonus + wisdom_bonus + equip_bonus

    @property
    def damage(self):
        """Итоговый физический урон: база + сила + уровень"""
        strength_bonus = self._stats.get("strength", 0) * 2
        level_bonus = self.level * 1  # self.level уже через @property
        return self.base_damage + strength_bonus + level_bonus + self._equip_damage_bonus
    
    # --- ТЕКУЩИЕ ЗНАЧЕНИЯ (только чтение) ---
    @property
    def health(self):
        return self._current_health

    @property
    def mana(self):
        return self._current_mana
      
    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        # Уровень не может быть меньше 1
        self._level = max(1, value)
        # Если позже захочешь потолок (например, 100):
        self._level = max(0, min(100, value))   
                
    def display(self):
        """Показать информацию о персонаже"""
        print(f"🎯 {self.name}")
        print(f"   Level:  {self.level}")
        print(f"   Class:  {self.char_class}")
        print(f"   HP:     {self.health}/{self.max_health}")
        print(f"   Mana:   {self.mana}/{self.max_mana}")
        print(f"   Stats:  {self._stats}")
        print(f"   Points: {self.stat_points}")
    
    def to_dict(self):
        """Преобразовать в словарь"""
        return {
            "name": self.name,
            "level": self.level,
            "class": self.char_class,
            "health": self.health,
            "mana": self.mana,
            "stat_points": self.stat_points,
            "stats": self._stats,
            "last_activity_time": self.last_activity_time
        }
    
    @classmethod
    def from_dict(cls, data):
        char = cls(
            name=data["name"],
            level=data["level"],
            char_class=data["class"],
            health=data.get("health", 100),
            mana=data.get("mana", 50)
        )
        # Восстанавливаем статы или берём базовые (для старых сохранений)
        char._stats = data.get("stats", BASE_STATS.copy())
        char.stat_points = data.get("stat_points", 0)
        
        char.last_activity_time = data.get("last_activity_time", time.time())
        char.regenerate_resources()  # ← Вызов здесь!
        
        return char
    
    def take_damage(self, damage):
        self._current_health = max(0, self._current_health - damage)
        print(f"💥 {self.name} получил {damage} урона! HP: {self.health}/{self.max_health}")

    def heal(self, amount):
        self._current_health = min(self.max_health, self._current_health + amount)
        print(f"❤️ {self.name} восстановил {amount} HP. HP: {self.health}/{self.max_health}")
        
    def allocate_stat(self, stat_name: str, amount: int) -> bool:
        if stat_name not in self._stats:
            print(f"❌ Неизвестная характеристика: {stat_name}")
            return False
        if amount <= 0 or amount > self.stat_points:
            print("❌ Недостаточно очков или некорректное значение!")
            return False
        
        self._stats[stat_name] += amount
        self.stat_points -= amount
        
        # При прокачке выносливости/мудрости поднимаем текущие значения
        # но не обрезаем резко, если персонаж был ранен
        if stat_name == "endurance":
            bonus = amount * 10
            self._current_health = min(self.max_health, self._current_health + bonus)
        elif stat_name == "wisdom":
            bonus = amount * 8
            self._current_mana = min(self.max_mana, self._current_mana + bonus)
            
        print(f"✅ +{amount} к {stat_name}. Осталось очков: {self.stat_points}")
        return True 

    def level_up(self):
        """Повысить уровень и выдать очки характеристик"""
        self._level += 1
        self.stat_points += 5  # 5 очков за каждый уровень
        print(f"🎉 Уровень повышен до {self.level}! Получено 5 очков характеристик.")    
        
    def spend_mana(self, amount):
        """Списать ману, если она есть"""
        if self._current_mana >= amount:
            self._current_mana -= amount
            return True
        else:
            # Можно добавить авто-восстановление до 0, если вдруг ушло в минус
            self._current_mana = 0 
            return False

    def regenerate_resources(self):
        """Восстанавливает HP и Ману за прошедшее время"""
        now = time.time()
        elapsed_min = (now - self.last_activity_time) / 60.0
        
        if elapsed_min < 0.05:  # Игнорируем паузы < 3 секунд
            return
            
        printed_any = False
        
        # 🧪 Мана: 20% от максимума в минуту
        mana_regen = self.max_mana * 0.20 * elapsed_min
        if mana_regen > 0.5:  # Показываем, только если восстановилось > 0.5
            self._current_mana = min(self.max_mana, self._current_mana + mana_regen)
            print(f"💧 +{mana_regen:.1f} маны за {elapsed_min:.1f} мин")
            printed_any = True
            
        # ❤️ Здоровье: 20% от максимума в минуту
        hp_regen = self.max_health * 0.20 * elapsed_min
        if hp_regen > 0.5:
            self._current_health = min(self.max_health, self._current_health + hp_regen)
            print(f"❤️ +{hp_regen:.1f} HP за {elapsed_min:.1f} мин")
            printed_any = True
            
        if printed_any:
            print(f"⏱️ Ресурсы обновлены.\n")
            
        # Сбрасываем таймер
        self.last_activity_time = now