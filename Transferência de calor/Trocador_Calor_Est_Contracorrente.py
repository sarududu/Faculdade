# -*- coding: utf-8 -*-
"""
Simulação de Trocador de Calor com Otimização (Gráfico da Direita para a Esquerda)
"""

import matplotlib.pyplot as plt
from scipy.integrate import odeint
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

# Modelo Estacionário Concorrente
def f(T, x, UA, rhoq, cpq, vq, rhof, cpf, vf):
    Tq, Tf = T
    dTqdx = (UA / (rhoq * cpq * vq)) * (Tq - Tf)
    dTfdx = (UA / (rhof * cpf * vf)) * (Tq - Tf)
    return [dTqdx, dTfdx]

# Método de busca para otimização de y0qf
def optimize_y0qf(y0f, x, Tq_target, UA, rhoq, cpq, vq, rhof, cpf, vf, tolerance=1e-2):
    y0q_low, y0q_high = 20.0, 60.0  # Faixa inicial de busca
    while y0q_high - y0q_low > tolerance:
        y0q_mid = (y0q_low + y0q_high) / 2.0
        sol = odeint(f, [y0q_mid, y0f], x, args=(UA, rhoq, cpq, vq, rhof, cpf, vf))
        Tqf = sol[-1, 0]  # Temperatura final do fluido quente
        if Tqf < Tq_target:
            y0q_low = y0q_mid
        else:
            y0q_high = y0q_mid
    return (y0q_low + y0q_high) / 2.0

def calcular_UA(h_int, A_int, ln, k, h_ext, A_ext, L):
    return 1 / (
        (1 / (h_int * A_int)) +
        (ln / (2 * math.pi * k * L)) +
        (1 / (h_ext * A_ext))
    )

# Parâmetros fixos
h_int = 400
A_int = 0.5
ln = 50
k = 70
h_ext = 160
A_ext = 0.30
L = 10  # Exemplo padrão para comprimento

UA = calcular_UA(h_int, A_int, ln, k, h_ext, A_ext, L)

# Função para rodar a simulação e atualizar o gráfico
def rodar_simulacao():
    try:
        # Recuperar parâmetros
        rhoq = float(entry_rhoq.get())
        cpq = float(entry_cpq.get())
        vq = float(entry_vq.get())
        rhof = float(entry_rhof.get())
        cpf = float(entry_cpf.get())
        vf = float(entry_vf.get())
        L = float(entry_L.get())
        y0f = float(entry_y0f.get())
        Tq_target = float(entry_Tq_target.get())

        # Discretização
        x = np.linspace(0.0, L, 100)

        # Encontrar o valor ótimo de y0qf
        y0qf = optimize_y0qf(y0f, x, Tq_target, UA, rhoq, cpq, vq, rhof, cpf, vf)

        # Resolver o sistema de EDOs com o valor ótimo de y0qf
        sol = odeint(f, [y0qf, y0f], x, args=(UA, rhoq, cpq, vq, rhof, cpf, vf))

        # Extrair resultados
        Tq = sol[:, 0]
        Tf = sol[:, 1]
        print(UA)
        # Atualizar o gráfico
        ax.clear()
        ax.plot(x, Tq, 'r-', label='Fluido quente (Tq)')
        ax.plot(x, Tf, 'b-', label='Fluido frio (Tf)')
        ax.set_xlabel('Comprimento do trocador de calor (m)')
        ax.set_ylabel('Temperatura (°C)')
        ax.set_title(f'Distribuição de Temperatura (y0qf = {y0qf:.2f})')
        ax.legend()
        ax.grid(True)

        # Inverter o eixo x
        ax.invert_xaxis()

        canvas.draw()
    except ValueError:
        messagebox.showerror("Erro", "Verifique os valores de entrada!")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Simulação de Trocador de Calor com Otimização")
root.geometry("1000x700")
style = ttk.Style()
style.theme_use("clam")

# Ajustes de tema
style.configure("TLabel", font=("Arial", 14), padding=8)
style.configure("TEntry", font=("Arial", 14), padding=8)
style.configure("TButton", font=("Arial", 14), padding=8)

# Frame para os parâmetros
frame_params = ttk.Frame(root, padding=10)
frame_params.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

# Adicionar título ao lado dos parâmetros
ttk.Label(frame_params, text="Parâmetros de Simulação", font=("Arial", 16, "bold")).grid(
    row=0, column=0, columnspan=2, pady=(0, 10)
)

# Parâmetros de entrada
fields = [
    ("Densidade Quente (rhoq, kg/m³):", "1000"),
    ("Calor Específico Quente (cpq, J/kg·K):", "4100"),
    ("Velocidade Quente (vq, m/s):", "0.02"),
    ("Densidade Fria (rhof, kg/m³):", "1000"),
    ("Calor Específico Frio (cpf, J/kg·K):", "4100"),
    ("Velocidade Fria (vf, m/s):", "0.032"),
    ("Comprimento do Trocador (L, m):", "10"),
    ("Temperatura Esperada(°C):", "80"),
    ("Temperatura Inicial Fria (y0f, °C):", "25"),
]

entries = []
for i, (label_text, default) in enumerate(fields):
    ttk.Label(frame_params, text=label_text).grid(row=i + 1, column=0, sticky=tk.W, padx=5, pady=5)
    entry = ttk.Entry(frame_params)
    entry.insert(0, default)
    entry.grid(row=i + 1, column=1, padx=5, pady=5)
    entries.append(entry)

# Mapear entradas
(
    entry_rhoq,
    entry_cpq,
    entry_vq,
    entry_rhof,
    entry_cpf,
    entry_vf,
    entry_L,
    entry_Tq_target,
    entry_y0f,
) = entries

# Botão para rodar a simulação
button_run = ttk.Button(frame_params, text="Rodar Simulação", command=rodar_simulacao)
button_run.grid(row=len(fields) + 1, column=0, columnspan=2, pady=20)

# Frame para o gráfico
frame_graph = ttk.Frame(root, padding=10)
frame_graph.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Configuração do gráfico
fig, ax = plt.subplots(figsize=(8, 5))
canvas = FigureCanvasTkAgg(fig, master=frame_graph)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

# Adicionar barra de título acima do gráfico
ttk.Label(frame_graph, text="Resultado da Simulação", font=("Arial", 14, "bold")).pack(
    side=tk.TOP, pady=10
)

# Inicializar interface
root.mainloop()
