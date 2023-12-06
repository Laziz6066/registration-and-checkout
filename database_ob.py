import sqlite3
import tkinter as tk
from tkinter import ttk


def fetch_data_and_update_gui():
    global total_cash_sum_all_dates, total_plastic_sum_all_dates
    conn = sqlite3.connect('service_records.db')
    cursor = conn.cursor()

    dates_query = '''
        SELECT DISTINCT date FROM service_records
    '''
    cursor.execute(dates_query)
    dates = cursor.fetchall()
    for item in tree.get_children():
        tree.delete(item)

    total_cash_sum_all_dates = 0
    total_plastic_sum_all_dates = 0

    for date_info in dates:
        target_date = date_info[0]

        query = f'''
            SELECT * FROM service_records
            WHERE date = '{target_date}'
        '''
        cursor.execute(query)
        result = cursor.fetchall()

        category_totals = {'Наличными': 0, 'Пластик': 0}

        for row in result:
            service_price = row[4]
            payment_method = row[6]

            category_totals[payment_method] += service_price

        total_cash_sum_all_dates += category_totals['Наличными']
        total_plastic_sum_all_dates += category_totals['Пластик']

        total_sum = category_totals['Наличными'] + category_totals['Пластик']

        # Insert data into the treeview
        tree.insert('', 'end', values=(target_date, category_totals['Наличными'], category_totals['Пластик'], total_sum))

    conn.close()
    update_total_label()


def update_total_label():
    global total_cash_sum_all_dates, total_plastic_sum_all_dates
    total_label.config(text=f"Total Cash: {total_cash_sum_all_dates}, Total Plastic: {total_plastic_sum_all_dates}")


app = tk.Tk()
app.title("Service Records Analysis")
tree = ttk.Treeview(app, columns=('Дата', 'Наличные', 'Пластик', "Общая сумма"), show='headings')
tree.heading('Дата', text='Дата')
tree.heading('Наличные', text='Наличные')
tree.heading('Пластик', text='Пластик')
tree.heading('Общая сумма', text='Общая сумма')
tree.pack(padx=10, pady=10)
fetch_button = ttk.Button(app, text="Обновить", command=fetch_data_and_update_gui)
fetch_button.pack(pady=10)
total_label = ttk.Label(app, text="")
total_label.pack(pady=10)
app.mainloop()
