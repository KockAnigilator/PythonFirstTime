import os
import sys

# Добавляем пути для импорта
sys.path.append(os.path.join(os.path.dirname(__file__), 'Lab_3'))

from Lab_3.Task_3.Game import Game

if __name__ == "__main__":
    # Очистка консоли для лучшего отображения
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Создание и запуск игры
    game = Game()
    game.start()