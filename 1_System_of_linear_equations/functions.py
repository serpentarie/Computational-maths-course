from tabulate import tabulate
import random

def print_matrix(mrx: [[float]]):
    print(tabulate(mrx, floatfmt=".3f"))

def matrix_valid(mrx: [[float]]) -> str:
    n = len(mrx)
    if n > 20:
        return "Слишком большая матрица"
    for i in range(n):
        if len(mrx[i]) != n + 1:
            return "Невалидная матрица"
    return "ok"

def get_random_matrix() -> [[float]]:
    from input_from import get_n
    n = get_n()
    ans = []
    for i in range(n):
        ans.append([round(random.random() * 100, 4) for j in range(n + 1)])
    for i in range(n):
        ans[i][i] = round(sum([abs(ans[i][x]) for x in range(len(ans[i]) - 1)]), 4)
    return ans

def check_diagonal_dominance(mrx: [[float]]) -> (bool, [[float]]):
    abs_mrx = []
    for i in mrx:
        abs_mrx.append([abs(i[x]) for x in range(len(i) - 1)])
    max_indexes = [i.index(max(i)) for i in abs_mrx]
    if len(set(max_indexes)) != len(max_indexes):
        return False, mrx
    for i in abs_mrx:
        if max(i) <= sum(i) - max(i):
            return False, mrx
    ans = [[] for i in range(len(mrx))]
    j = 0
    for i in max_indexes:
        ans[i] = mrx[j]
        j += 1
    return True, ans

def get_precision() -> float:
    while True:
        try:
            ans = float(input("Введите точность: ").replace(",", "."))
            if 0 < ans < 1:
                return ans
            print("Точность должна быть больше 0 и меньше 1")
        except ValueError:
            print("Невалидный формат данных")

def print_results(x_1, errors, iter_count):
    if x_1 is None:
        return
    print(f"Вектора неизвестных:")
    n = len(x_1)
    for i in range(n):
        print(f"x_{i + 1}: {x_1[i]}")
    print("Вектора погрешностей:")
    for i in range(n):
        print(f"|x_{i + 1}({iter_count}) - x_{i + 1}({iter_count - 1})|: {errors[i]}")
    print(f"Решение было найдено за {iter_count} итераций")