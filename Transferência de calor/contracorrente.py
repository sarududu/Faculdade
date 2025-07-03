import matplotlib.pyplot as plt
from scipy.integrate import odeint
import numpy as np
from scipy.optimize import fsolve

# Modelo Estacionário Concorrente
def f(T, x):
    Tq, Tf = T  # Descompacta as variáveis do vetor T

    # Parâmetros do quente
    rhoq = 1000.0
    cpq = 4100.0
    vq = 0.02

    # Parâmetros do frio
    rhof = 1000.0
    cpf = 4100.0
    vf = 0.032

    # Cálculo do UA
    UA = 10000   

    # Equações diferenciais
    dTqdx = (UA / (rhoq * cpq * vq)) * (Tq - Tf)
    dTfdx = (UA / (rhof * cpf * vf)) * (Tq - Tf)
   
    return [dTqdx, dTfdx]  # Retorna uma lista com os resultados

# ------------- Programa Principal ------------------------------
# Defina as condições para frio em x = 0
y0f = 25

# Intervalo de discretização no espaço para todas as EDOs
L = 10.0
x = np.linspace(0.0, L, 30)

# Método de busca do resultado
def objective(y0q):
    sol = odeint(x,[y0q, y0f], x)  # Solução para o sistema
    Tqf = sol[-1, 0]  # Temperatura do quente na saída (x = L)
    Tq_esp = 80.0     # Temperatura desejada do quente na saída
    return Tqf - Tq_esp

# Resolver para encontrar a condição inicial ótima de y0q
y0q_optimal, = fsolve(objective, 10)  # Resolução do valor ótimo de y0q

# Resolver a equação com o valor de y0q encontrado
sol = odeint(f, [y0q_optimal, y0f], x)    

# Extração dos resultados
Tq = sol[:, 0]
Tf = sol[:, 1]

# Área de plotagem de resultados
plt.plot(x, Tq, 'r--', label='Tq (Quente)')
plt.plot(x, Tf, 'bo', label='Tf (Frio)')
plt.xlabel('Posição (x)')
plt.ylabel('Temperatura (°C)')
plt.legend()
plt.title('Perfil de Temperatura no Trocador de Calor')
plt.grid(True)
plt.show()
