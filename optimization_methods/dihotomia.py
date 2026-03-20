epsilon = 0.5
l = 2*epsilon
delta = 0.2
def f(x):
    return x*x - 4*x + 6

a = []
b = []
a.append(0)
b.append(10)

print("\n\nпоиск минимума функции методом Дихотомии\n")
k = 0
while (True):
    print(f'k = {k}')

    y = (a[k] + b[k] - delta)/2
    z = y + delta
    print(f'y_{k} = {y:.4f}, z_{k} = {z:.4f}')

    fy, fz = f(y), f(z)
    print(f"Сравнение f(y_{k}) и f(z_{k}):")
    if fy <= fz:
        ## a_k не изменится
        a.append(a[k])
        ## b_k = z
        b.append(z)
        print(f'f(y_{k}) = {fy:.4f} < f(z_{k}) = {fz:.4f}   ->  b[{k+1}] = z_{k} = {z:.4f}')
    else:
        ## b_k не изменится
        b.append(b[k])
        ## a[k+1] = y
        a.append(y)
        print(f'f(y_{k}) = {fy:.4f} > f(z_{k}) = {fz:.4f}   ->  a[{k+1}] = y_{k} = {y:.4f}')

    L = b[k+1] - a[k+1]
    if L <= l:
        print(f"L_{2*(k+1)} = {L:.4f} < 1   ->   процесс поиска завершён (за {k+1} итераций)!\n")
        print(f'x принадлежит отрезку L_{2*(k+1)} = [{a[k+1]:.4f}; {b[k+1]:.4f}]')
        print(f'приближённое решение: x* ~= {(a[k+1] + b[k+1])/2 :.5f} +- {L/2:.4f}\n')
        break
    else:
        print(f"L_{2*(k+1)} = {L:.4f} > 1   ->   переходим к следующей итерации.\n")
        k = k + 1
