import numpy as np
from sympy import Matrix

diccionario_encryt = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11,
            'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25,
            '0':26, '1': 27, '2':28, '3':29, '4':30, '5':31, '6':32, '7':33, '8':34, '9':35, '.': 36, ',': 37, ':': 38, '?': 39 , ' ': 40}

#Creamos un diccionario para almacenar nuestro alfabeto,  numeros y simbolos de forma ordenada
diccionario_decrypt = {'0' : 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E', '5': 'F', '6': 'G', '7': 'H', '8': 'I', '9': 'J', '10': 'K', '11': 'L', '12': 'M',
            '13': 'N', '14': 'O', '15': 'P', '16': 'Q', '17': 'R', '18': 'S', '19': 'T', '20': 'U', '21': 'V', '22': 'W', '23': 'X', '24': 'Y', '25': 'Z', '26': '0',
            '27': '1', '28': '2', '29': '3', '30': '4', '31': '5', '32' : '6', '33' : '7', '34' : '8', '35' : '9', '36' : '.', '37' : ',', '38' : ':', '39' : '?',
             '40' : ' '}
def cifradohill(message, key):
    ciphertext = ''
    matrix_mensaje = []
    list_temp = []
    cifrado_final = ''
    ciphertext_temp = ''
    cont = 0
    message = message.upper()  # Convertir el mensaje a mayusculas
    if len(message) <= len(key):# Si el tamaño del mensaje es menor o igual al tamaño de la clave
        # Convertir el tamaño del mensaje al tamaño de la clave, si no es igual, se añaden 'X' hasta que sean iguales los tamaños.
        while len(message) < len(key):#len(key), nos da como resultado la cantidad de filas que existen en "key"
            message = message + 'X'#se le concatena una 'X' a lo que tiene almacenado "message"
        for i in range(0, len(message)): # Crear la matriz para el mensaje
            matrix_mensaje.append(diccionario_encryt[message[i]])#se agrega a la lista "matrix_mensaje" cada numero que corresponderia
            #a cada letra que esta en "message"
        matrix_mensaje = np.array(matrix_mensaje)# Se crea la matriz
        cifrado = np.matmul(key, matrix_mensaje)# Se multiplica la matriz clave por la de mensaje
        cifrado = cifrado % 41# el valor de modulo se obtiene de la cantidad de valores del diccionario, y se saca el modulo para cada celda de "cifrado"
        # Se codifica de valores numericos a los del diccionario, añadiendo a ciphertext el valor en el diccionario pasandole como indice la i posicion de la variable cifrado
        for i in range(0, len(cifrado)):
            ciphertext += diccionario_decrypt[str(cifrado[i])]
    else:
    # Si el tamaño del mensaje es menor o igual al tamaño de la clave
        # Si al dividir en trozos del tamaño de la clave, existe algun trozo que tiene menos caracteres que la long. de la clave se añaden tantas 'X' como falten
        while len(message) % len(key) != 0:
            message = message + 'X'
        # Se troce el mensaje en subsstrings de tamaño len(key) y se alamcenan como valores de un array
        matrix_mensaje = [message[i:i + len(key)] for i in range(0,
                          len(message), len(key))]
        # Para cada valor del array (grupo de caracteres de la longitud de la clave)
        for bloque in matrix_mensaje:
            # Crear la matriz para el bloque
            for i in range(0, len(bloque)):
                list_temp.append(diccionario_encryt[bloque[i]])
            # Se crea la matriz de ese bloque
            matrix_encrypt = np.array(list_temp)
            # Se multiplica la matriz clave por la del bloque
            cifrado = np.matmul(key, matrix_encrypt)
            # Se obtiene el modulo sobre el diccionario de cada celda
            cifrado = cifrado % 41
            # Se codifica de valores numericos a los del diccionario, añadiendo a ciphertext el valor en el diccionario pasandole como indice la i posicion de la variable cifrado
            for i in range(0, len(cifrado)):
                ciphertext_temp += diccionario_decrypt[str(cifrado[i])]
            # Se inicializan las variables para el nuevo bloque
            matrix_encrypt = []
            list_temp = []
        # Se añade el mensaje encriptado a la variable que contiene el mensaje encriptado completo
        ciphertext = ciphertext_temp
    #--------------------------------
    return ciphertext
