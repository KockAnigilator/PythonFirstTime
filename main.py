import os
import random
import sys
import json

class InstanceCounter:
    """Класс для подсчета экземпляров других классов с сохранением в JSON"""
    
    _instance = None
    _counters = {}
    _filename = "instance_count.json"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InstanceCounter, cls).__new__(cls)
            cls._load_from_file()
        return cls._instance
    
    @classmethod
    def increment(cls, class_name):
        if class_name not in cls._counters:
            cls._counters[class_name] = 0
        cls._counters[class_name] += 1
        cls._save_to_file()
    
    @classmethod
    def decrement(cls, class_name):
        if class_name in cls._counters:
            cls._counters[class_name] = max(0, cls._counters[class_name] - 1)
            cls._save_to_file()
    
    @classmethod
    def get_count(cls, class_name):
        return cls._counters.get(class_name, 0)
    
    @classmethod
    def get_all_counts(cls):
        return cls._counters.copy()
    
    @classmethod
    def _save_to_file(cls):
        try:
            with open(cls._filename, 'w', encoding='utf-8') as f:
                json.dump(cls._counters, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Ошибка сохранения счетчиков: {e}")
    
    @classmethod
    def _load_from_file(cls):
        try:
            if os.path.exists(cls._filename):
                with open(cls._filename, 'r', encoding='utf-8') as f:
                    cls._counters = json.load(f)
        except Exception as e:
            print(f"❌ Ошибка загрузки счетчиков: {e}")
            cls._counters = {}
    
    @classmethod
    def reset_counters(cls):
        cls._counters = {}
        cls._save_to_file()
    
    def __str__(self):
        return f"InstanceCounter: {self._counters}"

class CountedUnit:
    """Базовый класс для юнитов с подсчетом экземпляров"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        InstanceCounter.increment(self.__class__.__name__)
    
    def __del__(self):
        InstanceCounter.decrement(self.__class__.__name__)

class SimpleUnit(CountedUnit):
    """Упрощенный класс юнита с подсчетом экземпляров"""
    
    def __init__(self, name, health=100, attack=10, armor=5, move_range=1):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.armor = armor
        self.move_range = move_range
        self.x = None
        self.y = None
        self.base = None
        super().__init__()
    
    def set_position(self, x, y):
        self.x = x
        self.y = y
    
    def get_position(self):
        return (self.x, self.y)
    
    def is_alive(self):
        return self.health > 0
    
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.armor)
        self.health -= actual_damage
        return actual_damage
    
    def move(self, new_x, new_y):
        distance = abs(new_x - self.x) + abs(new_y - self.y)
        if distance <= self.move_range:
            self.x, self.y = new_x, new_y
            return True
        return False
    
    def __str__(self):
        return f"{self.name} (HP: {self.health}, ATK: {self.attack})"

class SimpleGameField:
    """Упрощенное игровое поле"""
    
    def __init__(self, width=10, height=10, max_units=20):
        self.width = width
        self.height = height
        self.max_units = max_units
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.units = []
        self.bases = []
    
    def add_unit(self, unit, x, y):
        if len(self.units) >= self.max_units:
            print(f"❌ Максимум юнитов: {self.max_units}")
            return False
        
        if not (0 <= x < self.width and 0 <= y < self.height):
            print(f"❌ Неверные координаты: ({x}, {y})")
            return False
        
        if self.grid[y][x] is not None:
            print(f"❌ Клетка ({x}, {y}) занята")
            return False
        
        unit.set_position(x, y)
        self.grid[y][x] = unit
        self.units.append(unit)
        print(f"✅ {unit.name} добавлен на ({x}, {y})")
        return True
    
    def add_base(self, base, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        
        if self.grid[y][x] is not None:
            return False
        
        base.set_position(x, y)
        self.grid[y][x] = base
        self.bases.append(base)
        return True
    
    def display(self):
        print(f"\n🎮 ПОЛЕ {self.width}x{self.height}")
        print("   " + " ".join(f"{i:2}" for i in range(self.width)))
        
        for y in range(self.height):
            row = f"{y:2} "
            for x in range(self.width):
                cell = self.grid[y][x]
                if isinstance(cell, SimpleUnit):
                    if "вражеский" in cell.name.lower():
                        row += "[E]"
                    else:
                        row += "[U]"
                elif hasattr(cell, 'name') and 'база' in cell.name.lower():
                    if "вражеская" in cell.name.lower():
                        row += "[B]"
                    else:
                        row += "[H]"
                else:
                    row += " . "
            print(row)
        
        print("\n📊 Статистика:")
        print(f"  Юнитов: {len(self.units)}/{self.max_units}")
        print(f"  Баз: {len(self.bases)}")
        
        if self.units:
            print("\n👥 Юниты на поле:")
            for unit in self.units:
                x, y = unit.get_position()
                side = "Враг" if "вражеский" in unit.name.lower() else "Игрок"
                print(f"  - {unit.name} ({side}) на ({x}, {y}) - HP: {unit.health}")

class SimpleBase:
    """Упрощенная база"""
    
    def __init__(self, name):
        self.name = name
        self.health = 500
        self.resources = 200
        self.owned_units = []
        self.x = None
        self.y = None
    
    def set_position(self, x, y):
        self.x = x
        self.y = y
    
    def get_position(self):
        return (self.x, self.y)
    
    def create_unit(self, unit_type, game_field):
        unit_types = {
            'warrior': SimpleUnit("Воин", 120, 15, 10),
            'archer': SimpleUnit("Лучник", 80, 20, 5, 2),
            'knight': SimpleUnit("Рыцарь", 150, 25, 15)
        }
        
        if unit_type not in unit_types:
            print(f"❌ Неизвестный тип: {unit_type}")
            return False
        
        if self.resources < 100:
            print("❌ Недостаточно ресурсов")
            return False
        
        unit = unit_types[unit_type]
        
        if "вражеская" in self.name.lower():
            unit.name = "Вражеский " + unit.name.lower()
        
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                spawn_x, spawn_y = self.x + dx, self.y + dy
                if (0 <= spawn_x < game_field.width and 
                    0 <= spawn_y < game_field.height and 
                    game_field.grid[spawn_y][spawn_x] is None):
                    
                    if game_field.add_unit(unit, spawn_x, spawn_y):
                        self.owned_units.append(unit)
                        unit.base = self
                        self.resources -= 100
                        print(f"✅ Создан {unit.name}, ресурсов осталось: {self.resources}")
                        return True
        
        print("❌ Нет места для спавна")
        return False
    
    def get_status(self):
        return f"{self.name}: ❤️ {self.health} 💰 {self.resources} 👥 {len(self.owned_units)}"

class EnemyAI:
    """Простой ИИ для вражеской базы"""
    
    def __init__(self, game):
        self.game = game
        self.aggression = 0.4
    
    def take_turn(self):
        if not self.game.enemy_base or self.game.enemy_base.resources < 100:
            return
        
        if random.random() < self.aggression and len(self.game.enemy_base.owned_units) < 5:
            unit_type = random.choice(['warrior', 'archer', 'knight'])
            self.game.enemy_base.create_unit(unit_type, self.game.field)
        
        player_units = [u for u in self.game.field.units if u not in self.game.enemy_base.owned_units]
        enemy_units = [u for u in self.game.field.units if u in self.game.enemy_base.owned_units]
        
        if player_units and enemy_units and random.random() < self.aggression:
            attacker = random.choice(enemy_units)
            target = random.choice(player_units)
            self.attack(attacker, target)
    
    def attack(self, attacker, target):
        damage = max(1, attacker.attack - target.armor)
        target.take_damage(damage)
        print(f"⚔️ {attacker.name} атакует {target.name} и наносит {damage} урона!")
        
        if not target.is_alive():
            print(f"💀 {target.name} уничтожен!")
            x, y = target.get_position()
            self.game.field.grid[y][x] = None
            self.game.field.units.remove(target)
            if target.base:
                target.base.owned_units.remove(target)

class SimpleGame:
    """Улучшенная игра с системой подсчета экземпляров"""
    
    def __init__(self):
        self.field = None
        self.turn_count = 0
        self.enemy_base = None
        self.enemy_ai = EnemyAI(self)
    
    def initialize(self):
        print("\n🎮 ИНИЦИАЛИЗАЦИЯ ИГРЫ")
        
        width = 8
        height = 8
        self.field = SimpleGameField(width, height)
        
        base = SimpleBase("Главная база")
        self.field.add_base(base, 1, 1)
        
        self.enemy_base = SimpleBase("Вражеская база")
        self.field.add_base(self.enemy_base, 6, 6)
        
        warrior = SimpleUnit("Воин")
        self.field.add_unit(warrior, 2, 2)
        base.owned_units.append(warrior)
        warrior.base = base
        
        enemy_warrior = SimpleUnit("Вражеский воин")
        self.field.add_unit(enemy_warrior, 5, 5)
        self.enemy_base.owned_units.append(enemy_warrior)
        enemy_warrior.base = self.enemy_base
        
        print("✅ Игра инициализирована!")
        print("🎯 Цель: уничтожить вражескую базу!")
    
    def show_instance_counters_menu(self):
        """Меню для работы со счетчиками экземпляров"""
        while True:
            print(f"\n📊 СИСТЕМА ПОДСЧЕТА ЭКЗЕМПЛЯРОВ")
            print("=" * 40)
            print("1. Показать текущие счетчики")
            print("2. Сохранить счетчики в файл")
            print("3. Загрузить счетчики из файла")
            print("4. Сбросить все счетчики")
            print("5. Назад в главное меню")
            
            choice = input("Выберите действие: ")
            
            if choice == '1':
                self.show_instance_counters()
            elif choice == '2':
                InstanceCounter._save_to_file()
                print("✅ Счетчики сохранены в файл instance_count.json")
            elif choice == '3':
                InstanceCounter._load_from_file()
                print("✅ Счетчики загружены из файла")
                self.show_instance_counters()
            elif choice == '4':
                self.reset_instance_counters()
            elif choice == '5':
                break
            else:
                print("❌ Неверный выбор")
    
    def show_instance_counters(self):
        """Показать текущие счетчики экземпляров"""
        counters = InstanceCounter.get_all_counts()
        print(f"\n📈 СТАТИСТИКА ЭКЗЕМПЛЯРОВ:")
        if counters:
            total = 0
            for class_name, count in counters.items():
                print(f"  {class_name}: {count} экз.")
                total += count
            print(f"  Всего: {total} экземпляров")
        else:
            print("  Нет данных")
    
    def reset_instance_counters(self):
        """Сбросить все счетчики"""
        confirm = input("⚠️  Вы уверены, что хотите сбросить все счетчики? (y/n): ")
        if confirm.lower() == 'y':
            InstanceCounter.reset_counters()
            print("✅ Все счетчики сброшены")
        else:
            print("❌ Сброс отменен")
    
    def show_menu(self):
        while True:
            print(f"\n{'='*40}")
            print(f"🎮 ХОД {self.turn_count}")
            print(f"{'='*40}")
            print("1. Показать поле")
            print("2. Создать юнита")
            print("3. Переместить юнита") 
            print("4. Атаковать")
            print("5. Следующий ход")
            print("6. Статус игры")
            print("7. 📊 Управление счетчиками")
            print("8. Выход")
            
            choice = input("Выберите действие: ")
            
            if choice == '1':
                self.field.display()
            elif choice == '2':
                self.create_unit()
            elif choice == '3':
                self.move_unit()
            elif choice == '4':
                self.attack_menu()
            elif choice == '5':
                self.next_turn()
            elif choice == '6':
                self.show_status()
            elif choice == '7':
                self.show_instance_counters_menu()
            elif choice == '8':
                InstanceCounter._save_to_file()
                print("👋 До свидания! Счетчики сохранены.")
                break
            else:
                print("❌ Неверный выбор")
    
    def create_unit(self):
        if not self.field.bases:
            print("❌ Нет баз на поле")
            return
        
        base = self.field.bases[0]
        print("\n🏭 СОЗДАНИЕ ЮНИТА")
        print("1. Воин (100 ресурсов) - сильная атака, броня")
        print("2. Лучник (100 ресурсов) - дальняя атака") 
        print("3. Рыцарь (100 ресурсов) - много здоровья")
        
        unit_types = {'1': 'warrior', '2': 'archer', '3': 'knight'}
        choice = input("Выберите тип юнита: ")
        
        if choice in unit_types:
            base.create_unit(unit_types[choice], self.field)
        else:
            print("❌ Неверный выбор")
    
    def move_unit(self):
        if not self.field.units:
            print("❌ Нет юнитов на поле")
            return
        
        player_units = [u for u in self.field.units if u in self.field.bases[0].owned_units]
        if not player_units:
            print("❌ Нет ваших юнитов для перемещения")
            return
        
        print("\n🎯 ПЕРЕМЕЩЕНИЕ ЮНИТА")
        for i, unit in enumerate(player_units):
            x, y = unit.get_position()
            print(f"{i+1}. {unit.name} на ({x}, {y}) - дальность: {unit.move_range}")
        
        try:
            idx = int(input("Выберите юнита: ")) - 1
            if 0 <= idx < len(player_units):
                unit = player_units[idx]
                current_x, current_y = unit.get_position()
                
                print(f"\n📍 Текущая позиция: ({current_x}, {current_y})")
                print(f"🎯 Дальность перемещения: {unit.move_range} клеток")
                
                x = int(input("Новая координата X: "))
                y = int(input("Новая координата Y: "))
                
                distance = abs(x - current_x) + abs(y - current_y)
                if distance > unit.move_range:
                    print(f"❌ Слишком далеко! Максимум {unit.move_range} клеток")
                    return
                
                if not (0 <= x < self.field.width and 0 <= y < self.field.height):
                    print("❌ Координаты за пределами поля")
                    return
                
                if self.field.grid[y][x] is not None:
                    print("❌ Клетка уже занята")
                    return
                
                self.field.grid[current_y][current_x] = None
                unit.set_position(x, y)
                self.field.grid[y][x] = unit
                print(f"✅ {unit.name} перемещен на ({x}, {y})")
            else:
                print("❌ Неверный номер")
        except ValueError:
            print("❌ Введите число")
    
    def attack_menu(self):
        player_units = [u for u in self.field.units if u in self.field.bases[0].owned_units]
        if not player_units:
            print("❌ Нет ваших юнитов для атаки")
            return
        
        enemy_units = [u for u in self.field.units if u in self.enemy_base.owned_units]
        if not enemy_units:
            print("🎉 Все вражеские юниты уничтожены!")
            return
        
        print("\n⚔️ АТАКА")
        print("Ваши юниты:")
        for i, unit in enumerate(player_units):
            x, y = unit.get_position()
            print(f"{i+1}. {unit.name} на ({x}, {y}) - атака: {unit.attack}")
        
        try:
            attacker_idx = int(input("Выберите атакующего юнита: ")) - 1
            if 0 <= attacker_idx < len(player_units):
                attacker = player_units[attacker_idx]
                
                print("\nЦели:")
                for i, target in enumerate(enemy_units):
                    x, y = target.get_position()
                    distance = self.calculate_distance(attacker, target)
                    print(f"{i+1}. {target.name} на ({x}, {y}) - HP: {target.health}, расстояние: {distance}")
                
                target_idx = int(input("Выберите цель: ")) - 1
                if 0 <= target_idx < len(enemy_units):
                    target = enemy_units[target_idx]
                    self.perform_attack(attacker, target)
                else:
                    print("❌ Неверный номер цели")
            else:
                print("❌ Неверный номер атакующего")
        except ValueError:
            print("❌ Введите число")
    
    def calculate_distance(self, unit1, unit2):
        x1, y1 = unit1.get_position()
        x2, y2 = unit2.get_position()
        return abs(x1 - x2) + abs(y1 - y2)
    
    def perform_attack(self, attacker, target):
        distance = self.calculate_distance(attacker, target)
        
        max_range = 2 if "лучник" in attacker.name.lower() else 1
        if distance > max_range:
            print(f"❌ Слишком далеко! Максимальная дальность атаки: {max_range}")
            return
        
        damage = max(1, attacker.attack - target.armor)
        target.take_damage(damage)
        print(f"⚔️ {attacker.name} атакует {target.name} и наносит {damage} урона!")
        
        if not target.is_alive():
            print(f"💀 {target.name} уничтожен!")
            x, y = target.get_position()
            self.field.grid[y][x] = None
            self.field.units.remove(target)
            if target.base:
                target.base.owned_units.remove(target)
    
    def show_status(self):
        print(f"\n📊 СТАТУС ИГРЫ")
        print(f"Ход: {self.turn_count}")
        
        player_base = self.field.bases[0]
        print(f"\n🎪 Ваша база: {player_base.get_status()}")
        
        print(f"\n👹 Вражеская база: {self.enemy_base.get_status()}")
        
        if not self.enemy_base.owned_units and self.turn_count > 1:
            print("\n🎉 ПОБЕДА! Все вражеские юниты уничтожены!")
        elif not player_base.owned_units and self.turn_count > 1:
            print("\n💀 ПОРАЖЕНИЕ! Все ваши юниты уничтожены!")
    
    def next_turn(self):
        self.turn_count += 1
        
        for base in self.field.bases:
            if base == self.field.bases[0]:
                base.resources += 30
            else:
                base.resources += 25
        
        print(f"\n🔄 Ход {self.turn_count}")
        print("💰 Базы получили ресурсы")
        
        self.enemy_ai.take_turn()
        
        self.check_win_condition()
    
    def check_win_condition(self):
        if not self.enemy_base.owned_units:
            print("\n🎉 ПОБЕДА! Вражеская база уничтожена!")
            return True
        elif not self.field.bases[0].owned_units:
            print("\n💀 ПОРАЖЕНИЕ! Ваша база уничтожена!")
            return True
        return False
    
    def start(self):
        print("🎮 ДОБРО ПОЖАЛОВАТЬ В ИГРУ!")
        print("Простая тактическая стратегия")
        print("Цель: уничтожить все вражеские юниты!")
        
        self.initialize()
        self.show_menu()

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    game = SimpleGame()
    game.start()

if __name__ == "__main__":
    main()