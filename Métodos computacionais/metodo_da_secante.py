# código do método da secante
#
# definindo a função a ser resolvidA
def f(x):
    return x**2.0+x-2.0

# (1) leitura de informações
x0 = float(input("entre com o chute inicial x0 "))
x1 = float(input("entre com o chute iinical x1 "))
tol = float(input("entre com a tolerância de convergência "))
nit = int(input("entre com o número máximo de iterações "))

# (2) loop - estrutura de repetição
for i in range(1,nit):
    x = x0 - (f(x0)/((f(x1)-f(x0))/(x1-x0)))
    if abs(f(x))<= tol:
        print("a solução é: ", x)
        print("obtida na iteração: ", i)
        exit()
    else:
        x0 = x1
        x1 = x

# (3) se todas as iterações forem rodadas sem encontrar solução
print("todas as iterações foram rodadas e nenhuma solução foi encontrada. Tente novo chute")
    
    

