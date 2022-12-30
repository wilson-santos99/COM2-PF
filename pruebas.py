import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from operator import xor
#importamos la funcion "xor" del modulo "operator", "xor" se utiliza para realizar una operacion de "o exclusivo" en dos operandos booleanos.
import random
#importamos el modulo "random", este modulo contiene funciones que permiten generar numeros aleatorios.
from sympy import Matrix
#importamos la clase "Matrix" del modulo "sympy", "Matrix" se utiliza para crear y manipular matrices.
import numpy as np
#se importa el modulo numpy y se le da el alias "np", este modulo numpy proporciona funciones y herramientas para 
#trabajar vectores y matrices de forma eficiente.
import serial
from tkinter.scrolledtext import ScrolledText
from serial.tools import list_ports
import threading
import time
import os
import io
from io import open
from tkinter import filedialog
FONT = ("calbri", 20, "bold")


class Interfaz:
    def __init__(self, master):
        self.master = master
        ancho = 600    
        alto = 750
        tamaño = str(ancho)+"x"+str(alto)
        master.geometry(tamaño)
        master.title("CHAT GUI")
        master.iconbitmap('C:/Users/santo/Documents/GitHub/Laboratorio_Comunicaciones_2/Practica 3/icono.ico')
        master.resizable(False,False)
        master.eval('tk::PlaceWindow . center')
        self.texto_plano = tk.StringVar(master, value="")
        self.texto_cifrado = tk.StringVar(master, value="")
        self.clave = tk.IntVar(master)
        #Buscar puertos y ponerlos en una lista

        ports =  serial.tools.list_ports.comports()
        self.lis = []
        for port in ports:
            idx = str(port).find(' ')
            puerto = str(port)[0:idx]
            self.lis.append(puerto)

        self.master.title(f"CHAT PRIVADO/SEGURO")
        self.master.geometry("+50+50")
        self.master.resizable(0, 0)
        #Indicador de cierre
        self.cierre = False
        # ---------------------- SERIAL PORT --------------------------
        self.serial = None
        # Create an object of tkinter ImageTk
        # Create a photoimage object of the image in the path
        image1 = Image.open("C:/Users/santo/Documents/GitHub/Proyecto_Comunicaciones-2/imagenlogo.png")
        test = ImageTk.PhotoImage(image1)
        label1 = tk.Label(image=test)
        label1.image = test
        # Position image
        label1.grid(row=0,column=1)
        # texto_plano controls
        frm1 = tk.LabelFrame(master, text="Conexion",bg= '#6666CD').grid(row=0,column=0)
        frm2 = tk.Frame(master,bg= '#6666CD').grid(row=1,column=0)
        frm3 = tk.LabelFrame(master, text="Enviar mensaje",bg= '#6666CD').grid(row=2,column=0)
 # ------------------------ FRAME 1 ----------------------------
        self.lblCOM = tk.Label(frm1, text="Puerto COM:").grid(row=0, column=0, padx=5, pady=5)
        self.cboPort = ttk.Combobox(frm1, values=self.lis)
        self.lblSpace = tk.Label(frm1, text="")
        self.btnConnect = tk.Button(frm1, text="Conectar", width=16, command = self.Conectar)
        
        self.cboPort.grid(row=0, column=1, padx=5, pady=5)
        self.lblSpace.grid(row=1,column=0, padx=30, pady=5)
        self.lblbaud = tk.Label(frm1, text="Baudrare:").grid(row=1, column=0, padx=5, pady=5)
       # self. = tk.Entry(frm3, width=15).grid(row=2, column=0, padx=5, pady=5)
        #self.inbaud = tk.Entry(frm3, width=15) #ingresar mensaje a enviar
        #self.inbaud.grid(row=2, column=0, padx=5, pady=5)
        self.btnConnect.grid(row=1, column=1, padx=5, pady=5)
        velocidad=['9600','19200','38400','57600']
        self.inbaud=ttk.Combobox(frm3,values=velocidad)
        self.inbaud.grid(row=2,column=0,padx=5,pady=5)
        # ------------------------ FRAME 2 ---------------------------
        self.txtChat = ScrolledText(frm2, height=25, width=50, wrap=tk.WORD, state='disable')
        self.txtChat.grid(row=3, column=0, columnspan=3, padx=5, pady=5)     
        # ------------------------ FRAME 3 --------------------------
        self.lblText = tk.Label(frm3, text="Mensaje a Enviar:")
        self.inText = tk.Entry(frm3, width=45, state='disable') #ingresar mensaje a enviar
        self.btnSend = tk.Button(frm3, text="Enviar", width=12, state='disable', command=self.encriptar_callback)#lambda: )#command = self.Envio1)
        self.lblText.grid(row=4, column=0, padx=5, pady=5)
        self.inText.grid(row=4, column=1, padx=5, pady=5)
        self.btnSend.grid(row=5, column=0, padx=5, pady=5)           
        # --------------------------- StatusBar -----------------------
        self.statusBar = tk.Label(self.master, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusBar.grid(row=5,column=1)    
        # --------------------------- Button abrir fichero -----------------------
        self.btnabrir = tk.Button(frm3, text="Abrir txt", width=12, state='disable', command=self.AbrirFicher)#lambda: )#command = self.Envio1)
        self.btnabrir.grid(row=6, column=0, padx=5, pady=5) 
        # ------------- Control del boton "X" de la ventana -----------
        self.master.protocol("WM_DELETE_WINDOW", self.cerrar_puertos)
        #Eventos
        self.inText.bind('<Return>',self.encriptar_callback )#self.Envio)
        
###########################COMUNICACION SERIAL ###########################
    def AbrirFicher(self):
        tf = filedialog.askopenfilename(
        initialdir="", 
        title="Open Text file", 
        filetypes=(("Text Files", "*.txt"),)
        )
       
        tf = open(tf)  # or tf = open(tf, 'r')
        data = tf.read()
        self.inText.insert(tk.END, data)
        tf.close()

    def atrapa_texto(self):
        f = open ('fichero_prueba.txt','r')
        mensaje = f.read()
        print(mensaje)
        f.close()
        self.inText.insert(1.0,mensaje)
    def Tex_Envio(self):
        self.statusBar.config(text = "Enviando mensaje ...")
        time.sleep(1)
        self.statusBar.config(text = f"Conectando al {self.PORT_FIN} a {str(self.inbaud.get())}")

    def Tex_Recivido(self):
        self.statusBar.config(text = "Recibiendo mensaje ...")
        time.sleep(1)
        self.statusBar.config(text = f"Conectando al {self.PORT_FIN} a {str(self.inbaud.get())}")

    def Lectura(self):
        while True:
            if self.ser.in_waiting > 0:
                funcion2 = threading.Thread(target=self.Tex_Recivido, daemon=True)
                funcion2.start()
                # Se leen los datos y esperar al caracter EOL
                data = self.ser.readline()
                #La data recibida son bytes y hay que convertirlos
                string = data.decode('utf-8')
                self.txtChat.config(state = 'normal')
                self.txtChat.insert(tk.INSERT, string, 'black')
                self.txtChat.see("end")
                self.txtChat.config(state = 'disable')
                print(string[-2])
                if string[-2] =='c':
                    print('cesar')
                if string[-2] =='h':
                    print('hill')
                if string[-2] =='p':
                    print('propio')
            elif self.cierre == True:
                break          
    
    def Conectar(self):
        self.cierre = False
        #Activar todo
        self.PORT_FIN = self.cboPort.get()
        self.velocidad=str(self.inbaud.get())

        self.txtChat.tag_config('rojo', foreground='red')
        self.txtChat.tag_config('verde', foreground='green')
        try:
            #46274733
            #Establecer conexion con el purto serial
            self.statusBar.config(text = f"Conectando al {self.PORT_FIN} a {self.velocidad}")
            self.ser = serial.Serial(port = self.PORT_FIN,
                                baudrate = self.velocidad,
                                bytesize = 8,
                                stopbits=serial.STOPBITS_ONE)
            self.statusBar.config(text = f"Conectado al {self.PORT_FIN} a {str(self.inbaud.get())}")
            #Aviso de coneccion
            #lacanchisarriaga
            string = f"{self.PORT_FIN} SE HA CONECTADO"+'\n'
            data = string.encode("utf-8")
            self.ser.write(data)
            #Preparar para conexion
            self.btnSend.config(state = 'normal')
            self.inText.config(state = 'normal')
            self.inbaud.config(state='disable')
            self.cboPort.config(state = 'disable')
            self.btnabrir.config(state='normal')
            self.btnConnect.config(text = 'Desconectar', command = self.Desconectar)
            #Lectura de entrada
            funcion1 = threading.Thread(target=self.decrypt_callback, daemon=True)
            funcion1.start()
        except:
            self.statusBar.config(text = f"Error al conectar a {self.PORT_FIN}")
            
    def Desconectar(self):
        #Cierre de los bucles
        self.cierre = True
        #Aviso de desconeccion
        string = f"{self.PORT_FIN} SE HA DESCONECTADO"+'\n'
        data = string.encode("utf-8")
        self.ser.write(data)
        #Desconectar
        self.ser.close()
        #Predeterminado
        self.btnConnect.config(text = 'Conectar', command = self.Conectar)
        self.statusBar.config(text = "")
        self.btnSend.config(state = 'disable')
        self.inText.config(state = 'disable')
        self.cboPort.config(state = 'normal')
        self.inbaud.config(state='enable')
        self.btnabrir.config(state='disable')


    def Envio1(self,event):
        funcion3 = threading.Thread(target=self.Tex_Envio, daemon = True)
        funcion3.start()
        #Estraccion de datos
        string = f"[{self.PORT_FIN}] "+self.inText.get()+'\n'
        self.inText.delete(0,'end')
        self.txtChat.config(state = 'normal')
        self.txtChat.insert(tk.INSERT, string, 'verde')
        self.txtChat.config(state = 'disable')
        self.txtChat.see("end")
        data = string.encode("utf-8")
        self.ser.write(data)
    


    def cerrar_puertos(self):
        # Se cierran los puertos COM y la ventana de tkinter
        try:
            self.cierre = True
            self.ser.close()
        except:
            pass

        self.master.destroy()


#################################COMUNICACION SERIAL ###########################
    def encriptar_callback(self):
        #ser = serial.Serial(port='COM3',baudrate=str(self.inbaud.get()))
        #ser.close()
        cifrado_tipo=random.randint(0,2) #0,1,2


        if cifrado_tipo == 0:
            print("ha seleccionado cifrado cesar")
            clave = 3
            texto_cifrado_cesar = cifrado_cesar(self.inText.get(), clave) #self.texto_cifrado_entry.get()
            print('el texto cifrado en cesar es:   '+texto_cifrado_cesar)
            mensaje_cifrado_y_codificado= hamming(texto_cifrado_cesar)
            texto_enviad=" ".join(mensaje_cifrado_y_codificado)+'c'
            textoA=bytearray(texto_enviad,'utf8')
            #self.texto_cifrado_entry.insert(0, texto_enviad)
            funcion3 = threading.Thread(target=self.Tex_Envio, daemon = True)
            funcion3.start()
            #funcion3=self.encriptar_callback(dato)
            #Estraccion de datos
            dato = f"[{self.PORT_FIN}] "+self.inText.get()+'\n'
            print('el texto enviado es: '+texto_enviad)
            string =  texto_enviad
            self.inText.delete(0,'end')
            self.txtChat.config(state = 'normal')
            self.txtChat.insert(tk.INSERT, dato, 'verde')
            self.txtChat.config(state = 'disable')
            self.txtChat.see("end")
            data = string.encode("utf-8")
            self.ser.write(data) 
            texto_cifrado_cesar=''
            mensaje_cifrado_y_codificado=''
            data=''

        if cifrado_tipo==1: 
            #ser.open()
            print("ha seleccionado cifrado Hill")
            clave = [[13, 17], [10, 16]]
            texto_cifrado_hill= cifradohill(self.inText.get(), clave)
            print('el texto cifrado en hill es:   '+texto_cifrado_hill)
            mensaje_cifrado_y_codificado= hamming(texto_cifrado_hill)
            texto_enviad=" ".join(mensaje_cifrado_y_codificado)+'h'
            textoA=bytearray(texto_enviad,'utf8')
            funcion3 = threading.Thread(target=self.Tex_Envio, daemon = True)
            funcion3.start()
            #funcion3=self.encriptar_callback(dato)
            #Estraccion de datos
            dato = f"[{self.PORT_FIN}] "+self.inText.get()+'\n'
            print('el texto enviado es: '+texto_enviad)
            string =  texto_enviad+'\n'
            self.inText.delete(0,'end')
            self.txtChat.config(state = 'normal')
            self.txtChat.insert(tk.INSERT, dato, 'verde')
            self.txtChat.config(state = 'disable')
            self.txtChat.see("end")
            data = string.encode("utf-8")
            self.ser.write(data)
            texto_cifrado_cesar=''
            mensaje_cifrado_y_codificado=''
            data=''

        if cifrado_tipo ==2:
            #ser.open()
            print("ha seleccionado cifrado propio")
            texto_cifrado_propio = cifradopropio(self.inText.get())
            mensaje_cifrado_y_codificado= hamming(texto_cifrado_propio)
            texto_enviad=" ".join(mensaje_cifrado_y_codificado)+'p'
            textoA=bytearray(texto_enviad,'utf8')
            print('el texto cifrado en propio es:   '+texto_cifrado_propio)
            funcion3 = threading.Thread(target=self.Tex_Envio, daemon = True)
            funcion3.start()
            #funcion3=self.encriptar_callback(dato)
            #Estraccion de datos
            dato = f"[{self.PORT_FIN}] "+self.inText.get()+'\n'
            #dato=f"[{self.PORT_FIN}]"
            print('el texto enviado es: '+texto_enviad)
            string =  texto_enviad+'\n'
            self.inText.delete(0,'end')
            self.txtChat.config(state = 'normal')
            self.txtChat.insert(tk.INSERT, dato, 'verde')
            self.txtChat.config(state = 'disable')
            self.txtChat.see("end")
            data = string.encode("utf-8")
            self.ser.write(data) 
            texto_cifrado_cesar=''
            mensaje_cifrado_y_codificado=''
            data=''
        return texto_enviad
    
    def decrypt_callback(self):

        while True:
            #data=""
            #string=""
            #texto_recibido=""
            if self.ser.in_waiting > 0:
                funcion2 = threading.Thread(target=self.Tex_Recivido, daemon=True)
                funcion2.start()
                # Se leen los datos y esperar al caracter EOL
                data = self.ser.readline()
                #La data recibida son bytes y hay que convertirlos
                string = data.decode('utf-8')
                texto_recibido=string[:-2]+'\n'
                
                print(string[-2])                    
                if string[-2][-1]=='c':
                    print('ha recibido texxto cifrado en cesar')
                    #mensaje_recibido= self.texto_cifrado
                    clave = 3
                    texto_plano_decodificado=decodificacion(texto_recibido)
                    texto_plano = descifrado_cesar(texto_plano_decodificado, clave)
                    dato="usuario2:   "+texto_plano +'\n'
                    print('El codigo recibido es: '+texto_recibido)
                    print('El texto decodificado y descifrado es: '+texto_plano)
                    self.txtChat.config(state = 'normal')
                    self.txtChat.insert(tk.INSERT, dato, 'black')
                    self.txtChat.see("end")
                    self.txtChat.config(state = 'disable')
                    data=''
                    string=''
                    texto_recibido=''
                    texto_plano_decodificado=''
                    dato=''
                if string[-2][-1]=='h':
                    print('ha recibido texxto cifrado en hill')
                    #mensaje_recibido= self.texto_cifrado
                    clave = [[13, 17], [10, 16]]
                    texto_plano_decodificado=decodificacion(texto_recibido)
                    texto_plano = descifrado_hill(texto_plano_decodificado, clave)
                    dato="usuario2:   "+texto_plano +'\n'
                    
                    self.txtChat.config(state = 'normal')
                    print('El codigo recibido es: '+texto_recibido)
                    print('El texto decodificado y descifrado es: '+texto_plano)
                    self.txtChat.insert(tk.INSERT, dato, 'black')
                    self.txtChat.see("end")
                    self.txtChat.config(state = 'disable')
                    data=''
                    string=''
                    texto_recibido=''
                    texto_plano_decodificado=''
                    dato=''
                if string[-2][-1]=='p':
                    print('ha recibido texxto cifrado en  propio')
                    #mensaje_recibido= self.texto_cifrado
                    texto_plano_decodificado=decodificacion(texto_recibido)
                    texto_plano = descifrado_propio(texto_plano_decodificado)
                    self.txtChat.config(state = 'normal')
                    dato="usuario2:   "+texto_plano +'\n'
                    print('El codigo recibido es:  '+texto_recibido)
                    print('El texto decodificado y descifrado es: '+texto_plano)
                    self.txtChat.insert(tk.INSERT, dato, 'black')
                    self.txtChat.see("end")
                    self.txtChat.config(state = 'disable')
                    data=''
                    string=''
                    texto_recibido=''
                    texto_plano_decodificado=''
                    dato=''
                    
            elif self.cierre == True:
                break

###################################################################################3333333333333333333333

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

def decimal_a_binario(decimal): #la funcion toma un valor decimal como argumento 
    if decimal <= 0:            #compara si decimal es igual o menor a cero
        return "0"              #si la funcion if se cumple. retornara una cadena de texto "0"
    # Aquí almacenamos el resultado
    binario = ""
    # Mientras se pueda dividir...
    while decimal > 0:   #en esta parte se ejecutara el ciclo que ejecuta los calculos para representar el valor decimal en binario
        # Saber si es 1 o 0
        residuo = int(decimal % 2) #obtenemos el residuo  de la division del decimal entre 2,  y el resultado se convierte a entero
        decimal = int(decimal / 2) #se utiliza para dividir el numero decimal entre dos y obtener el resultado de la division, a este valor
        # se convierte en entero para asegurarnos que todo sea correcto y se almacena en la variable "decimal"
        binario = str(residuo) + binario #se convierte el valor de residuo a cadena de texto con el str(), luego se concatena el valor del 
        #residuo a la cadena de texto, "binario" usando el operador +, añadiendo el nuevo valor a la izquierda de la cadena.
    return binario
    #Esta funcion hara el trabajo de convertir un numero decimal a su representacion en binario. La funcion toma un numero decimal como 
    #argumento y devuelve una cadena de texto que representa el numero en binario.

def hamming(mensaje_a_codificar): #Esta función se llama "hamming" y recibe como parámetro un mensaje que se desea codificar
    arreglo = list(mensaje_a_codificar) #convierte el mensaje en una lista de caracteres.
    letra_a_binario = [ascii_a_binario(num) for num in arreglo] # convierte cada caracter en su representación binaria mediante una función llamada "ascii_a_binario". Esta representación se almacena en "letra_a_binario".
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
		prueba1= xor_5(d1,d2,d4,d5,d7)# se aplica el operador logico XOR a 5 valores y devuelve el resultado en prueba1
		prueba2= xor_5(d1,d3,d4,d6,d7)#se aplica el operador logico XOR a 5  valores y devuelve el resultado en prueba2
		prueba3= xor_3(d2,d3,d4)#se aplica el operador logico XOR a 3 valores y devuelve el resultado en prueba3
		prueba4= xor_3(d5,d6,d7)#se aplica el operador logico XOR a 3 valores y devuelve el resultado en prueba4
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

		posicion = binario_a_decimal(error)
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
		
		letraenbinario = decimal_a_binario(valor)#se asigna en "letraenbinario" el resultado de convertir el valor almacenado  
        # en la variable "valor", a una cadena binaria utilizando la funcion "decimal_a_binario" 

		letradeco = binario_a_ascii(letraenbinario)#se asigna en "letradeco" el resultado de convertir el valor binario almacenado en la variable
        # "letraenbinario", a una cadena en codigo ASCII utlizando la funcion "binario_a_ascii"

		salida = salida + letradeco #agrega el valor almacenado en la variable "letradeco" al final de la cadena almacenada en "salida" 


	return salida #se devuelve el valor de la variable "salida" como resultado de la funcion de decodificacion., esto representa el 
    #mensaje original decodificado.

###################################################################################3333333333333333333333###################################################################################3333333333333333333333
separador = " "  
#a la variable "separador", le asignamos un espacio vacio.

diccionario_encryt = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11,
            'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25,
            '0':26, '1': 27, '2':28, '3':29, '4':30, '5':31, '6':32, '7':33, '8':34, '9':35, '.': 36, ',': 37, ':': 38, '?': 39 , ' ': 40}

