"""С клавиатуры вводится два числа K и N. Квадратная матрица А(N,N), состоящая из 4-х равных по размерам подматриц,
B,C,D,E заполняется случайным образом целыми числами в интервале [-10,10].
Для тестирования использовать не случайное заполнение, а целенаправленное. Вид матрицы А:
 |B|C|
 |D|E|
Формируется матрица F следующим образом: скопировать в нее А и  если в С количество чисел, больших К в нечетных столбцах,
больше чем произведение чисел в нечетных строках, то поменять местами С и В симметрично, иначе С и Е поменять местами несимметрично.
При этом матрица А не меняется. После чего если определитель матрицы А больше суммы диагональных элементов матрицы F,
то вычисляется выражение: A*A^T – K * F^(-1), иначе вычисляется выражение (A^(-1) +G-F^Т)*K, где G-нижняя треугольная матрица, полученная из А.
Выводятся по мере формирования А, F и все матричные операции последовательно.
"""

import numpy as np
import random
import time

try:
    N = int(input("Введите длину матрицы (положительное, целое число, > 3): "))
    while N <= 3:
        N = int(input("Введите длину матрицы (положительное, целое число, > 3): "))
    K = int(input("Введите число K (целое число): "))
    start = time.monotonic()
    np.set_printoptions(linewidth=1000)
    # Создание и заполнение матрицы A:
    A = np.random.randint(-10.0, 10.0, (N, N))
    print("Матрица А:\n", A)
    # Создание подматриц:
    submatrix_length = N // 2                                                       # Длина подматрицы
    sub_matrix_C = np.array(A[:submatrix_length, submatrix_length+N % 2:N])
    sub_matrix_B = np.array(A[:submatrix_length, :submatrix_length])
    sub_matrix_E = np.array(A[submatrix_length+N % 2:N, submatrix_length+N % 2:N])
    # Создание матрицы F:
    F = A.copy()
    print("\nМатрица F: \n", F)
    # Обработка матрицы С:
    count_number_in_column = np.sum(sub_matrix_C[:, 0:submatrix_length:2] > K)
    multiplication_of_numbers = sub_matrix_C[1::2].prod()
    print("Сумма чисел стоящих в нечетных столбцах подматрицы С, которые больше К:", count_number_in_column)
    print("Произведение чисел стоящих в нечетных строках подматрицы С:", multiplication_of_numbers)
    # Формируем матрицу F:
    if count_number_in_column > multiplication_of_numbers:
        F[:submatrix_length, submatrix_length + N % 2:N] = sub_matrix_B[:submatrix_length, ::-1]
        F[:submatrix_length, :submatrix_length] = sub_matrix_C[:submatrix_length, ::-1]
    else:
        F[:submatrix_length, submatrix_length+N % 2:N] = sub_matrix_E
        F[submatrix_length+N % 2:N, submatrix_length+N % 2:N] = sub_matrix_C
    print("\nОтформатированная матрица F: \n", F)
    # Вычисляем выражение:
    try:
        if np.linalg.det(A) > sum(np.diagonal(F)):
            print("\n Результат выражения A*A^T - K*F^(-1): \n", A*A.transpose() - np.linalg.inv(F)*K)
        else:
            G = np.tri(N)*A
            print("\nРезультат выражения (A^(-1) +G-F^Т)*K:\n", (np.linalg.inv(A)+G-F.transpose())*K)
    except np.linalg.LinAlgError:
        print('Одна из матриц является вырожденной(определитель равен 0), поэтому обратную матрицу найти невозможно.')
    finish = time.monotonic()
    print("\nВремя работы программы:", finish - start, "sec.")
except ValueError:
    print("Введены неверные даннные")