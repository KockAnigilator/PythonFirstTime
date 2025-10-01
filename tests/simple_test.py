# Lab_3/test_simple.py
import os
import sys

sys.path.append(os.path.dirname(__file__))

from GameField import GameField
from Units import Swordsman

def test_simple():
    """Простой тест базовой функциональности"""
    print("🧪 ПРОСТОЙ ТЕСТ БАЗОВОЙ ФУНКЦИОНАЛЬНОСТИ")
    
    try:
        # Создаем поле
        field = GameField(5, 5)
        
        # Создаем и добавляем юнита
        swordsman = Swordsman()
        field.add_unit(swordsman, 1, 1)
        
        # Отображаем поле
        field.display()
        
        # Показываем информацию о юнитах
        field.get_unit_info()
        
        print("✅ Базовые импорты работают правильно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в базовых импортах: {e}")
        return False

if __name__ == "__main__":
    test_simple()