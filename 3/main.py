from integral_methods import *
from integrals import *

functions_dict = {
    "1": {"f": f1, "integral": integral1, "discontinuity": None, "odd": False, "converges": True},
    "2": {"f": f2, "integral": integral2, "discontinuity": None, "odd": False, "converges": True},
    "3": {"f": f3, "integral": integral3, "discontinuity": None, "odd": False, "converges": True},
    "4": {"f": f4, "integral": None, "discontinuity": 0, "odd": True, "converges": False},
    "5": {"f": f5, "integral": None, "discontinuity": 0, "odd": False, "converges": True},
    "6": {"f": f6, "integral": None, "discontinuity": 0, "odd": False, "converges": False},
    "7": {"f": f7, "integral": None, "discontinuity": 1, "odd": False, "converges": False}
}

methods_dict = {
    "1": left_rectangles,
    "2": right_rectangles,
    "3": middle_rectangles,
    "4": trapezoid,
    "5": simpson
}

methods_names = {
    left_rectangles: "Метод левых прямоугольников",
    right_rectangles: "Метод правых прямоугольников",
    middle_rectangles: "Метод средних прямоугольников",
    trapezoid: "Метод трапеций",
    simpson: "Метод Симпсона"
}

def solve(function_info, solving_method, A, B, eps):
    f = function_info["f"]
    discontinuity = function_info.get("discontinuity", None)
    converges = function_info.get("converges", True)
    odd = function_info.get("odd", False)
    epsilon = 1e-6

    if discontinuity is not None and A <= discontinuity <= B:
        c = discontinuity
        if not converges and not (odd and A < c < B):
            print("Интеграл не существует")
            return
        else:
            if odd and A < c < B:
                a_sym = max(A, -(B - c) + c)
                b_sym = min(B, -A + c + c)
                if a_sym < c < b_sym:
                    print(f"Интеграл на [{a_sym}, {b_sym}] равен 0 из-за нечетности функции")
                    if a_sym == A and b_sym == B:
                        ans = 0
                    elif a_sym == A:
                        print(f"Вычисляем интеграл от {b_sym + epsilon} до {B}:")
                        print("|".join(i.center(16) for i in '№ n I_0 I_1 |I_1-I_0|/2^k'.split()) + "\n" + "-" * 90)
                        ans, msg = solving_method(b_sym + epsilon, B, 4, f, eps)
                        print(msg)
                    elif b_sym == B:
                        print(f"Вычисляем интеграл от {A} до {a_sym - epsilon}:")
                        print("|".join(i.center(16) for i in '№ n I_0 I_1 |I_1-I_0|/2^k'.split()) + "\n" + "-" * 90)
                        ans, msg = solving_method(A, a_sym - epsilon, 4, f, eps)
                        print(msg)
                    else:
                        print(f"Вычисляем интеграл от {A} до {a_sym - epsilon}:")
                        print("|".join(i.center(16) for i in '№ n I_0 I_1 |I_1-I_0|/2^k'.split()) + "\n" + "-" * 90)
                        I1, msg1 = solving_method(A, a_sym - epsilon, 4, f, eps)
                        print(msg1)
                        print(f"Вычисляем интеграл от {b_sym + epsilon} до {B}:")
                        print("|".join(i.center(16) for i in '№ n I_0 I_1 |I_1-I_0|/2^k'.split()) + "\n" + "-" * 90)
                        I2, msg2 = solving_method(b_sym + epsilon, B, 4, f, eps)
                        print(msg2)
                        ans = I1 + I2
                else:
                    print(f"Разбиваем интервал на [{A}, {c - epsilon}] и [{c + epsilon}, {B}]")
                    print(f"Вычисляем интеграл от {A} до {c - epsilon}:")
                    print("|".join(i.center(16) for i in '№ n I_0 I_1 |I_1-I_0|/2^k'.split()) + "\n" + "-" * 90)
                    I1, msg1 = solving_method(A, c - epsilon, 4, f, eps)
                    print(msg1)
                    print(f"Вычисляем интеграл от {c + epsilon} до {B}:")
                    print("|".join(i.center(16) for i in '№ n I_0 I_1 |I_1-I_0|/2^k'.split()) + "\n" + "-" * 90)
                    I2, msg2 = solving_method(c + epsilon, B, 4, f, eps)
                    print(msg2)
                    ans = I1 + I2
            elif A < c < B:
                print(f"Разбиваем интервал на [{A}, {c - epsilon}] и [{c + epsilon}, {B}]")
                print(f"Вычисляем интеграл от {A} до {c - epsilon}:")
                print("|".join(i.center(16) for i in '№ n I_0 I_1 |I_1-I_0|/2^k'.split()) + "\n" + "-" * 90)
                I1, msg1 = solving_method(A, c - epsilon, 4, f, eps)
                print(msg1)
                print(f"Вычисляем интеграл от {c + epsilon} до {B}:")
                print("|".join(i.center(16) for i in '№ n I_0 I_1 |I_1-I_0|/2^k'.split()) + "\n" + "-" * 90)
                I2, msg2 = solving_method(c + epsilon, B, 4, f, eps)
                print(msg2)
                ans = I1 + I2
            elif A == c:
                print(f"Вычисляем интеграл от {A + epsilon} до {B}:")
                print("|".join(i.center(16) for i in '№ n I_0 I_1 |I_1-I_0|/2^k'.split()) + "\n" + "-" * 90)
                ans, msg = solving_method(A + epsilon, B, 4, f, eps)
                print(msg)
            elif B == c:
                print(f"Вычисляем интеграл от {A} до {B - epsilon}:")
                print("|".join(i.center(16) for i in '№ n I_0 I_1 |I_1-I_0|/2^k'.split()) + "\n" + "-" * 90)
                ans, msg = solving_method(A, B - epsilon, 4, f, eps)
                print(msg)
    else:
        print("|".join(i.center(16) for i in '№ n I_0 I_1 |I_1-I_0|/2^k'.split()) + "\n" + "-" * 90)
        ans, msg = solving_method(A, B, 4, f, eps)
        print(msg)

    print(f"Решение: {round(ans, 4)}")

