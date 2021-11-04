import numpy as np
import re
import math

from numpy.core.shape_base import vstack

np.set_printoptions(formatter={'float': lambda x: "{0:0.1f}".format(x)})

# Función que estandariza PPL
def estandarizar(restricciones: np.ndarray, costos: np.ndarray, isMin: bool, nomVariables: list = []):
    if not isMin:
        costos = -1*costos  # Si el problema trata de maximizar, multiplicamos el renglón de costos por -1 para estandarizar.

    costos = np.array([np.insert(costos, -1, 0)])   # Insertamos al final del renglón de costos un 0 para que sea de la misma dimensión que la matriz de restricciones
    restricciones = np.vstack((restricciones, costos))  # Juntamos la matriz de restricciones con el renglón de costos
    numRest = restricciones.shape[0]    # Almacenamos el numero de renglones que tiene la matriz nueva
    
    numVarsH = 1
    numVarsE = 1
        
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
        print("ERORORORORORO")
    else:
        indiceMinEpsilon = np.where(epsilon == minEpsilon)[0][0] # Si existen dos epsilons minimos iguales agarramos el primero (Regla de Bland)
    
    return indiceMinEpsilon

def isCanonico(vect: np.ndarray):
    indUno = -1
    for i in range(vect.size):
        if vect[i] == 1:
            if indUno != -1:
                return -1
            else:
                indUno = i
        elif vect[i] != 0:
            return -1
    return indUno

def checkMultiplesSoluciones(vect: np.ndarray):
    if vect[-1] < 1e-10 and vect[-1] > 0:
        for i in range(vect.size - 1):
            if vect[i] > 0:
                return True
    return False

def calcularSBF(tabla: np.ndarray):
    sbf = []
    canonicos = set()
    casiCanonicos = []
    multiplesSoluciones = False
    # Calcular el vector de solución básico fáctible
    for i in range(tabla.shape[1]-1):
        indiceCanonico = isCanonico(tabla[:,i])
        indiceCasiCanonico = isCanonico(tabla[0:-1,i])
        if indiceCanonico != -1:
            if indiceCanonico in canonicos:
                multiplesSoluciones = True
                sbf.append(0)
            else:
                canonicos.add(indiceCanonico)
                sbf.append(tabla[indiceCanonico,-1])
        elif indiceCasiCanonico != -1:
            casiCanonicos.append([indiceCasiCanonico, i])
            sbf.append(0)
        else:
            # Vectores no básicos
            if checkMultiplesSoluciones(tabla[:,i]):
                multiplesSoluciones = True
            sbf.append(0)
    
    # Checar si hay menos soluciones basicas factibles de lo que hay restricciones
    j = 0
    while len(canonicos) != (tabla.shape[0]-1):
        if j < len(casiCanonicos):
            indiceCasiCanonico = casiCanonicos[j][0]
            columnaCasiCanonico = casiCanonicos[j][1] 
            tabla[-1,:] = tabla[-1,:] - tabla[-1,columnaCasiCanonico]*tabla[indiceCasiCanonico,:]
            canonicos.add(indiceCasiCanonico)
        else:
            print("ERROR GRAVE")
        j += 1
    if j != 0:
        sbf, multiplesSoluciones = calcularSBF(tabla)

    return sbf, multiplesSoluciones


def singleSimplex(tabla: np.ndarray):
    tablasSimplex = [np.array(tabla)]

    # Entra una tabla simplex estandar inicial y sale la tabla simplex final
    costos = tabla[-1,:]
    numReng = tabla.shape[0]
    numCol = tabla.shape[1]
    
    while checkNegativos(costos) != -1:
        # Vemos que el indice de la variable que va a entrar (Siempre entra el más a la izquierda Regla de Bland)
        indVarEntrada = checkNegativos(costos)
        # Determinamos el indice del renglon que va a ser pivote
        indRengPivote = checkRenglonPivote(tabla[:,indVarEntrada], tabla[:,-1])
        
        # Hacemos ese primer 1 pivote
        tabla[indRengPivote,:] = tabla[indRengPivote,:]/tabla[indRengPivote,indVarEntrada]
        
        # La suma de renglones
        for i in range(numReng):
            if i != indRengPivote:
                tabla[i,:] = tabla[i,:] - (tabla[i,indVarEntrada])*tabla[indRengPivote, :]
        tablasSimplex.append(np.array(tabla))
    
    return tablasSimplex

