from systems import ScrollInventory, CooldownTracker
import time
from progression import NEWBIE_SKILLS, MAIN_CLASSES, SUBCLASSES

BASE_STATS = {
    "strength": 10,
    "agility": 10,
    "intuition": 8,
    "endurance": 10,
    "intelligence": 8,
    "wisdom": 8,
    "spirituality": 8
}

class Character:
    def __init__(self, name, level, char_class="Newbie", health=100, mana=50):
        self.name = name
        self._level = level
        self.char_class = char_class
        self._stats = BASE_STATS.copy()
        self.stat_points = 0
        self.base_damage = 5
        
        # ← ЯВНАЯ ИНИЦИАЛИЗАЦИЯ (вместо getattr)
        self._equip_damage_bonus = 0
        self._equip_health_bonus = 0
        self._equip_mana_bonus = 0
        
        self.scroll_inventory = ScrollInventory(max_slots=10)
        self._current_health = min(health, self.max_health)
        self._current_mana = min(mana, self.max_mana)
        self.cooldowns = CooldownTracker()
        self.last_activity_time = time.time()
        
        self.main_class = None
        self.subclass = None
        self.learned_skills = []
        self.skill_points = 0
        
        if char_class == "Newbie":
            self.learned_skills = ["basic_attack"]

    @property
    def max_health(self):
        base = 100
        level_bonus = self.level * 20
        endurance_bonus = self._stats.get("endurance", 0) * 10
        return base + level_bonus + endurance_bonus + self._equip_health_bonus

    @property
    def max_mana(self):
        base = 50
        level_bonus = self.level * 15
        wisdom_bonus = self._stats.get("wisdom", 0) * 8
        return base + level_bonus + wisdom_bonus + self._equip_mana_bonus

    @property
    def damage(self):
        strength_bonus = self._stats.get("strength", 0) * 2
        level_bonus = self.level * 1
        return self.base_damage + strength_bonus + level_bonus + self._equip_damage_bonus

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
        self._level = max(0, min(100, value))

    def display(self):
        print(f"🎯 {self.name}")
        print(f"   Level:  {self.level}")
        print(f"   Class:  {self.char_class}")
        print(f"   HP:     {self.health}/{self.max_health}")
        print(f"   Mana:   {self.mana}/{self.max_mana}")
        print(f"   Stats:  {self._stats}")
        print(f"   Points: {self.stat_points}")

    def to_dict(self):
        return {
            "name": self.name,
            "level": self.level,
            "class": self.char_class,
            "health": self.health,
            "mana": self.mana,
            "stat_points": self.stat_points,
            "stats": self._stats,
            "main_class": self.main_class,
            "learned_skills": self.learned_skills,
            "last_activity_time": self.last_activity_time
        }

    @classmethod
    def from_dict(cls, data):
        char = cls(
            name=data["name"],
            level=data["level"],
            char_class=data.get("class", "Newbie"),
            health=data.get("health", 100),
            mana=data.get("mana", 50)
        )
        char._stats = data.get("stats", BASE_STATS.copy())
        char.stat_points = data.get("stat_points", 0)       
        char.last_activity_time = data.get("last_activity_time", time.time())
        char.main_class = data.get("main_class")
        char.learned_skills = data.get("learned_skills", [])
        
        if char.main_class:
            char.char_class = char.main_class
        
        # ← ИСПРАВЛЕНО: silent=True
        char.regenerate_resources(silent=True)
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
        
        if stat_name == "endurance":
            bonus = amount * 10
            self._current_health = min(self.max_health, self._current_health + bonus)
        elif stat_name == "wisdom":
            bonus = amount * 8
            self._current_mana = min(self.max_mana, self._current_mana + bonus)
        
        print(f"✅ +{amount} к {stat_name}. Осталось очков: {self.stat_points}")
        return True 

    def level_up(self):
        self._level += 1
        self.stat_points += 5
        print(f"🎉 Уровень повышен до {self.level}! Получено 5 очков характеристик.")    
    
    def spend_mana(self, amount):
        if self._current_mana >= amount:
            self._current_mana -= amount
            return True
        else:
            self._current_mana = 0 
            return False

    def regenerate_resources(self, silent=False):
        now = time.time()
        elapsed_min = (now - self.last_activity_time) / 60.0
        
        if elapsed_min < 0.05:
            return
        
        printed_any = False
        
        mana_regen = self.max_mana * 0.20 * elapsed_min
        if mana_regen > 0.5 and not silent:  # ← ПРОВЕРКА silent
            self._current_mana = min(self.max_mana, self._current_mana + mana_regen)
            print(f"💧 +{mana_regen:.1f} маны за {elapsed_min:.1f} мин")
            printed_any = True
        
        hp_regen = self.max_health * 0.20 * elapsed_min
        if hp_regen > 0.5 and not silent:  # ← ПРОВЕРКА silent
            self._current_health = min(self.max_health, self._current_health + hp_regen)
            print(f"❤️ +{hp_regen:.1f} HP за {elapsed_min:.1f} мин")
            printed_any = True
        
        if printed_any:
            print(f"⏱️ Ресурсы обновлены.\n")
        
        self.last_activity_time = now
    
    def can_choose_main_class(self):
        """Проверяет, можно ли выбрать основной класс"""
        if self.level < 4:
            print(f"❌ Основной класс доступен с 4 уровня (сейчас {self.level})")
            return False
        if self.main_class:
            print(f"❌ Основной класс уже выбран: {self.main_class}")
            return False
        return True
    
    def choose_main_class(self, class_name):
        """Выбор основного класса (Warrior/Mage/Archer)"""
        if not self.can_choose_main_class():
            return False
        
        if class_name not in MAIN_CLASSES:
            print(f"❌ Неизвестный класс: {class_name}")
            print(f"Доступны: {', '.join(MAIN_CLASSES.keys())}")
            return False
        
        # Проверяем требования к статам
        reqs = MAIN_CLASSES[class_name]["stat_requirements"]
        for stat, value in reqs.items():
            if self._stats.get(stat, 0) < value:
                print(f"❌ Не хватает {stat}: нужно {value}, есть {self._stats.get(stat, 0)}")
                return False
        
        # Применяем класс
        self.main_class = class_name
        self.char_class = class_name  # ← ОБЯЗАТЕЛЬНО обновляем метку!
        print(f"✅ Класс изменён на: {self.char_class}")
                
        # Даем первый скилл класса
        first_skill = list(MAIN_CLASSES[class_name]["skills"].keys())[0]
        self.learned_skills.append(first_skill)
        
        print(f"✅ Выбран класс: {class_name}!")
        print(f"📚 Изучен навык: {MAIN_CLASSES[class_name]['skills'][first_skill]['name']}")
        return True
    
    def can_learn_skill(self, skill_name):
        """Проверяет, можно ли изучить навык"""
        # Определяем, к какому классу относится скилл
        skill_class = None
        skill_data = None
        
        # Ищем в скиллах основного класса
        if self.main_class and self.main_class in MAIN_CLASSES:
            if skill_name in MAIN_CLASSES[self.main_class]["skills"]:
                skill_class = self.main_class
                skill_data = MAIN_CLASSES[self.main_class]["skills"][skill_name]
        
        # Если не нашли, проверяем Newbie скиллы
        if not skill_data and skill_name in NEWBIE_SKILLS:
            skill_class = "Newbie"
            skill_data = NEWBIE_SKILLS[skill_name]
        
        if not skill_data:
            print(f"❌ Навык '{skill_name}' не найден или недоступен вашему классу")
            return False
        
        # Проверяем уровень
        if self.level < skill_data.get("level_req", 0):
            print(f"❌ Нужен уровень {skill_data['level_req']} (сейчас {self.level})")
            return False
        
        # Проверяем, не изучен ли уже
        if skill_name in self.learned_skills:
            print(f"⚠️ Навык '{skill_name}' уже изучен")
            return False
        
        # Проверяем требования к статам
        if "stat_req" in skill_data:
            for stat, value in skill_data["stat_req"].items():
                if self._stats.get(stat, 0) < value:
                    print(f"❌ Не хватает {stat}: нужно {value}, есть {self._stats.get(stat, 0)}")
                    return False
        
        # Проверяем, не мультиклассинг ли (если скилл из другого основного класса)
        if skill_class != "Newbie" and skill_class != self.main_class:
            print(f"❌ Нельзя изучать навыки класса {skill_class} будучи {self.main_class}")
            return False
        
        return True
    
    def learn_skill(self, skill_name):
        """Изучить навык"""
        if not self.can_learn_skill(skill_name):
            return False
        
        self.learned_skills.append(skill_name)
        
        # Определяем источник скилла
        if skill_name in NEWBIE_SKILLS:
            skill_data = NEWBIE_SKILLS[skill_name]
        elif self.main_class in MAIN_CLASSES:
            skill_data = MAIN_CLASSES[self.main_class]["skills"].get(skill_name, {})
        else:
            skill_data = {}
        
        print(f"✅ Изучен навык: {skill_data.get('name', skill_name)}")
        return True
    
    def can_choose_subclass(self):
        """Проверяет, можно ли выбрать специализацию"""
        if self.level < 10:
            print(f"❌ Специализация доступна с 10 уровня (сейчас {self.level})")
            return False
        if self.subclass:
            print(f"❌ Специализация уже выбрана: {self.subclass}")
            return False
        if not self.main_class:
            print("❌ Сначала выберите основной класс")
            return False
        return True
    
    def get_available_subclasses(self):
        """Получает доступные подклассы для текущего основного класса"""
        if not self.main_class or self.main_class not in MAIN_CLASSES:
            return []
        
        available = []
        for subclass_name in MAIN_CLASSES[self.main_class]["subclasses"]:
            if subclass_name in SUBCLASSES:
                available.append(subclass_name)
        
        return available
    
    def choose_subclass(self, subclass_name):
        """Выбор специализации"""
        if not self.can_choose_subclass():
            return False
        
        if subclass_name not in SUBCLASSES:
            print(f"❌ Неизвестная специализация: {subclass_name}")
            return False
        
        subclass_data = SUBCLASSES[subclass_name]
        
        # Проверяем требования к статам
        for stat, value in subclass_data["stat_requirements"].items():
            if self._stats.get(stat, 0) < value:
                print(f"❌ Не хватает {stat}: нужно {value}, есть {self._stats.get(stat, 0)}")
                return False
        
        # Проверяем требуемые скиллы
        for req_skill in subclass_data.get("required_skills", []):
            if req_skill not in self.learned_skills:
                print(f"❌ Требуется навык: {req_skill}")
                return False
        
        # Применяем специализацию
        self.subclass = subclass_name
        self.char_class = subclass_name  # ← ОБЯЗАТЕЛЬНО обновляем метку!
        print(f"✅ Специализация изменена на: {self.char_class}")
        
        # Применяем бонусы к статам
        for stat, bonus in subclass_data.get("bonus_stats", {}).items():
            self._stats[stat] = self._stats.get(stat, 0) + bonus
        
        print(f"✅ Выбрана специализация: {subclass_name}!")
        print(f"📖 {subclass_data['description']}")
        print(f"📈 Бонусы к характеристикам: {subclass_data.get('bonus_stats', {})}")
        return True
    
    def get_progression_info(self):
        """Показывает информацию о прогрессии персонажа"""
        print(f"\n📊 ПРОГРЕССИЯ: {self.name}")
        print(f"   Уровень: {self.level}")
        print(f"   Класс: {self.char_class}")
        if self.main_class:
            print(f"   Основная ветка: {self.main_class}")
        if self.subclass:
            print(f"   Специализация: {self.subclass}")
        
        print(f"\n📚 Изученные навыки ({len(self.learned_skills)}):")
        for skill in self.learned_skills:
            # Ищем данные скилла
            skill_name = skill
            if skill in NEWBIE_SKILLS:
                skill_name = NEWBIE_SKILLS[skill]["name"]
            elif self.main_class and self.main_class in MAIN_CLASSES:
                if skill in MAIN_CLASSES[self.main_class]["skills"]:
                    skill_name = MAIN_CLASSES[self.main_class]["skills"][skill]["name"]
            print(f"   • {skill_name}")
        
        # Показываем доступные опции
        if self.level >= 4 and not self.main_class:
            print(f"\n🎯 Доступен выбор основного класса!")
            print(f"   Варианты: {', '.join(MAIN_CLASSES.keys())}")
        
        if self.level >= 10 and not self.subclass and self.main_class:
            available = self.get_available_subclasses()
            if available:
                print(f"\n🎯 Доступен выбор специализации!")
                print(f"   Варианты: {', '.join(available)}")