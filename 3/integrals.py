def f1(x):
    return 2 * x ** 3 - 3 * x ** 2 + 5 * x - 9

def integral1(x):
    return x ** 4 / 2 - x ** 3 + 5 * x ** 2 / 2 - 9 * x

def f2(x):
    return -3 * x ** 3 - 5 * x ** 2 + 4 * x + 5

def integral2(x):
    return -0.75 * x ** 4 - 5 * x / 3 + 2 * x ** 2 - 5 * x

def f3(x):
    return x ** 3 - 2 * x ** 2 - 5 * x + 24

def integral3(x):
    return x ** 4 / 4 - 2 / 3 * x ** 3 - 5 / 2 * x ** 2 + 24 * x

def f4(x):
    return 1 / x

def f5(x):
    return 1 / abs(x)**0.5 if x != 0 else float('inf')  # Разрыв в x=0, интеграл сходится

def f6(x):
    return 1 / abs(x)**2 if x != 0 else float('inf')    # Разрыв в x=0, интеграл расходится

def f7(x):
    return 1 / (x - 1) if x != 1 else float('inf')      # Разрыв в x=1, интеграл расходится