import math

epsilon = 1e-3
epsilon1 = 1e-5      # точность остановки по норме градиента
epsilon2 = 1e-5     # точность по изменению аргумента и функции
M = 100              # максимальное число итераций DFP
x0 = [1.0, 1.0]      # начальная точка


def f(x1, x2):
    return x1*x1 + 5*x2*x2 + x1*x2 + x1

# ограничение-равенство
def g1_eq(x1, x2):
    return 2*x1 + 3*x2 - 1

equality_constraints = [g1_eq]

# штрафная функция
def P(x1, x2, r):
    val = g1_eq(x1, x2)          
    return r * 0.5 * val * val

def F(x1, x2, r):
    return f(x1, x2) + P(x1, x2, r)

def gradient_F(x1, x2, r, h=1e-6):
    df_dx1 = (F(x1 + h, x2, r) - F(x1 - h, x2, r)) / (2 * h)
    df_dx2 = (F(x1, x2 + h, r) - F(x1, x2 - h, r)) / (2 * h)
    return [df_dx1, df_dx2]

def norm(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1])

def minus(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1]]

def num_product(v, c):
    """число * вектор"""
    return [v[0]*c, v[1]*c]

def product(M, v):
    """матрица 2x2 * вектор 2"""
    return [M[0][0]*v[0] + M[0][1]*v[1],
            M[1][0]*v[0] + M[1][1]*v[1]]

def num_matr(M, a):
    """матрица * число"""
    return [[a*M[0][0], a*M[0][1]],
            [a*M[1][0], a*M[1][1]]]

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

# метод Свенна
def swann(phi):
    """Метод Свенна для поиска интервала, содержащего минимум phi(t)"""
    t0 = 0.0
    h = 0.1
    f0 = phi(t0)
    if f0 >= phi(t0 + h):
        delta = h
    else:
        delta = -h
    t1 = t0 + delta
    f1 = phi(t1)
    delta *= 2
    t2 = t1 + delta
    f2 = phi(t2)
    while f2 < f1:
        delta *= 2
        t0, t1 = t1, t2
        f0, f1 = f1, f2
        t2 = t1 + delta
        f2 = phi(t2)
    if delta > 0:
        return [t0, t2]
    else:
        return [t2, t0]

def find_t(x, d, r):
    alpha = (3 - math.sqrt(5)) / 2   # 0.382
    def phi(t):
        x1 = x[0] - t * d[0]
        x2 = x[1] - t * d[1]
        return F(x1, x2, r)
    interval = swann(phi)
    a, b = interval[0], interval[1]
    y = a + alpha * (b - a)
    z = a + b - y
    phi_y = phi(y)
    phi_z = phi(z)
    l = 2 * epsilon   # используем глобальный epsilon как точность поиска
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
    return (a + b) * 0.5

# метод Дэвидона-Флетчера-Пауэлла для минимизации F(x, r) 
def DFP_minimize(x_start, r):
    k = 0
    A = [[1.0, 0.0], [0.0, 1.0]]
    x = x_start[:]
    gr = gradient_F(x[0], x[1], r)
    flag = False

    while True:
        norm_gr = norm(gr)
        if norm_gr <= epsilon1:
            return x
        if k >= M:
            return x

        d = product(A, gr)          # направление спуска
        t = find_t(x, d, r)         # оптимальный шаг
        x_new = minus(x, num_product(d, t))
        gr_new = gradient_F(x_new[0], x_new[1], r)

        delta_x_vec = minus(x_new, x)
        delta_g_vec = minus(gr_new, gr)
        delta_x_norm = norm(delta_x_vec)
        delta_f = abs(F(x_new[0], x_new[1], r) - F(x[0], x[1], r))

        if (delta_x_norm < epsilon2) and (delta_f < epsilon2):
            if flag:
                return x_new
            else:
                flag = True
        else:
            flag = False

        if k >= 1:
            # Обновление матрицы A по формуле DFP
            dot_dx_dg = delta_x_vec[0]*delta_g_vec[0] + delta_x_vec[1]*delta_g_vec[1]
            if dot_dx_dg != 0:
                mn1 = 1.0 / dot_dx_dg
                term1 = [[delta_x_vec[0]**2, delta_x_vec[0]*delta_x_vec[1]],
                         [delta_x_vec[0]*delta_x_vec[1], delta_x_vec[1]**2]]
                term1 = num_matr(term1, mn1)

                A_dg = product(A, delta_g_vec)
                dot_dg_Adg = delta_g_vec[0]*A_dg[0] + delta_g_vec[1]*A_dg[1]
                if dot_dg_Adg != 0:
                    mn2 = 1.0 / dot_dg_Adg
                    outer = [[A_dg[0]**2, A_dg[0]*A_dg[1]],
                             [A_dg[0]*A_dg[1], A_dg[1]**2]]
                    term2 = num_matr(outer, mn2)
                    A = matr_plus(A, matr_minus(term1, term2))

        x = x_new
        gr = gr_new
        k += 1

def penalty_method(x_start, r0=1.0, c=10.0, EPS=1e-6, verbose=True):
    
    x = x_start[:]
    r = r0
    k = 0

    while True:
        if verbose:
            print(f"\nВнешняя итерация {k+1}, r = {r:.2f}")
        # минимизация F(x, r) методом DFP, начиная с текущего x
        x = DFP_minimize(x, r)
        # вычисляем нарушение ограничений
        violation = 0.0
        for g in equality_constraints:
            violation += abs(g(x[0], x[1]))
        
        if verbose:
            print(f"  Точка: x = [{x[0]:.6f}, {x[1]:.6f}], f(x) = {f(x[0], x[1]):.6f}")
            print(f"  Нарушение ограничений: {violation:.6f}")
        if violation < EPS:
            if verbose:
                print("Ограничения выполнены. Оптимум найден.")
            break
        r *= c
        k += 1
        if k >= 50:
            print("Предупреждение: достигнуто максимальное число внешних итераций")
            break
    return x

if __name__ == "__main__":
    print("Метод штрафных функций с внутренней оптимизацией DFP")
    print("Целевая функция: f(x1,x2) = x1^2 + 5x2^2 + x1x2 + x1")
    print("Ограничения:")
    print("  равенство:   3x1 + 2x2 = 1")
    print(f"Начальная точка: {x0}\n")

    opt = penalty_method(x0, r0=0.5, c=10.0, EPS=1e-6, verbose=True)
    print(f"x* = [{opt[0]:.6f}, {opt[1]:.6f}]")
    print(f"f(x*) = {f(opt[0], opt[1]):6f}")
    print(f"g1 = {g1_eq(opt[0], opt[1]):.6f}")