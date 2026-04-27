import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
from datetime import datetime

# Функции для работы с JSON
def load_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

# Основное приложение
class TrainingPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.data = load_data()

        # Создаем поля для ввода
        self.create_input_fields()

        # Создаем таблицу для отображения тренировок
        self.create_treeview()

        # Создаем кнопки
        self.create_buttons()

        # Загружаем существующие данные
        self.populate_treeview(self.data)

    def create_input_fields(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        # Дата
        tk.Label(frame, text="Дата (ДД-ММ-ГГГГ):").grid(row=0, column=0)
        self.date_entry = tk.Entry(frame)
        self.date_entry.grid(row=0, column=1)

        # Тип тренировки
        tk.Label(frame, text="Тип тренировки:").grid(row=1, column=0)
        self.type_entry = tk.Entry(frame)
        self.type_entry.grid(row=1, column=1)

        # Длительность
        tk.Label(frame, text="Длительность (мин):").grid(row=2, column=0)
        self.duration_entry = tk.Entry(frame)
        self.duration_entry.grid(row=2, column=1)

    def create_treeview(self):
        columns = ('date', 'type', 'duration')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        self.tree.heading('date', text='Дата')
        self.tree.heading('type', text='Тип')
        self.tree.heading('duration', text='Длительность')
        self.tree.pack(padx=10, pady=10)

    def create_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        add_btn = tk.Button(frame, text="Добавить тренировку", command=self.add_training)
        add_btn.pack(side=tk.LEFT, padx=5)

        save_btn = tk.Button(frame, text="Сохранить", command=self.save_to_json)
        save_btn.pack(side=tk.LEFT, padx=5)

        load_btn = tk.Button(frame, text="Загрузить", command=self.load_from_json)
        load_btn.pack(side=tk.LEFT, padx=5)

        filter_type_btn = tk.Button(frame, text="Фильтр по типу", command=self.filter_by_type)
        filter_type_btn.pack(side=tk.LEFT, padx=5)

        filter_date_btn = tk.Button(frame, text="Фильтр по дате", command=self.filter_by_date)
        filter_date_btn.pack(side=tk.LEFT, padx=5)

        reset_btn = tk.Button(frame, text="Сброс фильтра", command=self.reset_filter)
        reset_btn.pack(side=tk.LEFT, padx=5)

    def add_training(self):
        date_str = self.date_entry.get()
        t_type = self.type_entry.get()
        duration_str = self.duration_entry.get()

        # Проверка корректности данных
        if not self.validate_date(date_str):
            messagebox.showerror("Ошибка", "Некорректный формат даты.\nИспользуйте ДД-ММ-ГГГГ")
            return
        if not duration_str.isdigit() or int(duration_str) <= 0:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом.")
            return

        new_item = {'date': date_str, 'type': t_type, 'duration': duration_str}
        self.data.append(new_item)
        self.populate_treeview(self.data)

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, '%d-%m-%Y')
            return True
        except ValueError:
            return False

    def populate_treeview(self, data):
        self.tree.delete(*self.tree.get_children())
        for item in data:
            self.tree.insert('', tk.END, values=(item['date'], item['type'], item['duration']))

    def save_to_json(self):
        save_data(self.data)
        messagebox.showinfo("Успех", "Данные сохранены.")

    def load_from_json(self):
        self.data = load_data()
        self.populate_treeview(self.data)
        messagebox.showinfo("Успех", "Данные загружены.")

    def filter_by_type(self):
        t_type = simpledialog.askstring("Фильтр", "Введите тип тренировки для фильтрации:")
        if t_type is None:
            return  # отмена
        filtered = [item for item in self.data if item['type'] == t_type]
        self.populate_treeview(filtered)

    def filter_by_date(self):
        date_str = simpledialog.askstring("Фильтр", "Введите дату (ДД-ММ-ГГГГ) для фильтрации:")
        if date_str is None:
            return
        if not self.validate_date(date_str):
            messagebox.showerror("Ошибка", "Некорректный формат даты.")
            return
        filtered = [item for item in self.data if item['date'] == date_str]
        self.populate_treeview(filtered)

    def reset_filter(self):
        self.populate_treeview(self.data)

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlannerApp(root)
    root.mainloop()