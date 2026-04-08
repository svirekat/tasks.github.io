import sys
import pandas as pd
import plotly.graph_objects as go
import numpy as np

if len(sys.argv) < 2:
    print("Usage: python animation.py <csv_file>")
    sys.exit(1)

csv_file = sys.argv[1]
df = pd.read_csv(csv_file, delimiter=';')

x_vals = np.sort(df['x'].unique())
y_vals = np.sort(df['y'].unique())
t_vals = np.sort(df['t'].unique())

global_min = min(df['u'].min(), df['u_exact'].min())
global_max = max(df['u'].max(), df['u_exact'].max())
padding = (global_max - global_min) * 0.05  # 5% отступа сверху и снизу
z_range = [global_min - padding, global_max + padding]

def create_animation(data_column, title, filename):
    frames = []
    for t in t_vals:
        df_t = df[df['t'] == t].sort_values(['x', 'y'])
        Z = df_t[data_column].values.reshape(len(x_vals), len(y_vals))
        frames.append(go.Frame(
            data=[go.Surface(z=Z, x=x_vals, y=y_vals)],
            name=str(t)
        ))
    # Начальный кадр
    Z0 = df[df['t'] == t_vals[0]].sort_values(['x', 'y'])[data_column].values.reshape(len(x_vals), len(y_vals))
    fig = go.Figure(
        data=[go.Surface(z=Z0, x=x_vals, y=y_vals)],
        frames=frames,
        layout=go.Layout(
            title=title,
            updatemenus=[{
                'type': 'buttons',
                'buttons': [{
                    'label': 'Play',
                    'method': 'animate',
                    'args': [None, {'frame': {'duration': 200, 'redraw': True}, 'fromcurrent': True}]
                }]
            }],
            scene=dict(
                xaxis_title='x',
                yaxis_title='y',
                zaxis_title=data_column,
                zaxis=dict(range=z_range)   # <-- ФИКСИРОВАННЫЙ ДИАПАЗОН
            ),
            width=800,
            height=600
        )
    )
    fig.write_html(filename)
    print(f"график сохранен в {filename}")

create_animation('u', 'численное решение уравнения диффузии', 'numerical.html')
create_animation('u_exact', 'точное решение', 'exact.html')