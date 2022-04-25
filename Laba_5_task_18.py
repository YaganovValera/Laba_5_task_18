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

# Получаем пользовательский ввод:
while True:
    N = input("Введите длину матрицы (положительное, целое число, в диапазоне от 3 до 1000): ")
    N = N.strip()
    if N.isdigit():
        N = int(N)
        if (N >= 3) and (N <= 1000):
            break
        else:
            print("Ошибка. Заданное число не входит в разрешенный диапазон.")
    else:
        print("Неверный ввод данных.")
while True:
    flag_minus = False
    K = input("Введите число K (целое число): ")
    K = K.strip()
    # Проверка на ввод знака
    if K[0] == '-' or K[0] == '+':
        if K[0] == '-':
            flag_minus = True
            K = K.replace('-', '')
        else:
            K = K.replace('+', '')
    if K.isdigit():
        K = int(K)
        if flag_minus:
            K = - int(K)
        break
    else:
        print("Неверный ввод.")

start = time.monotonic()
np.set_printoptions(linewidth=1000)
# Создание и заполнение матрицы A:
A = np.array([[0] * N]*N)
number = 1
for row in range(N):
    for column in range(N):
        # A[row, column] = number
        # number += 1
        A[row, column] = random.randint(-10, 10)
print("Матрица А:\n", A)

# Создание подматриц:
submatrix_length = N // 2                                                       # Длина подматрицы
sub_matrix_C = np.array(A[:submatrix_length, submatrix_length+N % 2:N])
print("\nПодатрица С:\n", sub_matrix_C)
sub_matrix_B = np.array(A[:submatrix_length, :submatrix_length])
sub_matrix_E = np.array(A[submatrix_length+N % 2:N, submatrix_length+N % 2:N])

# Создание матрицы F:
F = A.copy()
print("\nМатрица F: \n", F)

# Обработка матрицы С:
count_number_in_column = np.sum(sub_matrix_C[:, 0:submatrix_length:2] > K)
print("\nКоличество чисел, стоящик в нечетных столбцах подматрицы С, больших К:", count_number_in_column)
multiplication_of_numbers = 1
flag_zero = False                                                               # Отвечает за наличие нуля
for row in range(0, submatrix_length, 2):
    for column in range(submatrix_length):
        if sub_matrix_C[row, column] == 0:
            flag_zero = True
            break
        if abs(multiplication_of_numbers) > count_number_in_column:
            if sub_matrix_C[row, column] < 0:
                multiplication_of_numbers *= (-1)
        else:
            multiplication_of_numbers *= sub_matrix_C[row, column]
    if flag_zero:
        multiplication_of_numbers = 0
        break
print("Произведение чисел, стоящик в нечетных строках подматрицы С:", multiplication_of_numbers)

# Формируем матрицу F:
if count_number_in_column > multiplication_of_numbers:
    F[:submatrix_length, submatrix_length + N % 2:N] = sub_matrix_B[:submatrix_length, ::-1]
    F[:submatrix_length, :submatrix_length] = sub_matrix_C[:submatrix_length, ::-1]
else:
    F[:submatrix_length, submatrix_length+N % 2:N] = sub_matrix_E
    F[submatrix_length+N % 2:N, submatrix_length+N % 2:N] = sub_matrix_C
print("\nОтформатированная матрица F: \n", F)

# Вычисляем выражение:
flag = False
main_diagonal_F = np.sum(F.diagonal())
print("\nСумма диагональных элементов матрицы F:", main_diagonal_F)
sign, logdet = np.linalg.slogdet(A)                                            # вычисляем определитель матрицы А
if logdet > 100:
    logdet = 100
if sign * np.exp(logdet) > main_diagonal_F:
    flag = True
print("Сокращенный определитель матрицы А: {:.3f}".format(sign * np.exp(logdet)))

try:
    if flag:
        print("\nМатрица А транспанированная: \n", A.transpose())
        print("\nПроизведение матрицы А на А^T: \n", A * A.transpose())
        print("\nОбратная матрица F: \n", np.linalg.inv(F))
        print("\nПроизведение обратной матрицы F на K: \n", np.linalg.inv(F)*K)
        print("\n Результат выражения A*A^T - K*F^(-1): \n", A*A.transpose() - np.linalg.inv(F)*K)
    else:
        print("\nОбратная матрица А: \n", np.linalg.inv(A))
        G = np.tri(N)*A
        print("\nНижняя треугольная матрица G, из матрицы А: \n", G)
        print("\nТранспанированная матрица F:\n", F.transpose())
        print("\nВыражение (A^(-1) +G-F^Т): \n", np.linalg.inv(A)+G-F.transpose())
        print("\nРезультат выражения (A^(-1) +G-F^Т)*K:\n", (np.linalg.inv(A)+G-F.transpose())*K)
except np.linalg.LinAlgError:
    print('Ошибка. Одна из матриц является вырожденной(определитель равен 0), поэтому обратную матрицу найти невозможно.')

finish = time.monotonic()
print("\nВремя работы программы:", finish - start, "sec.")