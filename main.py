import funciones as f
import numpy as np

if __name__ == "__main__":
    # matNEst = np.array([[1,2,10,-1],[1,2,5,-1],[1,-1,2,-1]])
    # costNEst = np.array([[2,-1,0]])
    # nomVar = ["x1","x2"]

    #print(costNEst)
    # mat = estandarizar(matNEst, costNEst, False, nomVar)[0]
    # print(mat)

    # mat = np.array([[1,2,1,0,0,10],[1,2,0,1,0,5],[1,-1,0,0,1,2]]).astype(float)
    # funcionObjetivo = input("Porfavor ingrese la función objetivo: ")
    # rengCostos = f.parseFuncionObjetivo(funcionObjetivo)
    # print(rengCostos)
    # mat = np.vstack((mat, rengCostos))
    # #mat2 = np.vstack((mat[0:2], arr1, mat[2:,:])) # Insertar un renglon


    # res = f.simplex(mat)
    # for i in range(len(res)):
    #     print(res[i])
    #     print()
    
    # min_max = input("min o max").lower()
    
    # cantRestricciones = int(input("Cuantas restricciones desea ingresar: "))
    # for i in range(cantRestricciones):
    #     print("YEHYEH")

    ##############################
    # ##########Final#############
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

    matRestricciones = np.array([[1,1,8,-1],[-1,1,4,-1],[1,0,6,-1]]).astype(float)
    rengCostos = np.array([[1,3,0]])
    isMin = False

    matSimplex, nomVars = f.estandarizar(matRestricciones,rengCostos, isMin)

    tablasFase1, tablasFase2 = f.simplex(matSimplex)
    
    # Logica para enseñar especificamente que variable es que
    if tablasFase2 == None:
        print("Tablas Fase 1:")
        for t in tablasFase1:
            print(t)
        print("No solushon")
    else:
        sbf = []
        tablaFinal = tablasFase2[-1]
        # Calcular el vector de solución básico fáctible
        for i in range(tablaFinal.shape[1]-1):
            indiceCanonico = f.isCanonico(tablaFinal[:,i])
            indiceCanonicoSCostos = f.isCanonico(tablaFinal[0:-1,i])
            if indiceCanonico != -1:
                sbf.append(tablaFinal[indiceCanonico,-1])
            elif indiceCanonicoSCostos != -1:
                tablaFinal[-1,:] = tablaFinal[-1,:] - tablaFinal[-1,i]*tablaFinal[indiceCanonicoSCostos,:]
                sbf.append(tablaFinal[indiceCanonicoSCostos,-1])
            else:
                sbf.append(0)

        # Imprimir resultado
        print("Tablas Fase 1:")
        for t in tablasFase1:
            print(t)
        print("Tablas Fase 2:")
        for t in tablasFase2:
            print(t)
        print("Soluciones")
        print("La solución básica factible es:")
        print(nomVars)
        print(sbf)