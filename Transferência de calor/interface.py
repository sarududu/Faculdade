import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog

# Função para rodar a simulação
def rodar_simulacao(a, length, time, nodes):
    dx = length / (nodes - 1)
    dt = 0.5 * dx**2 / a

    u = np.zeros(nodes) + 20  # Placa Iniciando com 20 graus
    u[0] = 100  # Condição de contorno
    u[-1] = 0

    fig, axis = plt.subplots()
    pcm = axis.pcolormesh([u], cmap=plt.cm.jet, vmin=0, vmax=100)
    plt.colorbar(pcm, ax=axis)
    axis.set_ylim([-2, 3])

    counter = 0
    while counter < time:
        w = u.copy()
        for i in range(1, nodes - 1):
            u[i] = dt * a * (w[i - 1] - 2 * w[i] + w[i + 1]) / dx**2 + w[i]

        counter += dt

        print("t: {:.3f} [s], Average temperature: {:.2f} Celcius".format(counter, np.average(u)))
        pcm.set_array([u])
        axis.set_title("Distribuição do calor em: {:.3f} [s].".format(counter))
        plt.pause(0.01)

    plt.show()

# Função para abrir a interface gráfica
def abrir_interface():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal

    # Solicita os valores 
    a = simpledialog.askfloat("Configuração", "Digite a difusividade térmica (a):", initialvalue=70)
    length = simpledialog.askfloat("Configuração", "Digite o comprimento da placa (mm):", initialvalue=100)
    time = simpledialog.askfloat("Configuração", "Digite o tempo total da simulação (s):", initialvalue=50)
    nodes = simpledialog.askinteger("Configuração", "Digite o número de nós (malhas):", initialvalue=50)

    if None not in (a, length, time, nodes):
        rodar_simulacao(a, length, time, nodes)
    else:
        print("Simulação cancelada.")

# Executa a interface
abrir_interface()
