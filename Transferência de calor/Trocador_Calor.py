import matplotlib.pyplot as plt
from scipy.integrate import odeint
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

def f_concorrente(T, x, UA, rhoq, cpq, vq, rhof, cpf, vf):
    Tq, Tf = T
    dTqdx = -(UA / (rhoq * cpq * vq)) * (Tq - Tf)
    dTfdx = (UA / (rhof * cpf * vf)) * (Tq - Tf)
    return [dTqdx, dTfdx]

def f_contracorrente(T, x, UA, rhoq, cpq, vq, rhof, cpf, vf):
    Tq, Tf = T
    dTqdx = (UA / (rhoq * cpq * vq)) * (Tq - Tf)
    dTfdx = (UA / (rhof * cpf * vf)) * (Tq - Tf)
    return [dTqdx, dTfdx]

def calcular_UA(h_int, A_int, ln, k, h_ext, A_ext, L):
    return 1 / (
        (1 / (h_int * A_int)) +
        (ln / (2 * math.pi * k * L)) +
        (1 / (h_ext * A_ext))
    )
def optimize_y0qf_contracorrente(y0f, x, Tq_target, UA, rhoq, cpq, vq, rhof, cpf, vf, tolerance=1e-2):
    y0q_low, y0q_high = 20.0, 60.0  # Faixa inicial de busca
    while y0q_high - y0q_low > tolerance:
        y0q_mid = (y0q_low + y0q_high) / 2.0
        sol = odeint(f_contracorrente, [y0q_mid, y0f], x, args=(UA, rhoq, cpq, vq, rhof, cpf, vf))
        Tqf = sol[-1, 0]  # Temperatura final do fluido quente
        if Tqf < Tq_target:
            y0q_low = y0q_mid
        else:
            y0q_high = y0q_mid
    return (y0q_low + y0q_high) / 2.0
    
        
        
def rodar_simulacao():
    try:
        h_int = float(entry_h_int.get())
        A_int = float(entry_A_int.get())
        T_média = float(entry_ln.get())
        k = float(entry_k.get())
        h_ext = float(entry_h_ext.get())
        A_ext = float(entry_A_ext.get())
        L = float(entry_L.get())
        rhoq = float(entry_rhoq.get())
        cpq = float(entry_cpq.get())
        vq = float(entry_vq.get())
        rhof = float(entry_rhof.get())
        cpf = float(entry_cpf.get())
        vf = float(entry_vf.get())
        L = float(entry_L.get())
        y0q = float(entry_y0q.get())
        y0f = float(entry_y0f.get())
        Tq_target = y0q
        
        UA = calcular_UA(h_int, A_int, T_média, k, h_ext, A_ext, L)
        
        y0 = [y0q, y0f]
        x = np.linspace(0.0, L, 100)
        y0qf = optimize_y0qf_contracorrente(y0f, x, Tq_target, UA, rhoq, cpq, vq, rhof, cpf, vf)
        if modo_simulacao.get() == "Concorrente":
            sol = odeint(f_concorrente, y0, x, args=(UA, rhoq, cpq, vq, rhof, cpf, vf))
        else:
            sol = odeint(f_contracorrente, [y0qf, y0f], x, args=(UA, rhoq, cpq, vq, rhof, cpf, vf))
        
        Tq, Tf = sol[:, 0], sol[:, 1]
        
        ax.clear()
        ax.plot(x, Tq, label="Temperatura Quente (Tq)", color="red")
        ax.plot(x, Tf, label="Temperatura Fria (Tf)", color="blue")
        ax.text(0.85, 0.8, f'UA = {UA:.2f}', transform=ax.transAxes, fontsize=12, color='green')
        ax.set_title(f"Simulação de Trocador de Calor - {modo_simulacao.get()}")
        ax.set_xlabel("Comprimento do Trocador (m)")
        ax.set_ylabel("Temperatura (°C)")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
        
        if modo_simulacao.get() == "Contracorrente":
            ax.invert_xaxis()
            ax.set_title(f'Distribuição de Temperatura (y0qf = {y0qf:.2f})')
        
        canvas.draw()
    except ValueError:
        messagebox.showerror("Erro", "Verifique os valores de entrada!")

root = tk.Tk()
root.title("Simulação de Trocador de Calor")
root.geometry("1920x1080")
modo_simulacao = tk.StringVar(value="Concorrente")

frame_params = ttk.Frame(root, padding=10)
frame_params.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

fields = [
    ("h_int (W/m²·K):", "150"),
    ("A_int (m²):", "0.5"),
    ("T_média (°C):", "50"),
    ("k (W/m·K):", "70"),
    ("h_ext (W/m²·K):", "160"),
    ("A_ext (m²):", "0.30"),
    ("Comprimento do Trocador (L, m):", "20"),
    ("Densidade Quente (rhoq, kg/m³):", "1000"),
    ("Calor Específico Quente (cpq, J/kg·K):", "4100"),
    ("Velocidade Quente (vq, m/s):", "0.02"),
    ("Densidade Fria (rhof, kg/m³):", "1000"),
    ("Calor Específico Frio (cpf, J/kg·K):", "4100"),
    ("Velocidade Fria (vf, m/s):", "0.032"),
    ("Temperatura Inicial Quente (y0q, °C):", "80"),
    ("Temperatura Inicial Fria (y0f, °C):", "25"),
]
entries = []
for i, (label_text, default) in enumerate(fields):
    ttk.Label(frame_params, text=label_text).grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
    entry = ttk.Entry(frame_params)
    entry.insert(0, default)
    entry.grid(row=i, column=1, padx=5, pady=5)
    entries.append(entry)

(entry_h_int, entry_A_int, entry_ln, entry_k, entry_h_ext, entry_A_ext, entry_L,
 entry_rhoq, entry_cpq, entry_vq, entry_rhof, entry_cpf, entry_vf, entry_y0q, entry_y0f) = entries


modo_frame = ttk.LabelFrame(frame_params, text="Modo de Simulação")
modo_frame.grid(row=len(fields), column=0, columnspan=2, pady=10, padx=5, sticky=tk.W)

rb1 = ttk.Radiobutton(modo_frame, text="Concorrente", variable=modo_simulacao, value="Concorrente")
rb2 = ttk.Radiobutton(modo_frame, text="Contracorrente", variable=modo_simulacao, value="Contracorrente")
rb1.pack(side=tk.LEFT, padx=5)
rb2.pack(side=tk.LEFT, padx=5)

button_run = ttk.Button(frame_params, text="Rodar Simulação", command=rodar_simulacao)
button_run.grid(row=len(fields) + 1, column=0, columnspan=2, pady=20)

frame_graph = ttk.Frame(root, padding=10)
frame_graph.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

fig, ax = plt.subplots(figsize=(8, 5))
canvas = FigureCanvasTkAgg(fig, master=frame_graph)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

ttk.Label(frame_graph, text="Resultado da Simulação", font=("Arial", 14, "bold")).pack(side=tk.TOP, pady=10)

root.mainloop()
