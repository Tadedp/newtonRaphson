import sympy

def newtonRaphson(f, df, xn, tolerancia, iteraciones):
    #Iterar hasta alcanzar el valor de la variable 'iteraciones' o hasta fallar o tener éxito.
    for n in range(iteraciones):
        #Evaluar la función en xn.
        fxn = f(xn)

        #Comprobar si el método tuvo éxito. Si lo tuvo, retorna xn.
        if abs(fxn) < tolerancia:
            print(f"Convergencia alcanzada en {n} iteraciones.")
            return xn

        #Evaluar la derivada en xn.
        dfxn = df(xn)

        #Comprobar si la derivada evaluada en xn se anula. Si se anula (imposible continuar), se retorna None.
        if dfxn == 0:
            print(f"Derivada igual a cero en iteración número {n}, imposible continuar con el método.")
            return None
    
        #Calcular xn+1 y guardar el valor en la variable xn para la siguiente iteración.
        xn = xn - fxn / dfxn
    
    #Si el máximo de iteraciones fue alcanzado, se retorna None.
    print(f"Se alcanzaron {iteraciones} iteraciones. No se encontró la raíz con una tolerancia de {tolerancia}.")
    return None

def main():
    print("---------------------------------------MÉTODO NEWTON RAPHSON---------------------------------------")
    print("")
    
    #Declarar la variable simbólica 'x' para crear y manipular expresiones simbólicas.
    x = sympy.symbols("x")
    
    #Recibir y validar entradas del usuario
    while True:
        try:
            f_input = input("Ingrese la función en términos de x (ingrese \'h\' para ayuda): ").lower()
            
            if f_input.lower() == "h":
                print("")
                print("Ayuda para ingresar funciones a través de la terminal:")
                print("_Potencia: '**'                              -> x**2")
                print("_Exponencial: 'exp()'                        -> exp(x)")
                print("_Raíz cuadrada: 'sqrt()'                     -> sqrt(x)")
                print("_Trigonométricas: 'sin()', 'cos()', 'tan()'  -> tan(x)")
                print("_Logaritmo natural: 'log()'                  -> log(x)")
                print("_Logaritmo en base n: 'log(,n)'              -> log(x,n)")
                print("")
                print("Ejemplo: (x**2)/(sin(x) + 3)")
                print("")    
                continue
            
            #Convertir la entrada del usuario en una expresión simbólica de SymPy.
            f = sympy.sympify(f_input)
            
            #Verificar si la función depende de una sola variable.
            if len(f.free_symbols) != 1:
                raise ValueError("La función debe depender de una sola variable.")
            
            #Verificar si la función depende de x.
            if x not in f.free_symbols:
                raise ValueError("La función debe depender de x.")
            
            #Verificar si la función es lineal.
            if f.is_polynomial():
                f_coeficientes = f.as_coefficients_dict()
                if len(f_coeficientes) == 2 and 1 in f_coeficientes.keys() and x in f_coeficientes.keys():
                    raise ValueError("La función no debe ser lineal.")
                
                if len(f_coeficientes) == 1 and (1 in f_coeficientes.keys() or x in f_coeficientes.keys()):
                    raise ValueError("La función no debe ser lineal.")
            break

        except sympy.SympifyError:
            print("Error: Función inválida.")    
            print("")
        
        except Exception as e:
            print("Error: Función inválida.")
            print(e)
            print("")    
    
    #Hallar las derivadas de la función con respecto a x.
    df = sympy.diff(f, x)
    ddf = sympy.diff(df, x)
    
    #Convertir las expresiones simbólicas de SymPy en funciones de Python para que puedan ser evaluadas.
    f_convertida = sympy.lambdify(x, f)
    df_convertida = sympy.lambdify(x, df)
    ddf_convertida = sympy.lambdify(x, ddf)
    
    print("")    
    print(f"f(x) = {f}")
    print(f"f'(x) = {df}")
    print(f"f''(x) = {ddf}")
    print("")    
    
    #Recibir y validar entradas del usuario
    while True:
        try:
            x0 = float(input("Ingrese el punto inicial: "))
            
            #Verificar si la función y su derivada se encuentran definidas en el punto inicial.
            try:
                f_convertida(x0) 
                df_convertida(x0)
                ddf_convertida(x0)
            except:
                raise ValueError(f"La función o alguna de sus derivadas no se encuentran definidas en {x0}.")

            #Verificar si la derivada se anula en el punto inicial.
            if df_convertida(x0) == 0:
                raise ValueError(f"La derivada se anula en {x0}.")

            #Verificar si se cumple con la condición de convergencia.
            g = (f_convertida(x0) * ddf_convertida(x0)) / (df_convertida(x0) ** 2)              
            
            if abs(g) >= 1:
                raise ValueError("No se cumple la condición de convergencia.")
            
            break
        except Exception as e:
            print("Error: Punto inicial inválido.")
            print(e)
            print("")    
            
    print("")    
    while True:
        try:
            tolerancia = float(input("Ingrese la tolerancia: "))
            break
        except Exception:
            print("Error: Tolerancia inválida.")
            print("")    
    
    print("")    
    while True:
        try:
            iteraciones = int(input("Ingrese la cantidad máxima de iteraciones: "))
            if iteraciones < 1:
                raise Exception
            break
        except Exception:
            print("Error: Cantidad máxima de iteraciones inválida.")
            print("")    
    
    print("")    
    #Llamar al método newtonRaphson() para encontrar una raíz aproximada de la funcion f.
    raiz = newtonRaphson(f_convertida, df_convertida, x0, tolerancia, iteraciones)
    
    #Solo si el método pudo encontrar una raíz aproximada, mostrar el resultado.
    if raiz != None:
        print(f"La raíz aproximada de f(x) = {f} encontrada es: {raiz}")
        print(f"f({raiz}) = {f_convertida(raiz)}")
        
if __name__ == '__main__':
    main()