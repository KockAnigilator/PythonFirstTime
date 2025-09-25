from abc import ABC, abstractmethod

class Unit(ABC):
    """Абстрактный базовый класс для всех юнитов."""
    
    def __init__(self, name, health, armor, attack, move_range=1):
        self.name = name
        self.max_health = health
        self.health = health
        self.armor = armor
        self.attack = attack
        self.move_range = move_range  # дальность перемещения за ход
        self.x = None
        self.y = None

    @abstractmethod
    def move(self, new_x, new_y):
        pass

    @abstractmethod
    def special_ability(self):
        """Специальная способность юнита"""
        pass

    def take_damage(self, damage):
        actual_damage = max(0, damage - self.armor)
        self.health -= actual_damage
        return actual_damage

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)

    def is_alive(self):
        return self.health > 0

    def get_position(self):
        return (self.x, self.y)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.name} (HP: {self.health}/{self.max_health}, ATK: {self.attack}, ARM: {self.armor})"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

# ===== ПЕХОТА =====
class Infantry(Unit):
    """Базовый класс пехоты - хороший баланс характеристик"""
    
    def move(self, new_x, new_y):
        # Пехота перемещается на 1 клетку за ход
        distance = abs(new_x - self.x) + abs(new_y - self.y)
        if distance <= self.move_range:
            print(f"{self.name} марширует к клетке ({new_x}, {new_y}).")
            return True
        else:
            print(f"{self.name} не может переместиться так далеко за один ход.")
            return False

class Swordsman(Infantry):
    """Мечник - сильная атака в ближнем бою"""
    
    def __init__(self):
        super().__init__(name="Мечник", health=120, armor=15, attack=25, move_range=1)
        
    def special_ability(self):
        """Мощная атака - удвоенный урон на следующем ходу"""
        bonus_damage = self.attack * 2
        print(f"{self.name} готовит мощную атаку! Урон удваивается: {bonus_damage}")
        return bonus_damage

class Spearman(Infantry):
    """Копейщик - защита от кавалерии"""
    
    def __init__(self):
        super().__init__(name="Копейщик", health=100, armor=20, attack=20, move_range=1)
        self.against_cavalry_bonus = 1.5  # бонус против кавалерии

    def special_ability(self):
        """Установка копий против кавалерии"""
        print(f"{self.name} устанавливает копья! Бонус против кавалерии: x{self.against_cavalry_bonus}")
        return self.against_cavalry_bonus

# ===== ЛУЧНИКИ =====
class Archer(Unit):
    """Базовый класс лучников - дальнобойные атаки"""
    
    def __init__(self, name, health, armor, attack, attack_range=3, move_range=1):
        super().__init__(name, health, armor, attack, move_range)
        self.attack_range = attack_range  # дальность атаки

    def move(self, new_x, new_y):
        # Лучники могут перемещаться на 1 клетку
        distance = abs(new_x - self.x) + abs(new_y - self.y)
        if distance <= self.move_range:
            print(f"{self.name} осторожно перемещается к клетке ({new_x}, {new_y}).")
            return True
        else:
            print(f"{self.name} не может переместиться так далеко.")
            return False

    def can_attack(self, target_x, target_y):
        """Проверка возможности атаки цели"""
        distance = abs(target_x - self.x) + abs(target_y - self.y)
        return distance <= self.attack_range

class Crossbowman(Archer):
    """Арбалетчик - мощный выстрел, но медленная перезарядка"""
    
    def __init__(self):
        super().__init__(name="Арбалетчик", health=80, armor=5, attack=35, attack_range=4, move_range=1)
        self.bolt_loaded = True

    def special_ability(self):
        """Заряженный болт - пробивает броню"""
        if self.bolt_loaded:
            print(f"{self.name} заряжает тяжелый болт! Игнорирует броню цели.")
            self.bolt_loaded = False
            return "armor_piercing"
        else:
            print(f"{self.name} перезаряжает арбалет...")
            self.bolt_loaded = True
            return "reloading"

