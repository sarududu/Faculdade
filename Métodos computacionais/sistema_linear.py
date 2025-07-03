# -----------------------------------------------------
# funções - para calcular os sistemas
# -----------------------------------------------------

# para sistema diagonal
def diagonal(n,A,b):
    x = []
    print("a solução é:")       
    for i in range(n):
        x.append(b[i][0]/A[i][i])
    print(x)

# para sistema triangular inferior
def trian_inf(n,A,b):
    x = []
    print("a solução é:")
    x = [0]*(n)
    x[0] = b[0][0]/A[0][0]
    for i in range(1,n):
        soma = 0.0
        for j in range(0,i):
            soma = soma + A[i][j]*x[j]
        x[i]=(b[i][0]-soma)/A[i][i]
    print(x) 

# para sistema triangular superior
def trian_sup(n,A,b):
    x = []
    print("a solução é:")
    x = [0]*(n)
    x[n-1]= b[n-1][0]/A[n-1][n-1]
    for i in range(n-2,-1,-1):
        soma = 0.0
        for j in range(i+1,n):
            soma = soma + A[i][j]*x[j]
        x[i]=(b[i][0]-soma)/A[i][i]
    print(x) 

# para transformar o sistema por Gauss
def Gauss(n,A,b):
    print("Gauss")
    Ae = []
    for i in range(n):
        linha=[]
        for j in range(n):
            linha.append(A[i][j])
        linha.append(b[i][0])
        Ae.append(linha)

    for i in range(n-1):
        pivo = Ae[i][i]
        for k in range(i+1,n):
            fator = Ae[k][i]/pivo
            for j in range(n+1):
                Ae[k][j] = Ae[k][j]-fator*Ae[i][j]
                 
    for i in range(n):
        for j in range(n):
            A[i][j] = Ae[i][j]
        b[i][0] = Ae[i][n]

    trian_sup(n,A,b)
    

# para transformar o sistema por Jordan
def Jordan(n,A,b):
    print("Jordan")
    Ae = []
    for i in range(n):
        linha=[]
        for j in range(n):
            linha.append(A[i][j])
        linha.append(b[i][0])
        Ae.append(linha)

    for i in range(n):
        pivo = Ae[i][i]
        for k in range(n):
            if i!=k:
                fator = Ae[k][i]/pivo
                for j in range(n+1):
                    Ae[k][j] = Ae[k][j]-fator*Ae[i][j]
                  
    for i in range(n):
        for j in range(n):
            A[i][j] = Ae[i][j]
        b[i][0] = Ae[i][n]

    diagonal(n,A,b)

  

#--------------------------------
#------- Principal---------------
#--------------------------------        

# abrindo o arquivo de dados
file = open('entrada_dados.txt', mode='r')

# lendo a dimensão do sistema a partir do arquivo
n = int(file.readline().strip())

# lendo a matriz A do sistema a partir do arquivo
A = []
for i in range(n):
    linha = list(map(float,file.readline().split()))
    A.append(linha)

# lendo o vetor b do sistema a partir do arquivo
b = []
for i in range(n):
    linha = list(map(float,file.readline().split()))
    b.append(linha)

# testando se o sistema é diagonal
soma = 0.0
for i in range(n):
    for j in range(n):
        if i!=j:
            soma = soma+abs(A[i][j])
if soma==0.0:
    print("o sistema é diagonal")
    diagonal(n,A,b)
    exit()

# testando se o sistema é triangular inferior
soma = 0.0
for i in range(n):
    for j in range(n):
        if i<j:
            soma = soma+abs(A[i][j])

if soma==0.0:
    print("o sistema é triangular inferior")
    trian_inf(n,A,b)
    exit()

# testando se o sistema é triangular superior
soma = 0.0
for i in range(n):
    for j in range(n):
        if i>j:
            soma = soma+abs(A[i][j])

if soma==0.0:
    print("o sistema é triangular superior")
    trian_sup(n,A,b)
    exit()
else:
    print("o sistema não é diagonal nem triangular")
    Gauss(n,A,b)
    Jordan(n,A,b)
       
    

    
   
    
    
   
