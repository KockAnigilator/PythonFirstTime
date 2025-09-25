"""
Лабораторная работа №2 — Вариант 5
Синтаксис Python. Работа с типами данных, файлами, сериализацией.
"""

import pickle
import json
from collections import deque

# === ЗАДАЧА 1.0 и 1.4: Что будет результатом выражений? ===
def task_1_0():
    """Выражение: "agility"[2:5] + "taxonomy"[3:6]"""
    result = "agility"[2:5] + "taxonomy"[3:6]
    print(f"Задача 1.0: 'agility'[2:5] + 'taxonomy'[3:6] = '{result}'")
    print("Объяснение: [2:5] → 'gil', [3:6] → 'ono' → 'gilono'")
    # Вывод: gilono

def task_1_4():
    """Выражение: type([False, True, False, True][2:3])"""
    lst = [False, True, False, True][2:3]
    result_type = type(lst)
    print(f"Задача 1.4: type([False, True, False, True][2:3]) = {result_type}")
    print("Объяснение: срез возвращает список из одного элемента → тип list")
    # Вывод: <class 'list'>

# === ЗАДАЧА 6: Подсчёт частоты символов в строке ===
def task_6():
    """
    Считает количество вхождений символов в строку.
    Пример: 'google.com' → {'g':2, 'o':3, ...}
    """
    text = "google.com"

    # Решение 1: через цикл и словарь (мой подход)
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1

    # Решение 2: через dict comprehension
    freq_comp = {char: text.count(char) for char in set(text)}

    # Решение 3: через Counter (GPT-style)
    from collections import Counter
    freq_counter = dict(Counter(text))

    print(f"Задача 6: частота символов в '{text}'")
    print("Решение 1 (цикл):", freq)
    print("Решение 2 (comprehension):", freq_comp)
    print("Решение 3 (Counter):", freq_counter)

    # Вывод
    print("Вывод: Решение 1 наиболее читаемое и эффективное. "
          "Решение 2 неэффективно для длинных строк (count() вызывается много раз). "
          "Решение 3 — лучшее для реальных проектов.")
    # ✅ Моё решение — первое

# === ЗАДАЧА 18: Удаление дубликатов из списка (сохраняя порядок) ===
def task_18():
    """
    Удалить все повторяющиеся элементы из списка.
    """
    original = [1, 2, 2, 3, 4, 4, 5]

    # Решение 1: через цикл и проверку (моё)
    unique = []
    seen = set()
    for item in original:
        if item not in seen:
            seen.add(item)
            unique.append(item)

    # Решение 2: через dict.fromkeys() (современный способ)
    unique_ordered = list(dict.fromkeys(original))

    # Решение 3: через set() — теряет порядок
    unique_unordered = list(set(original))

    print(f"Задача 18: удаление дубликатов из {original}")
    print("Решение 1 (цикл + set):", unique)
    print("Решение 2 (dict.fromkeys):", unique_ordered)
    print("Решение 3 (set):", unique_unordered)

    # Вывод
    print("Вывод: Решение 1 даёт полный контроль. "
          "Решение 2 — самый короткий и правильный в Python >=3.7. "
          "Решение 3 не сохраняет порядок — неприемлемо, если это важно.")
    # ✅ Моё решение — 1 и 2

# === ЗАДАЧА 27: Найти min и max среди значений словаря ===
def task_27():
    """
    Найти максимальное и минимальное значение среди значений словаря.
    """
    d = {'a': 10, 'b': 5, 'c': 20, 'd': 3}

    # Решение 1: min() и max() по values()
    min_val = min(d.values())
    max_val = max(d.values())

    # Решение 2: через sorted
    sorted_vals = sorted(d.values())
    min_sorted, max_sorted = sorted_vals[0], sorted_vals[-1]

    # Решение 3: через цикл
    min_loop = float('inf')
    max_loop = float('-inf')
    for v in d.values():
        if v < min_loop:
            min_loop = v
        if v > max_loop:
            max_loop = v

    print(f"Задача 27: min и max в значениях {d}")
    print("Решение 1 (min/max):", min_val, max_val)
    print("Решение 2 (sorted):", min_sorted, max_sorted)
    print("Решение 3 (цикл):", min_loop, max_loop)

    # Вывод
    print("Вывод: Решение 1 — самое простое и эффективное. "
          "Решение 2 — избыточно (сортировка ради двух значений). "
          "Решение 3 — полезно для обучения, но не нужно в продакшене.")
    # ✅ Моё решение — 1

