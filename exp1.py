import mmap
import time

PAGE = mmap.PAGESIZE
SIZE = 256 << 20

def read_status():
    vsize_kb = 0
    rss_kb = 0
    with open("/proc/self/status") as f:
        for line in f:
            if line.startswith("VmSize:"):
                vsize_kb = int(line.split()[1])
            elif line.startswith("VmRSS:"):
                rss_kb = int(line.split()[1])
    return vsize_kb, rss_kb

def read_minflt():
    with open("/proc/self/stat") as f:
        text = f.read()
    tail = text[text.rfind(")") + 1:].split()
    return int(tail[7])

def print_mem(stage, prev_minflt=None):
    vsize_kb, rss_kb = read_status()
    mf = read_minflt()
    delta = "" if prev_minflt is None else f" (+{mf - prev_minflt} minor)"
    print(f"{stage:25s} VmSize = {vsize_kb/1024:8.1f} МиБ  RSS = {rss_kb/1024:8.1f} МиБ  minflt = {mf}{delta}")
    return mf

print(f"Размер страницы: {PAGE} байт")
mf0 = print_mem("Начало")

block = mmap.mmap(-1, SIZE)
mf1 = print_mem("После выделения", mf0)

checksum = 0
t0 = time.perf_counter()
for i in range(0, SIZE, PAGE):
    checksum += block[i]
t1 = time.perf_counter()
mf2 = print_mem("После первого чтения", mf1)
print(f"  время чтения: {(t1 - t0) * 1000:.1f} мс, контрольная сумма: {checksum}")

t0 = time.perf_counter()
for i in range(0, SIZE, PAGE):
    block[i] = 1
t1 = time.perf_counter()
mf3 = print_mem("После первой записи", mf2)
print(f"  время 1-й записи: {(t1 - t0) * 1000:.1f} мс")

t0 = time.perf_counter()
for i in range(0, SIZE, PAGE):
    block[i] = 2
t1 = time.perf_counter()
mf4 = print_mem("После повторной записи", mf3)
print(f"  время 2-й записи: {(t1 - t0) * 1000:.1f} мс")

print(f"Проверка значений: block[0]={block[0]}, block[{PAGE}]={block[PAGE]}, block[{SIZE-PAGE}]={block[SIZE-PAGE]}")

block.close()
mf5 = print_mem("После освобождения", mf4)
