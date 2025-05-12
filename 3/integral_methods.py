def runge_rule(I_0, I_1, eps, name):
    divi = 4 if "simpson" in name else 2
    return abs(I_1 - I_0) / (2 ** divi - 1) <= eps

def left_rectangles(a, b, n, f, eps) -> (float, str):
    I_0, I_1 = 0, 0
    iter_count = 0
    result_msg = ""

    while (I_0 == 0 and I_1 == 0) or not runge_rule(I_0, I_1, eps, left_rectangles.__name__):
        I_0, I_1 = 0, 0
        iter_count += 1
        delta_x = (b - a) / (2 * n)
        for i in range(2 * n):
            x_i = a + delta_x * i
            I_1 += f(x_i) * delta_x

            if i % 2 == 0:
                I_0 += f(x_i) * delta_x * 2

        result_msg += '|'.join([i.center(16) for i in
                                f"{iter_count} {n} {round(I_0, 4)} {round(I_1, 4)} {round(abs(I_0 - I_1) / 3, 4)}".split()]) + '\n'

        n *= 2
    return I_1, result_msg

def right_rectangles(a, b, n, f, eps) -> (float, str):
    I_0, I_1 = 0, 0
    iter_count = 0
    result_msg = ""

    while (I_0 == 0 and I_1 == 0) or not runge_rule(I_0, I_1, eps, right_rectangles.__name__):
        I_0, I_1 = 0, 0
        iter_count += 1
        delta_x = (b - a) / (2 * n)
        for i in range(2 * n):
            x_i = a + delta_x * (i + 1)
            I_1 += f(x_i) * delta_x

            if i % 2 == 0:
                I_0 += f(x_i) * delta_x * 2

        result_msg += '|'.join([i.center(16) for i in
                                f"{iter_count} {n} {round(I_0, 4)} {round(I_1, 4)} {round(abs(I_0 - I_1) / 3, 4)}".split()]) + '\n'

        n *= 2
    return I_1, result_msg

def middle_rectangles(a, b, n, f, eps) -> (float, str):
    I_0, I_1 = 0, 0
    iter_count = 0
    result_msg = ''
    while (I_0 == 0 and I_1 == 0) or not runge_rule(I_0, I_1, eps, middle_rectangles.__name__):
        I_0, I_1 = 0, 0
        iter_count += 1
        delta_x = (b - a) / (2 * n)
        for i in range(2 * n):
            left, right = a + delta_x * i, a + delta_x * (i + 1)
            x_i = (left + right) / 2
            I_1 += f(x_i) * delta_x

            if i % 2 == 0:
                I_0 += f(x_i) * delta_x * 2

        result_msg += '|'.join([i.center(16) for i in
                                f"{iter_count} {n} {round(I_0, 4)} {round(I_1, 4)} {round(abs(I_0 - I_1) / 3, 4)}".split()]) + '\n'

        n *= 2
    return I_1, result_msg

def trapezoid(a, b, n, f, eps) -> (float, str):
    I_0, I_1 = 0, 0
    iter_count = 0
    result_msg = ""

    while iter_count == 0 or not runge_rule(I_0, I_1, eps, trapezoid.__name__):
        iter_count += 1
        I_0 = trapezoid_count(a, b, n, f)
        I_1 = trapezoid_count(a, b, n * 2, f)

        result_msg += '|'.join([i.center(16) for i in
                                f"{iter_count} {n} {round(I_0, 4)} {round(I_1, 4)} {round(abs(I_0 - I_1) / 3, 4)}".split()]) + '\n'

        n *= 2
    return I_1, result_msg

def trapezoid_count(a, b, n, f):
    res = 0
    delta_x = (b - a) / n
    for i in range(n):
        x_i_1 = a + delta_x * i
        x_i = a + delta_x * (i + 1)
        s_i = (f(x_i_1) + f(x_i)) * delta_x / 2
        res += s_i
    return res

def simpson(a, b, n, f, eps) -> (float, str):
    I_0, I_1 = 0, 0
    iter_count = 0
    result_msg = ""

    while iter_count == 0 or not runge_rule(I_0, I_1, eps, simpson.__name__):
        iter_count += 1
        I_0 = simpson_count(a, b, n, f)
        I_1 = simpson_count(a, b, n * 2, f)

        result_msg += '|'.join([i.center(16) for i in
                                f"{iter_count} {n} {round(I_0, 4)} {round(I_1, 4)} {round(abs(I_0 - I_1) / 3, 4)}".split()]) + '\n'

        n *= 2

    return I_1, result_msg

def simpson_count(a, b, n, f):
    res = 0
    delta_x = (b - a) / n
    for i in range(n):
        x_i_1 = a + delta_x * i
        x_i = a + delta_x * (i + 1)
        s_i = (f(x_i_1) + 4 * f((x_i_1 + x_i) / 2) + f(x_i)) * delta_x / 6
        res += s_i

    return res
