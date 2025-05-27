import numpy as np

def draw_linear_graph_on_ax(ax, X, Y, a, b):
    ax.scatter(X, Y, color='pink', label='исходные точки (X, Y)', zorder=5)
    if a is not None and b is not None:
        x_line = np.linspace(min(X) - 0.1, max(X) + 0.1, 100)
        y_line = a * x_line + b
        ax.plot(x_line, y_line, label=f'y = {round(a, 3)}x + {round(b, 3)}', color='darkcyan')
    ax.set_title('Линейная аппроксимация')
    ax.set_xlabel('Ox')
    ax.set_ylabel('Oy')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()


def draw_quadratic_graph_on_ax(ax, X, Y, a, b, c):
    ax.scatter(X, Y, color='pink', label='исходные точки (X, Y)', zorder=5)
    if all(coef is not None for coef in [a, b, c]):
        x_line = np.linspace(min(X) - 0.1, max(X) + 0.1, 100)
        y_line = a * x_line ** 2 + b * x_line + c
        ax.plot(x_line, y_line, label=f'y = {round(a, 3)}x² + {round(b, 3)}x + {round(c, 3)}', color='lightseagreen')
    ax.set_title('Квадратичная аппроксимация')
    ax.set_xlabel('Ox')
    ax.set_ylabel('Oy')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()


def draw_cubic_approximation_on_ax(ax, X, Y, a, b, c, d):
    ax.scatter(X, Y, color='pink', label='исходные точки (X, Y)', zorder=5)
    if all(coef is not None for coef in [a, b, c, d]):
        x_line = np.linspace(min(X) - 0.1, max(X) + 0.1, 100)
        y_line = a * x_line ** 3 + b * x_line ** 2 + c * x_line + d
        ax.plot(x_line, y_line, label=f'y = {round(a, 3)}x³ + {round(b, 3)}x² + {round(c, 3)}x + {round(d, 3)}',
                color='mediumpurple')
    ax.set_title('Кубическая аппроксимация')
    ax.set_xlabel('Ox')
    ax.set_ylabel('Oy')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()


def draw_exp_approximation_on_ax(ax, X_orig, Y_orig, acc_X, acc_Y, a, b):
    ax.scatter(X_orig, Y_orig, color='pink', label='исходные точки (X, Y)', zorder=5)
    if all(coef is not None for coef in [a, b]) and acc_X:
        x_line = np.linspace(min(acc_X) - 0.1, max(acc_X) + 0.1, 100)
        y_line = a * np.exp(b * x_line)
        ax.plot(x_line, y_line,
                label=f'y = {round(a, 3)}*e^({round(b, 3)}x)',
                color='gold')
    ax.set_title('Экспоненциальная аппроксимация')
    ax.set_xlabel('Ox')
    ax.set_ylabel('Oy')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()


def draw_log_approximation_on_ax(ax, X_orig, Y_orig, acc_X, acc_Y, a, b):
    ax.scatter(X_orig, Y_orig, color='pink', label='исходные точки (X, Y)', zorder=5)
    if all(coef is not None for coef in [a, b]) and acc_X:
        safe_min_x = max(min(acc_X), 1e-9)
        x_line = np.linspace(safe_min_x, max(acc_X) + 0.1, 100)
        y_line = a * np.log(x_line) + b
        ax.plot(x_line, y_line,
                label=f'y = {round(a, 3)}*ln(x) + {round(b, 3)}',
                color='lightcoral')
    ax.set_title('Логарифмическая аппроксимация')
    ax.set_xlabel('Ox')
    ax.set_ylabel('Oy')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()


def draw_pow_approximation_on_ax(ax, X_orig, Y_orig, acc_X, acc_Y, a, b):
    ax.scatter(X_orig, Y_orig, color='pink', label='исходные точки (X, Y)', zorder=5)
    if all(coef is not None for coef in [a, b]) and acc_X:
        safe_min_x = max(min(acc_X), 1e-9)
        x_line = np.linspace(safe_min_x, max(acc_X) + 0.1, 100)
        y_line = a * x_line ** b
        ax.plot(x_line, y_line,
                label=f'y = {round(a, 3)}x^{round(b, 3)}',
                color='darkorange')
    ax.set_title('Степенная аппроксимация')
    ax.set_xlabel('Ox')
    ax.set_ylabel('Oy')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()


def draw_all_approximations_on_ax(ax, X, Y, results):
    ax.scatter(X, Y, color='blue', label='Исходные точки', zorder=10, s=50)

    x_min_orig = min(X) if X else 0
    x_max_orig = max(X) if X else 1

    all_acc_X_sets = [results.get(key, [None, None, [], []])[2] for key in ["exp", "log", "pow"]]
    all_acc_X_flat = [val for sublist in all_acc_X_sets if sublist for val in sublist]

    combined_X_for_range = X + all_acc_X_flat
    if not combined_X_for_range:
        x_min, x_max = -1, 1
    else:
        x_min = min(combined_X_for_range) - 0.5
        x_max = max(combined_X_for_range) + 0.5

    x_line = np.linspace(x_min, x_max, 500)

    coeffs = results.get("linear")
    if coeffs and all(c is not None for c in coeffs):
        a, b = coeffs
        y_vals = a * x_line + b
        ax.plot(x_line, y_vals, label=f'Лин: {round(a, 2)}x+{round(b, 2)}', linestyle='-')

    coeffs = results.get("quadratic")
    if coeffs and all(c is not None for c in coeffs):
        a, b, c_ = coeffs
        y_vals = a * x_line ** 2 + b * x_line + c_
        ax.plot(x_line, y_vals, label=f'Квадр: {round(a, 2)}x²+{round(b, 2)}x+{round(c_, 2)}', linestyle='-')

    coeffs = results.get("cubic")
    if coeffs and all(c is not None for c in coeffs):
        a, b, c_, d = coeffs
        y_vals = a * x_line ** 3 + b * x_line ** 2 + c_ * x_line + d
        ax.plot(x_line, y_vals, label=f'Куб: {round(a, 2)}x³+{round(b, 2)}x²+{round(c_, 2)}x+{round(d, 2)}',
                linestyle='-')

    exp_res = results.get("exp")
    if exp_res and all(c is not None for c in exp_res[0:2]) and exp_res[2]:
        a, b = exp_res[0:2]
        y_vals = a * np.exp(b * x_line)
        ax.plot(x_line, y_vals, label=f'Эксп: {round(a, 2)}e^({round(b, 2)}x)', linestyle='--')

    log_res = results.get("log")
    if log_res and all(c is not None for c in log_res[0:2]) and log_res[2]:
        a, b = log_res[0:2]
        x_line_safe_log = x_line[x_line > 1e-9]
        y_vals = a * np.log(x_line_safe_log) + b
        ax.plot(x_line_safe_log, y_vals, label=f'Лог: {round(a, 2)}ln(x)+{round(b, 2)}', linestyle='--')

    pow_res = results.get("pow")
    if pow_res and all(c is not None for c in pow_res[0:2]) and pow_res[2]:
        a, b = pow_res[0:2]
        x_line_safe_pow = x_line[x_line > 1e-9]
        try:
            y_vals = a * (x_line_safe_pow ** b)
            ax.plot(x_line_safe_pow, y_vals, label=f'Степ: {round(a, 2)}x^{round(b, 2)}', linestyle='--')
        except (ValueError, TypeError, RuntimeWarning) as e:
            print({e})

    ax.set_title('Все аппроксимации')
    ax.set_xlabel('Ox')
    ax.set_ylabel('Oy')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='best', fontsize='small')