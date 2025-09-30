import copy
from typing import List, Optional, Tuple

from Units import *

import copy
import random
from typing import List, Optional, Tuple, Dict

class GameField:
    """Класс игрового поля - контейнер для юнитов и управления ими"""
    
    def __init__(self, width: int, height: int, max_units: int = 50):
        if width <= 0 or height <= 0:
            raise ValueError("Размеры поля должны быть положительными числами")
        if max_units <= 0:
            raise ValueError("Максимальное количество юнитов должно быть положительным")
            
        self.width = width
        self.height = height
        self.max_units = max_units
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.units = []
        self.unit_id_counter = 1  # для присвоения уникальных ID юнитам

    def add_unit(self, unit: Unit, x: int, y: int) -> bool:
        """Добавить юнита на поле в указанные координаты"""
        
        # Проверка ограничений
        if len(self.units) >= self.max_units:
            print(f"❌ Достигнуто максимальное количество юнитов: {self.max_units}")
            return False
            
        if not self._is_valid_position(x, y):
            print(f"❌ Неверные координаты: ({x}, {y})")
            return False
            
        if not self.is_cell_empty(x, y):
            print(f"❌ Клетка ({x}, {y}) уже занята")
            return False
            
        if not unit.is_alive():
            print(f"❌ Юнит {unit.name} мертв и не может быть размещен")
            return False

        # Размещаем юнита
        unit.set_position(x, y)
        unit.id = self.unit_id_counter  # присваиваем уникальный ID
        self.unit_id_counter += 1
        
        self.grid[y][x] = unit
        self.units.append(unit)
        
        print(f"✅ {unit.name} размещен на клетке ({x}, {y})")
        return True

    def remove_unit(self, unit: Unit) -> bool:
        """Удалить юнита с поля"""
        if unit not in self.units:
            print(f"❌ Юнит {unit.name} не найден на поле")
            return False
            
        x, y = unit.get_position()
        if self._is_valid_position(x, y) and self.grid[y][x] == unit:
            self.grid[y][x] = None
            
        self.units.remove(unit)
        print(f"🗑️ Юнит {unit.name} удален с поля")
        return True

    def move_unit(self, unit: Unit, new_x: int, new_y: int) -> bool:
        """Переместить юнита на новые координаты"""
        if unit not in self.units:
            print(f"❌ Юнит {unit.name} не найден на поле")
            return False
            
        if not self._is_valid_position(new_x, new_y):
            print(f"❌ Неверные координаты: ({new_x}, {new_y})")
            return False
            
        if not self.is_cell_empty(new_x, new_y):
            print(f"❌ Клетка ({new_x}, {new_y}) уже занята")
            return False
            
        # Получаем текущую позицию
        old_x, old_y = unit.get_position()
        
        # Проверяем возможность перемещения юнитом
        if not unit.move(new_x, new_y):
            return False
            
        # Обновляем сетку
        self.grid[old_y][old_x] = None
        self.grid[new_y][new_x] = unit
        unit.set_position(new_x, new_y)
        
        print(f"🎯 {unit.name} перемещен с ({old_x}, {old_y}) на ({new_x}, {new_y})")
        return True

    def get_unit_at(self, x: int, y: int) -> Optional[Unit]:
        """Получить юнита в указанной клетке"""
        if not self._is_valid_position(x, y):
            return None
        return self.grid[y][x]

    def is_cell_empty(self, x: int, y: int) -> bool:
        """Проверить, свободна ли клетка"""
        return self.get_unit_at(x, y) is None

    def get_units_in_range(self, center_x: int, center_y: int, radius: int) -> List[Unit]:
        """Получить список юнитов в радиусе от указанной точки"""
        units_in_range = []
        for y in range(max(0, center_y - radius), min(self.height, center_y + radius + 1)):
            for x in range(max(0, center_x - radius), min(self.width, center_x + radius + 1)):
                unit = self.get_unit_at(x, y)
                if unit and unit != self.get_unit_at(center_x, center_y):
                    distance = abs(x - center_x) + abs(y - center_y)
                    if distance <= radius:
                        units_in_range.append(unit)
        return units_in_range

    def attack_unit(self, attacker: Unit, target_x: int, target_y: int) -> bool:
        """Атака юнита другим юнитом"""
        target = self.get_unit_at(target_x, target_y)
        if not target:
            print(f"❌ В клетке ({target_x}, {target_y}) нет юнита")
            return False
            
        if attacker == target:
            print("❌ Нельзя атаковать самого себя")
            return False
            
        if not attacker.is_alive():
            print(f"❌ {attacker.name} мертв и не может атаковать")
            return False
            
        if not target.is_alive():
            print(f"❌ {target.name} уже мертв")
            return False

        # Проверка дальности атаки для лучников
        if isinstance(attacker, Archer):
            if not attacker.can_attack(target_x, target_y):
                print(f"❌ {attacker.name} не может атаковать так далеко")
                return False

        # Выполняем атаку
        damage = attacker.attack
        actual_damage = target.take_damage(damage)
        
        print(f"⚔️ {attacker.name} атакует {target.name}!")
        print(f"💥 Нанесено урона: {actual_damage}")
        
        if not target.is_alive():
            print(f"💀 {target.name} уничтожен!")
            self.remove_unit(target)
            
        return True

    def _is_valid_position(self, x: int, y: int) -> bool:
        """Проверить, что координаты находятся в пределах поля"""
        return 0 <= x < self.width and 0 <= y < self.height

    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """Получить список всех свободных клеток"""
        empty_cells = []
        for y in range(self.height):
            for x in range(self.width):
                if self.is_cell_empty(x, y):
                    empty_cells.append((x, y))
        return empty_cells

    def display(self):
        """Отобразить поле в консоли"""
        print(f"\n🎮 ИГРОВОЕ ПОЛЕ {self.width}x{self.height} (юнитов: {len(self.units)}/{self.max_units})")
        print("   " + " ".join(f"{i:2}" for i in range(self.width)))
        
        for y in range(self.height):
            row_str = f"{y:2} "
            for x in range(self.width):
                unit = self.grid[y][x]
                if unit:
                    # Символы для разных типов юнитов
                    if isinstance(unit, Infantry):
                        symbol = "I"
                    elif isinstance(unit, Archer):
                        symbol = "A"
                    elif isinstance(unit, Cavalry):
                        symbol = "C"
                    elif isinstance(unit, Healer):
                        symbol = "H"
                    else:
                        symbol = "U"
                    row_str += f" {symbol} "
                else:
                    row_str += " . "
            print(row_str)

    def get_unit_info(self):
        """Получить информацию о всех юнитах на поле"""
        print(f"\n📊 ИНФОРМАЦИЯ О ЮНИТАХ:")
        for i, unit in enumerate(self.units, 1):
            x, y = unit.get_position()
            status = "жив" if unit.is_alive() else "мертв"
            print(f"{i}. {unit.name} [{unit.id}] - ({x}, {y}) - HP: {unit.health}/{unit.max_health} - {status}")

    def __deepcopy__(self, memo):
        """Создание глубокой копии поля с юнитами"""
        new_field = GameField(self.width, self.height, self.max_units)
        new_field.unit_id_counter = self.unit_id_counter
        
        # Копируем юнитов
        for unit in self.units:
            unit_copy = copy.deepcopy(unit)
            x, y = unit.get_position()
            new_field.add_unit(unit_copy, x, y)
            
        return new_field

    def save_state(self) -> dict:
        """Сохранить состояние поля для возможной сериализации"""
        return {
            'width': self.width,
            'height': self.height,
            'max_units': self.max_units,
            'unit_id_counter': self.unit_id_counter,
            'units': [
                {
                    'type': unit.__class__.__name__,
                    'x': unit.x,
                    'y': unit.y,
                    'health': unit.health,
                    'max_health': unit.max_health
                }
                for unit in self.units
            ]
        }

