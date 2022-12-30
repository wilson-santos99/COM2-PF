
###################################################################################3333333333333333333333
def cifrado_cesar (plaintext, clave):   #funcion cuyo argumento es el texto que se ingresara por consolda 
    #posicion1 = int(input(("Ingrese la llave>>: "))) #solicita el numero de posiciones que se movera hacia la derecha
    alfabeto_min = "abcdefghijklmnopqrstuvwxyz"  #creamos variable con alfabetro en minusculas
    alfabeto_may = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" #creamos variable con alfabeto en mayusculas
    longitud_alfabeto = len(alfabeto_min) #determinamos la longitud de la variable alfabeto
    texto_cifrado_cesar= ""  #variable que almacenara el mensaje cifrado, se hace la iteracion sobre cada letra del "mensaje"
    for letra in plaintext:  #inicia una variable letra que ira recorriendo cada caracter del texto  #casa 
        if not letra.isalpha() or letra.lower() == 'ñ':  #si el texto contiene una letra ñ el codigo lo deja tal y como esta
            texto_cifrado_cesar+= letra  #la variable texto_cifradoalmacenara cada letra y las concatenara
            continue  #continua el proceso a la siguiente linea
        valor_letra = ord(letra)  #recibe un carácter y devuelve su representación en código unicode
        alfabeto_a_usar = alfabeto_min  #si el texto es minuscula utilizara el alfabeto en minuscula
        limite = 97   #limite unicode minuscula     
        if letra.isupper():     #si la letra es mayuscula
            limite = 65 #limiite unicode mayuscula
            alfabeto_a_usar = alfabeto_may #utilizara el alfabeto mayuscula
        posicion = (valor_letra - limite + clave) % longitud_alfabeto   #posicioin que movemos a la derecha
        texto_cifrado_cesar+= alfabeto_a_usar[posicion]  #regresa los valores a letras y las concatena
    return texto_cifrado_cesar #devuelve la variable codificado_cesar

def descifrado_cesar(texto_cifrado_cesar, clave):
    print('Texto Cifrado recibido : '+str(texto_cifrado_cesar))
   # if texto_cifrado[-1] =='c':
    texto_descifrado_cesar = "" #variable que almacenara el mensaje descifrado
    #posicion1 = int(input(("Ingrese la llave>>: "))) #solicita el numero de posiciones que se movio a la derecha el texto original
    alfabeto_min = "abcdefghijklmnopqrstuvwxyz" #creamos variable con alfabetro en minusculas
    alfabeto_may = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" #creamos variable con alfabetro en minusculas
    longitud_alfabeto = len(alfabeto_min) #determinamos la longitud de la variable alfabeto

    for letra in texto_cifrado_cesar : #inicia una variable letra que ira recorriendo cada caracter del texto 
        if not letra.isalpha() or letra.lower() == 'ñ':  #si el texto contiene una letra ñ el codigo lo deja tal y como esta
            texto_descifrado_cesar += letra #la variable texto_cifrado  almacenara cada letra y las concatenara
            continue #continua el proceso a la siguiente linea
        valor_letra = ord(letra)  #recibe un carácter y devuelve su representación en código unicode
        alfabeto_a_usar = alfabeto_min   #si el texto es minuscula utilizara el alfabeto en minuscula
        limite = 97   #limite unicode minuscula 
        if letra.isupper():   #si la letra es mayuscula
            limite = 65  #limiite unicode mayuscula
            alfabeto_a_usar = alfabeto_may #utilizara el alfabeto mayuscula
        posicion = (valor_letra - limite +26-clave) % longitud_alfabeto #uso el complemento de 26-posicion
        texto_descifrado_cesar  += alfabeto_a_usar[posicion]  #regresa los valores a letras y las concatena
        #texto_descifrados_cesar=texto_descifrado_cesar[:-1]
    return texto_descifrado_cesar #devuelve el texto cifrado en la variable decod_cesar
