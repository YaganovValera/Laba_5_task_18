>С клавиатуры вводится два числа K и N. Квадратная матрица А(N,N), состоящая из 4-х равных по размерам подматриц,
B,C,D,E заполняется случайным образом целыми числами в интервале [-10,10].
Для тестирования использовать не случайное заполнение, а целенаправленное. Вид матрицы А:
> 
> <a><img src="https://i.ibb.co/jWGcYHk/2022-03-27-150217.png" alt="2022-03-27-150217" border="0"></a>
> 
>Формируется матрица F следующим образом: скопировать в нее А и  если в С количество чисел, больших К в нечетных столбцах,
больше чем произведение чисел в нечетных строках, то поменять местами С и В симметрично, иначе С и Е поменять местами несимметрично.
При этом матрица А не меняется. После чего если определитель матрицы А больше суммы диагональных элементов матрицы F,
то вычисляется выражение: A*A^T – K * F^(-1), иначе вычисляется выражение (A^(-1) +G-F^Т)*K, где G-нижняя треугольная матрица, полученная из А.
Выводятся по мере формирования А, F и все матричные операции последовательно.
