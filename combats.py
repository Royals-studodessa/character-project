# combats.py
import time
import random
from status import StatusEffect

VALID_ZONES = {"head", "torso", "waist", "legs"}


class CombatAction:
    """Контейнер для хранения выбора игрока"""

    def __init__(self, player_name, action_type, attack_zones=None, block_zones=None, skills=None):
        self.player_name = player_name
        self.action_type = action_type
        self.attack_zones = set(attack_zones) if attack_zones else set()  # ← СПИСОК → SET
        self.block_zones = set(block_zones) if block_zones else set()
        self.skills = skills if skills else []


class CombatSession:
    """Управление боем (Серверная логика)"""

    def __init__(self, player1, player2, timeout_sec=60):
        self.players = {player1.name: player1, player2.name: player2}
        self.actions = {}
        self.timeout = timeout_sec
        self.turn_start_time = time.time()
        self.is_active = True

    def submit_action(self, player_name, action_type, attack_zones=None, block_zones=None, skills=None):
        """Принимает ход от игрока"""
        if not self.is_active:
            return False, "Бой завершён"

        if action_type not in ["attack", "skill_only", "defend", "skip"]:
            return False, "Неверный тип действия"

        self.actions[player_name] = {
            "action_type": action_type,
            "attack_zones": set(attack_zones) if attack_zones else set(),
            "block_zones": set(block_zones) if block_zones else set(),
            "skills": skills if skills else []
        }
        return True, "✅ Ход принят"

    def check_timeout_and_finalize(self):
        """Проверяет таймаут и ставит SKIP молчунам"""
        elapsed = time.time() - self.turn_start_time
        for name in self.players:
            if name not in self.actions:
                if elapsed >= self.timeout:
                    self.actions[name] = {
                        "action_type": "skip",
                        "attack_zone": None,
                        "block_zones": set(),
                        "skills": []
                    }
                    print(f"⏳ {name} не ответил вовремя → пропускает ход!")
        return len(self.actions) == len(self.players)

    def resolve_turn(self):
        """Разрешает ходы с учетом приоритета Магов"""
        if not self.check_timeout_and_finalize():
            print("⏳ Ждём действий обоих игроков...")
            return

        print("\n⚔️ --- РАЗРЕШЕНИЕ ХОДА ---")

        names = list(self.players.keys())
        p1 = self.players[names[0]]
        p2 = self.players[names[1]]
        act1 = self.actions[names[0]]
        act2 = self.actions[names[1]]

        # Определяем типы классов для приоритета
        p1_is_mage = "Mage" in (p1.char_class or "")
        p2_is_mage = "Mage" in (p2.char_class or "")

        # Сценарий А: Маг против Воина (Приоритет у Мага)
        if p1_is_mage and not p2_is_mage:
            print("🔮 Маг имеет приоритет! Каст летит первым.")
            if act1["action_type"] != "skip":
                self._execute_action(p1, p2, act1, act2)
            if p2.health <= 0:
                print(f"💀 {p2.name} испепелен мгновенно! Он не успел ответить.")
            elif act2["action_type"] != "skip":
                self._execute_action(p2, p1, act2, act1)

        elif p2_is_mage and not p1_is_mage:
            print("🔮 Маг имеет приоритет! Каст летит первым.")
            if act2["action_type"] != "skip":
                self._execute_action(p2, p1, act2, act1)
            if p1.health <= 0:
                print(f"💀 {p1.name} испепелен мгновенно! Он не успел ответить.")
            elif act1["action_type"] != "skip":
                self._execute_action(p1, p2, act1, act2)

        # Сценарий Б: Два воина / Два мага (Одновременный обмен)
        else:
            print("⚔️ Оружие скрещивается! Удары наносятся одновременно.")
            if act1["action_type"] != "skip":
                self._execute_action(p1, p2, act1, act2)
            if act2["action_type"] != "skip":
                self._execute_action(p2, p1, act2, act1)

        print("⚔️ --- ХОД ЗАВЕРШЁН ---\n")
        
        for p in self.players.values():
            p.tick_effects()
            
        self.actions.clear()
        self.turn_start_time = time.time()

    def _execute_action(self, attacker, defender, att_act, def_act):
        """Полный расчёт боя: Зоны, Урон, Крит, Пассивки"""
        if att_act["action_type"] == "skip":
            return

        print(f"\n🎯 {attacker.name} ({attacker.char_class}) атакует {defender.name}...")
        
        # 1. Получаем статы экипировки (сколько атак можно сделать)
        eq_stats = attacker.get_equipment_stats()
        max_attacks = eq_stats["num_attacks"]
        
        # 2. Берём зоны атаки (не больше, чем позволяет оружие)
        attack_zones = list(att_act["attack_zones"])[:max_attacks]
        if not attack_zones:
            attack_zones = [None]
            
        # 3. Цикл по ударам
        for i, zone in enumerate(attack_zones, 1):
            print(f"\n  ⚔️ Атака #{i} (зона: {zone})")
            
            # --- Проверка попадания в блок ---
            is_blocked = zone in def_act["block_zones"] if zone else False
            if is_blocked:
                print(f"  🛡️ {defender.name} заблокировал зону '{zone}'!")
            else:
                print(f"  💥 Попадание в открытую зону '{zone}'!")
            
            # --- Расчёт базового урона ---
            base_strike = attacker.damage
            off_hand = attacker.equipment.get("off_hand")

            # Если атак 2 (двуручность или щит)
            if max_attacks == 2:
                # Логика ЩИТА: 2-я атака = 20% урона
                if i == 2 and off_hand and off_hand.combat_props.get("is_shield"):
                    base_strike = int(attacker.damage * 0.2)
                    print(f"  🛡️ Удар щитом (20% от базы = {base_strike})")
                # Логика ДВУХ ОРУЖИЙ (ножи/мечи): делим урон пополам (50%)
                else:
                    base_strike = int(attacker.damage * 0.5)
            
            final_dmg = 0
            log_msg = ""
            
            # --- Бросок на КРИТ ---
            is_crit = "crit_passive" in eq_stats["passives"] and random.random() < 0.25
            
            # --- ФИНАЛЬНАЯ МАТЕМАТИКА ---
            if is_blocked:
                if is_crit:
                    final_dmg = base_strike  # Крит через блок: x1
                    log_msg = "⚡ КРИТ пробил блок!"
                elif "ranged_pierce" in eq_stats["passives"]:
                    final_dmg = int(base_strike * 0.5)  # Стрелок
                    log_msg = "🏹 Стрела прошивает блок!"
                else:
                    final_dmg = 0  # Обычный блок (Танк/Воин)
                    log_msg = "🛡️ Блок полностью поглотил удар."
            else:
                if is_crit:
                    final_dmg = int(base_strike * 2.0)  # Крит в открытую: x2
                    log_msg = "⚡ КРИТИЧЕСКИЙ УДАР!"
                else:
                    final_dmg = base_strike
                    log_msg = "💥 Прямое попадание."
            
            # ==========================================
            # 🔴 ВЫВОД РЕЗУЛЬТАТА (Этого не было в логе!)
            # ==========================================
            print(f"  {log_msg} Итоговый урон: {final_dmg}")
            
            if final_dmg > 0:
                defender.take_damage(final_dmg)
            else:
                print(f"  🛡️ Урон полностью поглощён!")
            
            # --- ПАССИВКИ ---
            # 1. Кровотечение (Доджер / 2 ножа) - только в ОТКРЫТУЮ зону
            if "dual_bleed" in eq_stats["passives"] and not is_blocked:
                if random.random() < 0.05:
                    print(f"  🩸 Сработала пассивка 'Кровотечение'!")
                    bleed = StatusEffect("Bleed", 5, "damage", 2.5)
                    defender.apply_status(bleed)
                    
            # 2. Оглушение (Танк / Щит) - только ВТОРЫМ ударом и в ОТКРЫТУЮ
            if "shield_stun" in eq_stats["passives"] and max_attacks == 2 and i == 2 and not is_blocked:
                if random.random() < 0.20:
                    print(f"  💥 Удар щитом оглушил!")
                    stun = StatusEffect("Stun", 1, "control", 0)
                    defender.apply_status(stun)

        # Тикаем эффекты в конце хода
        # defender.tick_effects()