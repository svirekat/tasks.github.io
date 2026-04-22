import math

epsilon = 0.05
epsilon1 = 0.1
epsilon2 = 0.1
M = 100
x0 = [1, 1]
Raphson = True

def f(x1, x2):
    return x1*x1 + 5*x2*x2 + x1*x2 + x1

def gradient_f(x1, x2, h=1e-6):
    df_dx1 = (f(x1 + h, x2) - f(x1 - h, x2)) / (2 * h)
    df_dx2 = (f(x1, x2 + h) - f(x1, x2 - h)) / (2 * h)
    return [df_dx1, df_dx2]

def norm(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1])

def hessian(f, x, y, h=1e-5):
    d2f_dx2 = (f(x + h, y) - 2*f(x, y) + f(x - h, y)) / (h**2)
    d2f_dy2 = (f(x, y + h) - 2*f(x, y) + f(x, y - h)) / (h**2)
    d2f_dxdy = (f(x + h, y + h) - f(x + h, y - h) - f(x - h, y + h) + f(x - h, y - h)) / (4 * h**2)
    return [[d2f_dx2, d2f_dxdy], [d2f_dxdy, d2f_dy2]]

def positive(M):
    a, b = M[0][0], M[0][1]
    c, d = M[1][0], M[1][1]
    return a > 0 and (a * d - b * c) > 0

def invert_hessian(H):
    a, b = H[0][0], H[0][1]
    c, d = H[1][0], H[1][1]
    det = a*d - b*c
    if abs(det) < 1e-12:
        raise ValueError("Матрица Гессе вырождена")
    return [[d/det, -b/det], [-c/det, a/det]]

def product(M, v):   ## матрица * вектор
    return [M[0][0]*v[0] + M[0][1]*v[1], M[1][0]*v[0] + M[1][1]*v[1]]

def num_product(M, c):   ## число * матрица
    cM = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            cM[i][j] = c * M[i][j]
    return cM

def minus(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1]]

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

def find_t(x, grad):
    alpha = (3 - 5**0.5) / 2
    def phi(t):
        x1 = x[0] + t * grad[0]
        x2 = x[1] + t * grad[1]
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


def NewtonMethod(x_start, Raphson):
    k = 0
    x = x_start[:]
    flag = False
    while True:
        print(f'\nk = {k}')
        gr = gradient_f(x[0], x[1])
        norm_gr = norm(gr)
        print(f'норма градиента: {norm_gr:.4f}')

        if norm_gr <= epsilon1:
            print("Остановка: норма градиента мала")
            return x
        if k >= M:
            print("Остановка: превышено макс. число итераций")
            return x
        
        f_cur = f(x[0], x[1])

        H = hessian(f, x[0], x[1])
        H_inv = invert_hessian(H)

        if positive(H_inv):
            d = product(num_product(H_inv, -1), gr)
        else:
            d = [-gr[0], -gr[1]]

        if (Raphson == True):       ## метод Ньютона-Рафсона
            t = find_t(x, d)
            x_new = [x[0] + t*d[0], x[1] + t*d[1]]
            f_new = f(x_new[0], x_new[1])
        
        else:           ## метод Ньютона
            if positive(H_inv):
                t = 1
                x_new = [x[0] + t*d[0], x[1] + t*d[1]]
                f_new = f(x_new[0], x_new[1])
            else:
                t = 0.5
                x_new = [x[0] + t*d[0], x[1] + t*d[1]]
                f_new = f(x_new[0], x_new[1])
                while f_new >= f_cur:
                    t *= 0.5
                    x_new = [x[0] + t*d[0], x[1] + t*d[1]]
                    f_new = f(x_new[0], x_new[1])

        print(f'x_{k} = {x[0]:.4f}, {x[1]:.4f}')
        print(f'x_{k+1} = {x_new[0]:.4f},{x_new[1]:.4f}')
        print(f'f(x_{k}) = {f_cur:.4f}')
        print(f'f(x_{k+1}) = {f_new:.4f}')

        delta_x = norm(minus(x_new, x))
        delta_f = abs(f_new - f_cur)
        print(f'малое изменение аргумента: {delta_x:.4f}')
        print(f'малое изменение функции: {delta_f:.4f}')

        if (delta_x < epsilon2) and (delta_f < epsilon2):
            if flag:
                print("Остановка: условия окончания выполнены 2 раза подряд")
                return x_new
            else:
                flag = True
        else:
            flag = False
        x = x_new
        k += 1
if Raphson:
    print(f'\nпоиск минимума методом Ньютона-Рафсона')
else:
    print(f'\nпоиск минимума методом Ньютона')
ans = NewtonMethod(x0, Raphson)
print('\nминимум функции f = x1^2 + 5x2^2 + x1x2 + x1:')
print(f'x1={ans[0]:.4f}, x2={ans[1]:.4f}')
print(f'значение функции: {f(ans[0], ans[1]):.4f}')
