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
        self.actions.clear()
        self.turn_start_time = time.time()

    # <-- ВАЖНО: Этот метод должен быть ВНУТРИ класса CombatSession (с отступом)
    def _execute_action(self, attacker, defender, att_act, def_act):
        """Расчёт урона с учётом МНОЖЕСТВЕННЫХ атак"""

        if att_act["action_type"] == "skip":
            return

        print(f"\n🎯 {attacker.name} ({attacker.char_class}) атакует {defender.name}...")

        # Определяем, сколько атак будет
        attack_zones = list(att_act["attack_zones"])
        num_attacks = len(attack_zones)

        # Если зон нет — ставим одну пустую атаку
        if num_attacks == 0:
            attack_zones = [None]
            num_attacks = 1

        # === ЦИКЛ ПО ВСЕМ АТАКАМ ===
        for i, zone in enumerate(attack_zones, 1):
            if num_attacks > 1:
                print(f"\n  ⚔️ Атака #{i} (зона: {zone})")

            # 1. Проверяем блок
            is_blocked = False
            if zone and zone in def_act["block_zones"]:
                is_blocked = True
                print(f"  🛡️ {defender.name} заблокировал зону '{zone}'!")
            elif zone:
                print(f"  💥 Попадание в открытую зону '{zone}'!")

            # 2. Расчёт урона
            base_damage = attacker.damage

            # Если атак несколько (2 ножа/меча) → делим урон пополам
            if num_attacks == 2:
                base_damage = int(base_damage * 0.5)

            # Если это ВТОРАЯ атака Танка (щит) → 20% урона
            if num_attacks == 2 and "Tank" in (attacker.char_class or "") and i == 2:
                base_damage = int(attacker.damage * 0.2)
                print(f"  🛡️ Удар щитом на {base_damage} урона")

            # Применяем множители
            if is_blocked:
                final_dmg = int(base_damage * 0.4)
            else:
                final_dmg = base_damage

            # 3. Наносим урон
            if final_dmg > 0:
                defender.take_damage(final_dmg)

            # 4. ПРОВЕРКА ПАССИВОК (для каждой атаки отдельно!)

            # Dodger: кровотечение (если НЕ в блок)
            if "Dodger" in (attacker.char_class or "") and not is_blocked:
                if random.random() < 0.95:  # 5% шанс
                    print(f"  🩸 Сработала пассивка 'Кровотечение'!")
                    bleed = StatusEffect("Bleed", 5, "damage", 2.5)
                    defender.apply_status(bleed)

            # Tank: оглушение (если ВТОРАЯ атака щитом и НЕ в блок)
            if "Tank" in (attacker.char_class or "") and i == 2 and not is_blocked:
                if random.random() < 0.20:  # 20% шанс
                    print(f"  💥 Удар щитом оглушил!")
                    stun = StatusEffect("Stun", 1, "control", 0)
                    defender.apply_status(stun)

            # Crit: пробитие блока (50%)
            if "Crit" in (attacker.char_class or "") and is_blocked:
                if random.random() < 0.05:  # 50% шанс пробить блок
                    print(f"  ⚡ Критический удар пробил блок!")
                    # Наносим дополнительный урон
                    crit_dmg = int(attacker.damage * 0.5)
                    defender.take_damage(crit_dmg)

        # В конце — тик эффектов
        defender.tick_effects()