def simplex(tabla: np.ndarray):
    rengCostos = tabla[-1,:]
    numRest = tabla.shape[0]-1
    # Fase 1
    tablaFase1 = np.vstack((tabla[0:-1],np.zeros(tabla.shape[1])))
    for i in range(numRest):
        colH = np.zeros(tabla.shape[0])
        colH[i] = 1
        colH[-1] = 1
        colH = np.array([colH]).T
        tablaFase1 = np.hstack((tablaFase1[:,0:-1],colH, tablaFase1[:,-1:]))
        tablaFase1[-1,:] = tablaFase1[-1,:] - tablaFase1[i,:]
    tablasFase1 = singleSimplex(tablaFase1) # La ultima tabla simplex de la fase 1
    simplexFase1 = tablasFase1[-1]
    ## Checar si existe solución
    for i in range(numRest):
        if isCanonico(simplexFase1[:,-numRest-1+i]) != -1:
            ## No existe solución
            return simplexFase1, None

    # Fase 2
    tablaFase2 = np.hstack((simplexFase1[:,0:-numRest-1], simplexFase1[:,-1:]))
    tablaFase2 = np.vstack((tablaFase2[0:-1,:], rengCostos))
    simplexFinal = singleSimplex(tablaFase2)

    return tablasFase1, simplexFinal



def parseFuncionObjetivo(funcObj: str, vars):
        funcObj = funcObj.replace(" ", "").replace("-x","-1x").replace("+x","+1x").replace("-|x","-|1x").replace("+|x","+|1x")
        
        rengAbs = np.zeros(vars)

        for i in range(0,vars):
            srch = re.search('(\|)(\d+)(x)(' + str(i+1) + ')',funcObj)
            if srch != None:
                rengAbs[i] = 1

        funcObj = funcObj.replace("|","")

        rengObj = np.zeros(vars + 1)

        for i in range(0,vars):
            srch = re.search('(-?\d+)(x)(' + str(i+1) + ')',funcObj)
            if srch != None:
                rengObj[i] = float(srch.group(1))
        
        return rengObj, rengAbs

def parseRestriccion(funcObj: str, vars):
    funcObj = funcObj.replace(" ", "").replace("-x","-1x").replace("+x","+1x").replace("-|x","-|1x").replace("+|x","+|1x")

    op_cons = re.search('(>=|<=|=>|=<|=)(.*)',funcObj)
    op = op_cons.group(1)
    cons = op_cons.group(2)

    funcObj = re.sub('(>=|<=|=>|=<|=)(.*)','',funcObj)

    rengAbs = np.zeros(vars)

    for i in range(0,vars):
        srch = re.search('(\|)(\d+)(x)(' + str(i+1) + ')',funcObj)
        if srch != None:
            rengAbs[i] = 1

    funcObj = funcObj.replace("|","")

    rengRest = np.zeros(vars+2)

    rengRest[vars] = cons

    if op == "=":
        rengRest[vars+1] = 0
    elif op == '>=' or op == '=>':
        rengRest[vars+1] = 1
    elif op == '<=' or op == '=<':
        rengRest[vars+1] = -1

    for i in range(0,vars):
        srch = re.search('(-?\d+)(x)(' + str(i+1) + ')',funcObj)
        if srch != None:
            rengRest[i] = float(srch.group(1))
    
    return rengRest,rengAbs

    