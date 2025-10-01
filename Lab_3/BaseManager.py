from GameField import GameField



class BaseManager:
    """Класс для управления базой через консольный интерфейс"""
    
    def __init__(self, game_field: GameField):
        self.game_field = game_field
        self.selected_base = None
    
    def select_base(self) -> bool:
        if not self.game_field.bases:
            print("❌ На поле нет баз")
            return False
        
        if len(self.game_field.bases) == 1:
            self.selected_base = self.game_field.bases[0]
            print(f"✅ Выбрана база: {self.selected_base.name}")
            return True
        else:
            print(f"\n🏰 ВЫБОР БАЗЫ ДЛЯ УПРАВЛЕНИЯ")
            for i, base in enumerate(self.game_field.bases, 1):
                print(f"{i}. {base.name} ({base.health} HP)")
            
            try:
                choice = int(input("\nВведите номер базы для выбора: ")) - 1
                if 0 <= choice < len(self.game_field.bases):
                    self.selected_base = self.game_field.bases[choice]
                    print(f"✅ Выбрана база: {self.selected_base.name}")
                    return True
                else:
                    print("❌ Неверный номер базы")
                    return False
            except ValueError:
                print("❌ Введите число")
                return False
    
    def show_base_status(self):
        if not self.selected_base:
            print("❌ База не выбрана")
            return
        
        print(self.selected_base.get_status())
    
    def create_unit_from_base(self):
        if not self.selected_base:
            if not self.select_base():
                return
        
        print(f"\n🏭 СОЗДАНИЕ ЮНИТА ЧЕРЕЗ БАЗУ '{self.selected_base.name}'")
        print("Доступные типы юнитов:")
        
        unit_types = [
            ('swordsman', 'Мечник', 100),
            ('spearman', 'Копейщик', 80),
            ('crossbowman', 'Арбалетчик', 120),
            ('longbowman', 'Дальнобойный лучник', 150),
            ('knight', 'Рыцарь', 200),
            ('horseman', 'Всадник', 180),
            ('healer', 'Лекарь', 90)
        ]
        
        for i, (unit_type, name, cost) in enumerate(unit_types, 1):
            print(f"{i}. {name} - {cost} ресурсов")
        
        try:
            choice = int(input("\nВыберите тип юнита: ")) - 1
            if 0 <= choice < len(unit_types):
                unit_type = unit_types[choice][0]
                self.selected_base.create_unit(unit_type, self.game_field)
            else:
                print("❌ Неверный выбор")
        except ValueError:
            print("❌ Введите число")
    
    def collect_resources(self):
        if not self.selected_base:
            if not self.select_base():
                return
        
        try:
            amount = int(input("Введите количество ресурсов для сбора: "))
            if amount > 0:
                self.selected_base.collect_resources(amount)
            else:
                print("❌ Количество должно быть положительным")
        except ValueError:
            print("❌ Введите число")
    
    def show_base_menu(self):
        if not self.selected_base:
            if not self.select_base():
                return
        
        while True:
            print(f"\n🏰 УПРАВЛЕНИЕ БАЗОЙ: {self.selected_base.name}")
            print("1. 📊 Показать статус")
            print("2. 🏭 Создать юнит")
            print("3. 💰 Собрать ресурсы")
            print("4. 🔄 Выбрать другую базу")
            print("5. ↩️ Назад в главное меню")
            
            try:
                choice = input("Выберите действие: ")
                
                if choice == '1':
                    self.show_base_status()
                elif choice == '2':
                    self.create_unit_from_base()
                elif choice == '3':
                    self.collect_resources()
                elif choice == '4':
                    if self.select_base():
                        continue
                    else:
                        break
                elif choice == '5':
                    break
                else:
                    print("❌ Неверный выбор")
            except Exception as e:
                print(f"❌ Ошибка: {e}")