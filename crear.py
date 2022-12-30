import os
import time
def creararchivo(message):
    nombre = time.strftime("Texto_Recibido-%Y%m%d-%H%M%S")
    try:
        #PATTH : C:\Users\santo\Desktop\proyecto final com2
        #f = open("C:/Users/santo/Downloads/Proyecto_Comunicaciones-2version/Proyecto_Comunicaciones-2version/mensajesrecibidos/"+nombre+".txt","w")
        f = open("C:/Users/santo/Desktop/proyecto final com2/mensajesrecibidos/"+nombre+".txt","w")
        print(str(nombre))
        f.write(message)
        f.close()
    except:
        print("ocurrio un error")

#message="mincho prueba"
#creararchivo(message)