from functions import *

def get_input_type() -> int:
    print("Выберите тип ввода:\n"
          "1. С клавиатуры\n"
          "2. С файла\n"
          "3. Рандомно генерированная матрица")
    while True:
        inp = input()
        if inp == "1":
            return 1
        elif inp == "2":
            return 2
        elif inp == "3":
            return 3
        print("Повтори ввод")

def get_n() -> int:
    print("Выберите тип ввода:\n"
          "1. С клавиатуры\n"
          "2. С файла")
    inp = ""
    while True:
        inp = input()
        if inp == "1" or inp == "2":
            break
    if inp == "1":
        while True:
            try:
                n = int(input("n: "))
                if 0 < n <= 20:
                    return n
                print("n выходит за границы")
            except ValueError:
                print("n не валидно")
    else:
        while True:
            try:
                inp = input("Введите имя файла: ")
                f = open("/home/serpentarie/PycharmProjects/Computational-maths-course/1_System_of_linear_equations/resources/" + inp)
                n = int(f.readline())
                f.close()
                if 0 < n <= 20:
                    return n
                print("n выходит за границы")
            except ValueError:
                print("n не валидно")
            except EOFError:
                print("n это не файл")
            except FileNotFoundError:
                print("файл не найден")

def get_matrix_from_file() -> [[float]]:
    while True:
        try:
            file = input("Введите имя файла:")
            f = open("/home/serpentarie/PycharmProjects/Computational-maths-course/1_System_of_linear_equations/resources/" + file)
            ans = []
            for line in f:
                ans.append([float(x.replace(",", ".")) for x in line.split(" ")])
            res = matrix_valid(ans)
            f.close()
            if res == "ok":
                return ans
            print(res)
        except FileNotFoundError:
            print("Нет такого файла")
        except ValueError:
            print("Невалидный файл")

def get_matrix_from_console() -> [[float]]:
    while True:
        try:
            ans = [[float(x.replace(",", ".")) for x in input().split(" ")]]
            for i in range(len(ans[0]) - 2):
                ans.append([float(x.replace(",", ".")) for x in input().split(" ")])
            res = matrix_valid(ans)
            if res == 'ok':
                return ans
            print(res)
        except ValueError:
            print("Невалидный формат ввода")