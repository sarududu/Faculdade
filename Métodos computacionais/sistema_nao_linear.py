# ---------------------------
# Implementação das funções
# ---------------------------

def func(x):
    func = []
    for i in range(n):
        func.append(0.0)

    func[0] = (x[0])**2.0 +(x[1])**2.0 - 2.0
    func[1] = (x[0])**2.0 -(1.0/9.0)*(x[1])**2.0 - 1.0
    return func 

# --------------------------
# Matriz Jacobiana
# --------------------------

def Jac(x):
    Jac = []
    for i in range(n):
        linha = []
        for j in range(n):
            linha.append(0.0)
        Jac.append(linha)
  
    Jac[0][0] = 2.0*x[0]
    Jac[0][1] = 2.0*x[1]
    Jac[1][0] = 2.0*x[0]
    Jac[1][1] = (-2.0/9.0)*x[1]
    return Jac

# --------------------------
# Matriz Inversa
# --------------------------

def Ainv(A):
    Ainv = []
    for i in range(n):
        linha = []
        for j in range(n):
            linha.append(0.0)
        Ainv.append(linha)

    Ae = []
    for i in range(n):
        linha=[]
        for j in range(n):
            linha.append(A[i][j])
        for j in range(n):
            if i!=j:
                linha.append(0.0)
            if i==j:
                linha.append(1.0)
        Ae.append(linha)

    for i in range(n):
        pivo = Ae[i][i]
        if pivo == 0.0:
            print("a matriz é não inversível")
            exit()
        for k in range(n):
            if i!=k:
                fator = Ae[k][i]/pivo
                for j in range(2*n):
                    Ae[k][j] = Ae[k][j]-fator*Ae[i][j]
    
    for i in range(n):
        pivo = Ae[i][i]
        for j in range(2*n):
            Ae[i][j] = Ae[i][j]/pivo
     
    for i in range(n):
        for j in range(n):
            Ainv[i][j] = Ae[i][j+n]
    return Ainv            

#-------------------------------------------
# função para multiplica matriz por um vetor
#-------------------------------------------
def Mult(A,b):
    Mult = []
    for i in range(n):
        Mult.append(0.0)
    
    for i in range(n):
        soma = 0.0
        for j in range(n):
            soma = A[i][j]*b[j]+soma
        Mult[i] = soma
    return Mult
 
# -------------------------------------
# Método de Newton-Raphson multivariado
# -------------------------------------

# lendo informações
nit = int(input("entre com o número máximo de iterações "))
n = int(input("entre com a dimensão do sistema não linear "))
tol = float(input("entre com a tolerância de convergência "))
x0 = []
for i in range(n):
    x0.append(  float(input("entre com o chute inicial de x" + str(i)+ " ")) )

x = []
for i in range(n):
    x.append(0.0)
    
# loop de Newton-Raphson
for k in range(nit):   
    f = func(x0)
    A = Jac(x0)
    Jacinv = Ainv(A)
    resp = Mult(Jacinv,f)
    for i in range(n):
        x[i] = x0[i] - resp[i]
    f = func(x)
    for i in range(n):
        f[i] = abs(f[i])
    if max(f) <= tol:
        print("a solução foi encontrada na iteração " + str(k))
        for i in range(n):
            print("x"+str(i)+ " = " + str(x[i]))
        exit()
    else:
        for i in range(n):
            x0[i] = x[i]

print("nenhuma solução foi encontrada")
print("tente novo chute")
    
    






  
  
