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

class CooldownTracker:
    """Отслеживает кулдауны способностей"""
    
    def __init__(self):
        self.cooldowns = {}  # {"ability_name": remaining_turns}
    
    def start(self, ability_name, turns):

        self.cooldowns[ability_name] = turns
        print(f"⏳ {ability_name} на кулдауне {turns} ходов")
    
    def is_ready(self, ability_name):
        """Проверить, готова ли способность к использованию"""

        return True if ability_name not in self.cooldowns or self.cooldowns[ability_name] <= 0 else False
    
    def tick(self):
        """Уменьшить все активные кулдауны на 1 ход (вызывать в конце хода)"""
 
        updated_cooldowns = {}
        
        for ability, turns in self.cooldowns.items():
            new_turns = turns - 1
            
            if new_turns > 0:
                # Если ещё не готово, сохраняем
                updated_cooldowns[ability] = new_turns
            else:
                # Если готово, выводим сообщение и НЕ сохраняем
                print(f"✅ Способность '{ability}' готова к использованию!")
        
        # Заменяем старый словарь новым
        self.cooldowns = updated_cooldowns        
    
    def show(self):
        """Показать активные кулдауны"""
        if not self.cooldowns:
            print("✅ Все способности готовы")
        else:
            print("\n⏳ Активные кулдауны:")
            for ability, turns in self.cooldowns.items():
                print(f"   • {ability}: {turns} ходов")