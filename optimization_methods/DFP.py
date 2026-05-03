import math

epsilon = 0.05
epsilon1 = 0.01  # точность для градиента
epsilon2 = 0.01  # точность для функции
M = 100
x0 = [1, 1]

def f(x1, x2):
    return x1*x1 + 5*x2*x2 + x1*x2 + x1

def gradient_f(x1, x2, h=1e-6):
    df_dx1 = (f(x1 + h, x2) - f(x1 - h, x2)) / (2 * h)
    df_dx2 = (f(x1, x2 + h) - f(x1, x2 - h)) / (2 * h)
    return [df_dx1, df_dx2]

def norm(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1])

def minus(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1]]

def num_matr(M, a):     ## матрица * число
    return [ [a*M[0][0], a*M[0][1]], [a*M[1][0], a*M[1][1]] ]

def product(M, v):   ## матрица * вектор
    return [M[0][0]*v[0] + M[0][1]*v[1], M[1][0]*v[0] + M[1][1]*v[1]]

def num_product(v, c):   ## число * вектор
    return [v[0]*c, v[1]*c]

def matr_plus(A, B):
    return [[A[0][0]+B[0][0], A[0][1]+B[0][1]],
            [A[1][0]+B[1][0], A[1][1]+B[1][1]]]

def matr_minus(A, B):
    return [[A[0][0]-B[0][0], A[0][1]-B[0][1]],
            [A[1][0]-B[1][0], A[1][1]-B[1][1]]]

def matr_product(A, B):
    return [[A[0][0]*B[0][0] + A[0][1]*B[1][0],
             A[0][0]*B[0][1] + A[0][1]*B[1][1]],
            [A[1][0]*B[0][0] + A[1][1]*B[1][0],
             A[1][0]*B[0][1] + A[1][1]*B[1][1]]]

def swann(f):
    x0 = 0
    h = 0.1
    f_x0 = f(x0)
    if f_x0 >= f(x0+h):
        delta = h
    else:
        delta = -h
    x1 = x0 + delta
    f_x1 = f(x1)

    delta *= 2
    x2 = x1 + delta
    f_x2 = f(x2)

    while f_x2 < f_x1:
        delta *= 2
        x0, x1 = x1, x2
        f_x0, f_x1 = f_x1, f_x2
        x2 = x1 + delta
        f_x2 = f(x2)
    if delta > 0:
        return [x0, x2]
    else:
        return [x2, x0]

def find_t(x, Agrad):
    alpha = (3 - 5**0.5) / 2
    def phi(t):
        x1 = x[0] - t * Agrad[0]
        x2 = x[1] - t * Agrad[1]
        return f(x1, x2)
    interval = swann(phi)
    a, b = interval[0], interval[1]
    y = a + alpha*(b-a)
    z = a + b - y
    phi_y = phi(y)
    phi_z = phi(z)
    l = 2 * epsilon
    while abs(b - a) > l:
        if phi_y < phi_z:
            b = z
            z = y
            phi_z = phi_y
            y = a + alpha * (b - a)
            phi_y = phi(y)
        else:
            a = y
            y = z
            phi_y = phi_z
            z = a + b - y
            phi_z = phi(z)
    t_opt = (a + b) * 0.5
    return t_opt

def DFP(x_start):
    k = 0
    A = [[1.0, 0.0], [0.0, 1.0]]
    x = x_start[:]
    gr = gradient_f(x[0], x[1])
    flag = False

    while True:
        print(f'\nk = {k}')
        norm_gr = norm(gr)
        print(f'норма градиента: {norm_gr:.4f}')

        if norm_gr <= epsilon1:
            print("Остановка: норма градиента мала")
            return x
        
        if k >= M:
            print("Остановка: превышено макс. число итераций")
            return x
        
        d = product(A, gr)
        t = find_t(x, d)
        x_new = minus(x, num_product(d, t))
        gr_new = gradient_f(x_new[0], x_new[1])

        f_new = f(x_new[0], x_new[1])
        f_cur = f(x[0], x[1])

        print(f'x_{k} = {x[0]:.4f}, {x[1]:.4f}')
        print(f'x_{k+1} = {x_new[0]:.4f},{x_new[1]:.4f}')
        print(f'f(x_{k}) = {f_cur:.4f}')
        print(f'f(x_{k+1}) = {f_new:.4f}')

        delta_x_vec = minus(x_new, x)
        delta_g_vec = minus(gr_new, gr)
        delta_x_norm = norm(delta_x_vec)
        delta_g_norm = norm(delta_g_vec)
        delta_f = abs(f_new - f_cur)

        print(f'малое изменение аргумента: {delta_x_norm:.4f}')
        print(f'малое изменение функции: {delta_f:.4f}')
        print(f'малое изменение градиента: {delta_g_norm:.4f}')

        if (delta_x_norm < epsilon2) and (delta_f < epsilon2):
            if flag:
                print("Остановка: условия окончания выполнены 2 раза подряд")
                return x_new
            else:
                flag = True
        else:
            flag = False

        if k >= 1:

            mn1 = 1 / (delta_x_vec[0]*delta_g_vec[0] + delta_x_vec[1]*delta_g_vec[1])
            term1 = [[delta_x_vec[0]**2, delta_x_vec[0]*delta_x_vec[1]],
                      [delta_x_vec[0]*delta_x_vec[1], delta_x_vec[1]**2]]
            term1 = num_matr(term1, mn1)
                
            A_delta_g = product(A, delta_g_vec)
            mn2 = 1 / (delta_g_vec[0]*A_delta_g[0] + delta_g_vec[1]*A_delta_g[1])
            outer = [[A_delta_g[0]**2, A_delta_g[0]*A_delta_g[1]],
                         [A_delta_g[0]*A_delta_g[1], A_delta_g[1]**2]]
            term2 = num_matr(outer, mn2)
                
            # A_new = A + term1 - term2
            A = matr_plus(A, matr_minus(term1, term2))
        
        x = x_new
        gr = gr_new
        k += 1

print(f'\nпоиск минимума методом Дэвидона-Флетчера-Пауэлла')
ans = DFP(x0)
print('\nминимум функции f = x1^2 + 5x2^2 + x1x2 + x1:')
print(f'x1={ans[0]:.4f}, x2={ans[1]:.4f}')
print(f'значение функции: {f(ans[0], ans[1]):.4f}')