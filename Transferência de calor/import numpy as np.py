import numpy as np
import matplotlib.pyplot as plt



#Definindo Problema

a = 70 #Difusividade térmica
length = 100 #mm
time = 50 #Tempo s faça uma interface gráfica para esse código 
nodes = 50 #Número de Malhas

# Configuração Inicial 

dx = length / (nodes-1)
dt = 0.5 * dx**2 / a
t_nodes = int(time/dt) + 1

u = np.zeros(nodes) + 20 # Placa Iniciando com 20 graus

# Condições de Contorno

u[0] = 100
u[-1] = 0


# Configuração da Animação

fig, axis = plt.subplots()

pcm = axis.pcolormesh([u], cmap=plt.cm.jet, vmin=0, vmax=100)
plt.colorbar(pcm, ax=axis)
axis.set_ylim([-2, 3])

#Simulação

counter = 0

while counter < time :

    w = u.copy()

    for i in range(1, nodes - 1):

        u[i] = dt * a * (w[i - 1] - 2 * w[i] + w[i + 1]) / dx ** 2 + w[i]

    counter += dt

    print("t: {:.3f} [s], Average temperature: {:.2f} Celcius".format(counter, np.average(u)))

    # Plot do problema

    pcm.set_array([u])
    axis.set_title("Distribuição do calor em: {:.3f} [s].".format(counter))
    plt.pause(0.01)


plt.show()