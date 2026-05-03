import math

epsilon1 = 0.01  # точность для градиента
epsilon2 = 0.01  # точность для функции
M = 100
x0 = [1, 1]
mu0 = 20

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

def invert_hessian(H):
    a, b = H[0][0], H[0][1]
    c, d = H[1][0], H[1][1]
    det = a*d - b*c
    if abs(det) < 1e-12:
        raise ValueError("Матрица Гессе вырождена")
    return [[d/det, -b/det], [-c/det, a/det]]

def product(M, v):   ## матрица * вектор
    return [M[0][0]*v[0] + M[0][1]*v[1], M[1][0]*v[0] + M[1][1]*v[1]]

def num_product(v, c):   ## число * вектор
    return [v[0]*c, v[1]*c]

def minus(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1]]

def plus_mu(M, mu):
    P = [row[:] for row in M]
    P[0][0] += mu
    P[1][1] += mu
    return P

def markvardt(x_start):
    k = 0
    mu = mu0
    x = x_start[:]

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
        H_plus_mu = plus_mu(H, mu)
        H_plus_mu_inv = invert_hessian(H_plus_mu)
        d = product(H_plus_mu_inv, gr)

        x_new = minus(x, d)
        f_new = f(x_new[0], x_new[1])

        delta_x = norm(minus(x_new, x))
        delta_f = abs(f_new - f_cur)
        print(f'малое изменение аргумента: {delta_x:.4f}')
        print(f'малое изменение функции: {delta_f:.4f}')

        if f_new < f_cur:
            k += 1
            x = x_new
            mu = mu * 0.5
            if delta_x < epsilon2 and delta_f < epsilon2:
                print("Остановка: малые изменения x и f")
                return x
        else:
            mu = mu * 2

ans = markvardt(x0)
print(f'x1={ans[0]:.4f}, x2={ans[1]:.4f}')
print(f'значение функции: {f(ans[0], ans[1]):.4f}')     
