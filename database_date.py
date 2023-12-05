import sqlite3
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

def show_results():
    target_date = entry.get()

    # Запрос для получения данных за конкретный день
    query = f'''
        SELECT * FROM service_records
        WHERE date = '{target_date}'
    '''

    cursor.execute(query)
    result = cursor.fetchall()

    # Очищаем старый вывод
    for item in tree.get_children():
        tree.delete(item)

    # Вставляем новые данные в таблицу
    category_totals = {}
    total_cash_sum = 0
    total_plastic_sum = 0

    for row in result:
        tree.insert('', 'end', values=row[1:])
        if row[6] == 'Наличными':
            total_cash_sum += int(row[4])
        elif row[6] == 'Пластик':
            total_plastic_sum += row[4]

        # Суммируем общие суммы по категориям и способам оплаты
        category = row[3]
        if category not in category_totals:
            category_totals[category] = {'Наличными': 0, 'Пластик': 0}

        category_totals[category][row[6]] += row[4]

    # Добавляем строки с общими суммами по каждой категории
    for category, totals in category_totals.items():
        total_cash = totals['Наличными']
        total_plastic = totals['Пластик']
        total_sum = total_cash + total_plastic
        tree.insert('', 'end', values=['', '', f'Пластик {category}', total_plastic, f'Наличные {category}', total_cash, f'Общая сумма {category}', total_sum])

    # Добавляем строки с общими суммами по пластикам, наличным и их суммой
    tree.insert('', 'end', values=['', '', 'Пластик:', total_plastic_sum, 'Наличные:', total_cash_sum, 'Общая сумма', total_cash_sum + total_plastic_sum])

    # Автоматически устанавливаем ширину столбцов
    for col in columns:
        tree.column(col, width=tkFont.Font().measure(col) + 10)  # 10 - это небольшой отступ

# Создаем GUI
root = tk.Tk()
root.title("Анализ записей о услугах")

# Создаем и размещаем виджеты
label = tk.Label(root, text="Введите дату:")
label.pack(pady=10)

entry = tk.Entry(root)
entry.pack(pady=10)

button = tk.Button(root, text="Показать результаты", command=show_results)
button.pack(pady=10)

# Создаем Treeview для отображения результатов в таблице
columns = ("Фамилия имя отчество клиента", "Номер телефона", "Отделение по клинике", "Сумма оказанных услуг",
           "Статус оплаты услуг", "Способ оплаты", "Дата оказанных услуг", "Время оказанных услуг")
tree = ttk.Treeview(root, columns=columns, show="headings")

# Настраиваем заголовки столбцов
for col in columns:
    tree.heading(col, text=col)

# Настраиваем выравнивание данных в столбцах
for col in columns:
    tree.column(col, anchor="center", width=tkFont.Font().measure(col) + 10)  # 10 - это небольшой отступ

tree.pack(pady=10)

# Подключаем базу данных
conn = sqlite3.connect('C:/Users/User/Documents/service_records.db')
cursor = conn.cursor()

# Запускаем главный цикл
root.mainloop()

# Закрываем соединение с базой данных после завершения работы программы
conn.close()
