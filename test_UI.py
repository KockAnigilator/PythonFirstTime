# test_interface.py
import GameField
from Lab_3.Task_2 import Base
from Lab_3.Task_2.NeutralObject import HealingFountain, TreasureChest
from Lab_3.Task_3 import BaseManager, UnitManager
from Units import Crossbowman, Swordsman


def test_interface():
    """Быстрое тестирование интерфейса"""
    print("🧪 ТЕСТИРОВАНИЕ ИНТЕРФЕЙСА")
    
    # Создаем мини-поле для теста
    field = GameField(6, 6, 10)
    
    # Добавляем базу
    base = Base("Тестовая база")
    field.add_base(base, 1, 1)
    
    # Добавляем несколько юнитов
    swordsman = Swordsman()
    archer = Crossbowman()
    field.add_unit(swordsman, 2, 2)
    field.add_unit(archer, 3, 3)
    
    # Добавляем объекты
    field.add_neutral_object(HealingFountain(), 4, 4)
    field.add_neutral_object(TreasureChest(), 1, 4)
    
    # Тестируем менеджеры
    unit_manager = UnitManager(field)
    base_manager = BaseManager(field)
    
    print("✅ Интерфейс готов к работе!")
    return field, unit_manager, base_manager

if __name__ == "__main__":
    test_interface()