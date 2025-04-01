def do_simple_iteration(c: [[float]], d: [float], x: [float]) -> [float]:
    ans_x = []
    for i in range(len(d)):
        ans_x.append(d[i] + sum([x[j] * c[i][j] for j in range(len(c[i]))]))
    return ans_x

def iteration_algo(mrx: [[float]], precision: float):
    n = len(mrx)
    d = [mrx[i][-1] / mrx[i][i] for i in range(n)]
    iter_count = 0
    x = d.copy()
    c = []

    for i in range(n):
        c_row = []
        for j in range(n):
            if i == j:
                c_row.append(0)
            else:
                value = -(mrx[i][j] / mrx[i][i])
                c_row.append(value)
        c.append(c_row)

    row_sums = [sum(abs(c[i][j]) for j in range(n)) for i in range(n)]
    max_row_sum = max(row_sums)

    if max_row_sum >= 1:
        print("Метод простой итерации не сходиться, так как норма матрицы >= 1\n")
        return None, None, None, max_row_sum

    last_err = float('inf')
    while True:
        iter_count += 1
        x_1 = do_simple_iteration(c, d, x)
        errors = [abs(x_1[i] - x[i]) for i in range(len(x))]
        if max(errors) <= precision:
            return x_1, errors, iter_count, max_row_sum
        if max(errors) > last_err:
            print("Ответ не может быть найден")
            return None, None, None, max_row_sum
        last_err = max(errors)
        x = x_1