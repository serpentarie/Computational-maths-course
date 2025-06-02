import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import math
from interpolation_methods import *

matplotlib.use('TkAgg')

def linspace(start, end, num):
    if num <= 0:
        return []
    if num == 1:
        return [start]

    step = (end - start) / (num - 1)
    return [start + i * step for i in range(num)]


class InterpolationGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Программа интерполяции")
        self.root.geometry("1200x800")

        self.x_data = []
        self.y_data = []
        self.x_interp = 0.0

        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.input_frame = ttk.Frame(notebook)
        notebook.add(self.input_frame, text='Ввод данных')

        self.results_frame = ttk.Frame(notebook)
        notebook.add(self.results_frame, text='Результаты')

        self.plot_frame = ttk.Frame(notebook)
        notebook.add(self.plot_frame, text='График')

        self.create_input_widgets()
        self.create_results_widgets()
        self.create_plot_widgets()

    def create_input_widgets(self):
        input_method_frame = ttk.LabelFrame(self.input_frame, text="Способ ввода данных")
        input_method_frame.pack(fill='x', padx=10, pady=5)

        self.input_method = tk.StringVar(value="manual")
        ttk.Radiobutton(input_method_frame, text="Ручной ввод",
                        variable=self.input_method, value="manual",
                        command=self.toggle_input_method).pack(anchor='w')
        ttk.Radiobutton(input_method_frame, text="Из файла",
                        variable=self.input_method, value="file",
                        command=self.toggle_input_method).pack(anchor='w')
        ttk.Radiobutton(input_method_frame, text="Функция",
                        variable=self.input_method, value="function",
                        command=self.toggle_input_method).pack(anchor='w')

        self.manual_frame = ttk.LabelFrame(self.input_frame, text="Ручной ввод точек")
        self.manual_frame.pack(fill='both', expand=True, padx=10, pady=5)

        points_control_frame = ttk.Frame(self.manual_frame)
        points_control_frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(points_control_frame, text="Количество точек:").pack(side='left')
        self.points_count = tk.StringVar(value="5")
        ttk.Entry(points_control_frame, textvariable=self.points_count, width=10).pack(side='left', padx=5)
        ttk.Button(points_control_frame, text="Создать таблицу",
                   command=self.create_points_table).pack(side='left', padx=5)

        self.points_table_frame = ttk.Frame(self.manual_frame)
        self.points_table_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self.file_frame = ttk.LabelFrame(self.input_frame, text="Ввод из файла")

        file_control_frame = ttk.Frame(self.file_frame)
        file_control_frame.pack(fill='x', padx=5, pady=5)

        self.file_path = tk.StringVar()
        ttk.Entry(file_control_frame, textvariable=self.file_path, width=40).pack(side='left', padx=5)
        ttk.Button(file_control_frame, text="Выбрать файл",
                   command=self.select_file).pack(side='left', padx=5)
        ttk.Button(file_control_frame, text="Загрузить",
                   command=self.load_from_file).pack(side='left', padx=5)

        self.function_frame = ttk.LabelFrame(self.input_frame, text="Ввод через функцию")

        func_control_frame = ttk.Frame(self.function_frame)
        func_control_frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(func_control_frame, text="Функция:").pack(side='left')
        self.function_choice = tk.StringVar(value="sin")
        func_combo = ttk.Combobox(func_control_frame, textvariable=self.function_choice,
                                  values=["sin(x)", "cos(x)", "ln(1 + x)"], state="readonly", width=15)
        func_combo.pack(side='left', padx=5)

        ttk.Label(func_control_frame, text="Начало:").pack(side='left', padx=(10, 0))
        self.func_start = tk.DoubleVar(value=0)
        ttk.Entry(func_control_frame, textvariable=self.func_start, width=10).pack(side='left', padx=5)

        ttk.Label(func_control_frame, text="Конец:").pack(side='left')
        self.func_end = tk.DoubleVar(value=2)
        ttk.Entry(func_control_frame, textvariable=self.func_end, width=10).pack(side='left', padx=5)

        ttk.Label(func_control_frame, text="Точек:").pack(side='left')
        self.func_points = tk.IntVar(value=10)
        ttk.Entry(func_control_frame, textvariable=self.func_points, width=10).pack(side='left', padx=5)

        ttk.Button(func_control_frame, text="Генерировать",
                   command=self.generate_function_data).pack(side='left', padx=10)

        interp_frame = ttk.LabelFrame(self.input_frame, text="Значение для интерполяции")
        interp_frame.pack(fill='x', padx=10, pady=5)

        interp_control_frame = ttk.Frame(interp_frame)
        interp_control_frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(interp_control_frame, text="X для интерполяции:").pack(side='left')
        self.x_interp_var = tk.DoubleVar(value=1.0)
        ttk.Entry(interp_control_frame, textvariable=self.x_interp_var, width=15).pack(side='left', padx=5)

        ttk.Button(interp_control_frame, text="Вычислить интерполяцию",
                   command=self.calculate_interpolation).pack(side='left', padx=20)

        self.toggle_input_method()

    def create_results_widgets(self):
        results_text_frame = ttk.LabelFrame(self.results_frame, text="Результаты интерполяции")
        results_text_frame.pack(fill='both', expand=True, padx=10, pady=5)

        self.results_text = scrolledtext.ScrolledText(results_text_frame, height=15, width=80)
        self.results_text.pack(fill='both', expand=True, padx=5, pady=5)

        diff_table_frame = ttk.LabelFrame(self.results_frame, text="Таблица конечных разностей")
        diff_table_frame.pack(fill='both', expand=True, padx=10, pady=5)

        self.diff_table_text = scrolledtext.ScrolledText(diff_table_frame, height=10, width=80)
        self.diff_table_text.pack(fill='both', expand=True, padx=5, pady=5)

    def create_plot_widgets(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, self.plot_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

        methods_frame = ttk.LabelFrame(self.plot_frame, text="Выбор методов интерполяции")
        methods_frame.pack(fill='x', padx=10, pady=5)

        methods_control_frame = ttk.Frame(methods_frame)
        methods_control_frame.pack(fill='x', padx=5, pady=5)

        self.show_lagrange = tk.BooleanVar(value=True)
        self.show_newton = tk.BooleanVar(value=True)
        self.show_gauss = tk.BooleanVar(value=True)

        ttk.Checkbutton(methods_control_frame, text="Лагранж",
                        variable=self.show_lagrange, command=self.update_plot).pack(side='left', padx=10)
        ttk.Checkbutton(methods_control_frame, text="Ньютон",
                        variable=self.show_newton, command=self.update_plot).pack(side='left', padx=10)
        ttk.Checkbutton(methods_control_frame, text="Гаусс",
                        variable=self.show_gauss, command=self.update_plot).pack(side='left', padx=10)

        quick_select_frame = ttk.Frame(methods_frame)
        quick_select_frame.pack(fill='x', padx=5, pady=5)

        ttk.Button(quick_select_frame, text="Выбрать все",
                   command=self.select_all_methods).pack(side='left', padx=5)
        ttk.Button(quick_select_frame, text="Снять все",
                   command=self.deselect_all_methods).pack(side='left', padx=5)

        plot_control_frame = ttk.Frame(self.plot_frame)
        plot_control_frame.pack(fill='x', padx=10, pady=5)

        ttk.Button(plot_control_frame, text="Обновить график",
                   command=self.update_plot).pack(side='left', padx=5)
        ttk.Button(plot_control_frame, text="Сохранить график",
                   command=self.save_plot).pack(side='left', padx=5)

    def toggle_input_method(self):
        self.manual_frame.pack_forget()
        self.file_frame.pack_forget()
        self.function_frame.pack_forget()

        if self.input_method.get() == "manual":
            self.manual_frame.pack(fill='both', expand=True, padx=10, pady=5)
            self.create_points_table()
        elif self.input_method.get() == "file":
            self.file_frame.pack(fill='x', padx=10, pady=5)
        elif self.input_method.get() == "function":
            self.function_frame.pack(fill='x', padx=10, pady=5)

    def create_points_table(self):
        for widget in self.points_table_frame.winfo_children():
            widget.destroy()

        try:
            n = int(self.points_count.get())
            if n <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное количество точек")
            return

        ttk.Label(self.points_table_frame, text="X", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=5, pady=2)
        ttk.Label(self.points_table_frame, text="Y", font=('Arial', 10, 'bold')).grid(row=0, column=1, padx=5, pady=2)

        self.x_entries = []
        self.y_entries = []

        for i in range(n):
            x_var = tk.DoubleVar(value=i)
            y_var = tk.DoubleVar(value=0.0)

            x_entry = ttk.Entry(self.points_table_frame, textvariable=x_var, width=15)
            y_entry = ttk.Entry(self.points_table_frame, textvariable=y_var, width=15)

            x_entry.grid(row=i + 1, column=0, padx=5, pady=2)
            y_entry.grid(row=i + 1, column=1, padx=5, pady=2)

            self.x_entries.append(x_var)
            self.y_entries.append(y_var)

        ttk.Button(self.points_table_frame, text="Применить данные",
                   command=self.apply_manual_data).grid(row=n + 1, column=0, columnspan=2, pady=10)

    def apply_manual_data(self):
        try:
            self.x_data = [x_var.get() for x_var in self.x_entries]
            self.y_data = [y_var.get() for y_var in self.y_entries]
            messagebox.showinfo("Успех", f"Загружено {len(self.x_data)} точек")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при чтении данных: {str(e)}")

    def select_file(self):
        filename = filedialog.askopenfilename(
            title="Выберите файл с данными",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.file_path.set(filename)

    def load_from_file(self):
        try:
            path = self.file_path.get()
            if not path:
                messagebox.showerror("Ошибка", "Выберите файл")
                return

            x, y = [], []
            with open(path, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        x.append(float(parts[0]))
                        y.append(float(parts[1]))

            self.x_data = x
            self.y_data = y
            messagebox.showinfo("Успех", f"Загружено {len(self.x_data)} точек из файла")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при загрузке файла: {str(e)}")

    def generate_function_data(self):
        try:
            func_name = self.function_choice.get()
            start = self.func_start.get()
            end = self.func_end.get()
            n = self.func_points.get()

            if start >= end:
                messagebox.showerror("Ошибка", "Начало интервала должно быть меньше конца")
                return

            if func_name == "ln(1 + x)" and (start <= -1 or end <= -1):
                messagebox.showerror("Ошибка", "Для ln(1 + x) значения должны быть > -1")
                return

            func_map = {
                "sin(x)": math.sin,
                "cos(x)": math.cos,
                "ln(1 + x)": lambda x: math.log(1 + x)
            }

            func = func_map[func_name]
            x = linspace(start, end, n)
            y = [func(xi) for xi in x]

            self.x_data = x
            self.y_data = y

            messagebox.showinfo("Успех", f"Сгенерировано {len(self.x_data)} точек для {func_name}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при генерации данных: {str(e)}")

    def format_data_points(self):
        if not self.x_data or not self.y_data:
            return "Нет данных"

        data_text = "\n"
        data_text += f"{'№':<4} {'X':<12} {'Y':<12}\n"
        data_text += "-" * 32 + "\n"

        for i in range(len(self.x_data)):
            data_text += f"{i + 1:<4} {self.x_data[i]:<12.6f} {self.y_data[i]:<12.6f}\n"

        return data_text

    def calculate_interpolation(self):
        if not self.x_data or not self.y_data:
            messagebox.showerror("Ошибка", "Сначала введите данные")
            return

        try:
            x_interp = self.x_interp_var.get()

            if not (min(self.x_data) <= x_interp <= max(self.x_data)):
                messagebox.showerror("Ошибка", "Значение X должно быть в интервале интерполяции")
                return

            y_lagr = lagrange(self.x_data, self.y_data, x_interp)

            f_newton = newton_divided_diff(self.x_data, self.y_data)
            y_newton = newton_divided_interpolation(self.x_data, f_newton, x_interp)

            y_gauss = gauss_central_even(self.x_data, self.y_data, x_interp)

            results = f"""РЕЗУЛЬТАТЫ ИНТЕРПОЛЯЦИИ для x = {x_interp}:

Интерполяция многочленом Лагранжа: y = {y_lagr:.8f}
Интерполяция многочленом Ньютона (разделенные разности): y = {y_newton:.8f}
Интерполяция многочленом Гаусса: y = {y_gauss:.8f}

ИСХОДНЫЕ ДАННЫЕ:
Количество узлов: {len(self.x_data)}
Интервал: [{min(self.x_data):.4f}, {max(self.x_data):.4f}]
Узлы интерполяции:{self.format_data_points()}
"""

            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, results)

            self.create_difference_table()

            self.update_plot()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при вычислении: {str(e)}")

    def create_difference_table(self):
        try:
            deltas = finite_diff_table(self.y_data)

            table_text = "ТАБЛИЦА КОНЕЧНЫХ РАЗНОСТЕЙ:\n\n"

            table_text += f"{'i':<3} {'x':<10} {'y':<10}"
            for i in range(1, len(self.x_data)):
                table_text += f"{'∆^' + str(i) + ' y':<12}"
            table_text += "\n" + "-" * (13 + 12 * (len(self.x_data) - 1)) + "\n"

            for i in range(len(self.x_data)):
                table_text += f"{i:<3} {self.x_data[i]:<10.4f} {self.y_data[i]:<10.4f}"
                for j in range(1, len(deltas)):
                    if i < len(deltas[j]):
                        table_text += f"{deltas[j][i]:<12.6f}"
                    else:
                        table_text += f"{'':12}"
                table_text += "\n"

            self.diff_table_text.delete(1.0, tk.END)
            self.diff_table_text.insert(tk.END, table_text)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при создании таблицы разностей: {str(e)}")

    def select_all_methods(self):
        self.show_lagrange.set(True)
        self.show_newton.set(True)
        self.show_gauss.set(True)
        self.update_plot()

    def deselect_all_methods(self):
        self.show_lagrange.set(False)
        self.show_newton.set(False)
        self.show_gauss.set(False)
        self.update_plot()

    def update_plot(self):
        if not self.x_data or not self.y_data:
            return

        try:
            self.ax.clear()

            x_plot = linspace(min(self.x_data), max(self.x_data), 500)

            self.ax.plot(self.x_data, self.y_data, "ro", color="cyan", markersize=8, label='Узлы', zorder=10)

            if self.show_lagrange.get():
                y_l_plot = [lagrange(self.x_data, self.y_data, xi) for xi in x_plot]
                self.ax.plot(x_plot, y_l_plot, color="deeppink", linestyle='--', alpha=0.8, linewidth=2,
                             label='Лагранж')

            if self.show_newton.get():
                f_newton = newton_divided_diff(self.x_data, self.y_data)
                y_n_plot = [newton_divided_interpolation(self.x_data, f_newton, xi) for xi in x_plot]
                self.ax.plot(x_plot, y_n_plot, color="purple", linestyle='-.', alpha=0.8, linewidth=2, label='Ньютон')

            if self.show_gauss.get():
                y_g_plot = plot_gauss(self.x_data, self.y_data, x_plot)
                self.ax.plot(x_plot, y_g_plot, color="lime", linestyle=':', alpha=0.9, linewidth=2, label='Гаусс')

            x_interp = self.x_interp_var.get()
            if min(self.x_data) <= x_interp <= max(self.x_data):
                self.ax.axvline(x_interp, color='gray', linestyle=':', alpha=0.6, linewidth=1, label=f'x = {x_interp}')

            self.ax.legend(loc='best', framealpha=0.9)
            self.ax.set_title("Методы интерполяции", fontsize=14, fontweight='bold')
            self.ax.set_xlabel("x", fontsize=12)
            self.ax.set_ylabel("y", fontsize=12)
            self.ax.grid(True, color="lightgray", alpha=0.7, linestyle='-', linewidth=0.5)

            self.ax.spines['top'].set_visible(False)
            self.ax.spines['right'].set_visible(False)
            self.ax.spines['left'].set_color('gray')
            self.ax.spines['bottom'].set_color('gray')

            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при построении графика: {str(e)}")

    def save_plot(self):
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("All files", "*.*")]
            )
            if filename:
                self.fig.savefig(filename, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Успех", f"График сохранен как {filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении: {str(e)}")

def main():
    root = tk.Tk()
    app = InterpolationGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()