#print(len(diccionario_encryt))
#Creamos un diccionario para almacenar nuestro alfabeto,  numeros y simbolos de forma ordenada
diccionario_decrypt = {'0' : 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E', '5': 'F', '6': 'G', '7': 'H', '8': 'I', '9': 'J', '10': 'K', '11': 'L', '12': 'M',
            '13': 'N', '14': 'O', '15': 'P', '16': 'Q', '17': 'R', '18': 'S', '19': 'T', '20': 'U', '21': 'V', '22': 'W', '23': 'X', '24': 'Y', '25': 'Z', '26': '0',
            '27': '1', '28': '2', '29': '3', '30': '4', '31': '5', '32' : '6', '33' : '7', '34' : '8', '35' : '9', '36' : '.', '37' : ',', '38' : ':', '39' : '?', '40' : ' '}
#Creamos un diccionario para almacenar nuestro alfabeto,  numeros y simbolos de forma ordenada
#----------------------Funciones ----------------------------------

    ###############################################################CIFRADO Y DESCIFRADO CESAR
def cifradohill(message, key):
    ciphertext = ''
    matrix_mensaje = []
    list_temp = []
    cifrado_final = ''
    ciphertext_temp = ''
    cont = 0
    # Convertir el mensaje a mayusculas
    message = message.upper()
    # Si el tamaño del mensaje es menor o igual al tamaño de la clave
    if len(message) <= len(key):
        # Convertir el tamaño del mensaje al tamaño de la clave, si no es igual, se añaden 'X' hasta que sean iguales los tamaños.
        while len(message) < len(key):
            message = message + 'X'

        # Crear la matriz para el mensaje

        for i in range(0, len(message)):
            matrix_mensaje.append(diccionario_encryt[message[i]])

        # Se crea la matriz

        matrix_mensaje = np.array(matrix_mensaje)

        # Se multiplica la matriz clave por la de mensaje

        cifrado = np.matmul(key, matrix_mensaje)

        # Se obtiene el modulo sobre el diccionario de cada celda

        cifrado = cifrado % 41

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

    # --------------------------------

    return ciphertext
###################################################################################################################
def descifrado_hill(message, key):#definimos esta funcion con dos argumentos, el mensaje y la llave cuadrada
    plaintext = '' #se utilizara para almacenar el mensaje decodificado

    matrix_mensaje = [] #se utilizara para aplicar la clave al mensaje cifrado
    plaintext_temp = ''
    list_temp = []
    matrix_inversa = []
    matrix_mensaje = [message[i:i + len(key)] for i in range(0,
                      len(message), len(key))]#se utilizara para aplicar la clave inversa a cada bloque del mensaje cifrado y decodificado.
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
###################################################################################3333333333333333333333###################################################################################3333333333333333333333
if __name__ == "__main__":
    root = tk.Tk()
    caesar = Interfaz(root)
    root.mainloop()