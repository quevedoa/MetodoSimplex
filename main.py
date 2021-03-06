import funciones as f
import numpy as np
import re

if __name__ == "__main__":

    ### FINAL ###

    def inputter():
        print("-----------------------------------------------------------------------------------------------------------")
        vars = int(input("Ingresa la cantidad de variables: "))
        minOMax = input("¿Es min o max?: ")
        if minOMax.lower() == "min":
            isMin = True
        else:
            isMin = False

        fun_obj = input("Ingresa la función objetivo: ")
        objetivo, absObj = f.parseFuncionObjetivo(fun_obj,vars)

        rest = int(input("¿Cuántas restricciones de más de una variable tienes?: "))

        restricciones = np.empty((rest,vars+2))
        absRest = np.empty((rest,vars))

        for i in range(0,rest):
            str_rest = input("Ingresa la restricción " + str(i+1) + ": ")
            restricciones[i], absRest[i] = f.parseRestriccion(str_rest,vars)
        
        return objetivo, restricciones, isMin

    menu = (
        "-----------------------------------------------------------------------------------------------------------" + 
        "\n-------------------------------------------------Menu------------------------------------------------------" + 
        "\n-----------------------------------------------------------------------------------------------------------" +
        "\nIngresa: start - para ingresar un problema de PL nuevo y resolver." +
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

        resp=input("Ingresa una opción válida: ") 

        if resp=="start":
            rengCostos, matRestricciones, isMin = inputter()
            
            matSimplex, nomVars = f.estandarizar(matRestricciones,rengCostos, isMin)
            tablasFase1, tablasFase2 = f.simplex(matSimplex)

            # Logica para enseñar especificamente que variable es que
            if np.any(tablasFase1) == None and np.any(tablasFase2) == None:
                ## Problema no acotado
                print()
                print("-----------------------------------------------------------------------------------------------------------")
                print("No acotado - No existe solución óptima")
            elif tablasFase2 == None:
                for t in tablasFase1:
                    print(t)
                print()
                print("-----------------------------------------------------------------------------------------------------------")
                print("No pasó la fase 1 - No existe solución óptima")
            else:
                tablaFinal = tablasFase2[-1]
                multSol = "Existe una solución única\nLa solución óptima es:"
                msgCosto = "El valor de la función objetivo es:"

                # Calcular el vector de solución básico fáctible
                sbf, multSolFase2 = f.calcularSBF(tablaFinal)
                if multSolFase2 == True:
                    multSol = "Existen soluciones múltiples\nUna posible solución es:" 

                # Imprimir resultado
                print("-----------------------------------------------------------------------------------------------------------")
                print("\nUtilizando el método de las dos fases...")
                print("\n\nTABLAS FASE 1:")
                for t in tablasFase1:
                    print(t)
                    print("\n")
                print("-----------------------------------------------------------------------------------------------------------")
                print("\nTABLAS FASE 2:")
                for t in tablasFase2:
                    print(t)
                    print("\n")

                print("-----------------------------------------------------------------------------------------------------------")
                print("\nSOLUCIONES:")
                print(multSol)
                print(sbf)
                print()
                print(msgCosto)
                print((tablaFinal[-1,-1])*(-1))
                print()
                
        elif resp=="quit":
            run = False
        else:
            print("\n" + "'" + resp + "' no es una opción válida. Intenta de nuevo.")

    ## PROBLEMAS DE PRUEBA ##
    # matRestricciones = np.array([[15,5,300,-1],[10,6,240,-1],[8,12,450,-1]]).astype(float)
    # rengCostos = np.array([[500,300,0]])
    # isMin = False