def ask_to_continue():
    while True:
        print("\nПродолжать выполнение?")
        print("(д)а / (н)ет")
        print("(y)es / (n)o")
        answer = input().lower().strip()
        if answer in ["y", "yes", "д", "да"]:
            return True
        elif answer in ["n", "no", "н", "нет"]:
            return False
        else:
            print("Пожалуйста, введите да или нет")

if __name__ == "__main__":
    while True:
        print("Выберите функцию для интегрирования: ")
        print("1) 2x^3 - 3x^2 + 5x - 9".center(40))
        print("2) -3x^3 - 5x^2 + 4x + 5".center(40))
        print("3) x^3 - 2x^2 - 5x + 24".center(40))
        print("4) 1/x".center(22))
        print("5) 1/|x|^0.5 (разрыв в 0, сходится)".center(52))
        print("6) 1/|x|^2 (разрыв в 0, расходится)".center(52))
        print("7) 1/(x-1) (разрыв в 1, расходится)".center(52))
        function_num = None
        while function_num is None:
            function_num = input("Введите номер функции, которую хотите проинтегрировать: ").strip()
            if "1" <= function_num <= "7":
                break
            function_num = None
            print("Такой функции нету")

        function = functions_dict[function_num]

        A, B = None, None
        while A is None or B is None:
            try:
                A_str, B_str = input("Введите границы интегрирования через пробел: ").split()
                A = float(A_str.replace(",", "."))
                B = float(B_str.replace(",", "."))
                if A > B:
                    raise ValueError
                break
            except ValueError:
                print("Введите числа, они должны идти по возрастанию")
                A, B = None, None

        print("Методы интегрирования:")
        print("\n".join(f"\t{k}) {methods_names[v]}" for k, v in methods_dict.items()))

        method_num = None
        while method_num is None:
            method_num = input("Введите номер метода: ").strip()
            if "1" <= method_num <= "5":
                break
            method_num = None
            print("Такого метода нет")

        method = methods_dict[method_num]
        eps = None
        while eps is None:
            try:
                eps_str = input("Введите точность: ")
                eps = float(eps_str.replace(",", "."))
                if eps <= 0:
                    raise ValueError
            except ValueError:
                print("Точность должна быть положительным числом")
                eps = None

        solve(functions_dict[function_num], method, A, B, eps)
        if not ask_to_continue():
            break