# === ЗАДАЧА 32: Посчитать количество кортежей в списке ===
def task_32():
    """
    Подсчитайте количество элементов типа кортеж в списке.
    """
    mixed_list = [1, (2, 3), 'hello', (4, 5), [6, 7], {'key': 'value'}, (8,)]

    # Решение 1: через isinstance (рекомендуется)
    count_isinstance = sum(1 for item in mixed_list if isinstance(item, tuple))

    # Решение 2: через type()
    count_type = sum(1 for item in mixed_list if type(item) == tuple)

    # Решение 3: через filter
    count_filter = len(list(filter(lambda x: isinstance(x, tuple), mixed_list)))

    print(f"Задача 32: количество кортежей в {mixed_list} = {count_isinstance}")
    print("Решение 1 (isinstance):", count_isinstance)
    print("Решение 2 (type):", count_type)
    print("Решение 3 (filter):", count_filter)

    # Вывод
    print("Вывод: isinstance() лучше type(), потому что учитывает наследование. "
          "Решение 1 — наиболее безопасное и питоническое.")
    # ✅ Моё решение — 1

# === ЗАДАЧА 40: Работа с файлом — запись, чтение, последние n строк ===
def task_40():
    """
    Добавьте текст в файл, покажите содержимое, добавьте функцию чтения последних n строк.
    """
    filename = "example.txt"
    content = "Строка 1\nСтрока 2\nСтрока 3\nСтрока 4\nСтрока 5\nФинальная строка\n"

    # Запись
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

    # Чтение всего
    with open(filename, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()
        print("Весь файл:")
        print(''.join(all_lines).strip())

    # Последние n строк — эффективно через deque
    n = 3
    with open(filename, 'r', encoding='utf-8') as f:
        last_lines = list(deque(f, maxlen=n))
        print(f"\nПоследние {n} строк:")
        print(''.join(last_lines).strip())

    print(f"Задача 40: успешно записано в '{filename}' и прочитано.")

    # Вывод
    print("Вывод: Использование deque с maxlen=n — самый эффективный способ "
          "для больших файлов. Не загружает всё в память.")

# === ЗАДАЧА 44: Сохранение словаря через pickle ===
def task_44():
    """
    Запишите словарь в файл через pickle и прочитайте его.
    """
    filename = "data.pkl"
    data = {'name': 'Alice', 'age': 30, 'city': 'Moscow'}

    # Сохранение
    with open(filename, 'wb') as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

    # Загрузка
    with open(filename, 'rb') as f:
        loaded = pickle.load(f)

    print(f"Задача 44: pickle — сохранён и загружен словарь:")
    print("Оригинал:", data)
    print("Загруженный:", loaded)
    print("Совпадают:", data == loaded)

    # Вывод
    print("Вывод: pickle идеален для сериализации Python-объектов, "
          "но не подходит для обмена с другими языками.")

# === ЗАДАЧА 46: Сохранение словаря через json ===
def task_46():
    """
    Запишите словарь в файл через json и прочитайте его.
    """
    filename = "data.json"
    data = {'name': 'Bob', 'age': 25, 'city': 'St. Petersburg'}

    # Сохранение
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    # Загрузка
    with open(filename, 'r', encoding='utf-8') as f:
        loaded = json.load(f)

    print(f"Задача 46: JSON — сохранён и загружен словарь:")
    print("Оригинал:", data)
    print("Загруженный:", loaded)
    print("Совпадают:", data == loaded)

    # Вывод
    print("Вывод: JSON — стандартный формат для обмена данными. "
          "Человекочитаемый, кроссплатформенный. Лучше для API и конфигов.")


# === МЕНЮ ВЫБОРА (как switch-case) ===
def show_menu():
    print("\n" + "="*50)
    print("Лабораторная работа №2 — Вариант 5")
    print("Выберите задачу для запуска:")
    print("1.  Задача 1.0: 'agility'[2:5]+'taxonomy'[3:6]")
    print("2.  Задача 1.4: type([False, True, False, True][2:3])")
    print("3.  Задача 6: Частота символов в строке")
    print("4.  Задача 18: Удаление дубликатов из списка")
    print("5.  Задача 27: Min/Max значений в словаре")
    print("6.  Задача 32: Количество кортежей в списке")
    print("7.  Задача 40: Работа с файлом (последние строки)")
    print("8.  Задача 44: Сохранение словаря (pickle)")
    print("9.  Задача 46: Сохранение словаря (json)")
    print("0.  Выход")
    print("="*50)

def main():
    while True:
        show_menu()
        try:
            choice = input("Введите номер задачи (0–9): ").strip()
            if choice == '1':
                task_1_0()
            elif choice == '2':
                task_1_4()
            elif choice == '3':
                task_6()
            elif choice == '4':
                task_18()
            elif choice == '5':
                task_27()
            elif choice == '6':
                task_32()
            elif choice == '7':
                task_40()
            elif choice == '8':
                task_44()
            elif choice == '9':
                task_46()
            elif choice == '0':
                print("Выход из программы. До свидания!")
                break
            else:
                print("Неверный выбор. Пожалуйста, введите число от 0 до 9.")
        except Exception as e:
            print(f"Ошибка при выполнении: {e}")

        input("\nНажмите Enter, чтобы продолжить...")

if __name__ == "__main__":
    main()