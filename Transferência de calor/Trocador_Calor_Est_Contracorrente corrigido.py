# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 16:05:45 2025

@author: salom
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 11:38:02 2025

@author: domin
"""

import matplotlib.pyplot as plt
from scipy.integrate import odeint
import numpy as np
from scipy.optimize import fsolve

# Modelo Estacionário Concorrente
def f(T,x):
        
    Tq, Tf = T

    # Parâmetros do quente
    rhoq = 1000.0
    cpq = 4100.0
    vq = 0.02
    
    # Parâmetros do frio
    rhof = 1000.0
    cpf = 4100.0
    vf = 0.032
    
    # Calculo do UA
    UA = 10000   
      
    # Equações 
    dTqdx = (UA/(rhoq*cpq*vq))*(Tq - Tf)
    dTfdx = (UA/(rhof*cpf*vf))*(Tq - Tf)
   
    return [dTqdx, dTfdx]

# ------------- Programa Principal ------------------------------
# Defina as condições x = 0 para frio
y0f = 25
# Intervalo de discretização no espaço para todas as EDOs
L = 10.0
x = np.linspace(0.0,L,30)

# Método de busca do resultado --------

for i in range(20,60,1):
    y0f = 25
    y0q = 0.9*i
    sol = odeint(f,[y0q,y0f],x) 
    Tqf = sol[-1,0]
    Tq_esp = 80.0
    #print (Tqf, Tq_esp, abs(Tqf - Tq_esp))
    if (abs(Tqf - Tq_esp) <= 1):
        y0qf = y0q
        print(y0qf)

# Resolver e plotar a resposta Ótima
sol = odeint(f,[y0qf,y0f],x)    

# Impressão dos resultados - reatribuir os resultados na matriz sol as 
Tq = sol[:,0]
Tf = sol[:,1]
# Área de plotagem de resultados
plt.plot(x, Tq, 'r--')
plt.plot(x, Tf, 'bo')
plt.show()
