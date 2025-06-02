from math import factorial
from prettytable import PrettyTable

def lagrange(x_data, y_data, x):
    result = 0
    n = len(x_data)
    for i in range(n):
        xi, yi = x_data[i], y_data[i]
        li = yi
        for j in range(n):
            if j != i:
                li *= (x - x_data[j]) / (xi - x_data[j])
        result += li
    return result


def newton_divided_diff(x_data, y_data):
    n = len(x_data)
    f = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(0.0)
        f.append(row)

    for i in range(n):
        f[i][0] = y_data[i]

    for k in range(1, n):
        for i in range(n - k):
            f[i][k] = (f[i + 1][k - 1] - f[i][k - 1]) / (x_data[i + k] - x_data[i])
    return f


def newton_divided_interpolation(x_data, f, x):
    n = len(f)
    result = f[0][0]
    for k in range(1, n):
        term = f[0][k]
        for j in range(k):
            term *= (x - x_data[j])
        result += term
    return result

def finite_diff_table(y):
    deltas = [list(y)]
    n = len(y)
    for k in range(1, n):
        prev = deltas[-1]
        curr = [prev[i + 1] - prev[i] for i in range(len(prev) - 1)]
        deltas.append(curr)
    return deltas

def gauss_central_even(x_data, y_data, x):
    h = x_data[1] - x_data[0]
    n = len(x_data)
    m = n // 2

    if n % 2 == 0:
        center = m - 1
        x0 = (x_data[center] + x_data[center + 1]) / 2
    else:
        center = m
        x0 = x_data[center]

    t = (x - x0) / h
    deltas = finite_diff_table(y_data)

    result = y_data[center]

    t_term = 1
    k = 1

    for i in range(1, n):
        if i >= len(deltas) or center - (i // 2) < 0 or center + ((i - 1) // 2) >= len(deltas[i]):
            break

        idx = center - (i // 2)
        val = deltas[i][idx]

        t_term *= t + (k - 1) if i % 2 == 1 else t - (k - 1)
        if i % 2 == 0:
            k += 1

        term = (t_term * val) / factorial(i)
        result += term

    return result

def plot_gauss(x, y, x_plot):
    return [gauss_central_even(x, y, xi) for xi in x_plot]