###################################################################################################################
def descifrado_hill(message, key):#definimos esta funcion con dos argumentos, el mensaje y la llave cuadrada
    print('hay un ser extraño..::::',message)
    plaintext = '' #se utilizara para almacenar el mensaje decodificado

    matrix_mensaje = [] #se utilizara para aplicar la clave al mensaje cifrado
    plaintext_temp = ''
    list_temp = []
    matrix_inversa = []
    matrix_mensaje = [message[i:i + len(key)] for i in range(0,len(message), len(key))]#se utilizara para aplicar la clave inversa a cada bloque del mensaje cifrado y decodificado.
    # Se calcula la matriz inversa aplicando el modulo 41 a cada elemento de la matriz resultante.
    matrix_inversa = Matrix(key).inv_mod(41)#calcula la matriz inversa de la clave utilizando la clase "matrix" del modulo "numpy"
    matrix_inversa = np.array(matrix_inversa)# convierte la matriz inversa calculada en una matriz "numpy", ya que con ella se puede calcular
    #mas facilmente, multiplicaciones de matrices, aplicacion de modulo a los elementos de la matriz.
    matrix_inversa = matrix_inversa.astype(float)#convierte los elementos  de la matriz inversa en numeros de punto flotante.
    for bloque in matrix_mensaje:
        # Se encripta el mensaje encriptado
        for i in range(0, len(bloque)): #se hace la iteracion por la longitud del bloque del mensaje cifrado.
            list_temp.append(diccionario_encryt[bloque[i]])#se convierten los caracteres del bloque del mensaje cifrado en numeros utilizando 
            #el "diccionario_encryt"

        matrix_encrypt = np.array(list_temp)#convierte la lista de numeros que representan a los caracters del bloque en una matriz de "numpy"

        cifrado = np.matmul(matrix_inversa, matrix_encrypt)#se multiplican la matriz inversa y la matriz del bloque del mensaje cifrado,
        #la matriz resultante se guarda en "cifrado"

        cifrado = np.remainder(cifrado, 41).flatten()# Se le aplica a cada elemento de la matriz el modulo 41
   # Se desencripta el mensaje
        for i in range(0, len(cifrado)):
            plaintext_temp += diccionario_decrypt[str(int(cifrado[i]))]#se convierten los numeros del bloque decodificado en caracteres utilizando
            #el diccionario "diccionario_decrypt"

        matrix_encrypt = []#se utiliza para llevar la "matriz_encrypt" a su estado inicial vacio
        list_temp = []#se utiliza para llevar la "list_temp" a su estado inicial vacio
    plaintext = plaintext_temp #asignamos el valor de la variable "plaintext_temp" a "plaintext"

    # Se eleminan las X procedentes de su addicion en la encriptacion para tener bloques del tamaño de la clave

    while plaintext[-1] == 'X': #se compara si el ultimo valor de "plaintext" es una "X"
        plaintext = plaintext.rstrip(plaintext[-1]) #con "rstrip" eliminamos un caracter especifico de la derecha de una cadena de texto,
        #en este caso esta eliminando el ultimo caracter de la cadena de texto almacenada en "plaintext",  estas "X" que queremos eliminar son 
        #las que se agregan al final del mensaje del cifrado para completar los bloques hasta el tamaño de la clave

    return plaintext #retorna lo que este almacenado en "plaintext", lo cual es el mensaje decodificado.

#------------Mensaje recibido----------------#
# clave = [[13, 17], [10, 16]]
# entrada=input("Cifrar(1) o Descifrar (2)\n")
# if entrada=='1':
#     texto=input('INGRESE EL TEXTO A CIFRAR \n')
#     texticifrado=cifradohill(texto,clave)
#     print("el texto cifrado es: "+texticifrado)

# elif entrada=='2':
#     texto=input('INGRESE EL TEXTO A DESCIFRAR \n')
#     textodes=descifrado_hill(texto,clave)
#     print("El texto descifrado es: "+textodes)

