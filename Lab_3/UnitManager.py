from GameField import GameField
from Units import *

class UnitManager:
    """Класс для управления юнитами через консольный интерфейс"""
    
    def __init__(self, game_field: GameField):
        self.game_field = game_field
        self.selected_unit = None
    
    def select_unit(self) -> bool:
        if not self.game_field.units:
            print("❌ На поле нет юнитов")
            return False
        
        print(f"\n🎯 ВЫБОР ЮНИТА ДЛЯ УПРАВЛЕНИЯ")
        self.game_field.get_unit_info()
        
        try:
            choice = int(input("\nВведите номер юнита для выбора: ")) - 1
            if 0 <= choice < len(self.game_field.units):
                self.selected_unit = self.game_field.units[choice]
                print(f"✅ Выбран юнит: {self.selected_unit.name}")
                self.show_unit_status()
                return True
            else:
                print("❌ Неверный номер юнита")
                return False
        except ValueError:
            print("❌ Введите число")
            return False
    
    def show_unit_status(self):
        if not self.selected_unit:
            print("❌ Юнит не выбран")
            return
        
        unit = self.selected_unit
        x, y = unit.get_position()
        terrain = self.game_field.get_terrain_at(x, y)
        
        print(f"\n📊 СТАТУС ЮНИТА:")
        print(f"🏷️  Имя: {unit.name} [ID: {unit.id}]")
        print(f"📍 Позиция: ({x}, {y}) - {terrain}")
        print(f"❤️  Здоровье: {unit.health}/{unit.max_health}")
        print(f"🛡️  Броня: {unit.armor}")
        print(f"⚔️  Атака: {unit.attack}")
        print(f"🎯 Дальность перемещения: {unit.move_range}")
        
        if isinstance(unit, Archer):
            print(f"🏹 Дальность атаки: {unit.attack_range}")
        
        self.show_available_moves()
    
    def show_available_moves(self):
        if not self.selected_unit:
            return
        
        unit = self.selected_unit
        x, y = unit.get_position()
        
        print(f"\n🗺️  ДОСТУПНЫЕ КЛЕТКИ ДЛЯ ПЕРЕМЕЩЕНИЯ:")
        available_cells = []
        
        for dy in range(-unit.move_range, unit.move_range + 1):
            for dx in range(-unit.move_range, unit.move_range + 1):
                if dx == 0 and dy == 0:
                    continue
                
                new_x, new_y = x + dx, y + dy
                if (self.game_field._is_valid_position(new_x, new_y) and 
                    self.game_field.is_cell_empty(new_x, new_y)):
                    
                    terrain = self.game_field.get_terrain_at(new_x, new_y)
                    if terrain and terrain.can_pass(unit):
                        available_cells.append((new_x, new_y))
                        print(f"  ({new_x}, {new_y}) - {terrain}")
        
        if not available_cells:
            print("  Нет доступных клеток для перемещения")
    
    def move_unit(self) -> bool:
        if not self.selected_unit:
            print("❌ Сначала выберите юнита")
            return False
        
        try:
            x = int(input("Введите координату X для перемещения: "))
            y = int(input("Введите координату Y для перемещения: "))
            
            if self.game_field.move_unit(self.selected_unit, x, y):
                self.show_unit_status()
                return True
            return False
        except ValueError:
            print("❌ Введите числа для координат")
            return False
    
    def attack_with_unit(self) -> bool:
        if not self.selected_unit:
            print("❌ Сначала выберите юнита")
            return False
        
        if not self.selected_unit.is_alive():
            print("❌ Юнит мертв и не может атаковать")
            return False
        
        try:
            x = int(input("Введите координату X цели: "))
            y = int(input("Введите координату Y цели: "))
            
            return self.game_field.attack_unit(self.selected_unit, x, y)
        except ValueError:
            print("❌ Введите числа для координат")
            return False
    
    def use_special_ability(self):
        if not self.selected_unit:
            print("❌ Сначала выберите юнита")
            return
        
        if not self.selected_unit.is_alive():
            print("❌ Юнит мертв и не может использовать способности")
            return
        
        result = self.selected_unit.special_ability()
        print(f"✨ Результат использования способности: {result}")
    
    def interact_with_neutral(self) -> bool:
        if not self.selected_unit:
            print("❌ Сначала выберите юнита")
            return False
        
        try:
            x = int(input("Введите координату X объекта: "))
            y = int(input("Введите координату Y объекта: "))
            
            return self.game_field.interact_with_object(self.selected_unit, x, y)
        except ValueError:
            print("❌ Введите числа для координат")
            return False
    
    def show_unit_menu(self):
        if not self.selected_unit:
            if not self.select_unit():
                return
        
        while True:
            print(f"\n🎮 УПРАВЛЕНИЕ ЮНИТОМ: {self.selected_unit.name}")
            print("1. 📊 Показать статус")
            print("2. 🎯 Переместить")
            print("3. ⚔️ Атаковать")
            print("4. ✨ Использовать способность")
            print("5. 🎁 Взаимодействовать с объектом")
            print("6. 🔄 Выбрать другого юнита")
            print("7. ↩️ Назад в главное меню")
            
            try:
                choice = input("Выберите действие: ")
                
                if choice == '1':
                    self.show_unit_status()
                elif choice == '2':
                    self.move_unit()
                elif choice == '3':
                    self.attack_with_unit()
                elif choice == '4':
                    self.use_special_ability()
                elif choice == '5':
                    self.interact_with_neutral()
                elif choice == '6':
                    if self.select_unit():
                        continue
                    else:
                        break
                elif choice == '7':
                    break
                else:
                    print("❌ Неверный выбор")
            except Exception as e:
                print(f"❌ Ошибка: {e}")