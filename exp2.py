import time
import numpy as np

N = 8192  # 8192x8192x4 байта = 256 МБ

def timeit(fn, repeats=3):
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        s = fn()
        t1 = time.perf_counter()
        times.append((t1 - t0) * 1000)
    return sum(times) / len(times), s

print("Создаем матрицу...")
a = np.arange(N * N, dtype=np.int32).reshape(N, N)

def sum_rows():
    s = 0
    for i in range(N):
        s += int(a[i, :].sum())
    return s

def sum_cols():
    s = 0
    for j in range(N):
        s += int(a[:, j].sum())
    return s

print("Считаем сумму по строкам...")
tr, sr = timeit(sum_rows)

print("Считаем сумму по столбцам...")
tc, sc = timeit(sum_cols)

print(f"\nСумма по строкам:  {sr}")
print(f"Сумма по столбцам: {sc}")
print(f"Совпадают: {sr == sc}")
print(f"Время по строкам:  {tr:.1f} мс")
print(f"Время по столбцам: {tc:.1f} мс")
print(f"Столбцы медленнее в {tc / tr:.2f} раз")
print(f"Проверка элемента a[{N-1}, {N-1}]: {a[N-1, N-1]}")
