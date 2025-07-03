import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

# Variável global para controle de execução
simulacao_ativa = False

def f(t, T, UA, rhoq, cpq, vq, rhof, cpf, vf, L):
    n = len(T) // 2
    Tq = T[:n]
    Tf = T[n:]

    dx = L / n

    # Inicialização das derivadas
    dTqdt = np.zeros_like(Tq)
    dTfdt = np.zeros_like(Tf)

    # Troca de calor entre as correntes
    for i in range(n):
        dTqdt[i] -= (UA / (rhoq * cpq * dx)) * (Tq[i] - Tf[i])
        dTfdt[i] += (UA / (rhof * cpf * dx)) * (Tq[i] - Tf[i])

    # Propagação espacial com diferenças finitas
    for i in range(1, n):
        dTqdt[i] += vq * (Tq[i - 1] - Tq[i]) / dx
        dTfdt[i] += vf * (Tf[i - 1] - Tf[i]) / dx

    # Condições de contorno
    dTqdt[0] = 0  # Entrada quente mantém a temperatura inicial
    dTfdt[0] = 0  # Entrada fria mantém a temperatura inicial

    return np.concatenate([dTqdt, dTfdt])

def rodar_simulacao():
    global sol, UA, rhoq, cpq, vq, rhof, cpf, vf, L, n, y0q, y0f, simulacao_ativa
    try:
        # Obter os valores dos campos de entrada
        UA = float(entry_UA.get())
        rhoq = float(entry_rhoq.get())
        cpq = float(entry_cpq.get())
        vq = float(entry_vq.get())
        rhof = float(entry_rhof.get())
        cpf = float(entry_cpf.get())
        vf = float(entry_vf.get())
        L = float(entry_L.get())
        y0q = float(entry_y0q.get())
        y0f = float(entry_y0f.get())
        t_final = float(entry_t_final.get())
        n = int(entry_n.get())

        # Condições iniciais e discretização espacial
        Tq0 = np.full(n, y0q)
        Tf0 = np.full(n, y0f)
        T0 = np.concatenate([Tq0, Tf0])
        t_span = (0, t_final)
        t_eval = np.linspace(0, t_final, 200)

        # Resolver as equações diferenciais
        sol = solve_ivp(
            f, t_span, T0, t_eval=t_eval, method="RK45",
            args=(UA, rhoq, cpq, vq, rhof, cpf, vf, L)
        )

        # Ativar simulação
        simulacao_ativa = True

        def update(frame):
            if not simulacao_ativa:
                ani.event_source.stop()
                return

            ax.clear()
            ax.plot(np.linspace(0, L, n), sol.y[:n, frame], label="Tq (Quente)", color='red')
            ax.plot(np.linspace(0, L, n), sol.y[n:, frame], label="Tf (Frio)", color='blue')
            ax.set_title(f"Tempo: {sol.t[frame]:.2f} s")
            ax.set_xlabel("Comprimento do Trocador (m)")
            ax.set_ylabel("Temperatura (°C)")
            ax.legend()
            ax.grid(True)
            ax.set_ylim(min(y0f, y0q) - 5, max(y0f, y0q) + 5)

        ani = FuncAnimation(fig, update, frames=len(sol.t), interval=100, repeat=False)
        canvas.draw()

    except ValueError as e:
        messagebox.showerror("Erro", f"Por favor, insira valores válidos.\n{e}")

def parar_simulacao():
    global simulacao_ativa
    simulacao_ativa = False

def mostrar_resultado_final():
    try:
        if not simulacao_ativa:
            ax.clear()
            ax.plot(np.linspace(0, L, n), sol.y[:n, -1], label="Tq Final (Quente)", color='red')
            ax.plot(np.linspace(0, L, n), sol.y[n:, -1], label="Tf Final (Frio)", color='blue')
            ax.set_title(f"Resultado Final - Tempo: {sol.t[-1]:.2f} s")
            ax.set_xlabel("Comprimento do Trocador (m)")
            ax.set_ylabel("Temperatura (°C)")
            ax.legend()
            ax.grid(True)
            ax.set_ylim(min(y0f, y0q) - 5, max(y0f, y0q) + 5)
            canvas.draw()
        else:
            messagebox.showinfo("Aviso", "Pare a simulação antes de exibir o resultado final.")
    except NameError:
        messagebox.showerror("Erro", "Por favor, rode a simulação antes de visualizar o resultado final.")

# Interface gráfica
root = tk.Tk()
root.title("Simulação Transiente de Trocador de Calor")
root.geometry("1200x800")

frame_params = ttk.Frame(root, padding=10)
frame_params.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

# Criar campos de entrada
entries = {
    "UA (W/K)": ("10000", 0),
    "Densidade Quente (rhoq, kg/m³)": ("1000", 1),
    "Calor Específico Quente (cpq, J/kg·K)": ("4100", 2),
    "Velocidade Quente (vq, m/s)": ("0.02", 3),
    "Densidade Fria (rhof, kg/m³)": ("1000", 4),
    "Calor Específico Frio (cpf, J/kg·K)": ("4100", 5),
    "Velocidade Fria (vf, m/s)": ("0.032", 6),
    "Comprimento do Trocador (L, m)": ("20", 7),
    "Temperatura Inicial Quente (y0q, °C)": ("80", 8),
    "Temperatura Inicial Fria (y0f, °C)": ("25", 9),
    "Tempo Final (t_final, s)": ("50", 10),
    "Número de Elementos Discretos (n)": ("50", 11)
}

entries_widgets = {}

for label, (default, row) in entries.items():
    ttk.Label(frame_params, text=label).grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    entry = ttk.Entry(frame_params)
    entry.insert(0, default)
    entry.grid(row=row, column=1, padx=5, pady=5)
    entries_widgets[label] = entry

entry_UA = entries_widgets["UA (W/K)"]
entry_rhoq = entries_widgets["Densidade Quente (rhoq, kg/m³)"]
entry_cpq = entries_widgets["Calor Específico Quente (cpq, J/kg·K)"]
entry_vq = entries_widgets["Velocidade Quente (vq, m/s)"]
entry_rhof = entries_widgets["Densidade Fria (rhof, kg/m³)"]
entry_cpf = entries_widgets["Calor Específico Frio (cpf, J/kg·K)"]
entry_vf = entries_widgets["Velocidade Fria (vf, m/s)"]
entry_L = entries_widgets["Comprimento do Trocador (L, m)"]
entry_y0q = entries_widgets["Temperatura Inicial Quente (y0q, °C)"]
entry_y0f = entries_widgets["Temperatura Inicial Fria (y0f, °C)"]
entry_t_final = entries_widgets["Tempo Final (t_final, s)"]
entry_n = entries_widgets["Número de Elementos Discretos (n)"]

# Botões
button_run = ttk.Button(frame_params, text="Rodar Simulação", command=rodar_simulacao)
button_run.grid(row=12, column=0, columnspan=2, pady=10)

button_stop = ttk.Button(frame_params, text="Parar Simulação", command=parar_simulacao)
button_stop.grid(row=13, column=0, columnspan=2, pady=10)

button_final = ttk.Button(frame_params, text="Mostrar Resultado Final", command=mostrar_resultado_final)
button_final.grid(row=14, column=0, columnspan=2, pady=10)

frame_graph = ttk.Frame(root, padding=10)
frame_graph.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

fig, ax = plt.subplots(figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=frame_graph)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

root.mainloop()
