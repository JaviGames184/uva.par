#Javier Ramos Jimeno

#Variables generales
numero_filas = 12
numero_columnas = 10
puntos = 0
Tablero = []

def matrizTablero():
    creador_filas = 0
    contador_filas = 0
    creador_columnas = 0

    while creador_filas < numero_filas:
        Tablero.append([])
        creador_filas += 1
    
    while contador_filas < numero_filas:
        while creador_columnas < numero_columnas:
            Tablero[contador_filas].append(' ')
            creador_columnas += 1
        creador_columnas = 0
        contador_filas += 1

def filasGeneradas(nombre_archivo):
    lista_filas = []

    #Abre el fichero
    with open(nombre_archivo, "r") as fichero:
        for linea in fichero:
            lista_filas.append(linea)
    
    return lista_filas

def creacionSiguienteFila(iteraciones, fichero):
    actual = fichero[iteraciones]
    i = 0

    #Escribe en la matriz la siguiente fila
    while i < numero_columnas:
        if i == numero_columnas-1 and actual[i] != ' ':
            Tablero[0][i] = actual[i] * 2
        elif i == numero_columnas-1 and actual[i] == ' ':
            Tablero[0][i] = actual[i]
        elif (actual[i] == actual[i + 1]):
            Tablero[0][i] = actual[i]
        elif actual[i] == ' ':
            Tablero[0][i] = actual[i]
        else:
            Tablero[0][i] = actual[i] * 2
            
        i += 1

    #Comprueba si la siguiente fila existe
    if (iteraciones + 1) >= len(fichero):
        iteraciones = 0
    else:
        iteraciones += 1

    return iteraciones

def imprimirPantalla():
    Traductor = {"A":"#", "a":"#", "B":"$", "b":"$", " ":" "}
    separador = " "*3 + ("+---"*numero_columnas + "+")

    print(separador)
    i = 0
    j = 0

    while i < numero_filas:
        #Imprime la letra de la fila
        print( " " + chr(65 + i) + " " + "|", end="")

        #Imprime el resto de la fila
        while j < numero_columnas:
            if len(Tablero[i][j]) == 2:
                print(Traductor[Tablero[i][j][0]]*3 + "|", end="")
            elif(Tablero[i][j] == ' '):
                print(Traductor[Tablero[i][j][0]]*3 + "|", end="")

            else:
                print(Traductor[Tablero[i][j]] * 4, end="")

            j += 1
                                
        i +=1
        j = 0
        print("\n" + separador)

    #Imprime los números de las columnas
    numero = 0
    print(" "*5, end="")
    while(numero < numero_columnas):
        print(numero, " "*2, end="")
        numero += 1

    print("\n")

def comprobacionMovimiento(movimiento):
    letra_fila = ""
    columna_numero = ""
    mov = ""
    error_sintaxis = "Error de sintaxis en jugada"
    traductor_movimientos = {'<':-1, '>':1}

    if len(movimiento) != 3:
        print(error_sintaxis)
        return False
    elif movimiento == "---":
        return True
        #No hacer nada
    else:
        #Se comprueban que los valores están dentro del rango
        letra_fila = movimiento[0].upper()
        columna_numero = int(movimiento[1])
        mov = movimiento[2]

        if (columna_numero >= 0) and (columna_numero < numero_columnas):
            if (letra_fila >= chr(65)) and (letra_fila < chr(65 + numero_filas)):
                if (mov == ">") or (mov == "<"):
                    #La jugada introducida es correcta
                    letra_fila = ord(letra_fila) - 65
                    return (realizarMovimiento(letra_fila, columna_numero, traductor_movimientos[mov]))    
                else:
                    print(error_sintaxis)
                    return False
            else:
                print(error_sintaxis)
                return False
        else:
            print(error_sintaxis)
            return False

