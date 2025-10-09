import os
import sys

# Добавляем путь к Lab_3 для импортов
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Lab_3'))

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