import random
##########################################CIFRADO  Y DeSCIFRADO PROPIO
def cifradopropio (txt): # cadena de texto a cifrar
    tipcifra = random.randint(0,2) # seleccion de numero aleatorio para tipo de cifrado
    print("")
    if tipcifra  == 0: # si tipcifra es igual a 0 se utiliza este cifrado
        txt= txt.replace("m","0") # Reemplaza la letra "m" por el número 0
        txt= txt.replace("u","1") # Reemplaza la letra "u" por el número 1
        txt= txt.replace("r","2") # Reemplaza la letra "r" por el número 2
        txt= txt.replace("c","3") # Reemplaza la letra "c" por el número 3
        txt= txt.replace("i","4") # Reemplaza la letra "i" por el número 4
        txt= txt.replace("e","5") # Reemplaza la letra "e" por el número 5
        txt= txt.replace("l","6") # Reemplaza la letra "l" por el número 6
        txt= txt.replace("a","7") # Reemplaza la letra "a" por el número 7
        txt= txt.replace("g","8") # Reemplaza la letra "g" por el número 8
        txt= txt.replace("o","9") # Reemplaza la letra "o" por el número 9

    if tipcifra  == 1: # si tipcifra es igual a 1 se utiliza este cifrado
        txt= txt.replace("n","0") # Reemplaza la letra "n" por el número 0
        txt= txt.replace("e","1") # Reemplaza la letra "e" por el número 1
        txt= txt.replace("u","2") # Reemplaza la letra "u" por el número 2
        txt= txt.replace("m","3") # Reemplaza la letra "m" por el número 3
        txt= txt.replace("a","4") # Reemplaza la letra "a" por el número 4
        txt= txt.replace("t","5") # Reemplaza la letra "t" por el número 5
        txt= txt.replace("i","6") # Reemplaza la letra "i" por el número 6
        txt= txt.replace("c","7") # Reemplaza la letra "c" por el número 7
        txt= txt.replace("o","8") # Reemplaza la letra "o" por el número 8
        txt= txt.replace("s","9") # Reemplaza la letra "s" por el número 9

    if tipcifra  == 2: # si tipcifra es igual a 2 se utiliza este cifrado
        txt= txt.replace("e","0") # Reemplaza la letra "e" por el número 0
        txt= txt.replace("u","1") # Reemplaza la letra "u" por el número 1
        txt= txt.replace("c","2") # Reemplaza la letra "c" por el número 2
        txt= txt.replace("a","3") # Reemplaza la letra "a" por el número 3
        txt= txt.replace("l","4") # Reemplaza la letra "l" por el número 4
        txt= txt.replace("i","5") # Reemplaza la letra "i" por el número 5
        txt= txt.replace("p","6") # Reemplaza la letra "p" por el número 6
        txt= txt.replace("t","7") # Reemplaza la letra "t" por el número 7
        txt= txt.replace("o","8") # Reemplaza la letra "o" por el número 8
        txt= txt.replace("s","9") # Reemplaza la letra "s" por el número 9
    msg = txt+str(tipcifra) #  concatena el valor de la variable tipcifra a la cadena de texto cifrada
    return (msg)

def descifrado_propio(txt):
    #la funcion "descifrado_propio" recibe una cadena de texto "txt"
	#print(txt)
    print('mensaje cifrado recibido: '+str(txt))
    ultcar = txt[-1]
    #la variable "ultcar" hace referencia a "ultimo caracter". ya que txt[-1], nos guardara el ultimo caracter de la cadena txt, en "ultcar"
    #como en este cifrado propio al final del txt es donde se tiene pensado incluir la llave para el cifrado, es completamente necesario guardar
    # ese ultimo caracter que viene incluido en el mensaje txt.
    if ultcar == '0': #si el ultimo caracter es igual a cero, me aplicara esta llave
        txt= txt.replace("0","m") #le asigna a la m el valor cero
        txt= txt.replace("1","u") #le asigna a la u el valor 1
        txt= txt.replace("2","r") #le asigna a la r el valor 2
        txt= txt.replace("3","c") #le asigna a la c el valor 3
        txt= txt.replace("4","i") #le asigna a la i el valor 4
        txt= txt.replace("5","e") #le asigna a la e el valor 5
        txt= txt.replace("6","l") #le asigna a la l el valor 6
        txt= txt.replace("7","a") #le asigna a la a el valor 7
        txt= txt.replace("8","g") #le asigna a la g el valor 8
        txt= txt.replace("9","o") #le asigna a la o el valor 9
    #llave "murcielago" con su respectivo digito que correspondera a cada caracter
    if ultcar == '1':#si el ultimo caracter es igual a uno, me aplicara esta llave
        txt= txt.replace("0","n") #le asigna a la n el valor cero
        txt= txt.replace("1","e") #le asigna a la e el valor uno
        txt= txt.replace("2","u") #le asigna a la u el valor dos
        txt= txt.replace("3","m") #le asigna a la m el valor tres
        txt= txt.replace("4","a") #le asigna a la a el valor cuatro
        txt= txt.replace("5","t") #le asigna a la t el valor cinco
        txt= txt.replace("6","i") #le asigna a la i el valor seis
        txt= txt.replace("7","c") #le asigna a la c el valor siete
        txt= txt.replace("8","o") #le asigna a la o el valor ocho
        txt= txt.replace("9","s") #le asigna a la s el valor nueve
    #llave "neumaticos" con su respectivo digito que correspondera a cada caracter
    if ultcar == '2':#si el ultimo caracter es igual a dos, me aplicara esta llave
        txt= txt.replace("0","e") #le asigna a la e el valor cero
        txt= txt.replace("1","u") #le asigna a la u el valor uno
        txt= txt.replace("2","c") #le asigna a la c el valor dos
        txt= txt.replace("3","a") #le asigna a la a el valor tres
        txt= txt.replace("4","l") #le asigna a la l el valor cuatro
        txt= txt.replace("5","i") #le asigna a la i el valor cinco
        txt= txt.replace("6","p") #le asigna a la p el valor seis
        txt= txt.replace("7","t") #le asigna a la t el valor siete
        txt= txt.replace("8","o") #le asigna a la o el valor ocho
        txt= txt.replace("9","s") #le asigna a la s el valor nueve
    #llave "eucaliptos" con su respectivo digito que correspondera a cada caracter
    final_str = txt[:-1] 
    #creara una nueva cadena de texto igual a la cadena anterior txt, excepto que le faltara el ultimo caracter, gracias al operador de 
    #indexacion en cadenas "[inicio:fin]"
    return (final_str)
    #retornara la nueva cadena al inicio.
