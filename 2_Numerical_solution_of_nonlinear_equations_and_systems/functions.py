import math

def f1(x):
    return -1.38 * x ** 3 - 5.42 * x ** 2 + 2.57 * x + 10.95
def f2(x):
    return x ** 3 - 1.89 * x ** 2 - 2 * x + 1.76
def f3(x):
    return -1.8* x ** 3 - 2.94 * x ** 2 + 10.37 * x + 5.38

def df1(x):
    return -1.38 * 3 * x ** 2 - 5.42 * 2 * x + 2.57
def df2(x):
    return 3 * x ** 2 - 1.89 * 2 * x - 2
def df3(x):
    return 3 * -1.8 * x ** 2 - 2* 2.94 * x + 10.37

def ddf1(x):
    return -1.38 * 3 * 2 * x - 5.42 * 2
def ddf2(x):
    return 3 * x * 2 - 1.89 * 2
def ddf3(x):
    return 2 * 3 * -1.8 * x - 2 * 2.94

functions_single = {
    "f1(x) = -1.38*x^3 - 5.42*x^2 + 2.57*x + 10.95": f1,
    "f2(x) = x^3 - 1.89*x^2 - 2*x + 1.76": f2,
    "f3(x) = -1.8*x^3 - 2.94*x^2 + 10.37*x + 5.38": f3,
}
dr = {
    "f1(x)": df1,
    "f2(x)": df2,
    "f3(x)": df3,
}
ddr = {
    "f1(x)": ddf1,
    "f2(x)": ddf2,
    "f3(x)": ddf3,
}

#метод хорд
def chord_method(f, a, b, eps):
    log_iterations = []
    fa = f(a)
    fb = f(b)
    x_last = a
    if fa * fb > 0:
        raise ValueError("На отрезке [%g, %g] функция не меняет знак. Вероятно, нет корня или их несколько." % (a, b))
    iteration = 0
    while True:
        iteration += 1
        x = a-(b-a)/(fb-fa)*f(a)
        fx=f(x)
        log_str = f"{iteration}: a = {a:.3f}, b = {b:.3f}, x = {x:.3f}, f(x)={f(x):.6g}, |x_next - x_current| = {abs(x-x_last):.6g}"
        log_iterations.append(log_str)
        if abs(x-x_last) < eps:
            return x, f(x), iteration, log_iterations
        x_last = x
        if fa * fx < 0:
            b = x
        else:
            a = x
        fa = f(a)
        fb = f(b)

#метод Ньютона
def newton_method(f, df, ddf, a, b, eps):
    log_iterations = []
    fa = f(a)
    fb = f(b)
    if fa * fb > 0:
        raise ValueError("На отрезке [%g, %g] нет гарантии единственного корня (функция не меняет знак)." % (a, b))
    if fa * ddf(a) > 0:
        x_current = a
    else:
        x_current = b
    iteration = 0
    while True:
        iteration += 1
        fx = f(x_current)
        dfx = df(x_current)
        x_next = x_current - fx / dfx
        log_str = f"{iteration}: x = {x_next:.6f}, f(x) = {f(x_next):.6g}, |x_next - x_current| = {abs(x_next - x_current):.6g}"
        log_iterations.append(log_str)
        if abs(x_next - x_current) < eps:
            return x_next, f(x_next), iteration, log_iterations
        x_current = x_next

