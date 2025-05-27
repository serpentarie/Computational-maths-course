from approximation_methods import *
import io

def format_table_to_string(n, X, Y, phi_func, title):
    output_buffer = io.StringIO()
    current_sko = None

    print(f"{title}:".center(90), file=output_buffer)

    if not X or not Y:
        print("Нет данных для отображения в таблице.", file=output_buffer)
        return output_buffer.getvalue(), current_sko

    try:
        phi_values = [phi_func(x_val) for x_val in X]
    except Exception as e:
        print(f"Ошибка при вычислении phi(X): {e}", file=output_buffer)
        phi_values = ["N/A"] * n

    header_width = 12
    print("X".center(10) + "|" + "|".join([str(round(x_val, 4)).center(header_width) for x_val in X]),
          file=output_buffer)
    print("-" * (10 + 1 + n * (header_width + 1)), file=output_buffer)
    print("Y".center(10) + "|" + "|".join([str(round(y_val, 4)).center(header_width) for y_val in Y]),
          file=output_buffer)
    print("-" * (10 + 1 + n * (header_width + 1)), file=output_buffer)

    print("phi(X)".center(10) + "|" + "|".join(
        [str(round(pv, 4) if isinstance(pv, (int, float)) else pv).center(header_width) for pv in phi_values]),
          file=output_buffer)
    print("-" * (10 + 1 + n * (header_width + 1)), file=output_buffer)

    if all(isinstance(pv, (int, float)) for pv in phi_values) and all(
            isinstance(y_val, (int, float)) for y_val in Y) and n == len(phi_values):
        current_sko = standard_error_of_estimate(Y, phi_values)
        e_i = [phi_values[i] - Y[i] for i in range(n)]
        print("e_i".center(10) + "|" + "|".join([str(round(e, 4)).center(header_width) for e in e_i]),
              file=output_buffer)
        if current_sko is not None:
            print(f"Среднеквадратичное отклонение: {round(current_sko, 10)}", file=output_buffer)
        else:
            print("Среднеквадратичное отклонение: N/A", file=output_buffer)
    else:
        print("e_i".center(10) + "|" + "|".join(["N/A".center(header_width)] * n), file=output_buffer)
        print("Среднеквадратичное отклонение: N/A", file=output_buffer)

    print("\n", file=output_buffer)
    return output_buffer.getvalue(), current_sko