import random
from typing import List, Optional
from Units import Unit, Infantry, Archer, Cavalry, Healer
from Landscape import Landscape, Plain, Forest, Mountain, Swamp
from NeutralObject import NeutralObject
from Base import Base

class GameField:
    """Расширенный класс игрового поля с ландшафтом и нейтральными объектами"""
    
    def __init__(self, width: int, height: int, max_units: int = 50):
        if width <= 0 or height <= 0:
            raise ValueError("Размеры поля должны быть положительными числами")
        if max_units <= 0:
            raise ValueError("Максимальное количество юнитов должно быть положительным")
            
        self.width = width
        self.height = height
        self.max_units = max_units
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.terrain = self._generate_terrain()
        self.neutral_objects = []
        self.units = []
        self.bases = []
        self.unit_id_counter = 1

    def _generate_terrain(self) -> List[List[Landscape]]:
        terrain_grid = []
        for y in range(self.height):
            row = []
            for x in range(self.height):
                rand = random.random()
                if rand < 0.6:
                    row.append(Plain())
                elif rand < 0.8:
                    row.append(Forest())
                elif rand < 0.95:
                    row.append(Mountain())
                else:
                    row.append(Swamp())
            terrain_grid.append(row)
        return terrain_grid

    def add_base(self, base: Base, x: int, y: int) -> bool:
        if not self._is_valid_position(x, y):
            print(f"❌ Неверные координаты для базы: ({x}, {y})")
            return False
            
        if not self.is_cell_empty(x, y):
            print(f"❌ Клетка ({x}, {y}) уже занята")
            return False
            
        base.set_position(x, y)
        self.bases.append(base)
        self.grid[y][x] = base
        print(f"✅ База '{base.name}' размещена на клетке ({x}, {y})")
        return True

    def add_neutral_object(self, obj: NeutralObject, x: int, y: int) -> bool:
        if not self._is_valid_position(x, y):
            print(f"❌ Неверные координаты для объекта: ({x}, {y})")
            return False
            
        if not self.is_cell_empty(x, y):
            print(f"❌ Клетка ({x}, {y}) уже занята")
            return False
            
        obj.set_position(x, y)
        self.neutral_objects.append(obj)
        self.grid[y][x] = obj
        print(f"✅ {obj.name} размещен на клетке ({x}, {y})")
        return True

    def interact_with_object(self, unit: Unit, x: int, y: int) -> bool:
        if not self._is_valid_position(x, y):
            return False
            
        target = self.grid[y][x]
        if isinstance(target, NeutralObject):
            result = target % unit
            if result:
                self.neutral_objects.remove(target)
                self.grid[y][x] = None
            return result
        return False

    def move_unit(self, unit: Unit, new_x: int, new_y: int) -> bool:
        if unit not in self.units:
            print(f"❌ Юнит {unit.name} не найден на поле")
            return False
            
        if not self._is_valid_position(new_x, new_y):
            print(f"❌ Неверные координаты: ({new_x}, {new_y})")
            return False
            
        if not self.is_cell_empty(new_x, new_y):
            target = self.grid[new_x][new_y]
            if isinstance(target, NeutralObject):
                return self.interact_with_object(unit, new_x, new_y)
            else:
                print(f"❌ Клетка ({new_x}, {new_y}) уже занята")
                return False
        
        terrain = self.terrain[new_y][new_x]
        if not terrain.can_pass(unit):
            print(f"❌ {unit.name} не может пройти через {terrain}")
            return False
            
        old_x, old_y = unit.get_position()
        
        distance = abs(new_x - old_x) + abs(new_y - old_y)
        move_cost = terrain.move_cost
        if distance > unit.move_range / move_cost:
            print(f"❌ {unit.name} не может переместиться так далеко через {terrain}")
            return False
        
        self.grid[old_y][old_x] = None
        self.grid[new_y][new_x] = unit
        unit.set_position(new_x, new_y)
        
        attack_bonus = terrain.get_attack_bonus(unit)
        if attack_bonus != 1.0:
            print(f"🌄 {unit.name} на {terrain}: модификатор атаки {attack_bonus}")
        
        print(f"🎯 {unit.name} перемещен с ({old_x}, {old_y}) на ({new_x}, {new_y}) через {terrain}")
        return True

    def attack_unit(self, attacker: Unit, target_x: int, target_y: int) -> bool:
        target = self.get_unit_at(target_x, target_y)
        if not target:
            print(f"❌ В клетке ({target_x}, {target_y}) нет юнита")
            return False
            
        attacker_terrain = self.terrain[attacker.y][attacker.x]
        attack_modifier = attacker_terrain.get_attack_bonus(attacker)
        
        damage = int(attacker.attack * attack_modifier)
        actual_damage = target.take_damage(damage)
        
        print(f"⚔️ {attacker.name} атакует {target.name} с позиции {attacker_terrain}!")
        print(f"💥 Нанесено урона: {actual_damage} (модификатор: {attack_modifier})")
        
        if not target.is_alive():
            print(f"💀 {target.name} уничтожен!")
            self.remove_unit(target)
            
        return True

    def display(self):
        print(f"\n🎮 ИГРОВОЕ ПОЛЕ {self.width}x{self.height}")
        print(f"   Юнитов: {len(self.units)}/{self.max_units}, Баз: {len(self.bases)}, Объектов: {len(self.neutral_objects)}")
        print("   " + " ".join(f"{i:2}" for i in range(self.width)))
        
        terrain_symbols = {
            Plain: " ",
            Forest: "♣",
            Mountain: "▲", 
            Swamp: "~"
        }
        
        for y in range(self.height):
            row_str = f"{y:2} "
            for x in range(self.width):
                cell = self.grid[y][x]
                if cell:
                    if isinstance(cell, Unit):
                        if isinstance(cell, Infantry):
                            symbol = "I"
                        elif isinstance(cell, Archer):
                            symbol = "A" 
                        elif isinstance(cell, Cavalry):
                            symbol = "C"
                        elif isinstance(cell, Healer):
                            symbol = "H"
                        else:
                            symbol = "U"
                        row_str += f"[{symbol}]"
                    elif isinstance(cell, Base):
                        row_str += "[🏰]"
                    elif isinstance(cell, NeutralObject):
                        row_str += f"[{cell.symbol}]"
                else:
                    terrain_symbol = terrain_symbols.get(type(self.terrain[y][x]), " ")
                    row_str += f" {terrain_symbol} "
            print(row_str)

        print("\n📋 ЛЕГЕНДА:")
        print("I-пехота A-лучники C-кавалерия H-лекарь 🏰-база ⚱-фонтан ⚒-кузнец ⚠-ловушка ☢-сундук")
        print("♣-лес ▲-горы ~-болото  -равнина")

    def get_terrain_at(self, x: int, y: int) -> Optional[Landscape]:
        if not self._is_valid_position(x, y):
            return None
        return self.terrain[y][x]

    def _is_valid_position(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def is_cell_empty(self, x: int, y: int) -> bool:
        cell = self.get_unit_at(x, y)
        return cell is None or isinstance(cell, NeutralObject)

    def get_unit_at(self, x: int, y: int) -> Optional[Unit]:
        if not self._is_valid_position(x, y):
            return None
        cell = self.grid[y][x]
        return cell if isinstance(cell, Unit) else None

    def add_unit(self, unit: Unit, x: int, y: int) -> bool:
        if not self._is_valid_position(x, y):
            print(f"❌ Неверные координаты: ({x}, {y})")
            return False
            
        terrain = self.terrain[y][x]
        if not terrain.can_pass(unit):
            print(f"❌ {unit.name} не может быть размещен на {terrain}")
            return False
            
        if len(self.units) >= self.max_units:
            print(f"❌ Достигнуто максимальное количество юнитов: {self.max_units}")
            return False
            
        if not self.is_cell_empty(x, y):
            print(f"❌ Клетка ({x}, {y}) уже занята")
            return False
            
        if not unit.is_alive():
            print(f"❌ Юнит {unit.name} мертв и не может быть размещен")
            return False

        unit.set_position(x, y)
        unit.id = self.unit_id_counter
        self.unit_id_counter += 1
        
        self.grid[y][x] = unit
        self.units.append(unit)
        
        print(f"✅ {unit.name} размещен на клетке ({x}, {y}) на {terrain}")
        return True

    def remove_unit(self, unit: Unit) -> bool:
        if unit not in self.units:
            print(f"❌ Юнит {unit.name} не найден на поле")
            return False
            
        x, y = unit.get_position()
        if self._is_valid_position(x, y) and self.grid[y][x] == unit:
            self.grid[y][x] = None
            
        self.units.remove(unit)
        
        for base in self.bases:
            if unit in base.owned_units:
                base.owned_units.remove(unit)
                
        print(f"🗑️ Юнит {unit.name} удален с поля")
        return True