# Пример использования и тестирования
if __name__ == "__main__":
    # Создаем поле
    field = GameField(width=5, height=5, max_units=10)
    
    # Создаем юнитов
    swordsman = Swordsman()
    archer = Crossbowman()
    knight = Knight()
    healer = Healer()
    
    # Размещаем юнитов на поле
    field.add_unit(swordsman, 1, 1)
    field.add_unit(archer, 3, 2)
    field.add_unit(knight, 2, 3)
    field.add_unit(healer, 4, 4)
    
    # Отображаем поле
    field.display()
    field.get_unit_info()
    
    # Тестируем перемещение
    print("\n--- ТЕСТ ПЕРЕМЕЩЕНИЯ ---")
    field.move_unit(swordsman, 2, 1)
    field.display()
    
    # Тестируем атаку
    print("\n--- ТЕСТ АТАКИ ---")
    field.attack_unit(archer, 2, 1)  # Лучник атакует мечника
    
    # Создаем копию поля
    print("\n--- ТЕСТ КОПИРОВАНИЯ ---")
    field_copy = copy.deepcopy(field)
    field_copy.display()
    
    # Тестируем поиск юнитов в радиусе
    print("\n--- ТЕСТ ПОИСКА В РАДИУСЕ ---")
    units_near = field.get_units_in_range(2, 1, 2)
    print(f"Юниты рядом с (2, 1): {[unit.name for unit in units_near]}")