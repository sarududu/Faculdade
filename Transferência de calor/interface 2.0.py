import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Função para rodar a simulação
def rodar_simulacao(a, length, time, nodes, root):
    dx = length / (nodes - 1)
    dt = 0.5 * dx**2 / a

    u = np.zeros(nodes) + 20  # Placa Iniciando com 20 graus
    u[0] = 100  # Condição de contorno
    u[-1] = 0

    # Configuração da janela para exibir o gráfico
    sim_window = tk.Toplevel(root)
    sim_window.title("Simulação de Difusão de Calor")
    sim_window.geometry("800x600")

    fig, axis = plt.subplots(figsize=(8, 4))
    pcm = axis.pcolormesh([u], cmap=plt.cm.jet, vmin=0, vmax=100)
    plt.colorbar(pcm, ax=axis, label="Temperatura (°C)")
    axis.set_ylim([-2, 3])
    axis.set_xlabel("Posição na placa")
    axis.set_ylabel("Temperatura")

    canvas = FigureCanvasTkAgg(fig, master=sim_window)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    counter = 0
    while counter < time:
        w = u.copy()
        for i in range(1, nodes - 1):
            u[i] = dt * a * (w[i - 1] - 2 * w[i] + w[i + 1]) / dx**2 + w[i]
        counter += dt

        print(f"t: {counter:.3f} [s], Temperatura média: {np.average(u):.2f} °C")
        pcm.set_array(u)
        axis.set_title(f"Distribuição do calor: t = {counter:.3f} [s]")
        canvas.draw()
        sim_window.update_idletasks()

    plt.close(fig)

# Função para criar a interface principal
def abrir_interface():
    def iniciar_simulacao():
        try:
            a = float(difusividade_entry.get())
            length = float(comprimento_entry.get())
            time = float(tempo_entry.get())
            nodes = int(nos_entry.get())

            if a <= 0 or length <= 0 or time <= 0 or nodes < 3:
                raise ValueError

            rodar_simulacao(a, length, time, nodes, root)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores válidos.")

    # Configuração da janela principal
    root = tk.Tk()
    root.title("Simulação de Difusão de Calor")
    root.geometry("800x600")

    frame = ttk.Frame(root, padding="10")
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text="Configurações da Simulação", font=("Helvetica", 16)).pack(pady=10)

    # Difusividade térmica
    ttk.Label(frame, text="Difusividade térmica (a):").pack(anchor=tk.W, padx=10)
    difusividade_entry = ttk.Entry(frame)
    difusividade_entry.insert(0, "70")
    difusividade_entry.pack(fill=tk.X, padx=10, pady=5)

    # Comprimento da placa
    ttk.Label(frame, text="Comprimento da placa (mm):").pack(anchor=tk.W, padx=10)
    comprimento_entry = ttk.Entry(frame)
    comprimento_entry.insert(0, "100")
    comprimento_entry.pack(fill=tk.X, padx=10, pady=5)

    # Tempo total da simulação
    ttk.Label(frame, text="Tempo total da simulação (s):").pack(anchor=tk.W, padx=10)
    tempo_entry = ttk.Entry(frame)
    tempo_entry.insert(0, "50")
    tempo_entry.pack(fill=tk.X, padx=10, pady=5)

    # Número de nós
    ttk.Label(frame, text="Número de nós (malhas):").pack(anchor=tk.W, padx=10)
    nos_entry = ttk.Entry(frame)
    nos_entry.insert(0, "50")
    nos_entry.pack(fill=tk.X, padx=10, pady=5)

    # Botão para iniciar a simulação
    iniciar_button = ttk.Button(frame, text="Iniciar Simulação", command=iniciar_simulacao)
    iniciar_button.pack(pady=20)

    root.mainloop()

# Executa a interface
abrir_interface()

