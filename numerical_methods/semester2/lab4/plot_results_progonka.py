import pandas as pd
import matplotlib.pyplot as plt
import sys
import math
import numpy as np

def safe_float_convert(value):
    if isinstance(value, str):
        value = value.replace(',', '.')
    try:
        return float(value)
    except (ValueError, TypeError):
        return None
    
# точная функция для примера 1
def exact_solution1(x):
    return math.exp(x) - math.exp(-x) -2*x

# точная функция для примера 2
def exact_solution2(x):
    return -0.5*x*x + x + 1

# точная функция для примера 3
def exact_solution3(x):
    return math.sin(x) + math.cos(x) + 1

# точная функция для примера 4
def exact_solution4(x):
    return math.exp(x) + math.sin(x)*0.5


def problem_string(example_num):
    if example_num == 1:
        return "\ny'' - y = 2x\ny(0) = 0;  y'(1) = e + 1/e - 2"
    elif example_num == 2:
        return "\ny'' = -1\ny(0) = 1;  y'(1) = 0"
    elif example_num == 3:
        return "\ny'' + y = 1\ny(0) = 2;  y'(pi) = -1"
    elif example_num == 4:
        return "\ny'' - 2y' + y = cos(x)\ny(-3pi) = exp(-3pi); y'(0) = 0.5"
    return ""


def get_exact_solution(x, ex_number):
    if ex_number == 1:
        return exact_solution1(x)
    elif ex_number == 2:
        return exact_solution2(x)
    elif ex_number == 3:
        return exact_solution3(x)
    elif ex_number == 4:
        return exact_solution4(x)
    return None

def read_data(filename):
    try:
        df = pd.read_csv(filename, sep=';')
        x = df['x'].values
        y = df['y'].values
        y_exact = df['y_exact'].values
        abs_error = df['abs_error'].values
        return x, y, y_exact, abs_error
    except Exception as e:
        print(f"ошибка при загрузке {filename}: {e}")
        return None, None, None, None

def plot_results(x, y, y_exact, abs_error, example_num):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    fig.suptitle(f'решение краевой задачи {problem_string(example_num)}', fontsize=14, fontweight='bold')

    # График 1: Численное и точное решение
    ax1.plot(x, y, 'b--', linewidth=2, label='численное решение', alpha=0.8)
    ax1.plot(x, y_exact, 'r-', linewidth=2, label='точное решение', alpha=0.8)
    ax1.set_xlabel('x', fontsize=12)
    ax1.set_ylabel('y(x)', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=10)
    
    # График 2: Погрешность
    ax2.plot(x, abs_error, 'g-', linewidth=2, label='абсолютная погрешность')
    ax2.set_xlabel('x', fontsize=12)
    ax2.set_title('график абсолютной погрешности', fontsize=12)
    ax2.grid(True, alpha=0.3, which='both')
    ax2.legend(fontsize=10)
    
    # Добавляем информацию о максимальной погрешности
    max_error = np.max(abs_error)
    mean_error = np.mean(abs_error)
    textstr = f'макс. погрешность: {max_error:.2e}'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax2.text(0.05, 0.95, textstr, transform=ax2.transAxes, fontsize=10,
             verticalalignment='top', bbox=props)

    plt.tight_layout()
    plt.show(block=True) 

def main():
    if len(sys.argv) < 3:  
        sys.exit(1)

    filename = sys.argv[1]
    example_num = int(sys.argv[2])

    x, y, y_exact, abs_error = read_data(filename)
    
    if x is None or y is None or y_exact is None or abs_error is None:
        print("ошибка: не удалось загрузить данные из файла")
        sys.exit(1)

    print(f"максимальная погрешность: {np.max(abs_error):.2e}")
    
    plot_results(x, y, y_exact, abs_error, example_num)

if __name__ == "__main__":
    
    main()