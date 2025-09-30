from abc import *
from Units import *
from Task_1.GameField import *

class Base:
    """Класс базы для создания и управления юнитами"""
    
    def __init__(self, name: str, max_units: int = 10):
        self.name = name
        self.max_units = max_units
        self.health = 500
        self.max_health = 500
        self.x = None
        self.y = None
        self.owned_units = []  # юниты, принадлежащие базе
        self.resources = 1000  # ресурсы для создания юнитов
        
        # Стоимость создания юнитов
        self.unit_costs = {
            'swordsman': 100,
            'spearman': 80,
            'crossbowman': 120,
            'longbowman': 150,
            'knight': 200,
            'horseman': 180,
            'healer': 90
        }
    
    def set_position(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def get_position(self):
        return (self.x, self.y)
    
    def create_unit(self, unit_type: str, game_field: 'GameField') -> bool:
        """Создать юнит и разместить его рядом с базой"""
        if len(self.owned_units) >= self.max_units:
            print(f"❌ Достигнуто максимальное количество юнитов: {self.max_units}")
            return False
        
        if unit_type not in self.unit_costs:
            print(f"❌ Неизвестный тип юнита: {unit_type}")
            return False
        
        cost = self.unit_costs[unit_type]
        if self.resources < cost:
            print(f"❌ Недостаточно ресурсов. Нужно: {cost}, есть: {self.resources}")
            return False
        
        # Создаем юнит
        from Units import UnitFactory
        try:
            unit = UnitFactory.create_unit(unit_type)
        except ValueError as e:
            print(f"❌ Ошибка создания юнита: {e}")
            return False
        
        # Ищем свободную клетку рядом с базой
        spawn_x, spawn_y = self._find_spawn_position(game_field)
        if spawn_x is None:
            print("❌ Нет свободных клеток для размещения юнита рядом с базой")
            return False
        
        # Размещаем юнита на поле
        if game_field.add_unit(unit, spawn_x, spawn_y):
            self.owned_units.append(unit)
            self.resources -= cost
            print(f"✅ {self.name} создает {unit.name} за {cost} ресурсов")
            print(f"💰 Остаток ресурсов: {self.resources}")
            return True
        
        return False
    
    def _find_spawn_position(self, game_field: 'GameField') -> tuple:
        """Найти свободную позицию для спавна рядом с базой"""
        if self.x is None or self.y is None:
            return (None, None)
        
        # Проверяем клетки в радиусе 2 от базы
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if dx == 0 and dy == 0:
                    continue  # пропускаем саму базу
                
                spawn_x, spawn_y = self.x + dx, self.y + dy
                if (game_field._is_valid_position(spawn_x, spawn_y) and 
                    game_field.is_cell_empty(spawn_x, spawn_y)):
                    return (spawn_x, spawn_y)
        
        return (None, None)
    
    def collect_resources(self, amount: int = 100):
        """Собрать ресурсы"""
        self.resources += amount
        print(f"💰 {self.name} собирает {amount} ресурсов. Всего: {self.resources}")
    
    def take_damage(self, damage: int) -> int:
        """Получить урон"""
        actual_damage = damage
        self.health -= actual_damage
        if self.health <= 0:
            self.health = 0
            print(f"💀 База {self.name} уничтожена!")
        return actual_damage
    
    def is_alive(self) -> bool:
        return self.health > 0
    
    def update_units(self):
        """Обновить список юнитов (удалить мертвых)"""
        alive_units = []
        for unit in self.owned_units:
            if unit.is_alive():
                alive_units.append(unit)
            else:
                print(f"💀 Юнит {unit.name} погиб и удален из списка базы")
        
        self.owned_units = alive_units
    
    def get_status(self):
        """Получить статус базы"""
        status = f"\n🏰 БАЗА '{self.name}':\n"
        status += f"❤️  Здоровье: {self.health}/{self.max_health}\n"
        status += f"💰 Ресурсы: {self.resources}\n"
        status += f"🎯 Юнитов: {len(self.owned_units)}/{self.max_units}\n"
        
        if self.owned_units:
            status += "👥 Состав армии:\n"
            unit_types = {}
            for unit in self.owned_units:
                unit_type = unit.__class__.__name__
                unit_types[unit_type] = unit_types.get(unit_type, 0) + 1
            
            for unit_type, count in unit_types.items():
                status += f"  - {unit_type}: {count}\n"
        
        return status
    
    def __str__(self):
        return f"База '{self.name}' ({self.health} HP, {len(self.owned_units)} юнитов)"