def realizarMovimiento(num_fila, num_columna, desplazamiento):
    recorrer = desplazamiento
    #Derecha
    ancho_bloque_movimiento_derecha = 0
    cuanto_mover_derecha = 0
    #Izquierda
    ancho_bloque_movimiento_izquierda = 0
    cuanto_mover_izquierda = 0

    #Comprobamos que es un bloque
    if Tablero[num_fila][num_columna] == ' ':
        print("No hay ningún bloque en esa celda")
        return False
    else:
        #Comprobamos que se puede mover en esa dirección
        if ((num_columna + recorrer) < 0) or ((num_columna + recorrer) > (numero_columnas-1)):
            print("El bloque no puede moverse en esa dirección")
            return False

        caracter = Tablero[num_fila][num_columna][0]
        while caracter == Tablero[num_fila][num_columna + recorrer]:
            if recorrer > 0:
                recorrer += 1
            else:
                recorrer -= 1
        
        #Corrección de recorrer a la derecha
        if caracter == Tablero[num_fila][num_columna + recorrer][0] and recorrer > 0:
            recorrer += 1
        
        if Tablero[num_fila][num_columna + recorrer][0] != ' ':
            print("El bloque no puede moverse en esa dirección")
            return False
        else:
            if desplazamiento == 1:
                #Mover el bloque A DERECHA (recorrer = 1)
                while (num_columna + recorrer + cuanto_mover_derecha < numero_columnas) and (Tablero[num_fila][num_columna + recorrer + cuanto_mover_derecha][0] == ' ') :
                    cuanto_mover_derecha += 1
            
                #Calculamos el ancho bloque
                while (num_columna + recorrer - ancho_bloque_movimiento_derecha - 2 >= 0) and (len(Tablero[num_fila][num_columna + recorrer - ancho_bloque_movimiento_derecha - 2]) != 2):
                    ancho_bloque_movimiento_derecha += 1
                ancho_bloque_movimiento_derecha += 1
                    
                #Movemos el bloque
                recorrer -= 1
                while ancho_bloque_movimiento_derecha > 0:
                    Tablero[num_fila][num_columna + recorrer + cuanto_mover_derecha] = Tablero[num_fila][num_columna + recorrer]
                    Tablero[num_fila][num_columna + recorrer] = ' '
                    recorrer -= 1
                    ancho_bloque_movimiento_derecha -= 1

                return True
            
            else:
                #Mover el bloque A IZQUIERDA (recorrer = -1)
                while (num_columna + recorrer + cuanto_mover_izquierda >= 0) and (Tablero[num_fila][num_columna + recorrer + cuanto_mover_izquierda][0] == ' ') :
                    cuanto_mover_izquierda -= 1

                #Calculamos el ancho bloque
                while (num_columna + recorrer + ancho_bloque_movimiento_izquierda + 1 < numero_columnas) and (len(Tablero[num_fila][num_columna + recorrer + ancho_bloque_movimiento_izquierda + 1]) != 2):
                    ancho_bloque_movimiento_izquierda += 1
                ancho_bloque_movimiento_izquierda += 1    
                #Movemos el bloque
                recorrer += 1
                while ancho_bloque_movimiento_izquierda > 0:
                    Tablero[num_fila][num_columna + recorrer + cuanto_mover_izquierda] = Tablero[num_fila][num_columna + recorrer]
                    Tablero[num_fila][num_columna + recorrer] = ' '
                    recorrer += 1
                    ancho_bloque_movimiento_izquierda -= 1
                

                return True
        
def gravedadCompleta():
    recorredor_filas = numero_filas - 2
    recorredor_columnas = 0
    ancho = 0
    salto = False
    bajar = True
    
    #Recorre la matriz
    while recorredor_filas >= 0:
        while recorredor_columnas < numero_columnas :

            #Si el caracter es un espacio continua
            if Tablero[recorredor_filas][recorredor_columnas] != ' ':
                #Calculas la longitud del bloque
                salto = True     
                while (recorredor_columnas + ancho) < numero_columnas:
                    if len(Tablero[recorredor_filas][recorredor_columnas + ancho]) != 2:
                        ancho += 1
                    else:
                        ancho_guardado = ancho
                        break
                
                #Comprobamos si en la fila de abajo se puede colocar
                while ancho >= 0:
                    if Tablero[recorredor_filas + 1][recorredor_columnas + ancho] != ' ':
                        bajar = False
                    ancho -= 1
                
                ancho = ancho_guardado

                #Bajamos el bloque
                if bajar:
                    while ancho >= 0:
                        Tablero[recorredor_filas + 1][recorredor_columnas + ancho] = Tablero[recorredor_filas][recorredor_columnas + ancho]
                        Tablero[recorredor_filas][recorredor_columnas + ancho] = ' '
                        ancho -= 1
            
            #Recolocamos el recorredor de columnas
            if salto:
                recorredor_columnas += ancho_guardado + 1
            else:
                recorredor_columnas += 1                    
                       
            ancho = 0
            ancho_guardado = 0
            salto = False
            bajar = True
            

        recorredor_columnas = 0
        recorredor_filas -= 1    
    
