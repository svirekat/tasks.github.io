import math

epsilon = 0.5
epsilon1 = 0.1
epsilon2 = 0.1
M = 100
x0 = [1, 1]

def f(x1, x2):
    return x1*x1 + 5*x2*x2 + x1*x2 + x1

def gradient_f(x1, x2):
    return [2*x1 + x2 + 1, 10*x2 + x1]

def norm(v):
    x1, x2 = v[0], v[1]
    return math.sqrt(x1*x1 + x2*x2)

def minus(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1]]

def phi(x, t):
    grad = gradient_f(x)
    return f(x + t*(-grad))

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
        x1 = x[0] - t * grad[0]
        x2 = x[1] - t * grad[1]
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

def steepest_descent(x_start):
    k = 0
    x = x_start[:]
    flag = False
    while True:
        print(f'\nk = {k}')
        gr = gradient_f(x[0], x[1])
        norm_gr = norm(gr)
        print(f'норма градиента: {norm_gr:.4f}')

        if norm_gr < epsilon1:
            print("Остановка: норма градиента мала")
            return x
        if k >= M:
            print("Остановка: превышено число итераций")
            return x
        
        t = find_t(x, gr)
        print(f't = {t:.2f}')
        x_new = [x[0] - t * gr[0], x[1] - t * gr[1]]
        f_cur = f(x[0], x[1])
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

ans = steepest_descent(x0)
print('\nминимум функции f = x1^2 + 5x2^2 + x1x2 + x1:')
print(f'x1={ans[0]:.4f}, x2={ans[1]:.4f}')
print(f'значение функции: {f(ans[0], ans[1]):.4f}')

