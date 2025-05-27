import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import math
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from approximation_methods import (
    linear_approximation, quadratic_approximation, cubic_approximation,
    exponential_approximation, logarithm_approximation, pow_approximation,
    pearson_correlation, coefficient_of_determination,
)
from table_printer import format_table_to_string

class ApproximationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Инструмент аппроксимации функций")
        self.root.geometry("1200x900")

        self.X_data = []
        self.Y_data = []
        self.n_points = 0

        self.results = {}
        self.metrics = {}

        style = ttk.Style()
        style.theme_use('clam')

        input_frame = ttk.LabelFrame(root, text="Ввод данных", padding=10)
        input_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        self.input_method_var = tk.StringVar(value="manual")
        ttk.Radiobutton(input_frame, text="Ручной ввод", variable=self.input_method_var, value="manual",
                        command=self.toggle_input_fields).grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        ttk.Radiobutton(input_frame, text="Из файла", variable=self.input_method_var, value="file",
                        command=self.toggle_input_fields).grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)

        self.lbl_n = ttk.Label(input_frame, text="Кол-во точек (n):")
        self.lbl_n.grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        self.entry_n = ttk.Entry(input_frame, width=10)
        self.entry_n.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)
        self.entry_n.insert(0, "8")

        self.lbl_x = ttk.Label(input_frame, text="X (через пробел):")
        self.lbl_x.grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)
        self.entry_x = ttk.Entry(input_frame, width=50)
        self.entry_x.grid(row=2, column=1, columnspan=3, padx=5, pady=2, sticky=tk.EW)
        self.entry_x.insert(0, "1 2 3 4 5 6 7 8")

        self.lbl_y = ttk.Label(input_frame, text="Y (через пробел):")
        self.lbl_y.grid(row=3, column=0, padx=5, pady=2, sticky=tk.W)
        self.entry_y = ttk.Entry(input_frame, width=50)
        self.entry_y.grid(row=3, column=1, columnspan=3, padx=5, pady=2, sticky=tk.EW)
        self.entry_y.insert(0, "2.1 3.9 6.1 7.8 10.2 11.8 14.1 15.9")

        self.lbl_file = ttk.Label(input_frame, text="Файл:")
        self.lbl_file.grid(row=4, column=0, padx=5, pady=2, sticky=tk.W)
        self.entry_file = ttk.Entry(input_frame, width=40)
        self.entry_file.grid(row=4, column=1, columnspan=2, padx=5, pady=2, sticky=tk.EW)
        self.btn_browse = ttk.Button(input_frame, text="Обзор...", command=self.browse_file)
        self.btn_browse.grid(row=4, column=3, padx=5, pady=2)

        self.toggle_input_fields()

        self.btn_calculate = ttk.Button(input_frame, text="Рассчитать", command=self.process_data)
        self.btn_calculate.grid(row=5, column=0, columnspan=2, pady=10, sticky=tk.EW)

        self.btn_save_results = ttk.Button(input_frame, text="Сохранить отчет в файл",
                                           command=self.save_results_to_file)
        self.btn_save_results.grid(row=5, column=2, columnspan=2, pady=10, sticky=tk.EW)

        plot_options_frame = ttk.LabelFrame(root, text="Отображаемые графики", padding=10)
        plot_options_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        self.plot_vars = {}
        self.plot_types = {
            "linear": "Линейная", "quadratic": "Квадратичная", "cubic": "Кубическая",
            "exp": "Экспоненциальная", "log": "Логарифмическая", "pow": "Степенная",
            "all": "Показать все"
        }
        current_row, current_col = 0, 0
        checkboxes_per_row = 4
        for i, (key, text) in enumerate(self.plot_types.items()):
            var = tk.BooleanVar(value=(key == "all"))
            cb = ttk.Checkbutton(plot_options_frame, text=text, variable=var,
                                 command=lambda k=key: self.handle_plot_choice_change(k))
            cb.grid(row=current_row, column=current_col, padx=5, pady=2, sticky=tk.W)
            self.plot_vars[key] = var
            current_col += 1
            if current_col >= checkboxes_per_row:
                current_col = 0
                current_row += 1

        output_frame = ttk.Frame(root, padding=10)
        output_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        paned_window = ttk.PanedWindow(output_frame, orient=tk.VERTICAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        graph_frame = ttk.LabelFrame(paned_window, text="График")
        paned_window.add(graph_frame, weight=3)

        self.fig = Figure(figsize=(7, 5), dpi=100)
        self.ax_main_plot = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas, graph_frame)
        toolbar.update()

        results_frame = ttk.LabelFrame(paned_window, text="Результаты, таблицы и метрики")
        paned_window.add(results_frame, weight=2)

        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, width=80, height=20,
                                                      font=("Courier New", 9))
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.update_plot_display()

    def toggle_input_fields(self):
        if self.input_method_var.get() == "manual":
            self.entry_n.config(state=tk.NORMAL)
            self.entry_x.config(state=tk.NORMAL)
            self.entry_y.config(state=tk.NORMAL)
            self.entry_file.config(state=tk.DISABLED)
            self.btn_browse.config(state=tk.DISABLED)
        else:  # file
            self.entry_n.config(state=tk.DISABLED)
            self.entry_x.config(state=tk.DISABLED)
            self.entry_y.config(state=tk.DISABLED)
            self.entry_file.config(state=tk.NORMAL)
            self.btn_browse.config(state=tk.NORMAL)

    def browse_file(self):
        filepath = filedialog.askopenfilename(
            title="Выберите файл с данными",
            filetypes=(("Текстовые файлы", "*.txt"), ("Все файлы", "*.*"))
        )
        if filepath:
            self.entry_file.delete(0, tk.END)
            self.entry_file.insert(0, filepath)

    def validate_and_parse_data(self):
        try:
            if self.input_method_var.get() == "manual":
                n_str = self.entry_n.get()
                x_str = self.entry_x.get()
                y_str = self.entry_y.get()

                if not n_str or not x_str or not y_str:
                    messagebox.showerror("Ошибка ввода", "Все поля для ручного ввода должны быть заполнены.")
                    return False

                self.n_points = int(n_str)
                if not (2 <= self.n_points <= 50):
                    messagebox.showerror("Ошибка валидации", "Количество точек n должно быть от 2 до 50.")
                    return False

                self.X_data = [float(x.replace(",", ".")) for x in x_str.split()]
                self.Y_data = [float(y.replace(",", ".")) for y in y_str.split()]

                if len(self.X_data) != self.n_points or len(self.Y_data) != self.n_points:
                    messagebox.showerror("Ошибка валидации", "Количество X и Y значений не соответствует n.")
                    return False
            else:
                filepath = self.entry_file.get()
                if not filepath:
                    messagebox.showerror("Ошибка файла", "Путь к файлу не указан.")
                    return False
                with open(filepath, 'r') as f:
                    self.n_points = int(f.readline().strip())
                    if not (2 <= self.n_points <= 50):
                        messagebox.showerror("Ошибка валидации в файле", "Количество точек n должно быть от 2 до 50.")
                        return False
                    x_line = f.readline().strip().replace(",", ".")
                    y_line = f.readline().strip().replace(",", ".")
                    self.X_data = [float(x) for x in x_line.split()]
                    self.Y_data = [float(y) for y in y_line.split()]
                    if len(self.X_data) != self.n_points or len(self.Y_data) != self.n_points:
                        messagebox.showerror("Ошибка валидации в файле",
                                             "Количество X и Y значений не соответствует n.")
                        return False
            return True
        except ValueError:
            messagebox.showerror("Ошибка данных",
                                 "Некорректный формат чисел. Используйте точки как десятичный разделитель и пробелы для разделения.")
            return False
        except FileNotFoundError:
            filepath = self.entry_file.get()
            messagebox.showerror("Ошибка файла", f"Файл не найден: {filepath}")
            return False
        except Exception as e:
            messagebox.showerror("Неизвестная ошибка", f"Произошла ошибка при чтении данных: {e}")
            return False

    def get_r2_interpretation(self, r_squared):
        if r_squared is None:
            return "Коэффициент детерминации не рассчитан."
        if r_squared < 0:
            return f"R^2 = {r_squared:.4f}"
        elif r_squared < 0.3:
            return f"R^2 = {r_squared:.4f}."
        elif r_squared < 0.5:
            return f"R^2 = {r_squared:.4f}."
        elif r_squared < 0.7:
            return f"R^2 = {r_squared:.4f}."
        elif r_squared < 0.9:
            return f"R^2 = {r_squared:.4f}."
        elif r_squared <= 1.0:
            return f"R^2 = {r_squared:.4f}."
        else:
            return f"R^2 = {r_squared:.4f}. Некорректное значение R^2 (>1)."

    def process_data(self):
        if not self.validate_and_parse_data():
            return

        self.results_text.delete('1.0', tk.END)
        self.results = {}
        self.metrics = {}

        output_str_buffer = []
        self.results_text.insert(tk.END, "".join(output_str_buffer))
        self.root.update_idletasks()

        a_lin, b_lin = linear_approximation(self.n_points, self.X_data, self.Y_data)
        self.results["linear"] = (a_lin, b_lin)
        if a_lin is not None and b_lin is not None:
            phi_lin = lambda x: a_lin * x + b_lin
            Y_pred_lin = [phi_lin(x) for x in self.X_data]
            table_str, sko_lin = format_table_to_string(self.n_points, self.X_data, self.Y_data, phi_lin,
                                                        "ЛИНЕЙНАЯ АППРОКСИМАЦИЯ")
            output_str_buffer.append(table_str)
            output_str_buffer.append(f"  y = {a_lin:.4f}x + {b_lin:.4f}\n")

            pearson_r = pearson_correlation(self.X_data, self.Y_data)
            r_squared_lin = coefficient_of_determination(self.Y_data, Y_pred_lin)
            self.metrics["linear"] = {"sko": sko_lin, "r_squared": r_squared_lin, "pearson": pearson_r}

            if pearson_r is not None:
                output_str_buffer.append(f"  Коэффициент корреляции Пирсона: {pearson_r:.4f}\n")
            if r_squared_lin is not None:
                output_str_buffer.append(f"  {self.get_r2_interpretation(r_squared_lin)}\n")
            output_str_buffer.append("\n")
        else:
            output_str_buffer.append("ЛИНЕЙНАЯ АППРОКСИМАЦИЯ: Не удалось рассчитать коэффициенты.\n\n")
            self.metrics["linear"] = {"sko": float('inf'), "r_squared": None, "pearson": None}

        a_quad, b_quad, c_quad = quadratic_approximation(self.n_points, self.X_data, self.Y_data)
        self.results["quadratic"] = (a_quad, b_quad, c_quad)
        if all(coef is not None for coef in [a_quad, b_quad, c_quad]):
            phi_quad = lambda x: a_quad * x ** 2 + b_quad * x + c_quad
            Y_pred_quad = [phi_quad(x) for x in self.X_data]
            table_str, sko_quad = format_table_to_string(self.n_points, self.X_data, self.Y_data, phi_quad,
                                                         "КВАДРАТИЧНАЯ АППРОКСИМАЦИЯ")
            output_str_buffer.append(table_str)
            output_str_buffer.append(f"  y = {a_quad:.4f}x^2 + {b_quad:.4f}x + {c_quad:.4f}\n")

            r_squared_quad = coefficient_of_determination(self.Y_data, Y_pred_quad)
            self.metrics["quadratic"] = {"sko": sko_quad, "r_squared": r_squared_quad}
            if r_squared_quad is not None:
                output_str_buffer.append(f"  {self.get_r2_interpretation(r_squared_quad)}\n")
            output_str_buffer.append("\n")
        else:
            output_str_buffer.append("КВАДРАТИЧНАЯ АППРОКСИМАЦИЯ: Не удалось рассчитать коэффициенты.\n\n")
            self.metrics["quadratic"] = {"sko": float('inf'), "r_squared": None}

        a_cub, b_cub, c_cub, d_cub = cubic_approximation(self.n_points, self.X_data, self.Y_data)
        self.results["cubic"] = (a_cub, b_cub, c_cub, d_cub)
        if all(coef is not None for coef in [a_cub, b_cub, c_cub, d_cub]):
            phi_cub = lambda x: a_cub * x ** 3 + b_cub * x ** 2 + c_cub * x + d_cub
            Y_pred_cub = [phi_cub(x) for x in self.X_data]
            table_str, sko_cub = format_table_to_string(self.n_points, self.X_data, self.Y_data, phi_cub,
                                                        "КУБИЧЕСКАЯ АППРОКСИМАЦИЯ")
            output_str_buffer.append(table_str)
            output_str_buffer.append(f"  y = {a_cub:.4f}x^3 + {b_cub:.4f}x^2 + {c_cub:.4f}x + {d_cub:.4f}\n")

            r_squared_cub = coefficient_of_determination(self.Y_data, Y_pred_cub)
            self.metrics["cubic"] = {"sko": sko_cub, "r_squared": r_squared_cub}
            if r_squared_cub is not None:
                output_str_buffer.append(f"  {self.get_r2_interpretation(r_squared_cub)}\n")
            output_str_buffer.append("\n")
        else:
            output_str_buffer.append("КУБИЧЕСКАЯ АППРОКСИМАЦИЯ: Не удалось рассчитать коэффициенты.\n\n")
            self.metrics["cubic"] = {"sko": float('inf'), "r_squared": None}

        a_exp, b_exp, acc_X_exp, acc_Y_exp = exponential_approximation(self.n_points, self.X_data, self.Y_data)
        self.results["exp"] = (a_exp, b_exp, acc_X_exp, acc_Y_exp)
        if all(coef is not None for coef in [a_exp, b_exp]) and acc_X_exp:
            phi_exp = lambda x: a_exp * math.exp(b_exp * x)
            Y_pred_exp = [phi_exp(x) for x in acc_X_exp]  # Используем acc_X_exp
            table_str, sko_exp = format_table_to_string(len(acc_X_exp), acc_X_exp, acc_Y_exp, phi_exp,
                                                        "ЭКСПОНЕНЦИАЛЬНАЯ АППРОКСИМАЦИЯ")
            output_str_buffer.append(table_str)
            output_str_buffer.append(f"  y = {a_exp:.4f} * e^({b_exp:.4f}x)\n")

            r_squared_exp = coefficient_of_determination(acc_Y_exp, Y_pred_exp)  # Используем acc_Y_exp
            self.metrics["exp"] = {"sko": sko_exp, "r_squared": r_squared_exp, "n_points": len(acc_X_exp)}
            if r_squared_exp is not None:
                output_str_buffer.append(
                    f"  {self.get_r2_interpretation(r_squared_exp)}\n")
            output_str_buffer.append("\n")
        else:
            output_str_buffer.append(
                "ЭКСПОНЕНЦИАЛЬНАЯ АППРОКСИМАЦИЯ: Недостаточно данных или ошибка расчета (y > 0).\n\n")
            self.metrics["exp"] = {"sko": float('inf'), "r_squared": None, "n_points": 0}

        a_log, b_log, acc_X_log, acc_Y_log = logarithm_approximation(self.n_points, self.X_data, self.Y_data)
        self.results["log"] = (a_log, b_log, acc_X_log, acc_Y_log)
        if all(coef is not None for coef in [a_log, b_log]) and acc_X_log:
            phi_log = lambda x: a_log * math.log(x) + b_log if x > 0 else float('nan')
            Y_pred_log = [phi_log(x) for x in acc_X_log]
            table_str, sko_log = format_table_to_string(len(acc_X_log), acc_X_log, acc_Y_log, phi_log,
                                                        "ЛОГАРИФМИЧЕСКАЯ АППРОКСИМАЦИЯ")
            output_str_buffer.append(table_str)
            output_str_buffer.append(f"  y = {a_log:.4f} * ln(x) + {b_log:.4f}\n")

            r_squared_log = coefficient_of_determination(acc_Y_log, Y_pred_log)
            self.metrics["log"] = {"sko": sko_log, "r_squared": r_squared_log, "n_points": len(acc_X_log)}
            if r_squared_log is not None:
                output_str_buffer.append(
                    f"  {self.get_r2_interpretation(r_squared_log)}\n")
            output_str_buffer.append("\n")
        else:
            output_str_buffer.append(
                "ЛОГАРИФМИЧЕСКАЯ АППРОКСИМАЦИЯ: Недостаточно данных или ошибка расчета (x > 0).\n\n")
            self.metrics["log"] = {"sko": float('inf'), "r_squared": None, "n_points": 0}

        a_pow, b_pow, acc_X_pow, acc_Y_pow = pow_approximation(self.n_points, self.X_data, self.Y_data)
        self.results["pow"] = (a_pow, b_pow, acc_X_pow, acc_Y_pow)
        if all(coef is not None for coef in [a_pow, b_pow]) and acc_X_pow:
            phi_pow = lambda x: a_pow * (x ** b_pow) if x > 0 else float('nan')
            Y_pred_pow = [phi_pow(x) for x in acc_X_pow]
            table_str, sko_pow = format_table_to_string(len(acc_X_pow), acc_X_pow, acc_Y_pow, phi_pow,
                                                        "СТЕПЕННАЯ АППРОКСИМАЦИЯ")
            output_str_buffer.append(table_str)
            output_str_buffer.append(f"  y = {a_pow:.4f} * x^{b_pow:.4f}\n")

            r_squared_pow = coefficient_of_determination(acc_Y_pow, Y_pred_pow)
            self.metrics["pow"] = {"sko": sko_pow, "r_squared": r_squared_pow, "n_points": len(acc_X_pow)}
            if r_squared_pow is not None:
                output_str_buffer.append(
                    f"  {self.get_r2_interpretation(r_squared_pow)} \n")
            output_str_buffer.append("\n")
        else:
            output_str_buffer.append(
                "СТЕПЕННАЯ АППРОКСИМАЦИЯ: Недостаточно данных или ошибка расчета (x > 0, y > 0).\n\n")
            self.metrics["pow"] = {"sko": float('inf'), "r_squared": None, "n_points": 0}

        best_method_name = None

        valid_methods = {}
        for name, metric_data in self.metrics.items():
            if metric_data.get("r_squared") is not None and metric_data.get("sko") is not None:
                if name in ["exp", "log", "pow"] and metric_data.get("n_points", 0) < 2:
                    continue
                valid_methods[name] = metric_data

        if not valid_methods:
            output_str_buffer.append("Не удалось определить наилучшую аппроксимацию (нет валидных метрик).\n")
        else:
            sorted_methods = sorted(
                valid_methods.items(),
                key=lambda item: (
                    -item[1]["r_squared"] if item[1]["r_squared"] >= 0 else float('inf'),
                    item[1]["sko"]
                )
            )

            if sorted_methods:
                best_method_name = self.plot_types.get(sorted_methods[0][0],
                                                       sorted_methods[0][0])
                best_metrics = sorted_methods[0][1]
                output_str_buffer.append(f"Наилучшая аппроксимация: {best_method_name}\n")
                output_str_buffer.append(f"  СКО: {best_metrics['sko']:.10f}\n")
                output_str_buffer.append(f"  {self.get_r2_interpretation(best_metrics['r_squared'])}\n")

            else:
                output_str_buffer.append("Не удалось определить наилучшую аппроксимацию (нет валидных метрик).\n")

        self.results_text.delete('1.0', tk.END)
        self.results_text.insert(tk.END, "".join(output_str_buffer))

        self.plot_vars["all"].set(True)
        for key, var in self.plot_vars.items():
            if key != "all":
                var.set(False)

        self.update_plot_display()

    def save_results_to_file(self):
        content = self.results_text.get("1.0", tk.END)
        if not content.strip() or content.strip() == "Выполняется расчет...":
            messagebox.showinfo("Сохранение", "Нет результатов для сохранения.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")],
            title="Сохранить отчет как..."
        )
        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("Сохранение", f"Результаты успешно сохранены в {filepath}")
            except Exception as e:
                messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить файл: {e}")

    def handle_plot_choice_change(self, changed_key):
        if changed_key == "all" and self.plot_vars["all"].get():
            for key, var in self.plot_vars.items():
                if key != "all":
                    var.set(False)
        elif changed_key != "all" and self.plot_vars[changed_key].get():
            if self.plot_vars["all"].get():
                self.plot_vars["all"].set(False)
        elif changed_key != "all" and not self.plot_vars[changed_key].get():
            any_individual_selected = any(self.plot_vars[k].get() for k in self.plot_types if k != "all")
            if not any_individual_selected and not self.plot_vars["all"].get():
                self.plot_vars["all"].set(True)

        self.update_plot_display()

    def update_plot_display(self):
        self.ax_main_plot.clear()

        if not self.X_data or not self.Y_data:
            self.ax_main_plot.set_title("Нет данных для отображения")
            self.canvas.draw()
            return

        self.ax_main_plot.scatter(self.X_data, self.Y_data, color='blue', label='Исходные точки', zorder=10, s=30)

        all_acc_X_sets = [self.results.get(key, (None, None, [], []))[2] for key in ["exp", "log", "pow"] if
                          self.results.get(key)]
        all_acc_X_flat = [val for sublist in all_acc_X_sets if sublist for val in sublist]

        combined_X_for_range = list(self.X_data)
        if all_acc_X_flat:
            combined_X_for_range.extend(all_acc_X_flat)

        if not combined_X_for_range:
            x_min, x_max = -1, 1
        else:
            x_min = min(combined_X_for_range) - 0.5
            x_max = max(combined_X_for_range) + 0.5

        if x_min == x_max:
            x_min -= 1
            x_max += 1

        x_line = np.linspace(x_min, x_max, 500)

        drawn_something = False
        show_all_flag = self.plot_vars["all"].get()

        plot_definitions = [
            ("linear", lambda a, b: lambda x: a * x + b, f'Лин: {{a:.2f}}x+{{b:.2f}}', '-', 2),
            ("quadratic", lambda a, b, c: lambda x: a * x ** 2 + b * x + c, f'Квадр: {{a:.2f}}x²+{{b:.2f}}x+{{c:.2f}}',
             '-', 3),
            ("cubic", lambda a, b, c, d: lambda x: a * x ** 3 + b * x ** 2 + c * x + d,
             f'Куб: {{a:.2f}}x³+{{b:.2f}}x²+{{c:.2f}}x+{{d:.2f}}', '-', 4),
            ("exp", lambda a, b, acc_X, acc_Y: lambda x_val: a * math.exp(b * x_val), f'Эксп: {{a:.2f}}e^({{b:.2f}}x)',
             '--', 2),
            ("log", lambda a, b, acc_X, acc_Y: lambda x_val: a * math.log(x_val) + b if x_val > 1e-9 else float('nan'),
             f'Лог: {{a:.2f}}ln(x)+{{b:.2f}}', '--', 2),
            ("pow", lambda a, b, acc_X, acc_Y: lambda x_val: a * (x_val ** b) if x_val > 1e-9 else float('nan'),
             f'Степ: {{a:.2f}}x^{{b:.2f}}', '--', 2)
        ]

        for key, func_builder, label_format, style, num_label_coeffs in plot_definitions:
            if show_all_flag or self.plot_vars[key].get():
                res_tuple = self.results.get(key)
                if res_tuple:
                    all_args_for_builder = res_tuple[0:func_builder.__code__.co_argcount]
                    coeffs_for_label = res_tuple[0:num_label_coeffs]

                    valid_coeffs_for_calc = True
                    if key in ["exp", "log", "pow"]:
                        if not (len(res_tuple) >= 4 and all(c is not None for c in res_tuple[0:2]) and res_tuple[2]):
                            valid_coeffs_for_calc = False
                    else:
                        if not all(c is not None for c in all_args_for_builder):
                            valid_coeffs_for_calc = False

                    if not valid_coeffs_for_calc:
                        continue
                    if not all(c is not None for c in coeffs_for_label):
                        continue

                    phi_func = func_builder(*all_args_for_builder)

                    current_x_line = x_line
                    if key in ["log", "pow", "exp"]:
                        current_x_line = x_line[x_line > 1e-9]
                        if len(current_x_line) == 0: continue

                    try:
                        y_vals = [phi_func(val) for val in current_x_line]
                        formatted_coeffs_for_label = {chr(97 + i): round(c, 2) for i, c in enumerate(coeffs_for_label)}
                        label_str = label_format.format(**formatted_coeffs_for_label)

                        self.ax_main_plot.plot(current_x_line, y_vals, label=label_str, linestyle=style)
                        drawn_something = True
                    except (ValueError, TypeError, RuntimeWarning, OverflowError) as e:
                        print(
                            f"Ошибка при построении графика для {key} с x={current_x_line[0] if len(current_x_line) > 0 else 'N/A'}..: {e}")

        self.ax_main_plot.set_title('Аппроксимации функций')
        self.ax_main_plot.set_xlabel('Ox')
        self.ax_main_plot.set_ylabel('Oy')
        self.ax_main_plot.grid(True, linestyle='--', alpha=0.7)

        if drawn_something or (self.X_data and self.Y_data):
            self.ax_main_plot.legend(loc='best', fontsize='small')

        try:
            self.fig.tight_layout()
        except ValueError:
            pass
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = ApproximationApp(root)
    root.mainloop()