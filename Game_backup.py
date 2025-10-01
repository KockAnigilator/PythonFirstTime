import os
import sys

# Простой обходной путь - создаем класс Game прямо здесь
class SimpleGame:
    def __init__(self):
        self.turn_count = 0
    
    def start(self):
        print("🎮 ПРОСТАЯ ВЕРСИЯ ИГРЫ")
        print("=" * 40)
        print("Эта версия игры запускается без сложных импортов")
        print("Основная игра требует исправления структуры проекта")
        print(f"Текущий ход: {self.turn_count}")
        print("\nИгра работает в упрощенном режиме!")
        
        while True:
            cmd = input("\nВведите 'exit' для выхода или 'next' для следующего хода: ")
            if cmd == 'exit':
                break
            elif cmd == 'next':
                self.turn_count += 1
                print(f"Ход {self.turn_count} завершен")
            else:
                print("Неизвестная команда")

def main():
    """Запуск упрощенной игры"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("🎮 ЛАБОРАТОРНАЯ РАБОТА 3 - РЕЗЕРВНАЯ ВЕРСИЯ")
    print("=" * 60)
    
    game = SimpleGame()
    game.start()

if __name__ == "__main__":
    main()