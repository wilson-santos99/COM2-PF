separador = " "  
def ascii_a_binario(letra):
    #Llamaremos a esta funcion "ascii_a_binario", 
    valor = ord(letra)
    #print('el valor ascii es:   '+str(valor)) #Esta variable valor se encarga de almacenar el valor ASCII, de la letra anterior como argumento.
    numero_bin="{0:08b}".format(valor)
    #print('el numero binario de cada letra es:  '+numero_bin)
    return "{0:08b}".format(valor)
    #se usa la funcion "format", convierte el valor ASCII anterior a una cadena de 8 digitos en formato binario, y
    # finalmente devuelve esa cadena. 


def binario_a_ascii(binario):
    # Esta funcion tomara una cadena de digitos binarios como entrada.
    valor = int(binario, 2)
    #el "2" es la base del tipo de valor que esta recibiendo, como es binario entonces colocamos 2, el int convertira lo binario en un entero.
    #ese entero es el que se guardara en la variable valor
    return chr(valor)
    #Se encarga de convertir el entero en su caracter ASCII correspondiente.

def texto_a_binario(texto):
    texto_binario = ""  # El resultado
    contador = 0
    for letra in texto:
        texto_binario += ascii_a_binario(letra)
        # Agregar un espacio entre binarios, excepto si es el último carácter
        if contador + 1 < len(texto):
            texto_binario += separador
        contador += 1
    return texto_binario
#convierte una cadena de texto dad en una cadena binaria, lo hace iterando sobre cada caracter en el texto de entrada, convirtiendolo a binario
#utilizando la funcion "ascii_a_binario()" y agregandoloa la cadena binaria. tambien agrega un separador entre cada caracter, a menos que sea
#el ultimo caracter en el texto de entrada.


def binario_a_texto(texto_binario):
    texto_plano = ""
    for binario in texto_binario.split(separador):
        #se hace una iteracion sobre una cadena de texto que contiene valores binarios, separados por el caracter especificado 
        #en la variable "separador", la variable binario, se utiliza para almacenar cada uno de los valores binarios mientras se recorre la
        #cadena de texto.
        texto_plano += binario_a_ascii(binario)
        #para cada valor binario que se recorre anteriormente la funcion "binario_a_ascii" se encarga de convertir cada cadena de texto binario
        #a un caracter ASCII., almacenandolo en texto_plano
    return texto_plano
    #devuelve el texto ya en formato plano

def binario_a_decimal(binario):
    #la funcion recibe una cadena de texto que representa un numero binario
    posicion = 0
    decimal = 0
    binario = binario[::-1]
    #se invierte la cadena de digitos para recorrer los digitos del numero binario en el orden correcto, del menos signficativo hasta el 
    #mas significativo
    for digito in binario:
        # Elevar 2 a la posición actual en el numero binario
        multiplicador = 2**posicion
        decimal += int(digito) * multiplicador
        #mutiplica el digito actual por el valor calculado y almacenado en multiplicador., almacenandolo en la variable "decimal"
        posicion += 1 
        #incrementa la posicon en 1 para prepararse para la siguiente iteracion
    return decimal
    #una vez el bucle for completado, se devuelve el valor decimal final.

def decimal_a_binario(decimal):
    if decimal <= 0:
        return "0"
    # Aquí almacenamos el resultado
    binario = ""
    # Mientras se pueda dividir...
    while decimal > 0:
        # Saber si es 1 o 0
        residuo = int(decimal % 2)
        # E ir dividiendo el decimal
        decimal = int(decimal / 2)
        # Ir agregando el número (1 o 0) a la izquierda del resultado
        binario = str(residuo) + binario
    return binario
    #Esta funcion hara el trabajo de convertir un numero decimal a su representacion en binario. La funcion toma un numero decimal como 
    #argumento y devuelve una cadena de texto que representa el numero en binario.

