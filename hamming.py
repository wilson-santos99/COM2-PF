import conversiones
from operator import xor
    ###############################################################CODIGO HAMMING

def xor_5(num1,num2,num3,num4,num5):
    #la funcion toma 5 numeros como argumentos
    a = xor(num1,num2)#evalua la funcion xor entre num1 y num2
    b = xor(a,num3)   #evalua la funcion xor entre el valor almacenado en a y num3
    c = xor(b,num4)   #evalua la funcion xor entre el valor almacenado en b y num4
    d = xor(c,num5)   #evalua la funcion xor entre el valor almacenado en d y num5
    return (d)
    #Operacion XOR para numeros binarios, Devuelve el resultado de aplicar el operador XOR (o exclusiva) a estos numeros en secuencia. 
    #devovera un 1 si los valores de entrada son diferentes y un 0 si son iguales.

def xor_3(num1,num2,num3): #la funcion toma 3 numeros como argumentos
    a = xor(num1,num2)     #evalua la funcion xor entre num1 y num2
    b = xor(a,num3)        #evalua la funcion xor entre el valor almacenado en a y num3
    return (b)
    #esta funcion realiza lo mismo que la anterior mencionada, pero ahora solo con 3 argumentos.
def hamming(mensaje_a_codificar): #Esta función se llama "hamming" y recibe como parámetro un mensaje que se desea codificar
    arreglo = list(mensaje_a_codificar) #convierte el mensaje en una lista de caracteres.
    letra_a_binario = [conversiones.ascii_a_binario(num) for num in arreglo] # convierte cada caracter en su representación binaria mediante una función llamada "ascii_a_binario". Esta representación se almacena en "letra_a_binario".
    for index, value in enumerate(letra_a_binario): # Ciclo para extraer el valor del caracter en binario      
        l = str(value) # convierte el valor binario a una cadena de caracteres.
        letra = l[1:] #  reemplaza el valor original de la lista "letra_a_binario" con la cadena de caracteres.
        letra_a_binario[index] = letra # Las líneas 106-113 asignan cada uno de los bits de la cadena a una variable d1 a d7.
        d1 = int(letra[0]) 
        d2 = int(letra[1])
        d3 = int(letra[2])
        d4 = int(letra[3])
        d5 = int(letra[4])
        d6 = int(letra[5])
        d7 = int(letra[6])
        p1 = xor_5(d1,d2,d4,d5,d7) # Las líneas 114 y 115 calculan dos valores de paridad mediante una función llamada "xor_5".
        p2 = xor_5(d1,d3,d4,d6,d7) 
        p3 = xor_3(d2,d3,d4) # Las líneas 116 y 117 calculan otros dos valores de paridad mediante una función llamada "xor_3".
        p4 = xor_3(d5,d6,d7)
        letraH = str(p1)+str(p2)+str(d1)+str(p3)+str(d2)+str(d3)+str(d4)+str(p4)+str(d5)+str(d6)+str(d7) 
        #  concatena todos los bits y valores de paridad en el orden correcto para formar una palabra de 11 bits codificada mediante el código de Hamming.
        letra_a_binario[index] = letraH #  reemplaza el valor original de la lista "letra_a_binario" con la palabra codificada.
    return (letra_a_binario) # devuelve la lista "letra_a_binario" que contiene las palabras codificadas de cada caracter del mensaje original.
