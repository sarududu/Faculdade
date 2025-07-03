import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import numpy as np
from scipy.optimize import fsolve

# Modelo Estacionário Contra-Corrente
def f(T, x, UA, rhoq, cpq, vq, rhof, cpf, vf):
    Tq, Tf = T

    # Equações para contra-corrente
    dTqdx = (UA / (rhoq * cpq * vq)) * (Tf - Tq)  # Para o fluido quente
    dTfdx = -(UA / (rhof * cpf * vf)) * (Tf - Tq)  # Para o fluido frio

    return np.array([float(dTqdx), float(dTfdx)], dtype=np.float64)

# Função para calcular e plotar
def calcular():
    try:
        # Obter valores dos campos de entrada
        UA = float(entry_UA.get())
        rhoq = float(entry_rhoq.get())
        cpq = float(entry_cpq.get())
        vq = float(entry_vq.get())
        rhof = float(entry_rhof.get())
        cpf = float(entry_cpf.get())
        vf = float(entry_vf.get())
        y0f = float(entry_y0f.get())
        Tq_esp = float(entry_Tq_esp.get())

        # Configuração do intervalo de cálculo
        L = 10.0
        x = np.linspace(0.0, L, 30)

        # Método de busca para y0q
        def objective(y0q):
            try:
                sol = odeint(f, [y0q, y0f], x, args=(UA, rhoq, cpq, vq, rhof, cpf, vf))
                Tqf = sol[-1, 0]
                return Tqf - Tq_esp
            except Exception as e:
                print(f"Erro na função objetivo: {e}")  # Log do erro
                return np.inf

        y0q, = fsolve(objective, 10.0)

        # Resolver o sistema de EDOs
        sol = odeint(f, [y0q, y0f], x, args=(UA, rhoq, cpq, vq, rhof, cpf, vf))

        # Extração dos resultados
        Tq = sol[:, 0]
        Tf = sol[:, 1]

        # Limpar o gráfico anterior
        ax.clear()

        # Plotar resultados
        ax.plot(x, Tq, 'r--', label='Tq (Quente)')
        ax.plot(x, Tf, 'b--', label='Tf (Frio)')
        ax.set_xlabel('Posição (x)')
        ax.set_ylabel('Temperatura (°C)')
        ax.set_title('Perfil de Temperatura no Trocador de Calor - Contra-Corrente')
        ax.legend()
        ax.grid(True)

        # Atualizar o canvas
        canvas.draw()

    except ValueError:
        messagebox.showerror("Erro de Entrada", "Por favor, insira valores numéricos válidos.")
    except Exception as e:
        print(f"Erro inesperado: {e}")  # Log do erro sem mostrar janela

# Criar a interface gráfica
root = tk.Tk()
root.title("Simulação de Trocador de Calor - Contra-Corrente")
root.geometry("900x700")

# Estilo
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12))
style.configure("TEntry", font=("Helvetica", 12))

# Frame principal para parâmetros e gráfico
main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Frame para os parâmetros
param_frame = ttk.Frame(main_frame)
param_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# Parâmetros
params = [
    ("UA (Coeficiente Global de Transferência de Calor)", "10000"),
    ("Densidade do Quente (kg/m³)", "1000"),
    ("Capacidade Térmica do Quente (J/(kg·K))", "4100"),
    ("Velocidade do Quente (m/s)", "0.02"),
    ("Densidade do Frio (kg/m³)", "1000"),
    ("Capacidade Térmica do Frio (J/(kg·K))", "4100"),
    ("Velocidade do Frio (m/s)", "0.032"),
    ("Temperatura Inicial do Frio (°C)", "25"),
    ("Temperatura Desejada do Quente na Saída (°C)", "80"),
]

entries = []
for param, default in params:
    label = ttk.Label(param_frame, text=param)
    label.pack(anchor="w", pady=5)
    entry = ttk.Entry(param_frame)
    entry.pack(fill="x", pady=5)
    entry.insert(0, default)
    entries.append(entry)

(entry_UA, entry_rhoq, entry_cpq, entry_vq, entry_rhof, entry_cpf, entry_vf, entry_y0f, entry_Tq_esp) = entries

# Botão de calcular
calc_button = ttk.Button(param_frame, text="Calcular e Plotar", command=calcular)
calc_button.pack(pady=20)

# Frame para o gráfico
graph_frame = ttk.Frame(main_frame)
graph_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

# Configuração do gráfico
fig, ax = plt.subplots(figsize=(6, 5))
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill="both", expand=True)

# Configurar expansão das colunas e linhas
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=2)
main_frame.rowconfigure(0, weight=1)

# Rodapé
footer_label = ttk.Label(root, text="Desenvolvido com Python e Tkinter", font=("Helvetica", 10))
footer_label.pack(side="bottom", pady=10)

# Iniciar a interface
root.mainloop()
