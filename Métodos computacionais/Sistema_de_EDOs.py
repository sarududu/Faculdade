# ---------------------------
# Implementação das funções
# ---------------------------

def func(x,y):
    func = []
    for i in range(n):
        func.append(0.0)

    func[0] = (170*3.14*0.025/(0.2*4186))*(y[1]-y[0])
    func[1] = (-170*3.14*0.025/(0.1*1842))*(y[1]-y[0])
    return func 




# ------------------------------------
# Programa principal
# Resolve um sistema de EDOs de 1a ordem usando os métodos
# Euler, RK2, RK3 e RK4

# lendo informações
neq = int(input("entre com o número de EDOs: "))
n = int(input("entre com o número de pontos de discretização: "))
x0 = float(input("entre com o valor inicial de x, x0 = "))
xf = float(input("entre com o valor final de x, xf = "))
h = (xf-x0)/n
tipo = int(input("entre com o método de solução. Digite 1-Euler, 2-RK2, 3-RK3, 4-RK4 "))
xant = x0

# preenchendo previamente os vetores com valores nulos
ypos = []
yant = []
K1=[]
K2=[]
K3=[]
K4=[]
aux = []

for i in range(neq):
    ypos.append(0.0)
    yant.append(0.0)
    K1.append(0.0)
    K2.append(0.0)
    K3.append(0.0)
    K4.append(0.0)
    aux.append(0.0)

# lendo as condições iniciais de y
for i in range(neq):
    yant[i] = float(input("entre com o valor inicial de y[" + str(i)+"] = "))

# resolvendo o problema por Euler:
print(xant,yant)
if tipo == 1:
    for k in range(n):
        f = func(xant,yant)
        for j in range(neq):
            ypos[j]=yant[j]+h*f[j]
            xpos = xant + h
        print(xpos,ypos)
        xant = xpos
        yant = ypos
    

if tipo == 2:
    alfa = 0.5
    beta = 0.5
    for k in range(n):
        K1 = func(xant,yant)
        for i in range(neq):
            aux[i] = yant[i]+K1[i]*h
        K2 = func(xant+h,aux)
        for j in range(neq):
            ypos[j]=yant[j]+h*(alfa*K1[j]+beta*K2[j])
            xpos = xant + h
        print(xpos,ypos)
        xant = xpos
        yant = ypos    

if tipo == 3:
    alfa = (1.0/6.0)
    beta = (4.0/6.0)
    gama = (1.0/6.0)
    for k in range(n):
        K1 = func(xant,yant)
        for i in range(neq):
            aux[i] = yant[i]+K1[i]*(h/2)
        K2 = func(xant+(h/2),aux)
        for i in range(neq):
            aux[i] = yant[i]+2*h*K2[i]-h*K1[i]
        K3 = func(xant+h,aux)       
        for j in range(neq):
            ypos[j]=yant[j]+h*(alfa*K1[j]+beta*K2[j]+gama*K3[j])
            xpos = xant + h
        print(xpos,ypos)
        xant = xpos
        yant = ypos    

if tipo == 4:
    alfa = (1.0/6.0)
    beta = (2.0/6.0)
    gama = (2.0/6.0)
    sigma = (1.0/6.0)
    for k in range(n):
        K1 = func(xant,yant)
        for i in range(neq):
            aux[i] = yant[i]+K1[i]*(h/2)
        K2 = func(xant+(h/2),aux)
        for i in range(neq):
            aux[i] = yant[i]+K2[i]*(h/2)
        K3 = func(xant+(h/2),aux)       
        for i in range(neq):
            aux[i] = yant[i]+K3[i]*h
        K4 = func(xant+h,aux)       
        for j in range(neq):
            ypos[j]=yant[j]+h*(alfa*K1[j]+beta*K2[j]+gama*K3[j]+sigma*K4[j])
            xpos = xant + h
        print(xpos,ypos)
        xant = xpos
        yant = ypos    





        
      
    
