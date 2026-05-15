import math

epsilon = 1e-6      # точность остановки по P(x*)
epsilon1 = 0.05     # точность градиента для DFP
epsilon2 = 0.01     # точность изменения аргумента/функции для DFP
M = 100             # макс. число итераций для DFP
x0 = [1.0, 1.0]     # начальная точка

def f(x1, x2):
    return x1*x1 + 5*x2*x2 + x1*x2 + x1

def eq1(x1, x2):
    return 2*x1 + 3*x2 - 1

equality_constraints = [eq1]


# модифицированная функция Лагранжа
def L(x1, x2, lam, r):
    res = f(x1, x2)
    # равенство: λ·g + (r/2)·g²
    for j, g in enumerate(equality_constraints):
        val = g(x1, x2)
        res += lam[j] * val + (r / 2.0) * val * val
    return res

# вспомогательная функция P(x) для проверки остановки
def P_func(x1, x2, r):
    s = 0.0
    for g in equality_constraints:
        val = g(x1, x2)
        s += (r / 2.0) * val * val
    return s

def grad_L(x1, x2, lam, r, h=1e-6):
    df_dx1 = (L(x1 + h, x2, lam, r) - L(x1 - h, x2, lam, r)) / (2 * h)
    df_dx2 = (L(x1, x2 + h, lam, r) - L(x1, x2 - h, lam, r)) / (2 * h)
    return [df_dx1, df_dx2]

def norm(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1])

def minus(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1]]

def num_product(v, c):
    return [v[0]*c, v[1]*c]

def product(M, v):
    return [M[0][0]*v[0] + M[0][1]*v[1],
            M[1][0]*v[0] + M[1][1]*v[1]]

def num_matr(M, a):
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

def swann(phi_func):
    t0 = 0.0
    h = 0.1
    f0 = phi_func(t0)
    if f0 >= phi_func(t0 + h):
        delta = h
    else:
        delta = -h
    t1 = t0 + delta
    f1 = phi_func(t1)
    delta *= 2
    t2 = t1 + delta
    f2 = phi_func(t2)
    while f2 < f1:
        delta *= 2
        t0, t1 = t1, t2
        f0, f1 = f1, f2
        t2 = t1 + delta
        f2 = phi_func(t2)
    if delta > 0:
        return [t0, t2]
    else:
        return [t2, t0]

def find_t(x, d, lam, r):
    alpha = (3 - math.sqrt(5)) / 2   # 0.382
    def phi(t):
        x1 = x[0] - t * d[0]
        x2 = x[1] - t * d[1]
        return L(x1, x2, lam, r)
    interval = swann(phi)
    a, b = interval[0], interval[1]
    y = a + alpha * (b - a)
    z = a + b - y
    phi_y = phi(y)
    phi_z = phi(z)
    l = 2 * 1e-5   
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

# метод DFP для безусловной минимизации L(x)
def DFP_minimize_L(x_start, lam, r):
    k = 0
    A = [[1.0, 0.0], [0.0, 1.0]]
    x = x_start[:]
    gr = grad_L(x[0], x[1], lam, r)
    flag = False

    while True:
        norm_gr = norm(gr)
        if norm_gr <= epsilon1:
            return x
        if k >= M:
            return x

        d = product(A, gr)
        t = find_t(x, d, lam, r)
        x_new = minus(x, num_product(d, t))
        gr_new = grad_L(x_new[0], x_new[1], lam, r)

        delta_x = minus(x_new, x)
        delta_g = minus(gr_new, gr)
        delta_x_norm = norm(delta_x)
        delta_f = abs(L(x_new[0], x_new[1], lam, r) -
                     L(x[0], x[1], lam, r))

        if (delta_x_norm < epsilon2) and (delta_f < epsilon2):
            if flag:
                return x_new
            else:
                flag = True
        else:
            flag = False

        if k >= 1:
            dot_dx_dg = delta_x[0]*delta_g[0] + delta_x[1]*delta_g[1]
            if dot_dx_dg != 0:
                mn1 = 1.0 / dot_dx_dg
                term1 = [[delta_x[0]**2, delta_x[0]*delta_x[1]],
                         [delta_x[0]*delta_x[1], delta_x[1]**2]]
                term1 = num_matr(term1, mn1)

                A_dg = product(A, delta_g)
                dot_dg_Adg = delta_g[0]*A_dg[0] + delta_g[1]*A_dg[1]
                if dot_dg_Adg != 0:
                    mn2 = 1.0 / dot_dg_Adg
                    outer = [[A_dg[0]**2, A_dg[0]*A_dg[1]],
                             [A_dg[0]*A_dg[1], A_dg[1]**2]]
                    term2 = num_matr(outer, mn2)
                    A = matr_plus(A, matr_minus(term1, term2))

        x = x_new
        gr = gr_new
        k += 1

# модифицированный метод множителей Лагранжа
def modified_lagrangian(x_start, r0=1.0, C=10.0, EPS=1e-6, max_outer=50, verbose=True):

    x = x_start[:]
    r = r0
    lam = [0.0] * len(equality_constraints)   # множители для равенств
    k = 0

    while True:
        if verbose:
            print(f"\nВнешняя итерация {k+1}, r = {r:.2f}")
            print(f"lambda = {lam[0]:.6f}")

        x = DFP_minimize_L(x, lam, r)

        P_val = P_func(x[0], x[1], r)

        if verbose:
            print(f"  x = [{x[0]:.8f}, {x[1]:.6f}]")
            print(f"  P(x) = {P_val:.6f}")

        if abs(P_val) <= EPS:
            if verbose:
                print("Условие |P| <= epsilon выполнено, алгоритм завершён.")
            break

        # Для равенства: λ_new = λ + r * g(x)
        lam_new = []
        for j, g in enumerate(equality_constraints):
            lam_new.append(lam[j] + r * g(x[0], x[1]))
        
        # Увеличение штрафа
        r *= C

        lam = lam_new
        k += 1
        if k >= max_outer:
            print("Предупреждение: достигнуто максимальное число внешних итераций")
            break

    return x

if __name__ == "__main__":
    print("\nМодифицированный метод множителей Лагранжа")
    print("Целевая функция: f(x1,x2) = x1^2 + 5x2^2 + x1x2 + x1")
    print("Ограничение-равенство: 2*x1 + 3*x2 - 1 = 0\n")

    opt = modified_lagrangian(x0, r0=0.1, C=4.0, EPS=1e-6, verbose=True)

    print(f"x* = [{opt[0]:.6f}, {opt[1]:.6f}]")
    print(f"f(x*) = {f(opt[0], opt[1]):.6f}")
    print(f"Проверка ограничения: 2*x1+3*x2-1 = {2*opt[0]+3*opt[1]-1:.10f}")