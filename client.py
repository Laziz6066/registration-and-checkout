import socket
import tkinter as tk
from tkinter import Label, Entry, Button, OptionMenu


class ClientApp:
    def __init__(self, master):
        self.master = master
        master.title("Client Application")
        master.geometry("400x300")
        font_size = 12

        self.info_label = Label(master, text="", font=("Arial", font_size))
        self.info_label.pack()

        self.name_label = Label(master, text="Введите ФИО:", font=("Arial", font_size))
        self.name_label.pack()

        self.name_entry = Entry(master, font=("Arial", font_size))
        self.name_entry.pack()

        self.phone_label = Label(master, text="Введите номер телефона:", font=("Arial", font_size))
        self.phone_label.pack()

        self.phone_entry = Entry(master, font=("Arial", font_size))
        self.phone_entry.pack()

        self.service_categories = ["Гинекология_1", "Гинекология_2", "Уролог", "Кардиолог", "Невролог",
                                   "Жаррох", "Лор", "УЗИ_1", "УЗИ_2", "Лаборотория", "Физиотерапия", "Рентген"]
        self.current_category = tk.StringVar(master)
        self.current_category.set(self.service_categories[0])
        self.category_option_menu = OptionMenu(master, self.current_category, *self.service_categories)
        self.category_option_menu.config(font=("Arial", font_size))
        self.category_option_menu.pack()

        self.price_label = Label(master, text="Введите цену услуги:", font=("Arial", font_size))
        self.price_label.pack()

        self.price_entry = Entry(master, font=("Arial", font_size))
        self.price_entry.pack()

        self.submit_button = Button(master, text="Отправить данные", command=self.send_data, font=("Arial", font_size))
        self.submit_button.pack()

    def get_data(self):
        name = self.name_entry.get()
        phone_number = self.phone_entry.get()
        service_category = self.current_category.get()
        service_price = self.price_entry.get()
        data = (f"name={name.strip()},phone_number={phone_number.strip()},"
                f"service_category={service_category.strip()},service_price={service_price.strip()}")

        return data

    def send_data(self):
        self.data = self.get_data()
        self.submit_button.config(state="disabled")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ("192.168.100.42", 8080)
        sock.connect(server_address)

        sock.sendall(self.data.encode())
        print(sock)
        response = sock.recv(1024).decode()

        if response == "Да":
            self.info_label.config(text="Оплата принята")
        else:
            self.info_label.config(text="Оплата не принята")

        sock.close()

        self.data = None
        self.submit_button.config(state="normal")


def main():
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
