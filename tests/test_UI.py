"""
Тест с абсолютными импортами - должен работать в любом случае
"""
import os
import sys

# Добавляем текущую директорию в путь Python
current_dir = os.path.dirname(os.path.abspath(__file__))
lab3_dir = os.path.join(current_dir, '..', 'Lab_3')
sys.path.insert(0, lab3_dir)

# Теперь импортируем все модули
try:
    from GameField import GameField
    print("✅ GameField импортирован")
    
    from Units import Swordsman
    print("✅ Units импортированы")
    
    from Base import Base
    print("✅ Base импортирован")
    
    from Landscape import Plain
    print("✅ Landscape импортирован")
    
    from NeutralObject import HealingFountain
    print("✅ NeutralObject импортирован")
    
    print("\n🎉 Все импорты работают правильно!")
    
    # Быстрый тест создания объектов
    field = GameField(3, 3)
    unit = Swordsman()
    base = Base("Тест")
    terrain = Plain()
    obj = HealingFountain()
    
    print("✅ Все объекты созданы успешно!")
    
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print(f"📁 Текущий путь: {sys.path}")