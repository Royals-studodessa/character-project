# combats.py
import time
import random
from status import StatusEffect
from class_profiles import CLASS_PROFILES

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

    def submit_action(self, player_name, action_type, attack_zones=None, block_zones=None, skills=None, skill_name=None):
        """
        Принимает ход от игрока.
        skill_name: str - Название скилла для МАГОВ (например, "fireball").
        skills: list - Список баффов/карточек для ВОИНОВ (например, ["power_strike"]).
        """
        player = self.players[player_name]
        if not self.is_active:
            return False, "Бой завершён"
        
        if action_type not in ["attack", "skill_only", "defend", "skip"]:
            return False, "Неверный тип действия"
            
        # Для магов: обязателен skill_name
        if "Mage" in (player.char_class or "") and action_type == "skill_only":
            if not skill_name:
                return False, "Маг обязан выбрать заклинание!"

        self.actions[player_name] = {
            "action_type": action_type,
            "attack_zones": list(attack_zones) if attack_zones else list(),
            "block_zones": set(block_zones) if block_zones else set(),
            "skills": skills if skills else [],       # Баффы воина
            "skill_name": skill_name                  # Заклинание мага
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
        """ФАЗОВЫЙ ЦИКЛ ХОДА"""
        print(f"\n🟦 ФАЗА 1: Начало хода (Проверка статусов → Тик)")
        
        for name, player in self.players.items():
            if not player.is_alive: continue

            print(f"  🔄 {name}: проверка статусов...")
            
            # 1. Логируем текущие эффекты ДО тика
            for eff in player.active_effects:
                print(f"  📜 Висит: {eff.name} ({eff.duration} ходов)")

            # 2. Проверяем стан и ставим SKIP
            if player.is_stunned():
                print(f"  😵 {name} оглушён → действие заменено на SKIP!")
                self.actions[name] = {
                    "action_type": "skip",
                    "attack_zones": [],
                    "block_zones": set(),
                    "skills": [],
                    "skill_name": None
                }


            player.tick_effects()

        # Если кто-то умер от тика (например, от кровотечения) → завершаем бой
        for p in self.players.values():
            if not p.is_alive:
                print(f"\n💀 {p.name} погибает от эффектов!")
                self._end_battle()
                return

        print(f"\n🟨 ФАЗА 2: Размен действий")
        
        # 3. ОПРЕДЕЛЯЕМ ПОРЯДОК (Маги → Остальные)
        players_list = list(self.players.values())
        players_list.sort(key=lambda p: 0 if "Mage" in (p.char_class or "") else 1)

        # 4. ВЫПОЛНЯЕМ ДЕЙСТВИЯ
        for attacker in players_list:
            if not attacker.is_alive:
                continue
                
            defender = next(p for p in players_list if p != attacker)
            if not defender.is_alive:
                continue
                
            att_act = self.actions.get(attacker.name, {"action_type": "skip"})
            def_act = self.actions.get(defender.name, {"action_type": "skip"})
            
            # Вызываем расчёт удара
            self._execute_action(attacker, defender, att_act, def_act)

        print(f"\n🟥 ФАЗА 3: Конец хода")
        
        # 5. ПРОВЕРКА СМЕРТИ ПОСЛЕ УДАРОВ
        for p in self.players.values():
            if not p.is_alive:
                print(f"💀 {p.name} погибает в бою!")
                self._end_battle()
                return
                
        # 6. СБРОС ДЕЙСТВИЙ ДЛЯ СЛЕДУЮЩЕГО ХОДАы
        self.actions.clear()
    
    def _end_battle(self):
            """Останавливает бой и выводит победителя"""
            self.is_active = False
            winner = next((p for p in self.players.values() if p.is_alive), None)
            if winner:
                print(f"\n🏆 ПОБЕДИТЕЛЬ: {winner.name}!")
            else:
                print("\n🤝 НИЧЬЯ (оба погибли одновременно)!")       
        
    def _execute_action(self, attacker, defender, att_act, def_act):
        """Полный расчёт боя: Магия (статы+шмот) + Физика (зоны+щит+карты)"""
        if att_act["action_type"] == "skip":
            return

        print(f"\n🎯 {attacker.name} ({attacker.char_class}) атакует {defender.name}...")
        
        # 1. Определяем тип атаки
        is_magic = (att_act["action_type"] == "skill_only") and ("Mage" in (attacker.char_class or ""))
        ignore_block = False
        base_dmg = 0
        attack_zones = []
        max_attacks = 1
        eq_stats = {"passives": [], "num_attacks": 1} # Дефолт для магов

        # ==========================================
        # 🔮 ЛОГИКА МАГА
        # ==========================================
        if is_magic:
            from skills_db import ALL_SKILLS
            magic_skill = ALL_SKILLS.get(att_act.get("skill_name"))

            if not magic_skill:
                print("❌ Скилл не найден в базе!")
                return

            if not magic_skill.can_use(attacker):
                print(f"❌ {attacker.name} не хватает маны или скилл на КД!")
                return

            ignore_block = True
            attack_zones = ["magic"]
            max_attacks = 1

            # 1. Базовый урон скилла
            total_magic_dmg = magic_skill.damage
            
            # 2. Синергия статов (из class_profiles.py)
            from class_profiles import CLASS_PROFILES
            profile = CLASS_PROFILES.get(attacker.char_class.strip(), {})
            synergy = profile.get("stat_synergy", {})
            stat_bonus = sum(attacker._stats.get(stat, 0) * mult for stat, mult in synergy.items())
            total_magic_dmg += stat_bonus

            # 3. Бонусы экипировки (magic_bonus)
            gear_bonus = 0
            for item in attacker.equipment.values():
                if item and item.combat_props.get("magic_bonus"):
                    gear_bonus += item.combat_props["magic_bonus"]
            total_magic_dmg += gear_bonus

            base_dmg = int(total_magic_dmg)
            print(f"🔮 Каст: {magic_skill.name} | База: {magic_skill.damage} | Статы: +{int(stat_bonus)} | Шмот: +{gear_bonus} = Итого: {base_dmg}")

        # ==========================================
        # ⚔️ ЛОГИКА ВОИНА / ФИЗИКА
        # ==========================================
        else:
            eq_stats = attacker.get_equipment_stats()
            max_attacks = eq_stats["num_attacks"]
            attack_zones = list(att_act.get("attack_zones", []))[:max_attacks]
            if not attack_zones: 
                attack_zones = [None]

            # Применяем "Активные карты" воина (баффы к урону)
            from skills_db import ALL_SKILLS
            card_bonus = 0
            for buff_name in att_act.get("skills", []):
                buff = ALL_SKILLS.get(buff_name)
                if buff and buff.damage > 0:
                    card_bonus += buff.damage
                    print(f"💪 Карта '{buff.name}' усиливает атаку на +{buff.damage}!")
            
            # База + карты
            base_dmg = attacker.damage + card_bonus
            
            # Если 2 оружия, делим урон пополам для каждого удара
            if max_attacks == 2:
                base_dmg = int(base_dmg * 0.5)

        # ==========================================
        # ⚔️ ЦИКЛ АТАК И РАСЧЁТ БЛОКА/КРИТА
        # ==========================================
        for i, zone in enumerate(attack_zones, 1):
            display_zone = zone if not is_magic else "BODY"
            print(f"\n  ⚔️ Атака #{i} (зона: {display_zone})")

            # Проверка блока (магия игнорирует)
            is_blocked = False
            if not ignore_block:
                is_blocked = zone in def_act.get("block_zones", set()) if zone else False

            if is_blocked:
                print(f"  🛡️ {defender.name} заблокировал зону '{zone}'!")
            elif not is_magic:
                print(f"  💥 Попадание в открытую зону '{zone}'!")

            # Корректировка для 2-й атаки щитом (берёт 20% от ПОЛНОГО урона персонажа)
            current_dmg = base_dmg
            if not is_magic and max_attacks == 2 and i == 2:
                off_hand = attacker.equipment.get("off_hand")
                if off_hand and off_hand.combat_props.get("is_shield"):
                    current_dmg = int(attacker.damage * 0.2)
                    print(f"  🛡️ Удар щитом (20% от базы = {current_dmg})")

            final_dmg = current_dmg
            log_msg = ""

            # Бросок на крит (только физика)
            is_crit = False
            if not is_magic and "crit_passive" in eq_stats["passives"]:
                is_crit = random.random() < 0.25

            # Математика блока/крита
            if is_blocked and not ignore_block:
                if is_crit:
                    final_dmg = current_dmg  # Крит через блок: x1
                    log_msg = "⚡ КРИТ пробил блок!"
                elif "ranged_pierce" in eq_stats["passives"]:
                    final_dmg = int(current_dmg * 0.5)
                    log_msg = "🏹 Пробивает блок на 50%!"
                else:
                    final_dmg = 0
                    log_msg = "🛡️ Блок полностью поглотил удар."
            elif is_crit and not is_magic:
                final_dmg = int(current_dmg * 2.0)
                log_msg = "⚡ КРИТИЧЕСКИЙ УДАР!"
            else:
                log_msg = "💥 Прямое попадание." if not is_magic else "🔮 Магический прожиг!"

            # Применение урона
            print(f"  {log_msg} Итоговый урон: {final_dmg}")
            if final_dmg > 0:
                defender.take_damage(final_dmg)
            else:
                print(f"  🛡️ Урон полностью поглощён!")

            # Пассивки (только физика)
            if not is_magic:
                if "dual_bleed" in eq_stats["passives"] and not is_blocked and random.random() < 0.05:
                    print(f"  🩸 Сработала пассивка 'Кровотечение'!")
                    defender.apply_status(StatusEffect("Bleed", 5, "damage", 2.5))

                if "shield_stun" in eq_stats["passives"] and max_attacks == 2 and i == 2 and not is_blocked and random.random() < 0.20:
                    print(f"  💥 Удар щитом оглушил!")
                    defender.apply_status(StatusEffect("Stun", 1, "control", 0))

            # Расход маны и запуск КД для мага (только в первой итерации)
            if is_magic and i == 1:
                from skills_db import ALL_SKILLS
                skill = ALL_SKILLS.get(att_act.get("skill_name"))
                attacker.spend_mana(skill.mana_cost)
                attacker.cooldowns.start(skill.name, skill.cooldown_turns)

    def start_battle(self, max_turns=15):
            """Запускает автоматический цикл боя"""
            print("\n⚔️ === НАЧАЛО БОЯ ===")
            turn = 1
            
            while self.is_active and turn <= max_turns:
                print(f"\n{'─'*15} ХОД {turn} {'─'*15}")
                self.resolve_turn()
                if not self.is_active:
                    break
                turn += 1
                
            if self.is_active:
                print("\n⏱️ Превышен лимит ходов. Бой прерван.")
            print("⚔️ === БОЙ ЗАВЕРШЁН ===\n")
