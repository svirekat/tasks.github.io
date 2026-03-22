def f(x):
    return x*x - 4*x + 6

# функция вычисления N-ого числа фибоначчи и двух предыдущих
def fibonacci(N):
    if N == 1:
        return 1
    elif N == 2:
        return 1
    else:
        f1, f2 = 1, 1
        for i in range(3, N+1):
            f1, f2 = f2, f1 + f2
        return f2

# функция вычисления N
def calculateN(m):
    N = 1
    while fibonacci(N) < m:
        N += 1
    return N

epsilon = 0.5
l = 2 * epsilon
delta = 0.2

a = [0]
b = [10]
L0 = b[0] - a[0]

d = L0 / l
N = calculateN(d)

print("\n\nпоиск минимума функции методом Фибоначчи\n")
print(f'количество вычислений: N = {N}')

F_N_minus2 = fibonacci(N-2)
F_N_minus1 = fibonacci(N-1)
F_N = fibonacci(N)

y = a[0] + (F_N_minus2 / F_N) * (b[0] - a[0])
z = a[0] + b[0] - y
print(f'y_0 = {y:.4f}, z_0 = {z:.4f}')

k = 0
while(True):
    f_y, f_z = f(y), f(z)
    print(f"\nСравнение f(y_{k}) и f(z_{k}):")
    if f_y <= f_z:
        ## a_k+1 = a_k
        a.append(a[k])
        ## b_k+1 = z_k
        b.append(z)
        print(f'f(y_{k}) = {f_y:.4f} < f(z_{k}) = {f_z:.4f}   ->\n-> a_{k+1} = a_{k} = {a[k]:.4f}, b_{k + 1} = z_{k} = {z:.4f}')
        ## z_k+1 = y_k
        z = y
        print(f'z_{k+1} = y_{k} = {z:.4f}')
        ## y_k+1 = a_k+1 + b_k+1 - z_k+1
        y = a[k+1] + (fibonacci(N-k-3)/fibonacci(N-k-1)) * (b[k+1] - a[k+1])
        print(f'y_{k+1} = a_{k+1} + b_{k+1} - z_{k+1} = {a[k+1]:.4f} + {b[k+1]:.4f} - {z:.4f} = {y:.4f}')
    else:
        ## a_k+1 = y_k
        a.append(y)
        ## b_k+1 = b_k
        b.append(b[k])
        print(f'f(y_{k}) = {f_y:.4f} > f(z_{k}) = {f_z:.4f}   ->\n->  a[{k + 1}] = y_{k} = {z:.4f}, b_{k+1} = b_{k} = {b[k]:.4f}')
        ## y_k+1 = z_k
        y = z
        print(f'y_{k+1} = z_{k} = {y:.4f}')
        ## z_k+1 = b_k+1 - a_k+1 - y_k+1
        z = a[k+1] + (fibonacci(N-k-2)/fibonacci(N-k-1)) * (b[k+1] - a[k+1])
        print(f'z_{k+1} = a_{k+1} + b_{k+1} - y_{k+1} = {b[k + 1]:.4f} - {a[k + 1]:.4f} - {y:.4f} = {y:.4f}')
    
    if k == N - 3:
        print(f'\nk = N-3 = {k}')
        y = (a[N-2] + b[N-2]) / 2
        print(f'y_{N-1} = {y:.4f}')
        z = y + delta
        print(f'z_{N-1} = {z:.4f}')
        f_y_Nminus1 = f(y)
        f_z_Nminus1 = f(z)
        print(f'f(y_{N-1}) = {f_y_Nminus1:.4f}, f(z_{N-1}) = {f_z_Nminus1:.4f})')
        if (f_y_Nminus1 <= f_z_Nminus1):
            ## a_N-1 = a_N-2
            a.append(a[N-2])
            ## b_N-1 = z_N-1
            b.append(z)
            print(f'\na_{N-1} = {a[N-2]:.4f}, b_{N-1} = z_{N-1} = {z:.4f}')
        else:
            ## a_N-1 = y_N-1
            a.append(y)
            ## b_N-1 = b_N-2
            b.append(b[N-2])
            print(f'\na_N-1 = y_N-1 = {y:.4f}')
        break
    else:
        k = k + 1
print(f'\nпроцесс поиска завершён!\n')
print(f'x принадлежит отрезку [{a[N-1]:.4f}; {b[N-1]:.4f}]')
print(f'приближённое решение: x* ~= {(a[N-1] + b[N-1])/2 :.4f} +- {(b[N-1] - a[N-1])/2:.4f}\n')
        
