def f(x):
    return x*x - 4*x + 6

epsilon = 0.5
l = 2 * epsilon
alpha = (3 - 5**0.5) / 2

print("\n\nпоиск минимума функции методом золотого сечения")

a = [0]
b = [10]
L0 = b[0] - a[0]
print(f'L_0 = {b[0]:.2f} - {a[0]:.2f} = {L0:.2f}')

y = a[0] + alpha*L0
z = a[0] + b[0] - y
print(f'y_0 = {y:.4f}, z_0 = {z:.4f}')

f_y = f(y)
f_z = f(z)

k = 0
while True:
    print(f'\nk = {k}')

    if f_y <= f_z:
        print(f'т.к. f(y_{k}) = {f_y:.4f} <= f(z_{k}) = {f_z:.4f}, то:')
        ## a_k+1 = a_k
        a.append(a[k])
        print(f'a_{k+1} = {a[k+1]:.4f}')
        ## b_k+1 = z_k
        b.append(z)
        print(f'b_{k+1} = {b[k+1]:.4f}')
        ## z_k+1 = y_k
        z = y
        print(f'z_{k+1} = y_{k} = {z:.4f}')
        ## y_k+1 = a_k+1 + b_k+1 - y_k
        y = a[k+1] + b[k+1] - y
        print(f'y_{k+1} = a_{k+1} + b_{k+1} - y_{k} = {y:.4f}')

        f_z = f_y
        f_y = f(y)
    else:
        ## a_k+1 = y_k
        a.append(y)
        print(f'a_{k+1} = {a[k+1]:.4f}')
        ## b_k+1 = b_k
        b.append(b[k])
        print(f'b_{k+1} = {b[k+1]:.4f}')
        ## y_k+1 = z_k
        y = z
        print(f'y_{k+1} = z_{k} = {y:.4f}')
        ## z_k+1 = a_k+1 + b_k+1 - z_k
        z = a[k+1] + b[k+1] - z
        print(f'z_{k+1} = a_{k+1} + b_{k+1} - z_{k} = {z:.4f}')

        f_y = f_z
        f_z = f(z)

    L = abs(a[k+1] - b[k+1])
    print(f'L_{k+1} = b_{k+1} - a_{k+1} = {(b[k+1] - a[k+1]):.4f}')

    if L <= l:
        print(f'L_{k+1} = {L:.4f} < l ==> процесс поиска завершён!\n')
        break
    print(f'L_{k+1} = {L:.4f} > l')
    k = k + 1

print(f'x принадлежит отрезку [{a[k+1]:.4f}; {b[k+1]:.4f}]')
print(f'приближённое решение: x* ~= {(a[k+1] + b[k+1])/2 :.4f} +- {(b[k+1] - a[k+1])/2:.4f}\n')