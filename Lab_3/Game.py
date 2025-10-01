import os
import random
from GameField import GameField
from Units import UnitFactory
from Base import Base
from NeutralObject import HealingFountain, ArmorSmith, Trap, TreasureChest
from UnitManager import UnitManager
from BaseManager import BaseManager

class Game:
    """Главный класс игры с консольным интерфейсом"""
    
    def __init__(self):
        self.game_field = None
        self.unit_manager = None
        self.base_manager = None
        self.turn_count = 0
        self.is_running = False
    
    def initialize_game(self):
        print("\n🎮 ИНИЦИАЛИЗАЦИЯ НОВОЙ ИГРЫ")
        
        try:
            width = int(input("Ширина поля (рекомендуется 8-15): ") or "10")
            height = int(input("Высота поля (рекомендуется 8-15): ") or "10")
            max_units = int(input("Максимальное количество юнитов: ") or "20")
            
            self.game_field = GameField(width, height, max_units)
            self.unit_manager = UnitManager(self.game_field)
            self.base_manager = BaseManager(self.game_field)
            
            base_name = input("Название вашей базы: ") or "Главная база"
            base = Base(base_name)
            
            base_x, base_y = width // 4, height // 4
            self.game_field.add_base(base, base_x, base_y)
            
            print("\n🏭 СОЗДАНИЕ НАЧАЛЬНЫХ ЮНИТОВ...")
            base.create_unit('swordsman', self.game_field)
            base.create_unit('crossbowman', self.game_field)
            base.create_unit('healer', self.game_field)
            
            self._place_initial_objects()
            
            print("✅ Игра успешно инициализирована!")
            return True
            
        except ValueError as e:
            print(f"❌ Ошибка инициализации: {e}")
            return False
    
    def _place_initial_objects(self):
        objects = [
            HealingFountain(),
            ArmorSmith(),
            Trap(),
            TreasureChest()
        ]
        
        placed = 0
        attempts = 0
        max_attempts = 20
        
        while placed < len(objects) and attempts < max_attempts:
            x = random.randint(0, self.game_field.width - 1)
            y = random.randint(0, self.game_field.height - 1)
            
            if self.game_field.is_cell_empty(x, y) and not any(
                base.get_position() == (x, y) for base in self.game_field.bases
            ):
                self.game_field.add_neutral_object(objects[placed], x, y)
                placed += 1
            
            attempts += 1
    
    def display_game_status(self):
        print(f"\n📊 СТАТУС ИГРЫ - Ход {self.turn_count}")
        print(f"🎯 Юнитов на поле: {len(self.game_field.units)}/{self.game_field.max_units}")
        print(f"🏰 Баз: {len(self.game_field.bases)}")
        print(f"🎁 Нейтральных объектов: {len(self.game_field.neutral_objects)}")
        
        for base in self.game_field.bases:
            status = "жива" if base.is_alive() else "уничтожена"
            print(f"  {base.name}: {base.health} HP ({status})")
    
    def next_turn(self):
        self.turn_count += 1
        print(f"\n🔄 ХОД {self.turn_count}")
        
        for base in self.game_field.bases:
            base.update_units()
            
            if base.is_alive():
                base.collect_resources(50)
        
        alive_bases = [base for base in self.game_field.bases if base.is_alive()]
        if not alive_bases:
            print("💀 ВСЕ БАЗЫ УНИЧТОЖЕНЫ! Игра окончена.")
            self.is_running = False
            return
        
        print("✅ Ход завершен. Ресурсы баз пополнены.")
    
    def save_game(self):
        print("💾 Функция сохранения будет реализована в задаче 4")
    
    def load_game(self):
        print("📂 Функция загрузки будет реализована в задаче 4")
    
    def show_main_menu(self):
        while True:
            print(f"\n{'='*50}")
            print("🎮 ГЛАВНОЕ МЕНЮ ИГРЫ")
            print(f"{'='*50}")
            print("1. 🗺️  Показать поле")
            print("2. 🎯 Управление юнитами")
            print("3. 🏰 Управление базой")
            print("4. 📊 Статус игры")
            print("5. ➡️  Следующий ход")
            print("6. 💾 Сохранить игру")
            print("7. 📂 Загрузить игру")
            print("8. 🆕 Новая игра")
            print("9. 🚪 Выход")
            
            try:
                choice = input("\nВыберите действие: ")
                
                if choice == '1':
                    self.game_field.display()
                elif choice == '2':
                    self.unit_manager.show_unit_menu()
                elif choice == '3':
                    self.base_manager.show_base_menu()
                elif choice == '4':
                    self.display_game_status()
                elif choice == '5':
                    self.next_turn()
                elif choice == '6':
                    self.save_game()
                elif choice == '7':
                    self.load_game()
                elif choice == '8':
                    if self.initialize_game():
                        self.turn_count = 0
                        self.is_running = True
                elif choice == '9':
                    print("👋 До свидания!")
                    self.is_running = False
                    break
                else:
                    print("❌ Неверный выбор")
            except Exception as e:
                print(f"❌ Ошибка: {e}")
    
    def start(self):
        print("🎮 ДОБРО ПОЖАЛОВАТЬ В ИГРУ!")
        print("="*50)
        
        if self.initialize_game():
            self.is_running = True
            self.turn_count = 0
            self.show_main_menu()
        else:
            print("❌ Не удалось инициализировать игру")