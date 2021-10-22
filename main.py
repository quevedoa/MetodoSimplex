import numpy as np

def estandarizar(restricciones: np.ndarray, costos: np.ndarray, isMin: bool, nomVariables: list = []):
    costos = np.array([np.insert(costos, -1, 0)])
    restricciones = np.vstack((restricciones, costos))
    numRest = restricciones.shape[0]
    
    numVarsH = 1
    numVarsE = 1
    
    if not isMin:
        costos = -1*costos
        
    # La idea es que cuando pasemos las restricciones sean arreglos donde los primeros n elementos
    # sean las n variables de esa restricción, el elemento (n+1) sea la (b) de esa restricción y
    # que el ultimo elemento sea -1 si la restricción es <=, 1 si es >= y 0 si es =
    
    for i in range(numRest):
        op = restricciones[i,-1]
        if op == -1: # <=
            # Agregar variable de holgura
            colH = np.zeros(numRest) 
            colH[i] = 1 # Creamos columna de ceros menos un 1 en el current renglon 
            colH = np.array([colH]).T # Transponemos para hacer arreglo en columna
            restricciones = np.hstack((restricciones[:,0:-2], colH, restricciones[:,-2:]))
            nomVariables.append("h"+str(numVarsH))
            numVarsH += 1
        elif op == 1: # >=
            # Agregar variable de excedente
            colE = np.zeros(numRest) 
            colE[i] = -1 # Creamos columna de ceros menos un 1 en el current renglon 
            colE = np.array([colE]).T # Transponemos para hacer arreglo en columna
            restricciones = np.hstack((restricciones[:,0:-2], colE, restricciones[:,-2:]))
            nomVariables.append("e"+str(numVarsE))
            numVarsE += 1
        elif op != 0: # =
            print("ERROR: En creación de variables de holgura y/o excedente")
    
    tablaSimplexStd = restricciones[:,0:-1] # Quitamos la ultima columna que solo representaba las operaciones
    return tablaSimplexStd, nomVariables

def checkNegativos(arr: np.ndarray):
    # Regresa -1 si ninguno es negativo, si no regresa el indice del primer elemento negativo
    ind = 0
    for e in arr:
        if e < 0:
            return ind
        ind += 1
    return -1
    
def checkRenglonPivote(y: np.ndarray, b: np.ndarray):
    arrLength = b.size
    epsilon = np.ones(arrLength) # Crea un vector donde guardaremos todas las epsilon=bi/yi
    for i in range(arrLength):
        yi, bi = y[i], b[i]
        if yi == 0 or bi < 0 or yi < 0: 
            # Si yi = 0, o bi,yi < 0 entonces invalidamos esos cocientes guardando -infinito en esa entrada del
            # vector epsilon
            epsilon[i] = float('inf')
        else:
            # Si bi y yi son validos guardamos su cociente
            epsilon[i] = bi/yi
            
    minEpsilon = epsilon.min() # Encontramos el mínimo de epsilon
    if minEpsilon == float('inf'):
        raise Exception("No existe epsilon valida")
    else:
        indiceMinEpsilon = np.where(epsilon == minEpsilon)[0][0] # Si existen dos epsilons minimos iguales agarramos el primero (Regla de Bland)
    
    return indiceMinEpsilon

def simplex(tabla: np.ndarray):
    # Entra una tabla simplex estandar inicial y sale la tabla simplex final
    costos = tabla[-1,:]
    numReng = tabla.shape[0]
    numCol = tabla.shape[1]
    
    print('--------------------------------------------------------------\n')
    
    while checkNegativos(costos) != -1:
        # Vemos que el indice de la variable que va a entrar (Siempre entra el más a la izquierda Regla de Bland)
        indVarEntrada = checkNegativos(costos)
        # Determinamos el indice del renglon que va a ser pivote
        indRengPivote = checkRenglonPivote(tabla[:,indVarEntrada], tabla[:,-1])
        
        print("Entra la variable: ", indVarEntrada+1)
        print("Pivoteamos el renglón: ", indRengPivote+1)
        print(tabla)
        
        # Hacemos ese primer 1 pivote
        tabla[indRengPivote,:] = tabla[indRengPivote,:]/tabla[indRengPivote,indVarEntrada]
        
        # La suma de renglones
        for i in range(numReng):
            if i != indRengPivote:
                tabla[i,:] = tabla[i,:] - (tabla[i,indVarEntrada])*tabla[indRengPivote, :]
    
        print('--------------------------------------------------------------\n')

    print("Tabla Final")
    print(tabla)
        
    
if __name__ == "__main__":
    matNEst = np.array([[1,2,10,-1],[1,2,5,-1],[1,-1,2,-1]])
    costNEst = np.array([[2,-1,0]])
    nomVar = ["x1","x2"]

    #print(costNEst)
    print(estandarizar(matNEst, costNEst, False, nomVar)[0])

    val = input("Enter your value: ")
    print(val)