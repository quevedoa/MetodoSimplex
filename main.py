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