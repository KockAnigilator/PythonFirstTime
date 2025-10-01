from abc import *
from Units import *


class NeutralObject(ABC):
    """Абстрактный базовый класс для нейтральных объектов"""
    
    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol
        self.x = None
        self.y = None
    
    @abstractmethod
    def __mod__(self, unit: 'Unit') -> bool:
        """Перегрузка оператора % для взаимодействия юнита с объектом"""
        pass
    
    def set_position(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def get_position(self):
        return (self.x, self.y)
    
    def __str__(self):
        return f"{self.name} ({self.symbol})"

class HealingFountain(NeutralObject):
    """Целебный фонтан - восстанавливает здоровье"""
    
    def __init__(self):
        super().__init__("Целебный фонтан", "⚱")
        self.heal_power = 50
    
    def __mod__(self, unit: 'Unit') -> bool:
        """Юнит использует фонтан для лечения"""
        if unit.is_alive():
            old_health = unit.health
            unit.heal(self.heal_power)
            heal_amount = unit.health - old_health
            print(f"🎵 {unit.name} использует {self.name} и восстанавливает {heal_amount} HP!")
            return True
        return False

class ArmorSmith(NeutralObject):
    """Кузнец брони - временно усиливает броню"""
    
    def __init__(self):
        super().__init__("Кузнец брони", "⚒")
        self.armor_boost = 10
        self.duration = 3  # хода
    
    def __mod__(self, unit: 'Unit') -> bool:
        """Юнит улучшает броню"""
        if unit.is_alive():
            unit.armor += self.armor_boost
            print(f"🛡️ {unit.name} использует {self.name}! Броня увеличена на {self.armor_boost} на {self.duration} хода.")
            # Здесь можно добавить логику для отслеживания длительности эффекта
            return True
        return False

class Trap(NeutralObject):
    """Ловушка - наносит урон юниту"""
    
    def __init__(self):
        super().__init__("Ловушка", "⚠")
        self.damage = 30
        self.visible = False
    
    def __mod__(self, unit: 'Unit') -> bool:
        """Юнит активирует ловушку"""
        if unit.is_alive():
            actual_damage = unit.take_damage(self.damage)
            print(f"💥 {unit.name} активирует {self.name} и получает {actual_damage} урона!")
            self.visible = True
            return True
        return False

class TreasureChest(NeutralObject):
    """Сундук с сокровищами - дает временное усиление атаки"""
    
    def __init__(self):
        super().__init__("Сундук с сокровищами", "☢")
        self.attack_boost = 15
        self.duration = 2
    
    def __mod__(self, unit: 'Unit') -> bool:
        """Юнит открывает сундук"""
        if unit.is_alive():
            unit.attack += self.attack_boost
            print(f"💎 {unit.name} открывает {self.name}! Атака увеличена на {self.attack_boost} на {self.duration} хода.")
            return True
        return False