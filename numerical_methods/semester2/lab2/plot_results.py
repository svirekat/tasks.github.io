import pandas as pd
import matplotlib.pyplot as plt


df1 = pd.read_csv('results5.csv', sep=';', decimal=',')
df2 = pd.read_csv('results6.csv', sep=';', decimal=',')

## exact_solution = "e^{-t}"
## exact_solution = "2/e^t+t-1"
exact_solution = "(1 + t) * e^{-sin(t)}"

for col in ['t', 'y_numerical', 'y_exact']:
    if df1[col].dtype == object: # если колонка прочиталась как текст
        df1[col] = df1[col].astype(str).str.replace(',', '.').astype(float)
for col in ['t', 'y_numerical', 'y_exact']:
    if df2[col].dtype == object: # если колонка прочиталась как текст
        df2[col] = df2[col].astype(str).str.replace(',', '.').astype(float)

plt.figure(figsize=(10, 6))
# точное решение
plt.plot(df1['t'], df1['y_exact'], label='Точное решение ($' + exact_solution +'$)', 
         color='blue', linewidth=2)
# численное решение
plt.plot(df1['t'], df1['y_numerical'], 'r--', label='метод Адамса', 
         alpha=0.8)

plt.title('Решение задачи Коши: Точное и Численное', fontsize=14)
plt.xlabel('t', fontsize=12)
plt.ylabel('y(t)', fontsize=12)

plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend()


plt.figure(figsize=(10, 6))
# точное решение
plt.plot(df2['t'], df2['y_exact'], label='Точное решение ($' + exact_solution +'$)', 
         color='blue', linewidth=2)

# численное решение
plt.plot(df2['t'], df2['y_numerical'], 'r--', label='метод Адамса', 
         alpha=0.8)

plt.title('Решение задачи Коши: Точное и Численное', fontsize=14)
plt.xlabel('t', fontsize=12)
plt.ylabel('y(t)', fontsize=12)

plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend()


# Отдельное окно для ошибки
plt.figure(figsize=(10, 4))
plt.plot(df1['t'], df1['abs_error'], label = "h = 0.1")
plt.plot(df2['t'], df2['abs_error'], label = "h = 0.05")
plt.title('График абсолютной ошибки')
plt.yscale('log') # Логарифмическая шкала для наглядности

plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend()

plt.show()
