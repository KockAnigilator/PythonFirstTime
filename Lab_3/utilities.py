import os
import time

class ConsoleUtils:
    """Утилиты для работы с консолью"""
    
    @staticmethod
    def clear_screen():
        """Очистить экран консоли"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_header(text):
        """Напечатать заголовок"""
        print(f"\n{'='*60}")
        print(f"🎮 {text}")
        print(f"{'='*60}")
    
    @staticmethod
    def print_success(message):
        """Напечатать успешное сообщение"""
        print(f"✅ {message}")
    
    @staticmethod
    def print_error(message):
        """Напечатать сообщение об ошибке"""
        print(f"❌ {message}")
    
    @staticmethod
    def print_warning(message):
        """Напечатать предупреждение"""
        print(f"⚠️  {message}")
    
    @staticmethod
    def wait_for_enter():
        """Ожидание нажатия Enter"""
        input("\n↵ Нажмите Enter для продолжения...")
    
    @staticmethod
    def animate_text(text, delay=0.03):
        """Анимированный вывод текста"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()