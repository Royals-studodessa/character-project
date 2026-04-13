# character_class.py - Классы для управления персонажами
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
            "stats": self._stats 
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
     
class ScrollInventory:
    """Инвентарь свитков с ограничением слотов на поясе"""
    
    def __init__(self, max_slots=10):
        self.max_slots = max_slots
        self.storage = []   # Хранилище (БЕЗ лимита!)
        self.equipped = []  # Пояс (лимит 10)
    
    def add_scroll(self, scroll):
        """Добавить свиток в хранилище (без лимита)"""
        self.storage.append(scroll)  # ← ИСПРАВЛЕНО: добавляем в storage
        print(f"📜 Свиток '{scroll.name}' добавлен в хранилище")
        return True  # ← Да, return нужен для проверки успеха
    
    def equip_scroll(self, scroll):
        """Переложить свиток из хранилища на пояс"""
        # Проверяем, есть ли в хранилище
        if scroll not in self.storage:
            print(f"❌ Свиток '{scroll.name}' не найден в хранилище")
            return False
        
        # Проверяем лимит пояса
        if len(self.equipped) >= self.max_slots:
            print(f"❌ Все слоты экипировки заняты! (макс. {self.max_slots})")
            return False
        
        # Перекладываем
        self.storage.remove(scroll)
        self.equipped.append(scroll)
        print(f"✅ Свиток '{scroll.name}' экипирован в пояс")
        return True
    
    def use_scroll(self, scroll, target):
        """Использовать свиток с пояса"""
        if scroll not in self.equipped:
            print(f"❌ Свиток '{scroll.name}' не на поясе!")
            return False
        
        # Применяем эффект
        scroll.use(target)
        
        # Свиток исчезает
        self.equipped.remove(scroll)
        print(f"🔥 Свиток '{scroll.name}' использован и исчез!")
        return True
    
    def show(self):
        """Показать состояние инвентаря"""
        print(f"\n📚 СВИТКИ: {len(self.equipped)}/{self.max_slots} на поясе")
        print(f"📦 В хранилище: {len(self.storage)}")
        
        if self.equipped:
            print("\n⚡ На поясе:")
            for s in self.equipped:
                print(f"   • {s.name}")
        
        if self.storage:
            print("\n📦 В хранилище:")
            for s in self.storage:
                print(f"   • {s.name}")   
