# -----------------------------------------------------
# funções - para calcular a regressão
# -----------------------------------------------------

# modelo usado na regressão
def modelo(Nparam,Param,x):
    import math   
    A = Param[0]
    B = Param[1]
    # y = A*(1.0-math.exp(-B*x))    # Ex1
    # y = (1/A)*((0.05)**(1.0-B)-(x)**(1.0-B))/(1.0-B)  # Ex2
    y = 1.0 - math.exp(-A*((x-338.75)/(10.0))*math.exp((-B)/(8.314*x)))  # Ex3
    return y

# função objetivo - soma dos erros quadráticos
def SEQ(Nparam,Param,Nexp,Xexp,Yexp):
    soma = 0.0
    for i in range(Nexp):
        ym = modelo(Nparam,Param,Xexp[i])
        soma = soma +(ym-Yexp[i])**2.0
    return soma




#--------------------------------
#------- Principal---------------
#--------------------------------        

# abrindo o arquivo de dados
file = open('entrada_dados.txt', mode='r')

# lendo o número de dados experimentais a partir do arquivo
c = file.readline()
Nexp = int(file.readline().strip())
print(c, Nexp)

# lendo o vetor de Xexp  a partir do arquivo
c = file.readline()
Xexp = []
for i in range(Nexp):
    valor = float(file.readline().strip())
    Xexp.append(valor)
print(c,Xexp)

# lendo o vetor de Yexp  a partir do arquivo
c = file.readline()
Yexp = []
for i in range(Nexp):
    valor = float(file.readline().strip())
    Yexp.append(valor)
print(c, Yexp)

# lendo o número de partículas a partir do arquivo
c = file.readline()
Np = int(file.readline().strip())
print(c, Np)

# lendo o número de iterações a partir do arquivo
c = file.readline()
Nit = int(file.readline().strip())
print(c, Np)

# lendo o número de parâmetros do modelo a partir do arquivo
c = file.readline()
Nparam = int(file.readline().strip())
print(c,Nparam)

# lendo o vetor de valores mínimos dos parâmetros a partir do arquivo
c = file.readline()
MinParam = []
for j in range(Nparam):
    valor = float(file.readline().strip())
    MinParam.append(valor)
print(c, MinParam)

# lendo o vetor de valores máximos dos parâmetros a partir do arquivo
c = file.readline()
MaxParam = []
for j in range(Nparam):
    valor = float(file.readline().strip())
    MaxParam.append(valor)
print(c, MaxParam)

import random
# Geração inicial de partículas
print("# Fazendo a geração inicial de partículas...")
Param = []
Param_melhor = []
Param_Global = []
Param = [0]*(Nparam)
Param_melhor = [0]*(Nparam)
Param_Global = [0]*(Nparam)
Particula = []
Particula_melhor = []
for i in range(Np):
    linha = []
    for j in range(Nparam):
        linha.append(0)
    Particula.append(linha)
    Particula_melhor.append(linha)

SEQ_global = 10000000.0
for i in range(Np):
    for j in range(Nparam):
        Param[j] = MinParam[j]+(MaxParam[j] - MinParam[j])*random.random()
        Particula[i][j] = Param[j]
        Particula_melhor[i][j] = Param[j]
    resp = SEQ(Nparam,Param,Nexp,Xexp,Yexp)    
    if resp < SEQ_global:
        SEQ_global = resp
        for j in range(Nparam):
            Param_Global[j] = Param[j]

# Fazendo as iterações
print("# Fazendo as iterações...")

w = 0.7
c1 = 1.2
c2 = 1.2

velocidade = []
for i in range(Np):
    linha = []
    for j in range(Nparam):
        linha.append(0)
    velocidade.append(linha)

for k in range (Nit):
    for i in range(Np):
        for j in range(Nparam):
            velocidade[i][j] = w*velocidade[i][j] + c1*random.random()*(Particula_melhor[i][j]- Particula[i][j]) + c2*random.random()*(Param_Global[j]-Particula[i][j])
            Particula[i][j] = Particula[i][j] + velocidade[i][j]
            if Particula[i][j]> MaxParam[j]:
                Particula[i][j] = MaxParam[j]
                velocidade[i][j] = 0.0
            if Particula[i][j]< MinParam[j]:
                Particula[i][j] = MinParam[j]
                velocidade[i][j] = 0.0
            Param[j] = Particula[i][j]
            Param_melhor[j] = Particula_melhor[i][j]
        resp = SEQ(Nparam,Param,Nexp,Xexp,Yexp)
        resp_melhor = SEQ(Nparam,Param_melhor,Nexp,Xexp,Yexp)
        if resp < resp_melhor:
            resp_melhor = resp
            for j in range(Nparam):
                Particula_melhor[i][j] = Param[j]
        if resp < SEQ_global:
            SEQ_global = resp
            for j in range(Nparam):
                Param_Global[j] = Param[j]

    print("iteração: ", k)
    print("SEQ = ", SEQ_global)
    print("Parâmetros", Param_Global)
    print("")


