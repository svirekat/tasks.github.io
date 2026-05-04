import math

epsilon1 = 1e-3
epsilon = 1e-3
x0 = [1, 1]
M = 50

def f(x1, x2):
    return x1*x1 + 5*x2*x2 + x1*x2 + x1

def gradient_f(x1, x2, h=1e-6):
    df_dx1 = (f(x1 + h, x2) - f(x1 - h, x2)) / (2 * h)
    df_dx2 = (f(x1, x2 + h) - f(x1, x2 - h)) / (2 * h)
    return [df_dx1, df_dx2]

def norm(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1])

def plus(v1, v2):
    return [v1[0] + v2[0], v1[1] + v2[1]]

def minus(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1]]

def num_prod(v, c):   ## число * вектор
    return [v[0]*c, v[1]*c]

def swann(f):
    x0 = 0
    h = 0.01
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

def find_t(x, d):
    alpha = (3 - 5**0.5) / 2
    def phi(t):
        x1 = x[0] + t * d[0]
        x2 = x[1] + t * d[1]
        return f(x1, x2)
    interval = swann(phi)
    a, b = interval[0], interval[1]
    y = a + alpha*(b-a)
    z = a + b - y
    phi_y = phi(y)
    phi_z = phi(z)
    l = 2 * epsilon1
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

def powell(x_start):
    d0 = [0.0, 1.0]
    d1 = [1.0, 0.0]
    d2 = [0.0, 1.0]
    directions = [d0, d1, d2]

    x_prev = x_start[:]
    y0 = x_start[:]
    k = 0

    while k < M:
        y = y0[:]
        y_points = [y[:]] 

        print(f'\nk = {k}')
        print(f'x = [{x_prev[0]:.4f}, {x_prev[1]:.4f}]')

        print(f'y0 = [{y[0]:.4f}, {y[1]:.4f}]')
        # Спуск по d0 и d1
        for i in range(2):
            d = directions[i]
            t = find_t(y, d)
            y = plus(y, num_prod(d, t))
            y_points.append(y[:])  
            print(f'спуск по d{i}: t = {t:.4f}, y{i+1} = [{y[0]:.4f}, {y[1]:.4f}]')

        if math.dist(y_points[0], y_points[2]) < epsilon:
            print("Остановка: расстояние между y0 и y2 мало")
            return y_points[2]

        # Спуск по d2
        d2 = directions[2]
        t = find_t(y, d2)
        y = plus(y, num_prod(d2, t))
        y_points.append(y[:])
        print(f'спуск по d2: t = {t:.4f}, y3 = [{y[0]:.4f}, {y[1]:.4f}]')

        if math.dist(y_points[1], y_points[3]) < epsilon:
            print("Остановка: расстояние между y1 и y3 мало")
            return y_points[3]

        x_new = y_points[3] 
        print(f'x_new = [{x_new[0]:.4f}, {x_new[1]:.4f}]')

        if math.dist(x_prev, x_new) < epsilon:
            print("Остановка: расстояние между x_prev и x_new мало")
            return x_new

        # Построение нового направления: d_new = y^3 - y^1
        d_new = minus(y_points[3], y_points[1])
        new_directions = [directions[1][:], directions[2][:], d_new[:]]
        print("Новые направления:")
        print(f"d0 = [{new_directions[0][0]:.4f}, {new_directions[0][1]:.4f}]")
        print(f"d1 = [{new_directions[1][0]:.4f}, {new_directions[1][1]:.4f}]")
        print(f"d2 = [{new_directions[2][0]:.4f}, {new_directions[2][1]:.4f}]")

        # Проверка лнз d1' и d2'
        det = new_directions[1][0] * new_directions[2][1] - new_directions[1][1] * new_directions[2][0]
        if abs(det) > 1e-12:
            directions = new_directions

        x_prev = x_new
        y0 = x_new
        k += 1

    return x_prev

print(f'\nпоиск минимума методом Пауэлла')
ans = powell(x0)
print('\nминимум функции f = x1^2 + 5x2^2 + x1x2 + x1:')
print(f'x1={ans[0]:.4f}, x2={ans[1]:.4f}')
print(f'значение функции: {f(ans[0], ans[1]):.4f}')
