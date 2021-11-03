import funciones as f
import numpy as np

if __name__ == "__main__":

    ### FINAL ###

    ## POSIBLE LOGICA INPUT ##
    # print("Hola q me 123")
    # minOMax = input("min o max").lower()
    # isMin = True if minOMax == "min" else False

    # funcionObjetivo = input("Porfavor ingrese la función objetivo para", minOMax)
    # rengCostos = f.parseFuncionObjetivo(funcionObjetivo)
    # nomVars = []
    # for i in range(len(rengCostos)-1):
    #     nomVars.append("x" + str(i+1))

    # numRest = input("¿Cuántas restricciones desea ingresar?")
    # numCol = rengCostos.size
    # matRestricciones = np.array(np.zeros(numCol))
    # for i in range(numRest):
    #     currRest = input("Ingrese la restricción", i+1)
    #     rengRest = f.parseRestriccion(currRest)
    #     matRestricciones = np.vstack((matRestricciones,rengRest))

    import re
    import numpy as np

    def parseFuncionObjetivo(funcObj: str,vars):
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
        
        return np.array(rengObj,rengAbs)

    def parseRestriccion(funcObj: str, vars):
        funcObj = funcObj.replace(" ", "").replace("-x","-1x").replace("+x","+1x").replace("-|x","-|1x").replace("+|x","+|1x")
        print(funcObj)

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
        
        return np.array(rengRest,rengAbs)

    def inputter():
        print("------------------------------------------------------------------------")
        vars = input("Ingresa la cantidad de variables:")

        fun_obj = input("Ingresa la función objetivo:")
        objetivo = parseFuncionObjetivo(fun_obj,vars)

        rest = input("¿Cuántas restricciones de más de un variable tienes?")

        restricciones = []

        for i in range(0,rest):
            str_rest = input("Ingresa la restricción " + str(i+1) + ":")
            restricciones.append(parseRestriccion(str_rest,vars))

        

        for i in rest:


    import time

    menu = (
        "-----------------------------------------------------------------------------------------------------------" + 
        "\n-----------------------------Menu--------------------------------------------------------------------------" + 
        "\n-----------------------------------------------------------------------------------------------------------" +
        "\nIngresa: start - para ingresar un problema de PL nuevo y resolver." +
        "\n         restart - para comenzar de nuevo el ingreso de un problema PL." +
        "\n         quit - para salir del programa en cualquier punto." +
        "\n-----------------------------------------------------------------------------------------------------------") 

    run = True                                                                                                                               

    print(
        "-----------------------------------------------------------------------------------------------------------" +
        "\n-----------------------------------------------------------------------------------------------------------" +
        "\n _______ _______ _______  _____  ______   _____       _______ _____ _______  _____         _______ _     _" + 
        "\n |  |  | |______    |    |     | |     \ |     |      |______   |   |  |  | |_____] |      |______  \___/ " +
        "\n |  |  | |______    |    |_____| |_____/ |_____|      ______| __|__ |  |  | |       |_____ |______ _/   \_" +
        "\n-----------------------------------------------------------------------------------------------------------" + 
        "\nHecho por: Andres Quevedo, Aranzazu Natividad, Fernanda Hinze, Regina Garcia y Mariano Franco.")


    while run:
        print(menu)

        resp=input("Ingresa una opción válida:") 

        time.sleep(5)

        if resp=="start":
        inputter()
        elif resp=="restart":
        print("yes")
        elif resp=="quit":
            run = False
        else:
            print("\n" + "'" + resp + "' no es una opción válida. Intenta de nuevo.")






    ## PROBLEMAS DE PRUEBA ##
    # A
    # matRestricciones = np.array([[1,0,0,0,1,-1],[20,1,0,0,100,-1],[200,20,1,0,10000,-1],[2000,200,20,1,1000000,-1]]).astype(float)
    # rengCostos = np.array([[1000,100,10,1,0]])
    # isMin = False

    # B
    # matRestricciones = np.array([[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,4,0],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,2,1]]).astype(float)
    # rengCostos = np.array([[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,-1,0]])
    # isMin = True

    # C
    # matRestricciones = np.array([[1,1,-1,0,0,2,1],[-2,-1,0,-1,1,1,1],[1,1,2,3,0,10,-1],[1,2,-1,2,0,6,-1],[0,1,0,2,0,5,1]]).astype(float)
    # rengCostos = np.array([[8,-2,1,2,5,0]])
    # isMin = True

    # D
    matRestricciones = np.array([[15,5,300,-1],[10,6,240,-1],[8,12,450,-1]]).astype(float)
    rengCostos = np.array([[500,300,0]])
    isMin = False

    # Estandarizar y calcular el simplex
    matSimplex, nomVars = f.estandarizar(matRestricciones,rengCostos, isMin)
    tablasFase1, tablasFase2 = f.simplex(matSimplex)
    
    # Logica para enseñar especificamente que variable es que
    if tablasFase2 == None:
        print("TABLAS FASE 1:")
        for t in tablasFase1:
            print(t)
        print("No acotado - No existe solución óptima")
    else:
        tablaFinal = tablasFase2[-1]
        multSol = "Existe una Solución Única\nLa solución óptima es:"

        # Calcular el vector de solución básico fáctible
        sbf, multSolFase2 = f.calcularSBF(tablaFinal)
        if multSolFase2 == True:
            multSol = "Existen Soluciones Múltiples\nUna posible solución es:" 

        # Imprimir resultado
        print("------------------------------------")
        print("\nTABLAS FASE 1:")
        for t in tablasFase1:
            print(t)
        print("------------------------------------")
        print("\nTABLAS FASE 2:")
        for t in tablasFase2:
            print(t)

        print("------------------------------------")
        print("\nSOLUCIONES")
        print(multSol)
        print(sbf)