class Longbowman(Archer):
    """Дальнобойный лучник - большая дальность"""
    
    def __init__(self):
        super().__init__(name="Дальнобойный лучник", health=70, armor=3, attack=20, attack_range=5, move_range=1)

    def special_ability(self):
        """Прицельный выстрел - увеличенная дальность"""
        extended_range = self.attack_range + 2
        print(f"{self.name} совершает прицельный выстрел! Дальность: {extended_range}")
        return extended_range

# ===== КАВАЛЕРИЯ =====
class Cavalry(Unit):
    """Базовый класс кавалерии - высокая мобильность"""
    
    def move(self, new_x, new_y):
        # Кавалерия может перемещаться на 2-3 клетки за ход
        distance = abs(new_x - self.x) + abs(new_y - self.y)
        if distance <= self.move_range:
            print(f"{self.name} скачет к клетке ({new_x}, {new_y}).")
            return True
        else:
            print(f"{self.name} не может скакать так далеко за один ход.")
            return False

class Knight(Cavalry):
    """Рыцарь - тяжелая кавалерия"""
    
    def __init__(self):
        super().__init__(name="Рыцарь", health=150, armor=25, attack=30, move_range=2)

    def special_ability(self):
        """Рыцарская атака - таранный удар"""
        charge_damage = self.attack * 1.5
        print(f"{self.name} совершает рыцарскую атаку! Урон: {charge_damage}")
        return charge_damage

class Horseman(Cavalry):
    """Всадник - легкая кавалерия"""
    
    def __init__(self):
        super().__init__(name="Всадник", health=100, armor=10, attack=20, move_range=3)

    def special_ability(self):
        """Скоростная атака - может атаковать после перемещения"""
        print(f"{self.name} готовится к скоростной атаке! Может атаковать после полного перемещения.")
        return "hit_and_run"

# ===== СПЕЦИАЛЬНЫЕ ЮНИТЫ =====
class Healer(Unit):
    """Лекарь - может лечить другие юниты"""
    
    def __init__(self):
        super().__init__(name="Лекарь", health=60, armor=2, attack=5, move_range=1)
        self.heal_power = 25

    def move(self, new_x, new_y):
        distance = abs(new_x - self.x) + abs(new_y - self.y)
        if distance <= self.move_range:
            print(f"{self.name} перемещается к клетке ({new_x}, {new_y}).")
            return True
        return False

    def special_ability(self):
        """Исцеление союзного юнита"""
        print(f"{self.name} готов исцелить союзника на {self.heal_power} HP.")
        return self.heal_power

    def heal_ally(self, target_unit):
        """Метод для лечения другого юнита"""
        if target_unit.is_alive():
            heal_amount = min(self.heal_power, target_unit.max_health - target_unit.health)
            target_unit.heal(heal_amount)
            print(f"{self.name} исцеляет {target_unit.name} на {heal_amount} HP.")
            return heal_amount
        return 0

# Фабрика для удобного создания юнитов
class UnitFactory:
    """Фабрика для создания юнитов по имени типа"""
    
    @staticmethod
    def create_unit(unit_type):
        units = {
            'swordsman': Swordsman,
            'spearman': Spearman,
            'crossbowman': Crossbowman,
            'longbowman': Longbowman,
            'knight': Knight,
            'horseman': Horseman,
            'healer': Healer
        }
        
        if unit_type.lower() in units:
            return units[unit_type.lower()]()
        else:
            raise ValueError(f"Неизвестный тип юнита: {unit_type}")

# Пример использования
if __name__ == "__main__":
    # Создаем несколько юнитов
    units = [
        UnitFactory.create_unit('swordsman'),
        UnitFactory.create_unit('crossbowman'),
        UnitFactory.create_unit('knight'),
        UnitFactory.create_unit('healer')
    ]
    
    # Тестируем их
    for i, unit in enumerate(units):
        unit.set_position(i, i)  # устанавливаем позиции
        print(f"{i+1}. {unit}")
        print(f"   Способность: ", end="")
        unit.special_ability()
        print()