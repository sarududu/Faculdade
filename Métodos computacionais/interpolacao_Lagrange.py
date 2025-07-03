#--------------------------------
#------- Principal---------------
#--------------------------------        

# abrindo o arquivo de dados
file = open('entrada_dados_interpola.txt', mode='r')

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

x = float(input("entre com o valor de x que deseja interpolar"))

# loop de interpolação
soma = 0.0
for i in range(Nexp):
    prod = 1.0
    for j in range(Nexp):
        if j != i:
            prod = prod*(x-Xexp[j])/(Xexp[i]-Xexp[j])
    soma = soma + Yexp[i]*prod

# impressão
print("o valor de y interpolado para " + str(x) + " é: " + str(soma))
        
