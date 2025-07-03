import numpy as np
    
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def rodar_simulacao(root, a, length, total_time, nodes, axis, canvas, pcm):
    dx = length / (nodes - 1)
    dt = 0.5 * dx**2 / a

    u = np.zeros(nodes) + 20  # Placa iniciando com 20 graus
    u[0] = 100  # Condição de contorno
    u[-1] = 0

    counter = 0

    def atualizar_grafico():
        nonlocal u, dt, dx, total_time, counter

        if counter < total_time:
            w = u.copy()
            for i in range(1, nodes - 1):
                u[i] = dt * a * (w[i - 1] - 2 * w[i] + w[i + 1]) / dx**2 + w[i]

            counter += dt

            # Atualizando o gráfico
            pcm.set_array(u)
            axis.set_title(f"Distribuição do calor: t = {counter:.2f} s")
            canvas.draw()

            # Reprogramando a próxima atualização
            root.after(1, atualizar_grafico)

    atualizar_grafico()


# Função para criar a interface principal
def abrir_interface():
    def iniciar_simulacao():
        try:
            a = float(difusividade_entry.get())
            length = float(comprimento_entry.get())
            total_time = float(tempo_entry.get())
            nodes = int(50)

            if a <= 0 or length <= 0 or total_time <= 0 or nodes <= 0:
                raise ValueError

            rodar_simulacao(root, a, length, total_time, nodes, axis, canvas, pcm)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores válidos.")

    # Configuração da janela principal
    root = tk.Tk()
    root.title("Simulação de Difusão de Calor")
    root.geometry("1000x700")
    root.configure(bg="#f4f4f4")

    # Estilo personalizado
    style = ttk.Style()
    style.configure("TLabel", font=("Times New Roman", 18), background="#f4f4f4")
    style.configure("TButton", font=("Times New Roman", 18), background="#4caf50", foreground="black")
    style.configure("TEntry", font=("Times New Roman", 18))
    style.configure("TLabelFrame", font=("Helvetica", 18, "bold"), background="#f4f4f4")

    # Layout principal
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Configurações da simulação
    config_frame = ttk.LabelFrame(main_frame, text="Parâmetros da Simulação", padding="15")
    config_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

    # Difusividade térmica
    ttk.Label(config_frame, text="Difusividade térmica (a):").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
    difusividade_entry = ttk.Entry(config_frame)
    difusividade_entry.insert(0, "70")
    difusividade_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.EW)

    # Comprimento da placa
    ttk.Label(config_frame, text="Comprimento da placa (mm):").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
    comprimento_entry = ttk.Entry(config_frame)
    comprimento_entry.insert(0, "100")
    comprimento_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.EW)

    # Tempo total da simulação
    ttk.Label(config_frame, text="Tempo total da simulação (s):").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
    tempo_entry = ttk.Entry(config_frame)
    tempo_entry.insert(0, "50")
    tempo_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.EW)


    # Expansão das colunas
    config_frame.columnconfigure(1, weight=1)

    # Botão para iniciar a simulação
    iniciar_button = ttk.Button(config_frame, text="Iniciar Simulação", command=iniciar_simulacao)
    iniciar_button.grid(row=4, column=0, columnspan=2, pady=20)

    # Gráfico
    graph_frame = ttk.Frame(main_frame, padding="10")
    graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    fig, axis = plt.subplots(figsize=(8, 4))
    u_initial = np.zeros(50) + 20
    u_initial[0] = 100
    u_initial[-1] = 0

    pcm = axis.pcolormesh([u_initial], cmap=plt.cm.jet, vmin=0, vmax=150)
    plt.colorbar(pcm, ax=axis, label="Temperatura (°C)")
    axis.set_ylim([-2, 3])
    axis.set_xlabel("Posição na placa")
    axis.set_ylabel("Temperatura")

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    root.mainloop()


# Executa a interface
abrir_interface()
