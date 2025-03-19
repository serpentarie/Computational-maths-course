from input_from import *
from method import *

if __name__ == '__main__':
    while True:
        matrix = []
        inp_type = get_input_type()
        if inp_type == 1:
            matrix = get_matrix_from_console()
        elif inp_type == 2:
            matrix = get_matrix_from_file()
        else:
            matrix = get_random_matrix()
        res = check_diagonal_dominance(matrix)
        if not res[0]:
            print("Отсутствует диагональное преобладание")
        matrix = res[1]
        print_matrix(matrix)
        eps = get_precision()
        res_x, res_errors, res_iter, norm = iteration_algo(matrix, eps)
        print(f"Норма матрицы: {norm}")
        print_results(res_x, res_errors, res_iter)