def destructor():
    contador_fila = numero_filas - 1
    contador_columna = 0
    destruir = True
    bucles = 0
    puntos_acumular = 0

    #Fila entera
    fila_igual = True

    while contador_fila > 0:
        caracter = Tablero[contador_fila][contador_columna][0].lower()

        #Comprueba si la fila esta completa
        while contador_columna <= (numero_columnas - 1) and destruir :            
            #No esta completa
            if Tablero[contador_fila][contador_columna] == ' ':                
                destruir = False

            #Comprueba si la fila es del mismo elemento
            if Tablero[contador_fila][contador_columna][0].lower() != caracter or Tablero[contador_fila][contador_columna] == ' ':
                fila_igual = False

            contador_columna += 1
        
        if fila_igual:
            puntos_acumular = destructor_completo()
        elif destruir:
            contador_columna = 0
            #Destruye la fila
            puntos_acumular += numero_columnas
            while contador_columna <= (numero_columnas - 1) :            
                Tablero[contador_fila][contador_columna] = ' '
                contador_columna += 1
            
            #Caen los bloques
            while bucles < (numero_filas * 2):
                gravedadCompleta()
                bucles += 1  
            
            bucles = 0
            contador_fila = numero_filas - 1
            contador_columna = 0
            destruir = True
            fila_igual = True

            
        contador_fila -= 1
        destruir = True
        fila_igual = True
        contador_columna = 0

    return puntos_acumular

def destructor_completo():
    puntos_acumulador_completo = 0
    pasar_filas = numero_filas - 1
    pasar_columnas = 0

    #Recorres la matriz entera colocando espacios y contando los puntos
    while pasar_filas >= 0:
        while pasar_columnas <= (numero_columnas - 1):
            if Tablero[pasar_filas][pasar_columnas][0] != ' ':
                puntos_acumulador_completo += 1
            Tablero[pasar_filas][pasar_columnas] = ' '
            pasar_columnas += 1

        pasar_filas -= 1
        pasar_columnas = 0
    


    return puntos_acumulador_completo

if __name__ == "__main__":
    iteraciones = 0
    Continuar = True
    movimientos = ""
    movimiento_correcto = False
    bucle = 0
    puntos = 0
    fin = False
        
    #Se inicia el juego
    Generacion_Filas = filasGeneradas(str(input("Nombre del fichero de filas: ")))
    matrizTablero()
    

    while Continuar:
        #Coloca la siguiente fila
        iteraciones = creacionSiguienteFila(iteraciones, Generacion_Filas)
        puntos += destructor()
        print("\n1. INSERCION FILA")
        imprimirPantalla()

        #Imprime los puntos actuales
        print("Puntuación: " + str(puntos))

        #Movimientos a realizar
        while (not movimiento_correcto):
            movimientos = str(input("Introduzca jugada o --- o FIN: "))
            if movimientos.lower() == "fin":
                #Termina el programa
                Continuar = False
                fin = True
                movimiento_correcto = True
            else:
                movimiento_correcto = comprobacionMovimiento(movimientos)

        if Continuar:
            print("\n2. MOVIMIENTO")
            movimiento_correcto = False
            imprimirPantalla()

            #Baja la fila
            while bucle < (numero_filas * 2):
                gravedadCompleta()
                bucle += 1  

            print("3. CAÍDA")
            imprimirPantalla()

            #Se comprueba si se tienen que destruir bloques
            bucle = 0
            while bucle < (numero_filas * 2):
                puntos += destructor()
                bucle += 1  
            

            print("4. ELIMINACIÓN")
            imprimirPantalla()
        
            #Comprueba si tiene que finalizar
            bucle = 0
            for i in Tablero[0]:
                if i != ' ':
                    Continuar = False

    
    #Finaliza el juego
    if not fin:
        print("\nEl juego ha finalizado")
        
    print("\nPuntuación Total: " + str(puntos))