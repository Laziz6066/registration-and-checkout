import socket
import sqlite3
import tkinter as tk
from tkinter import Label, Button
import threading
from datetime import datetime


class ServerApp:
    data_dict = {}

    def __init__(self, master):
        self.master = master
        master.title("Server Application")
        master.geometry("500x400")
        font_size = 12
        self.start_button = Button(master, text="Start Server", command=self.start_server, font=("Arial", font_size))
        self.start_button.pack()

    def start_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ("192.168.100.208", 8080)
        sock.bind(server_address)
        sock.listen(1)
        connection, client_address = sock.accept()

        received_data = connection.recv(1024).decode()
        pairs = received_data.split(",")
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=')
                self.data_dict[key.strip()] = value.strip()

        font_size = 12
        info_label = Label(self.master, text="Received Data:", font=("Arial", font_size))
        info_label.pack()

        name_label = Label(self.master, text="Имя: {}".format(self.data_dict.get("name")), font=("Arial", font_size))
        name_label.pack()

        phone_label = Label(self.master, text="Номер телефона: {}".format(self.data_dict.get("phone_number")),
                            font=("Arial", font_size))
        phone_label.pack()

        category_label = Label(self.master, text="Категория услуги: {}".format(self.data_dict.get("service_category")),
                               font=("Arial", font_size))
        category_label.pack()

        price_label = Label(self.master, text="Цена услуги: {}".format(self.data_dict.get("service_price")),
                            font=("Arial", font_size))
        price_label.pack()

        payment_label = Label(self.master, text="Приняли оплату?", font=("Arial", font_size))
        payment_label.pack()

        cash_button = Button(self.master, text="Наличными",
                             command=lambda: self.process_payment(True, "Наличными"),
                             font=("Arial", font_size))
        cash_button.pack()

        plastic_button = Button(self.master, text="Пластик",
                                command=lambda: self.process_payment(True, "Пластик"),
                                font=("Arial", font_size))
        plastic_button.pack()

        no_button = Button(self.master, text="Без оплаты",
                           command=lambda: self.process_payment(False, 'без оплаты'),
                           font=("Arial", font_size))
        no_button.pack()

        connection.close()

    def process_payment(self, is_payment_received, payment_method):
        connection = sqlite3.connect('C:/Users/User/Documents/service_records.db')
        cursor = connection.cursor()

        if is_payment_received:
            current_datetime = datetime.now()
            formatted_date = current_datetime.strftime("%d %m %Y")

            current_datetime = datetime.now()
            formatted_time = current_datetime.strftime("%H:%M:%S")

            payment_status = "Оплачено"
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS service_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    phone_number TEXT,
                    service_category TEXT,
                    service_price REAL,
                    payment_status TEXT,
                    payment_method TEXT,
                    date TEXT,
                    time TEXT
                )
            ''')
            cursor.execute("""
                INSERT INTO service_records
                (name, phone_number, service_category, service_price, payment_status, payment_method, date, time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.data_dict.get("name"), self.data_dict.get("phone_number"),
                  self.data_dict.get("service_category"), self.data_dict.get("service_price"),
                  payment_status, payment_method, formatted_date, formatted_time))
        else:
            payment_status = "Не оплачено"

        connection.commit()
        connection.close()
        confirmation_label = Label(self.master, text="Запись сохранена.")
        confirmation_label.pack()
        for widget in self.master.winfo_children():
            if isinstance(widget, (Label, Button)):
                widget.destroy()

        threading.Timer(0.5, self.start_server).start()


def main():
    root = tk.Tk()
    app = ServerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