#метод_простых_иттераций
def simple_iteration_method_single(f, df, ddf, a, b, eps):
    log_iterations = []
    iteration = 0
    fa = f(a)
    fb = f(b)
    if fa * fb > 0:
        raise ValueError(
            "На отрезке [%g, %g] функция не меняет знак. Возможна ошибка: нет корня или их несколько." % (a, b))
    if abs(df(a)) > abs(df(b)):
        alpha = 1/df(a)
    else:
        alpha = 1/df(b)
    def g(x):
        return x - alpha * f(x)
    def dg(x):
        return 1 - alpha * df(x)
    if max(dg(a), dg(b)) > 1:
            raise ValueError("Достаточное условие сходимости метода простой итерации может быть нарушено!")
    if fa * ddf(a) > 0:
        x_current = a
    else:
        x_current = b
    while True:
        iteration += 1
        x_next = g(x_current)
        log_str = f"{iteration}: x = {x_next:.6f}, f(x)={f(x_next):.6g}, |x_next - x_current| = {abs(x_next - x_current):.6g}"
        log_iterations.append(log_str)
        if abs(x_next - x_current) < eps:
            return x_next, f(x_next), iteration, log_iterations
        x_current = x_next
def system1_f1_plot(x, y):
    return 0.1 * x ** 2 + x + 0.2 * y ** 2 - 0.3
def system1_f2_plot(x, y):
    return 0.2 * x ** 2 + y + 0.1 * x * y - 0.7
def system1_f1(x, y):
    return 0.3 - 0.1 * x ** 2 - 0.2 * y ** 2
def system1_f2(x, y):
    return 0.7 - 0.2 * x ** 2 - 0.1 * x * y
def system1_df1dx(x, y):
    return -0.2 * x
def system1_df1dy(x, y):
    return -0.4 * y
def system1_df2dx(x, y):
    return -0.4 * x - 0.1 * y
def system1_df2dy(x, y):
    return -0.1 * x

def system2_f1_plot(x, y):
    return 2 * x - math.sin(y - 0.5) - 1
def system2_f2_plot(x, y):
    return y + math.cos(x) - 1.5
def system2_f1(x, y):
    return 0.5 + 0.5 * math.sin(y - 0.5)
def system2_f2(x, y):
    return 1.5 - math.cos(x)
def system2_dg1dx(x, y):
    return 0
def system2_dg1dy(x, y):
    return math.cos(y - 0.5)
def system2_dg2dx(x, y):
    return math.sin(x)
def system2_dg2dy(x, y):
    return 0

systems = {
    "Система 1:\n{0.1x^2 + x + 0.2y^2 - 0.3 = 0;\n 0.2x^2 + x + 0.1xy - 0.7 = 0}":
        (system1_f1, system1_f2, system1_f1_plot, system1_f2_plot, (system1_df1dx, system1_df1dy,
                                                                    system1_df2dx, system1_df2dy)),
    "Система 2:\n{2x - sin(y-0.5) = 1;\n y + cos(x) = 1.5}":
        (system2_f1, system2_f2, system2_f1_plot, system2_f2_plot, (system2_dg1dx, system2_dg1dy,
                                                                    system2_dg2dx, system2_dg2dy)),
}

#метод итерации систем
def simple_iteration_method_system(f1, f2, x0, y0, G, eps):
    f1dx, f1dy, f2dx, f2dy = G
    if (abs(f1dx(x0, y0)) + abs(f1dy(x0, y0))) > 1 or (abs(f2dx(x0, y0)) + abs(f2dy(x0, y0))) > 1:
        print(abs(f1dx(x0, y0)) + abs(f1dy(x0, y0)))
        print(abs(f2dx(x0, y0)) + abs(f2dy(x0, y0)))
        raise ValueError("Ошибка", f"Условия сходимости не выполняются, ошибка")
    log_iterations = []
    x_current = x0
    y_current = y0
    iteration = 0
    while True:
        iteration += 1
        x_next = f1(x_current, y_current)
        y_next = f2(x_current, y_current)
        dist = max(abs(y_next - y_current), abs(x_next - x_current))

        log_str = (f"{iteration}: x = {x_next:.6f}, y = {y_next:.6f}, "
                   f"|max(|x_next-x_current|,|y_next-y_current|)|={dist:.6g}")
        log_iterations.append(log_str)

        if dist < eps:
            return x_next, y_next, iteration, log_iterations
        x_current, y_current = x_next, y_next