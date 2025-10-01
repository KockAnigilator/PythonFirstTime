from abc import ABC, abstractmethod
from enum import Enum
from Units import *

class TerrainType(Enum):
    PLAIN = "равнина"
    FOREST = "лес"
    MOUNTAIN = "горы"
    SWAMP = "болото"

class Landscape(ABC):
    """Абстрактный базовый класс для ландшафта"""
    
    def __init__(self, terrain_type: TerrainType, move_cost: int, attack_modifier: float = 1.0):
        self.terrain_type = terrain_type
        self.move_cost = move_cost  # стоимость перемещения
        self.attack_modifier = attack_modifier  # модификатор атаки
        
    @abstractmethod
    def can_pass(self, unit: 'Unit') -> bool:
        """Может ли юнит пройти через этот ландшафт"""
        pass
    
    def get_attack_bonus(self, unit: 'Unit') -> float:
        """Бонус/штраф к атаке для юнита"""
        return self.attack_modifier
    
    def __str__(self):
        return f"{self.terrain_type.value}"

class Plain(Landscape):
    """Равнина - легкопроходимая местность"""
    
    def __init__(self):
        super().__init__(TerrainType.PLAIN, move_cost=1, attack_modifier=1.0)
    
    def can_pass(self, unit: 'Unit') -> bool:
        return True

class Forest(Landscape):
    """Лес - укрытие для лучников, сложен для кавалерии"""
    
    def __init__(self):
        super().__init__(TerrainType.FOREST, move_cost=2, attack_modifier=1.2)
    
    def can_pass(self, unit: 'Unit') -> bool:
        # Кавалерия с трудом проходит через лес
        from Units import Cavalry
        if isinstance(unit, Cavalry):
            return unit.move_range >= 2  # только кавалерия с высокой подвижностью
        return True
    
    def get_attack_bonus(self, unit: 'Unit') -> float:
        from Units import Archer
        if isinstance(unit, Archer):
            return 1.3  # лучники получают бонус в лесу
        return 1.0

class Mountain(Landscape):
    """Горы - отличная позиция, но сложны для перемещения"""
    
    def __init__(self):
        super().__init__(TerrainType.MOUNTAIN, move_cost=3, attack_modifier=1.5)
    
    def can_pass(self, unit: 'Unit') -> bool:
        from Units import Cavalry
        # Кавалерия не может проходить через горы
        return not isinstance(unit, Cavalry)
    
    def get_attack_bonus(self, unit: 'Unit') -> float:
        from Units import Archer
        if isinstance(unit, Archer):
            return 1.5  # лучники получают большой бонус в горах
        return 1.2

class Swamp(Landscape):
    """Болото - замедляет всех, кроме некоторых типов"""
    
    def __init__(self):
        super().__init__(TerrainType.SWAMP, move_cost=4, attack_modifier=0.8)
    
    def can_pass(self, unit: 'Unit') -> bool:
        return True  # все могут пройти, но медленно
    
    def get_attack_bonus(self, unit: 'Unit') -> float:
        return 0.8  # штраф к атаке в болоте