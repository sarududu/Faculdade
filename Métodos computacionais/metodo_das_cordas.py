# código do método do meio intervalo
#
# definindo a função a ser resolvidA
def f(x):
      return x**2.0+x-2.0


# (1) leitura de informações

vmin = float(input("entre com o valor min do intervalo: "))
vmax = float(input("entre com o valor max do intervalo: "))
tol = float(input("entre com o valor de tolerância: "))
nit = int(input("entre com o valor do número máximo de iteraçoes: "))
#
# (2) testando se min ou max é solução
if abs(f(vmin)) <= tol:
    print ("a solução é: ",vmin)
    exit()

if abs(f(vmax)) <= tol:
    print("a solução é: ",vmax)
    exit()
    
for i in range(1,nit):
    a = (f(vmax)-f(vmin))/(vmax-vmin)
    b = f(vmin)-a*vmin
    xm = -b/a
    if abs(f(xm)) <= tol:
        print("a solução é: ", xm)
        print("obtida na iteração: ",i)
        exit()
    else:
        if f(vmin)*f(xm)>0 and f(xm)*f(vmax)<0:
            vmin = xm
        if f(vmin)*f(xm)<0 and f(xm)*f(vmax)>0:
            vmax = xm
        if f(vmin)*f(xm)<0 and f(xm)*f(vmax)<0:
            vmax = xm
        if f(vmin)*f(xm)>0 and f(xm)*f(vmax)>0:
            print("Pode não haver solução no intervalo dado. Tente novo intervalo")
            exit()
else:
    print("todas iteraçoes foram rodadas e nenhuma solução encontrada")
        
            
