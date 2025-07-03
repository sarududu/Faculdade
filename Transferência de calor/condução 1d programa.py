import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Variáveis globais
tarefa_agendada = None
simulacao_ativa = False  # Variável de controle de simulação

def rodar_simulacao(root, a, length, total_time, nodes, u_0, u_n, temperatura_inicial, axis, canvas, pcm, parar_simulacao_callback):
    global tarefa_agendada, simulacao_ativa  
    dx = length / (nodes - 1)
    dt = 0.5 * dx**2 / a

    x = np.linspace(0, length, nodes)
    y = np.array([0, 1])  # Para criar um gráfico 2D simples
    u = np.zeros(nodes) + temperatura_inicial  # Temperatura inicial
    u[0] = u_0  # Condição de contorno na extremidade esquerda
    u[-1] = u_n  # Condição de contorno na extremidade direita

    # Array 2D necessário para pcolormesh
    u_2d = np.vstack([u, u])  # Criar um array 2D duplicando u

    counter = 0

    def atualizar_grafico():
        nonlocal u, dt, dx, total_time, counter, u_2d
        if simulacao_ativa:  # Verifica se a simulação ainda está ativa
            if counter < total_time:
                w = u.copy()
                for i in range(1, nodes - 1):
                    u[i] = dt * a * (w[i - 1] - 2 * w[i] + w[i + 1]) / dx**2 + w[i]

                counter += dt

                # Atualizar o array 2D
                u_2d[0, :] = u
                u_2d[1, :] = u

                # Atualizando o gráfico
                pcm.set_array(u_2d.ravel())
                axis.set_title(f"Distribuição do calor: t = {counter:.2f} s")
                canvas.draw()

                # Reprogramando a próxima atualização
                tarefa_agendada = root.after(1, atualizar_grafico)
            else:
                parar_simulacao_callback()  # Parar a simulação quando o tempo total for alcançado

    simulacao_ativa = True  # Inicia a simulação
    atualizar_grafico()


# Interface principal
def abrir_interface():
    def iniciar_simulacao():
        try:
            # Chamada para os valores da simulação
            a = float(difusividade_entry.get())#difusividade térmica
            length = float(comprimento_entry.get())#comprimento
            total_time = float(tempo_entry.get()) #tempo
            nodes = int(100)  # Número de nós (malhas)
            u_0 = float(u_inicio_entry.get())  # Valor da condição de contorno na extremidade esquerda
            u_n = float(u_fim_entry.get())  # Valor da condição de contorno na extremidade direita
            temperatura_inicial = float(temperatura_inicial_entry.get())  # Temperatura inicial da placa

            # Verificação simples para valores negativos ou 0
            if a <= 0 or length <= 0 or total_time <= 0 or nodes <= 0 or u_0 < 0 or u_n < 0 or temperatura_inicial < 0:
                raise ValueError("Todos os valores devem ser positivos e válidos.")

            # Se tudo estiver ok, simulação roda
            rodar_simulacao(root, a, length, total_time, nodes, u_0, u_n, temperatura_inicial, axis, canvas, pcm, parar_simulacao)
            parar_simulacao_button.config(state=tk.NORMAL)  # Botão de parar após iniciar a simulação

        except ValueError as ve:
            print(f"Erro: {ve}")  # Exibe o erro no terminal para depuração
            messagebox.showerror("Erro", str(ve))  # Exibe o erro na interface

    def parar_simulacao():
        global tarefa_agendada, simulacao_ativa 
        nonlocal parar_simulacao_button
        # Cancelando a tarefa agendada de atualização do gráfico
        if tarefa_agendada is not None:
            root.after_cancel(tarefa_agendada)
            tarefa_agendada = None
        simulacao_ativa = False  # Interrompe a simulação
        parar_simulacao_button.config(state=tk.DISABLED)  # Desabilitar o botão de parar 

    # Configuração da janela principal
    root = tk.Tk()
    root.title("Simulação de Difusão de Calor")
    root.geometry("1000x700")
    root.configure(bg="#f4f4f4")

    # Estilo da janela
    style = ttk.Style()
    style.configure("TLabel", font=("Bookman Old Style", 18), background="#f4f4f4")
    style.configure("TButton", font=("Bookman Old Style", 18), background="#4caf50", foreground="black")
    style.configure("TEntry", font=("Bookman Old Style", 18))
    style.configure("TLabelFrame", font=("Bookman Old Style", 18, "bold"), background="#f4f4f4")

    # Layout principal
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Configurações da simulação
    config_frame = ttk.LabelFrame(main_frame, text="Parâmetros da Simulação", padding="15")
    config_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

    # Difusividade térmica
    ttk.Label(config_frame, text="Difusividade térmica (α):").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
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

    # Temperatura inicial da placa
    ttk.Label(config_frame, text="Temperatura inicial da placa (°C):").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
    temperatura_inicial_entry = ttk.Entry(config_frame)
    temperatura_inicial_entry.insert(0, "20")  # Temperatura inicial da placa
    temperatura_inicial_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.EW)

    # Condição de contorno inicial (u[0])
    ttk.Label(config_frame, text="Temperatura extremidade direita da placa:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
    u_inicio_entry = ttk.Entry(config_frame)
    u_inicio_entry.insert(0, "100")  # Valor inicial da condição de contorno
    u_inicio_entry.grid(row=4, column=1, padx=10, pady=5, sticky=tk.EW)

    # Condição de contorno final (u[-1])
    ttk.Label(config_frame, text="Temperatura extremidade esquerda da placa:").grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
    u_fim_entry = ttk.Entry(config_frame)
    u_fim_entry.insert(0, "0")  # Valor final da condição de contorno
    u_fim_entry.grid(row=5, column=1, padx=10, pady=5, sticky=tk.EW)

    # Expansão das colunas
    config_frame.columnconfigure(1, weight=1)

    # Botão para iniciar a simulação
    iniciar_button = ttk.Button(config_frame, text="Iniciar Simulação", command=iniciar_simulacao)
    iniciar_button.grid(row=6, column=0, columnspan=2, pady=20)

    # Botão para parar a simulação
    parar_simulacao_button = ttk.Button(config_frame, text="Parar Simulação", command=parar_simulacao)
    parar_simulacao_button.grid(row=7, column=0, columnspan=2, pady=20)
    parar_simulacao_button.config(state=tk.DISABLED)  # Inicialmente desabilitado

    # Gráfico
    graph_frame = ttk.Frame(main_frame, padding="10")
    graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    fig, axis = plt.subplots(figsize=(8, 4))
    x = np.linspace(0, 100, 100)  # Ajuste o comprimento conforme necessário
    y = np.array([0, 1])
    u_initial = np.zeros(100) + 20
    u_initial[0] = 100
    u_initial[-1] = 0
    u_initial_2d = np.vstack([u_initial, u_initial])  # Transformar para 2D

    pcm = axis.pcolormesh(x, y, u_initial_2d, cmap=plt.cm.jet, vmin=0, vmax=100)
    plt.colorbar(pcm, ax=axis, label="Temperatura (°C)")
    axis.set_xlabel("Posição na placa")
    axis.set_ylabel("Temperatura")

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    root.mainloop()


# Executa a interface
abrir_interface()
