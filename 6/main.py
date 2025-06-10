import tkinter as tk
from tkinter import ttk, messagebox
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class ODESolverApp:
    def __init__(self, master):
        self.master = master
        master.title("Решение ОДУ")
        self.plot_data = {}
        self._build_ui()

    def _build_ui(self):
        paned = ttk.PanedWindow(self.master, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        left_panel = ttk.Frame(paned)
        paned.add(left_panel, weight=1)

        right_panel = ttk.Frame(paned)
        paned.add(right_panel, weight=3)

        ttk.Label(left_panel, text="Выберите ОДУ:", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=5)
        self.eq_cmb = ttk.Combobox(left_panel, values=list(ODES.keys()), state="readonly", width=30)
        self.eq_cmb.current(0)
        self.eq_cmb.pack(fill=tk.X, pady=4, padx=5)
        self.eq_cmb.bind("<<ComboboxSelected>>", self._on_eq_select)

        def add_entry(frame, label_text):
            entry_frame = ttk.Frame(frame)
            entry_frame.pack(fill=tk.X, pady=2, padx=5)
            ttk.Label(entry_frame, text=label_text, width=6).pack(side=tk.LEFT)
            e = ttk.Entry(entry_frame, width=15)
            e.pack(side=tk.LEFT, padx=4, fill=tk.X, expand=True)
            return e

        self.x0_entry = add_entry(left_panel, "x₀ =")
        self.y0_entry = add_entry(left_panel, "y₀ =")
        self.xn_entry = add_entry(left_panel, "xₙ =")
        self.h_entry = add_entry(left_panel, "h =")
        self.eps_entry = add_entry(left_panel, "eps =")
        self.eps_entry.insert(0, "0.1")
        self.h_entry.insert(0, "0.1")

        ttk.Button(left_panel, text="Решить", command=self._on_solve).pack(pady=10)

        self.main_notebook = ttk.Notebook(right_panel)
        self.main_notebook.pack(fill=tk.BOTH, expand=True)

        self.graph_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.graph_tab, text="График")

        self.checkbox_frame = ttk.Frame(self.graph_tab)
        self.checkbox_frame.pack(side=tk.TOP, fill=tk.X, pady=5, padx=5)

        self.show_euler_var = tk.BooleanVar(value=True)
        self.show_improved_euler_var = tk.BooleanVar(value=True)
        self.show_milne_var = tk.BooleanVar(value=True)
        self.show_exact_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(self.checkbox_frame, text="Эйлер", variable=self.show_euler_var,
                        command=self._update_plot).pack(side=tk.LEFT, padx=3)
        ttk.Checkbutton(self.checkbox_frame, text="Модифицированный Эйлер", variable=self.show_improved_euler_var,
                        command=self._update_plot).pack(side=tk.LEFT, padx=3)
        ttk.Checkbutton(self.checkbox_frame, text="Милн", variable=self.show_milne_var, command=self._update_plot).pack(
            side=tk.LEFT, padx=3)
        ttk.Checkbutton(self.checkbox_frame, text="Точное", variable=self.show_exact_var,
                        command=self._update_plot).pack(side=tk.LEFT, padx=3)

        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.1)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_tab)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True, side=tk.BOTTOM)

        self.methods_details_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.methods_details_tab, text="Методы")

        methods_canvas = tk.Canvas(self.methods_details_tab)
        methods_scrollbar = ttk.Scrollbar(self.methods_details_tab, orient="vertical", command=methods_canvas.yview)
        self.scrollable_methods_frame = ttk.Frame(methods_canvas)

        self.scrollable_methods_frame.bind(
            "<Configure>",
            lambda e: methods_canvas.configure(
                scrollregion=methods_canvas.bbox("all")
            )
        )
        methods_canvas.create_window((0, 0), window=self.scrollable_methods_frame, anchor="nw")
        methods_canvas.configure(yscrollcommand=methods_scrollbar.set)

        methods_canvas.pack(side="left", fill="both", expand=True)
        methods_scrollbar.pack(side="right", fill="y")

        self.text_widgets = {}

        def create_text_section(parent, title, key_name, height=10):
            ttk.Label(parent, text=title, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=5, pady=(10, 2),
                                                                              fill=tk.X)
            txt_widget = tk.Text(parent, height=height, wrap="none", relief=tk.SOLID, borderwidth=1,
                                 font=("Consolas", 9))
            txt_widget.pack(fill=tk.X, expand=True, padx=5, pady=2)
            self.text_widgets[key_name] = txt_widget

        create_text_section(self.scrollable_methods_frame, "Метод Эйлера:", "Эйлер", height=12)
        create_text_section(self.scrollable_methods_frame, "Модифицированный метод Эйлера:", "Модифицированный Эйлер", height=12)
        create_text_section(self.scrollable_methods_frame, "Метод Милна:", "Милн", height=12)
        create_text_section(self.scrollable_methods_frame, "Итого:", "Итого", height=6)

        self._on_eq_select(None)
        self._update_plot()

    def _on_eq_select(self, event):
        ode = ODES[self.eq_cmb.get()]
        self.x0_entry.delete(0, tk.END)
        self.x0_entry.insert(0, str(ode["x0"]))
        self.y0_entry.delete(0, tk.END)
        self.y0_entry.insert(0, str(ode["y0"]))
        self.xn_entry.delete(0, tk.END)
        self.xn_entry.insert(0, str(ode["x0"] + 1.0))

        self.plot_data = {}
        self._clear_text_widgets()
        self._update_plot()

    def _clear_text_widgets(self):
        for key in self.text_widgets:
            self.text_widgets[key].config(state=tk.NORMAL)
            self.text_widgets[key].delete("1.0", tk.END)
            self.text_widgets[key].config(state=tk.DISABLED)

    def _update_plot(self):
        self.ax.cla()
        if not self.plot_data or not any(
                self.plot_data.get(m) for m in ["euler", "improved_euler", "milne", "exact_x"]):
            self.ax.set_title("Нет данных для отображения")
            self.ax.grid(True)
            self.canvas.draw_idle()
            return

        ode_key = self.eq_cmb.get()
        y_exact_func = ODES[ode_key]["exact"]
        legend_items = []

        if self.show_euler_var.get() and "euler" in self.plot_data:
            xs, ys = self.plot_data["euler"]
            line, = self.ax.plot(xs, ys, marker='o', linestyle='', markersize=4, label="Эйлер")
            legend_items.append(line)
        if self.show_improved_euler_var.get() and "improved_euler" in self.plot_data:
            xs, ys = self.plot_data["improved_euler"]
            line, = self.ax.plot(xs, ys, marker='s', linestyle='', markersize=4, label="Модифицированный Эйлер")
            legend_items.append(line)
        if self.show_milne_var.get() and "milne" in self.plot_data:
            xs, ys = self.plot_data["milne"]
            line, = self.ax.plot(xs, ys, marker='^', linestyle='', markersize=4, label="Милн")
            legend_items.append(line)

        if self.show_exact_var.get() and "exact_x" in self.plot_data and self.plot_data["exact_x"]:
            xs = self.plot_data["exact_x"]
            ys_exact = [y_exact_func(x_val) for x_val in xs]
            line, = self.ax.plot(xs, ys_exact, linestyle='-', color='black', linewidth=1.5, label="Точное")
            legend_items.append(line)

        if legend_items:
            self.ax.legend()
        self.ax.grid(True)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_title(f"Решение ОДУ: {ode_key}")
        self.canvas.draw_idle()

    def _on_solve(self):
        ode_key = self.eq_cmb.get()
        ode = ODES[ode_key]
        f, y_exact_func = ode["f"], ode["exact"]
        try:
            x0 = float(self.x0_entry.get().replace(",", "."))
            y0 = float(self.y0_entry.get().replace(",", "."))
            xn = float(self.xn_entry.get().replace(",", "."))
            h_init = float(self.h_entry.get().replace(",", "."))
            eps = float(self.eps_entry.get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Некорректные числовые значения.")
            return

        if not (xn > x0):
            messagebox.showerror("Ошибка ввода", "Требуется xₙ > x₀.")
            return
        if not (h_init > 0):
            messagebox.showerror("Ошибка ввода", "Начальный шаг h должен быть > 0.")
            return
        if not (eps > 0):
            messagebox.showerror("Ошибка ввода", "Точность eps должна быть > 0.")
            return

        try:
            h_e, n_e, xs_e, ys_e, err_e = solve_adaptive(euler_method, f, x0, y0, xn, h_init, eps, p=1)
            h_i, n_i, xs_i, ys_i, err_i = solve_adaptive(improved_euler_method, f, x0, y0, xn, h_init, eps, p=2)
            h_m, n_m, xs_m, ys_m, err_m = solve_adaptive(milne_method, f, x0, y0, xn, h_init, eps, p=4)
        except Exception as exc:
            messagebox.showerror("Ошибка решения", f"Произошла ошибка: {str(exc)}")
            self.plot_data = {}
            self._clear_text_widgets()
            self._update_plot()
            return

        self.plot_data = {
            "euler": (xs_e, ys_e),
            "improved_euler": (xs_i, ys_i),
            "milne": (xs_m, ys_m),
            "exact_x": xs_m,
        }
        self._update_plot()
        self._clear_text_widgets()

        def dump_to_widget(widget, xs_method, ys_method, method_name):
            widget.config(state=tk.NORMAL)
            widget.insert(tk.END, f"{'i':>3} {'x':>10} {'y (метод)':>15} {'y (точное)':>15} {'eps':>12}\n")
            widget.insert(tk.END, "-" * 60 + "\n")

            num_points_to_show = min(20, len(xs_method))

            step = 1
            if len(xs_method) > num_points_to_show * 1.5 and num_points_to_show > 0:
                step = max(1, (len(xs_method) - 1) // (num_points_to_show - 1 if num_points_to_show > 1 else 1))

            points_shown_indices = set()
            for i_loop in range(0, len(xs_method), step):
                idx = i_loop
                points_shown_indices.add(idx)
                x_val = xs_method[idx]
                y_method_val = ys_method[idx]
                y_exact_val = y_exact_func(x_val)
                error_val = abs(y_exact_val - y_method_val)
                widget.insert(tk.END,
                              f"{idx:3d} {x_val:10.5f} {y_method_val:15.6f} {y_exact_val:15.6f} {error_val:12.3e}\n")

            if len(xs_method) > 0 and (len(xs_method) - 1) not in points_shown_indices:
                idx = len(xs_method) - 1
                x_val = xs_method[idx]
                y_method_val = ys_method[idx]
                y_exact_val = y_exact_func(x_val)
                error_val = abs(y_exact_val - y_method_val)
                widget.insert(tk.END,
                              f"{idx:3d} {x_val:10.5f} {y_method_val:15.6f} {y_exact_val:15.6f} {error_val:12.3e}\n")
            widget.config(state=tk.DISABLED)

        dump_to_widget(self.text_widgets["Эйлер"], xs_e, ys_e, "Эйлер")
        dump_to_widget(self.text_widgets["Модифицированный Эйлер"], xs_i, ys_i, "Модифицированный Эйлер")
        dump_to_widget(self.text_widgets["Милн"], xs_m, ys_m, "Милн")

        sv = self.text_widgets["Итого"]
        sv.config(state=tk.NORMAL)
        sv.insert(tk.END, f"{'Метод':<20} {'Шаг (h)':>15} {'Кол-во шагов (N)':>20} {'Eps':>15}\n")
        sv.insert(tk.END, "-" * 75 + "\n")
        sv.insert(tk.END, f"{'Эйлер':<20} {h_e:15.3e} {n_e:20d} {err_e:15.3e}\n")
        sv.insert(tk.END, f"{'Модифицированный Эйлер':<20} {h_i:15.3e} {n_i:20d} {err_i:15.3e}\n")
        sv.insert(tk.END, f"{'Милн':<20} {h_m:15.3e} {n_m:20d} {err_m:15.3e}\n")
        sv.config(state=tk.DISABLED)

        self.scrollable_methods_frame.update_idletasks()
        methods_canvas = self.scrollable_methods_frame.master
        methods_canvas.config(scrollregion=methods_canvas.bbox("all"))

def euler_method(f, x0, y0, h, n_steps):
    xs, ys = [x0], [y0]
    x, y = x0, y0
    for i in range(n_steps):
        y += h * f(x, y)
        x += h
        xs.append(x)
        ys.append(y)
    return xs, ys

def improved_euler_method(f, x0, y0, h, n_steps):
    xs, ys = [x0], [y0]
    x, y = x0, y0
    for i in range(n_steps):
        y_pred = y + h * f(x, y)
        y += (h / 2) * (f(x, y) + f(x + h, y_pred))
        x += h
        xs.append(x)
        ys.append(y)
    return xs, ys

def milne_method(f, x0, y0, h, n_steps):
    if n_steps < 3:
        raise ValueError("Требуется не менее 4 точек.")

    xs, ys = [x0], [y0]
    x, y = x0, y0

    for j in range(3):
        y_pred = y + h * f(x, y)
        y += (h / 2) * (f(x, y) + f(x + h, y_pred))
        x += h
        xs.append(x)
        ys.append(y)

    for i in range(3, n_steps):
        x_m3, y_m3 = xs[i - 3], ys[i - 3]
        x_m2, y_m2 = xs[i - 2], ys[i - 2]
        x_m1, y_m1 = xs[i - 1], ys[i - 1]
        x_curr, y_curr = xs[i], ys[i]

        y_pred_next = y_m3 + (4 * h / 3) * (2 * f(x_curr, y_curr) - f(x_m1, y_m1) + 2 * f(x_m2, y_m2))
        x_next = x0 + (i + 1) * h
        y_corr_next = y_m1 + (h / 3) * (f(x_next, y_pred_next) + 4 * f(x_curr, y_curr) + f(x_m1, y_m1))

        xs.append(x_next)
        ys.append(y_corr_next)

    return xs, ys

def solve_adaptive(method, f, x0, y0, xn, h_init, eps, p, max_points=40960):
    h = h_init
    while True:
        n = int(round((xn - x0) / h))

        if n <= 0:
            if (xn - x0) > 0 and h > 0:
                h = (xn - x0) / 1.0
                n = 1
            else:
                raise ValueError("Некорректный интервал (xₙ <= x₀) или начальный шаг h.")

        if n >= max_points:
            raise OverflowError(f"Слишком много узлов ({n}), макс: {max_points}. Увеличьте h или уменьшите интервал.")

        try:
            xs1, ys1 = method(f, x0, y0, h, n)
            xs2, ys2 = method(f, x0, y0, h / 2, n * 2)
        except ValueError as e:
            if "Милна" in str(e) and n < 3:
                if (xn - x0) > 0:
                    h = (xn - x0) / 3.0
                    if h <= 1e-9:
                        raise ValueError(f"Интервал слишком мал для метода Милна с 3 шагами: {str(e)}")
                    continue
                else:
                    raise e
            else:
                raise e

        denom = 2 ** p - 1
        if denom == 0: denom = 1

        err = abs(ys1[-1] - ys2[-1]) / denom

        if err <= eps or h < 1e-9:
            return h, n, xs1, ys1, err
        h /= 2

ODES = {
    "y' = y + x": {"f": lambda x, y: y + x, "exact": lambda x: 2 * math.exp(x) - x - 1, "x0": 0.0, "y0": 1.0},
    "y' = x * y": {"f": lambda x, y: x * y, "exact": lambda x: math.exp(x * x / 2), "x0": 0.0, "y0": 1.0},
    "y' = y - x^2 + 1": {
        "f": lambda x, y: y - x * x + 1,
        "exact": lambda x: x ** 2 + 2 * x + 1 - math.exp(x),
        "x0": 0.0,
        "y0": 0.0,
    },
}

if __name__ == "__main__":
    root = tk.Tk()
    app = ODESolverApp(root)
    root.mainloop()