import random

paquetes=''
#string=""
def aleatorio(string):
    global paquetes
    #mi_lista = ['10110010011','01101101010','10101011111','11111001100c']
    #string= "11001100000 11110100101 01001100011 01001100011 01110101001h"
    mi_lista=string.split()
    #print("este es el elemento: "+str(mi_lista[2]))
    #print('lista cortada:' +str(mi_lista))
    #print("texto recibido sin error: "+string)
    #print('mi lista unida es: '+str(mi_lista))
    lista_final_error=[] 
    errores=[]
    #print("mensaje recibido con error es: "+str(lista_final_error))
    #print('el tamaño de las listas '+str(len(listas)))
    #for i in lista:#range(len(mi_lista)):
    for j in range(len(mi_lista)):  
        #print('el tamaño del elemento es: '+str(len(mi_lista)))
        
        listanueva=list(mi_lista[j])
       # print('mi nueva lista de trama es: '+str(listanueva))
        #print('el tamaño de la trama es:: '+str(len(listanueva)))
       
        PosicionAleatoria = random.randint(0, 10) 
        #print("valor aleatorio es:  ",(PosicionAleatoria))
        #print('trama sin error unido: '+''.join(listanueva))
        #print('codigo sin error: '+str(listanueva))
        if listanueva[PosicionAleatoria]=='1':
            listanueva[PosicionAleatoria]='0'
           # print('Wilson el error esta en la posicion: '+str(PosicionAleatoria))
            #print('codigo con error: '+str(listanueva))
            datos=''.join(listanueva)
           # print('codigo con error unido: '+str(datos))
            #print('lista con bit cambiado es: '+str(listanueva))           
            #print('trama con error unido: '+str(datos))
            #print('con error: '+datos)
            lista_final_error.insert(j,datos)   
           # print("mensaje recibido con error es: "+str(lista_final_error))
            errores.insert(j,PosicionAleatoria)
        elif listanueva[PosicionAleatoria]=='0':
            #print('Wilson el error esta en la posicion: '+str(PosicionAleatoria))
            listanueva[PosicionAleatoria]='1'    
           # print('Wilson el error esta en la posicion: '+str(PosicionAleatoria))
            #print('codigo con error: '+str(listanueva))
            datos=''.join(listanueva)
            #print('codigo con error unido: '+str(datos))
            #print('lista con bit cambiado es: '+str(listanueva))
            
            #print('trama con error unido: '+str(datos))
            #print('con error: '+datos)
            lista_final_error.insert(j,datos)   
            #print("mensaje recibido con error es: "+str(lista_final_error))
            errores.insert(j,PosicionAleatoria)
        else:
            print("ocurrio un error")

    paquetes=str(len(errores))
    enviadoss=' '.join(lista_final_error)
    print('cantidad de errores encontrados: '+paquetes)
    print('texto recibido con error: '+enviadoss)
    print('texto recibido sin error: '+string)
    print("Los errores estan en las siguientes posiciones de cada trama: "+str(errores))
    print("#################################################################################")
    print(enviadoss)
    return(enviadoss)

#string= "11001100000 11110100101 01001100011 01001100011 01110101001h"
#aleatorio(string)
