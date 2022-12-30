import conversiones
from operator import xor
import hamming
#mensaje_a_decodificar="01110101011 01001101101 00111011111 01100011100"
#mensaje_a_decodificar="01001101100 00110101100 01011111010 11110100101"
#mensaje_a_decodificar="11001100010 11110100101 01001100111 01110101011"
def decodificacion(mensaje_a_decodificar):#toma un mensaje codificado como argumento
	
	arreglo = mensaje_a_decodificar.split()#se divide el mensaje en un arreglo de palabras usando la funcino split()
	salida = ""
	for index, value in enumerate(arreglo):#Se itera sobre cada elemento de la lista "arreglo", "enumerate()" se utiliza para obtener el indice
        #y el valor de cada elemento de la lista en cada iteracion, en index se almacena el indice del elemento actual y en value, se almacena el 
        #valor del elemento actual
		letra = arreglo[index]# asignamos a "letra" el valor del elemento actual en la lista "arreglo", en la posicion especificada por "index"
		p1 = int(letra[0])#se asigna en p1 el valor del 1er carácter de la cadena almacenada en "letra", pero en su valor ASCII correspondiente.
		p2 = int(letra[1])#se asigna en p2 el valor del 2do carácter de la cadena almacenada en "letra", pero en su valor ASCII correspondiente.
		d1 = int(letra[2])#se asigna en d1 el valor del 3er carácter de la cadena almacenada en "letra", pero en su valor ASCII correspondiente.
		p3 = int(letra[3])#se asigna en p3 el valor del 4to carácter de la cadena almacenada en "letra", pero en su valor ASCII correspondiente.
		d2 = int(letra[4])#se asigna en d2 el valor del 5to carácter de la cadena almacenada en "letra", pero en su valor ASCII correspondiente.
		d3 = int(letra[5])#se asigna en d3 el valor del 6to carácter de la cadena almacenada en "letra", pero en su valor ASCII correspondiente.
		d4 = int(letra[6])#se asigna en d4 el valor del 7mo carácter de la cadena almacenada en "letra", pero en su valor ASCII correspondiente.
		p4 = int(letra[7])#se asigna en p4 el valor del 8vo carácter de la cadena almacenada en "letra", pero en su valor ASCII correspondiente.
		d5 = int(letra[8])#se asigna en d5 el valor del 9no carácter de la cadena almacenada en "letra", pero en su valor ASCII correspondiente.
		d6 = int(letra[9])#se asigna en d6 el valor del 10mo carácter de la cadena almacenada en "letra", pero en su valor ASCII correspondiente.
		d7 = int(letra[10])#se asigna en d7 el valor del 11vo carácter de la cadena almacenada en "letra", pero en su valor ASCII correspondiente.
		prueba1= hamming.xor_5(d1,d2,d4,d5,d7)# se aplica el operador logico XOR a 5 valores y devuelve el resultado en prueba1
		prueba2= hamming.xor_5(d1,d3,d4,d6,d7)#se aplica el operador logico XOR a 5  valores y devuelve el resultado en prueba2
		prueba3= hamming.xor_3(d2,d3,d4)#se aplica el operador logico XOR a 3 valores y devuelve el resultado en prueba3
		prueba4= hamming.xor_3(d5,d6,d7)#se aplica el operador logico XOR a 3 valores y devuelve el resultado en prueba4
		if (p4 == prueba4):#se hace la comparacion de igualdad entre p4 y prueba4
			error = "0"#sera almacenado el caracter "0" en error, si la sentencia anterior es verdadera
		else:
			error = "1"#si la sentencia anterior no es verdadera, se asigna el caracter "1" a la variable error

		if (p3 == prueba3):#se hace la comparacion de igualdad entre p3 y prueba3
			error = error+"0"#si al sentencia anterior se cumple, se agrega un caracter "0" al final de la cadena almacenada en "error"
		else:
			error = error+"1"#si al sentencia anterior no se cumple, se agrega un caracter "1" al final de la cadena almacenada en "error"

		if (p2 == prueba2):#se hace la comparacion de igualdad entre p2 y prueba2
			error = error+"0"#si al sentencia anterior se cumple, se agrega un caracter "0" al final de la cadena almacenada en "error"
		else:
			error = error+"1"#si al sentencia anterior no se cumple, se agrega un caracter "1" al final de la cadena almacenada en "error"

		if (p1 == prueba1):#se hace la comparacion de igualdad entre p1 y prueba1
			error = error+"0"#si al sentencia anterior se cumple, se agrega un caracter "0" al final de la cadena almacenada en "error"
		else:
			error = error+"1"#si al sentencia anterior no se cumple, se agrega un caracter "1" al final de la cadena almacenada en "error"

		posicion = conversiones.binario_a_decimal(error)
		pos_error=posicion-1
		print('El error esta en la posicion: '+str(pos_error))
		deco = [p1,p2,d1,p3,d2,d3,d4,p4,d5,d6,d7]#se crea una lista llamada deco asignandole los valores adentro de los corchetes
		poserror = int(letra[posicion -1])#el valor almacenado en la variable posicion se convierte en entero y se utiliza para acceder a un
        #elemento de la lista "letra", el valor almacenado en ese elemento se almacena en "poserror"
		if (posicion != 0):#se realiza la comparacion desigualdad de "posicion" diferente de cero
			if (poserror == 1):#se realiza la comparacion de igualdad de "posicion" y "1"
				deco[posicion-1] = 0 #el elemento en la posicion "posicion-1" de la lista "deco" se asignara el valor de cero.
			else:
				deco[posicion-1] = 1 #el elemento en la posicion "posicion-1" de la lista "deco" se asignara el valor de uno.
		
		dec =str(deco[10])+str(deco[9])+str(deco[8])+str(deco[6])+str(deco[5])+str(deco[4])+str(deco[2])+"0"
        #se crea una nueva lista "dec" que contiene los valores de los elementos con indices 10,9,8,6,5,4,2 de la lista "deco" en ese orden
		valor = 0 #a valor se le asigna el valor de cero

		for num in range(len(dec)):#con for se itera sobre cada caracter de la cadena "dec", utilizando la funcion"range()", el range()
            #lo que nos va a hacer es devolver un rango de valores que va desde cero hasta el valor especificado menos 1,depende delongitud de dec
			if(int(dec[num]) == 1): #comparacion del valor actual  en la cadena dec, convertido en entero, igualdad con "1"
				valor = valor + (2**num)#si la sentencia anterior se cumple, incremeta el valor de la variable "valor" en el resultado de 
                #elevar 2 a la potencia del indice del caracter actual, almacenado en la variable "num"
		
		letraenbinario = conversiones.decimal_a_binario(valor)#se asigna en "letraenbinario" el resultado de convertir el valor almacenado  
        # en la variable "valor", a una cadena binaria utilizando la funcion "decimal_a_binario" 

		letradeco = conversiones.binario_a_ascii(letraenbinario)#se asigna en "letradeco" el resultado de convertir el valor binario almacenado en la variable
        # "letraenbinario", a una cadena en codigo ASCII utlizando la funcion "binario_a_ascii"

		salida = salida + letradeco #agrega el valor almacenado en la variable "letradeco" al final de la cadena almacenada en "salida" 
	#print("LA SALIDA ES: "+salida)
	return salida #se devuelve el valor de la variable "salida" como resultado de la funcion de decodificacion., esto representa el 
    #mensaje original decodificado
#decodificacion(mensaje_a_decodificar)