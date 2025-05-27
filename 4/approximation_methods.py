import math

def solve_linear_system_custom(A_orig, B_orig):
    A = [row[:] for row in A_orig]
    B = B_orig[:]
    n = len(A)

    if not A or n == 0 or len(B) != n:
        return None
    for i in range(n):
        if len(A[i]) != n:
            return None

    epsilon = 1e-12

    for i in range(n):
        pivot_row = i
        max_val = abs(A[i][i])
        for k in range(i + 1, n):
            if abs(A[k][i]) > max_val:
                max_val = abs(A[k][i])
                pivot_row = k

        if pivot_row != i:
            A[i], A[pivot_row] = A[pivot_row], A[i]
            B[i], B[pivot_row] = B[pivot_row], B[i]

        if abs(A[i][i]) < epsilon:
            return None

        for k in range(i + 1, n):
            factor = A[k][i] / A[i][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            B[k] -= factor * B[i]

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        sum_ax = 0.0
        for j in range(i + 1, n):
            sum_ax += A[i][j] * x[j]

        if abs(A[i][i]) < epsilon:
            return None

        x[i] = (B[i] - sum_ax) / A[i][i]

    return x

def count_sums_1(n, X, Y):
    S_X = sum(X)
    S_Y = sum(Y)
    S_XX = sum(map(lambda x: x ** 2, X))
    S_XY = sum([X[i] * Y[i] for i in range(n)])
    return S_X, S_Y, S_XX, S_XY


def count_sums_2(n, X, Y):
    S_X3 = sum(map(lambda x: x ** 3, X))
    S_X2Y = sum([X[i] ** 2 * Y[i] for i in range(n)])
    S_X4 = sum(map(lambda x: x ** 4, X))
    return S_X3, S_X2Y, S_X4


def count_sums_3(n, X, Y):
    S_X5 = sum(map(lambda x: x ** 5, X))
    S_X3Y = sum([X[i] ** 3 * Y[i] for i in range(n)])
    S_X6 = sum(map(lambda x: x ** 6, X))
    return S_X5, S_X6, S_X3Y


def linear_approximation(n, X, Y) -> (float, float):
    S_X, S_Y, S_XX, S_XY = count_sums_1(n, X, Y)

    delta = S_XX * n - S_X ** 2

    if abs(delta) < 1e-12:
        return None, None

    delta_1 = S_XY * n - S_X * S_Y
    delta_2 = S_XX * S_Y - S_X * S_XY

    return delta_1 / delta, delta_2 / delta

def quadratic_approximation(n, X, Y) -> (float, float, float):

    S_X, S_Y, S_X2, S_XY = count_sums_1(n, X, Y)
    S_X3, S_X2Y, S_X4 = count_sums_2(n, X, Y)

    A = [[n, S_X, S_X2],
         [S_X, S_X2, S_X3],
         [S_X2, S_X3, S_X4]]
    B = [S_Y, S_XY, S_X2Y]

    solution = solve_linear_system_custom(A, B)

    if solution is None:
        return None, None, None

    a, b, c = solution[::-1]
    return a, b, c


def cubic_approximation(n, X, Y) -> (float, float, float, float):

    S_X, S_Y, S_X2, S_XY = count_sums_1(n, X, Y)
    S_X3, S_X2Y, S_X4 = count_sums_2(n, X, Y)
    S_X5, S_X6, S_X3Y = count_sums_3(n, X, Y)

    A = [
        [S_X6, S_X5, S_X4, S_X3],
        [S_X5, S_X4, S_X3, S_X2],
        [S_X4, S_X3, S_X2, S_X],
        [S_X3, S_X2, S_X, n]
    ]
    B = [S_X3Y, S_X2Y, S_XY, S_Y]

    solution = solve_linear_system_custom(A, B)

    if solution is None:
        return None, None, None, None

    return tuple(solution)


def exponential_approximation(n, X, Y):
    clean_X = []
    clean_Y = []

    for x, y_val in zip(X, Y):
        if y_val is not None and y_val > 0:
            clean_X.append(x)
            clean_Y.append(y_val)

    if len(clean_Y) < 8:
        return None, None, None, None

    try:
        lnY = [math.log(y_val) for y_val in clean_Y]
        b_coeff, ln_a_coeff = linear_approximation(len(lnY), clean_X, lnY)

        if b_coeff is None:
            return None, None, None, None

        return math.exp(ln_a_coeff), b_coeff, clean_X, clean_Y
    except (ValueError, TypeError):
        return None, None, None, None


def logarithm_approximation(n, X, Y):
    clean_X = []
    clean_Y = []

    for x_val, y_val in zip(X, Y):
        if x_val is not None and y_val is not None and x_val > 0:
            clean_X.append(x_val)
            clean_Y.append(y_val)

    if len(clean_X) < 8:
        return None, None, None, None

    try:
        lnX = [math.log(x_val) for x_val in clean_X]
        a_coeff, b_coeff = linear_approximation(len(lnX), lnX, clean_Y)

        if a_coeff is None:
            return None, None, None, None

        return a_coeff, b_coeff, clean_X, clean_Y
    except (ValueError, TypeError):
        return None, None, None, None


def pow_approximation(n, X, Y):
    clean_X = []
    clean_Y = []

    for x_val, y_val in zip(X, Y):
        if x_val is not None and y_val is not None and x_val > 0 and y_val > 0:
            clean_X.append(x_val)
            clean_Y.append(y_val)

    if len(clean_X) < 8:
        return None, None, None, None

    try:
        lnX = [math.log(x_val) for x_val in clean_X]
        lnY = [math.log(y_val) for y_val in clean_Y]

        b_coeff, ln_a_coeff = linear_approximation(len(lnX), lnX, lnY)

        if b_coeff is None:
            return None, None, None, None

        a_coeff = math.exp(ln_a_coeff)
        return a_coeff, b_coeff, clean_X, clean_Y
    except (ValueError, TypeError):
        return None, None, None, None


def pearson_correlation(X, Y):
    n = len(X)
    if n == 0 or len(Y) != n:
        return None

    sum_X = sum(X)
    sum_Y = sum(Y)
    sum_X_sq = sum(x ** 2 for x in X)
    sum_Y_sq = sum(y ** 2 for y in Y)
    sum_XY = sum(X[i] * Y[i] for i in range(n))

    numerator = n * sum_XY - sum_X * sum_Y
    denominator_X = math.sqrt(n * sum_X_sq - sum_X ** 2)
    denominator_Y = math.sqrt(n * sum_Y_sq - sum_Y ** 2)

    if denominator_X == 0 or denominator_Y == 0:
        return None

    return numerator / (denominator_X * denominator_Y)


def coefficient_of_determination(Y_observed, Y_predicted):
    if len(Y_observed) == 0 or len(Y_observed) != len(Y_predicted):
        return None

    mean_Y_observed = sum(Y_observed) / len(Y_observed)

    ss_total = sum((y_obs - mean_Y_observed) ** 2 for y_obs in Y_observed)

    if len(Y_observed) != len(Y_predicted):
        raise ValueError()

    ss_residual = sum((Y_observed[i] - Y_predicted[i]) ** 2 for i in range(len(Y_observed)))

    if ss_total == 0:
        return 1.0 if ss_residual == 0 else None

    r_squared = 1 - (ss_residual / ss_total)
    return r_squared


def standard_error_of_estimate(Y_observed, Y_predicted):
    n = len(Y_observed)
    if n == 0 or n != len(Y_predicted):
        return None

    squared_errors = [(Y_observed[i] - Y_predicted[i]) ** 2 for i in range(n)]
    mse = sum(squared_errors) / n
    return math.sqrt(mse)