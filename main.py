from unidecode import unidecode
import tkinter as tk
from tkinter import ttk
#from PIL import ImageTk, Image
from operator import xor
#importamos la funcion "xor" del modulo "operator", "xor" se utiliza para realizar una operacion de "o exclusivo" en dos operandos booleanos.
import random
#importamos el modulo "random", este modulo contiene funciones que permiten generar numeros aleatorios.

#importamos la clase "Matrix" del modulo "sympy", "Matrix" se utiliza para crear y manipular matrices.
#se importa el modulo numpy y se le da el alias "np", este modulo numpy proporciona funciones y herramientas para 
#trabajar vectores y matrices de forma eficiente.
import serial
#from tkinter.scrolledtext import ScrolledText
from tkinter import scrolledtext
from serial.tools import list_ports
import threading
import time
import os
import io
from io import open
from tkinter import filedialog
import hamming
import decodificar_hamming
import hill
import cesar
import propio
import Generar_ruido
FONT = ("calbri", 20, "bold")

###################################################################################3333333333333333333333###################################################################################3333333333333333333333
separador = " "  
#a la variable "separador", le asignamos un espacio vacio.
#------------Mensaje recibido----------------#
#Creamos un diccionario para almacenar nuestro alfabeto,  numeros y simbolos de forma ordenada
#----------------------Funciones ----------------------------------
class Interfaz:
    def __init__(self, master):
        self.master = master
        ancho = 600    
        alto = 750
        tamaño = str(ancho)+"x"+str(alto)
        master.geometry(tamaño)
        master.title("CHAT GUI")
        #master.iconbitmap('C:/Users/olivi/Documents/PROYECTOS VS CODE/LABORATORIO COM2/icono.ico')
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
        #image1 = Image.open("C:/Users/olivi/Documents/PROYECTOS VS CODE/LABORATORIO COM2/imagenlogo.png")
        #test = ImageTk.PhotoImage(image1)
        #label1 = tk.Label(image=test)
        #label1.image = test
        # Position image
        #label1.grid(row=0,column=1,columnspan=3)
        # texto_plano controls
        frm1 = tk.LabelFrame(master, text="Conexion",bg= '#6666CD').grid(row=0,column=0)
        frm2 = tk.Frame(master,bg= '#6666CD').grid(row=1,column=0)
        frm3 = tk.LabelFrame(master, text="Enviar mensaje",bg= '#6666CD').grid(row=2,column=0)
 # ------------------------ FRAME 1 ----------------------------
        velocidad=['9600','19200','38400','57600']
        cifrado=['HILL','CESAR','PROPIO']
        self.lblCOM = tk.Label(frm1, text="Puerto COM:")
        self.cboPort = ttk.Combobox(frm1, values=self.lis)
        self.lblbaud = tk.Label(frm1, text="Baudrare:")
        self.lblSpace = tk.Label(frm1, text="")
        self.btnConnect = tk.Button(frm1, text="Conectar", width=16, command = self.Conectar)
        self.tipocifrado=ttk.Combobox(frm3,values=cifrado)
        self.inbaud=ttk.Combobox(frm3,values=velocidad)
        self.lblcifrado = tk.Label(frm1, text="")
       # self. = tk.Entry(frm3, width=15).grid(row=2, column=0, padx=5, pady=5)
        #self.inbaud = tk.Entry(frm3, width=15) #ingresar mensaje a enviar
        #self.inbaud.grid(row=2, column=0, padx=5, pady=5)

        
        self.lblCOM.grid(row=0, column=0, padx=5, pady=5)
        self.cboPort.grid(row=0, column=1, padx=5, pady=5)
        self.lblbaud.grid(row=1, column=0, padx=5, pady=5)
        self.lblSpace.grid(row=1,column=0, padx=30, pady=5)
        self.btnConnect.grid(row=1, column=1, padx=5, pady=5)
        self.tipocifrado.grid(row=2,column=1,padx=5,pady=5)
        self.inbaud.grid(row=2,column=0,padx=5,pady=5)   
        self.lblcifrado.grid(row=3,column=0,padx=5,pady=5)  
        # ------------------------ FRAME 2 ---------------------------
        self.txtChat = scrolledtext.ScrolledText(frm2, height=25, width=65, wrap=tk.WORD, state='disable')
        self.txtChat.grid(row=5, column=0, columnspan=3, padx=5, pady=5)     
        # ------------------------ FRAME 3 --------------------------
        self.lblText = tk.Label(frm3, text="Mensaje a Enviar:")
        self.inText = tk.Entry(frm3, width=45, state='disable') #ingresar mensaje a enviar
        self.btnSend = tk.Button(frm3, text="Enviar", width=12, state='disable', command=self.encriptar_callback)#lambda: )#command = self.Envio1)
        self.lblText.grid(row=6, column=0, padx=5, pady=5)
        self.inText.grid(row=6, column=1, padx=5, pady=5)
        self.btnSend.grid(row=7, column=0, padx=5, pady=5)           
        # --------------------------- StatusBar -----------------------
        self.statusBar = tk.Label(self.master, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusBar.grid(row=7,column=1)    
        # --------------------------- Button abrir fichero -----------------------
        self.btnabrir = tk.Button(frm3, text="Abrir txt", width=12, state='disable', command=self.AbrirFicher)#lambda: )#command = self.Envio1)
        self.btnabrir.grid(row=8, column=0, padx=5, pady=5) 
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

    def Tex_Recibido(self):
        self.statusBar.config(text = "Recibiendo mensaje ...")
        time.sleep(1)
        self.statusBar.config(text = f"Conectando al {self.PORT_FIN} a {str(self.inbaud.get())}")
    def Lectura(self):
        while True:
            if self.ser.in_waiting > 0:
                funcion2 = threading.Thread(target=self.Tex_Recibido, daemon=True)
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
        self.cifrado_tipo =self.tipocifrado.get()
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
            self.tipocifrado.config(state='disable')
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
        self.tipocifrado.config(state='enable')
        self.txtChat.delete(tk.END, 1.0)
        



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
        self.ser.reset_output_buffer()
        #ser = serial.Serial(port='COM3',baudrate=str(self.inbaud.get()))
        #ser.close()
        
        if self.cifrado_tipo == 'CEsSAR':
            print("ha seleccionado cifrado cesar")
            clave = 3
            texto_cifrado_cesar = cesar.cifrado_cesar(self.inText.get(), clave) #self.texto_cifrado_entry.get()
            print('el texto cifrado en cesar es:   '+texto_cifrado_cesar)
            mensaje_cifrado_y_codificado= hamming.hamming(texto_cifrado_cesar)
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
            self.ser.reset_output_buffer()
            texto_cifrado_cesar=''
            mensaje_cifrado_y_codificado=''
            data=''
    #CESAR
        if self.cifrado_tipo=='CESAR': 
            #ser.open()
            print("ha seleccionado cifrado CESAR A")
            clave = 3
            texto_enviaruni=unidecode(self.inText.get())
            texto_cifrado_cesar= cesar.cifrado_cesar(texto_enviaruni, clave)
            print('el texto cifrado en hill es:   '+texto_cifrado_cesar)
            mensaje_cifrado_y_codificado= hamming.hamming(texto_cifrado_cesar)
            texto_enviad=" ".join(mensaje_cifrado_y_codificado)+'x'
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
            texto_cifrado_propio=''
            texto_cifrado_hill=''
            mensaje_cifrado_y_codificado=''
            self.ser.reset_output_buffer()
            data=''
        if self.cifrado_tipo=='HILL': 
            #ser.open()
            print("ha seleccionado cifrado Hill")
            clave = [[13, 17], [10, 16]]
            texto_enviaruni=unidecode(self.inText.get())
            texto_cifrado_hill= hill.cifradohill(texto_enviaruni, clave)
            print('el texto cifrado en hill es:   '+texto_cifrado_hill)
            mensaje_cifrado_y_codificado= hamming.hamming(texto_cifrado_hill)
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
            texto_cifrado_hill=''
            texto_cifrado_cesar=''
            texto_cifrado_propio=''
            texto_cifrado_hill=''
            mensaje_cifrado_y_codificado=''
            self.ser.reset_output_buffer()
            data=''

        if self.cifrado_tipo =='PROPIO':
            #ser.open()
            print("ha seleccionado cifrado propio")
            texto_cifrado_propio = propio.cifradopropio(self.inText.get())
            mensaje_cifrado_y_codificado=hamming.hamming(texto_cifrado_propio)
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
            print("EL DATO ENVIADO ES: DATA "+str(data))
            self.ser.write(data) 
            texto_cifrado_cesar=''
            texto_cifrado_propio=''
            texto_cifrado_hill=''
            mensaje_cifrado_y_codificado=''
            self.ser.reset_output_buffer()
            data=''
        return texto_enviad
    
    def decrypt_callback(self):

        while True:
            #string=""
            texto_recibido=""
            if self.ser.in_waiting > 0:
                funcion2 = threading.Thread(target=self.Tex_Recibido, daemon=True)
                funcion2.start()
            # Se leen los datos y esperar al caracter EOL
                data = self.ser.readline()
                print("MENSAJE : "+str(data))
                #La data recibida son bytes y hay que convertirlos
                string = data.decode('utf-8')

                print("codigo recibido" +string)
                texto_recibido=string[:-2]+'\n'
                print(texto_recibido)
                print(string[-2])      

                if string[-2][-1]=='a':
                    print('ha recibido texxto cifrado en cesar')
                    tipocifrado="RECIBIENDO : CIFRADO CESAR"
                    self.lblcifrado.config(text = tipocifrado)
                    #mensaje_recibido= self.texto_cifrado
                    clave = 3
                    codigo_ruido=Generar_ruido.aleatorio(texto_recibido) #mensaje con ruido
                    texto_plano_decodificado=decodificar_hamming.decodificacion(codigo_ruido)
                    texto_plano = cesar.descifrado_cesar(texto_plano_decodificado, clave) 
                    dato="usuario2:   "+texto_plano +'\n'
                    print('El codigo recibido es: '+texto_recibido)
                    print('El texto decodificado y descifrado es: '+texto_plano)
                    self.txtChat.config(state = 'normal')
                    self.txtChat.insert(tk.INSERT, dato, 'black')
                    self.txtChat.see("end")
                    self.txtChat.config(state = 'disable')
                    self.ser.reset_input_buffer()

                elif string[-2][-1]=='h':
                    print('ha recibido texxto cifrado en hill')
                    tipocifrado="RECIBIENDO : CIFRADO HILL"
                    self.lblcifrado.config(text = tipocifrado)
                    #mensaje_recibido= self.texto_cifrado
                    clave = [[13, 17], [10, 16]]
                    
                    codigo_ruido=Generar_ruido.aleatorio(texto_recibido)
                    texto_plano_decodificado=decodificar_hamming.decodificacion(codigo_ruido)
                    print('ASEDFel texto decodificado es ----',texto_plano_decodificado)
                    texto_plano = hill.descifrado_hill(texto_plano_decodificado, clave)
                    dato="usuario2:   "+texto_plano +'\n'
                    self.txtChat.config(state = 'normal')
                    print('El codigo recibido es: '+texto_recibido)
                    print('El texto decodificado y descifrado es: '+texto_plano)
                    self.txtChat.insert(tk.INSERT, dato, 'black')
                    self.txtChat.see("end")
                    self.txtChat.config(state = 'disable')
                    self.ser.reset_input_buffer()
                elif string[-2][-1]=='x':
                    print('ha recibido texxto cifrado en CEsar')
                    tipocifrado="RECIBIENDO : CIFRADO CEsar"
                    self.lblcifrado.config(text = tipocifrado)
                    #mensaje_recibido= self.texto_cifrado
                    clave = 3
                    
                    codigo_ruido=Generar_ruido.aleatorio(texto_recibido)
                    texto_plano_decodificado=decodificar_hamming.decodificacion(codigo_ruido)
                    print('ASEDFel texto decodificado es ----',texto_plano_decodificado)
                    texto_plano = cesar.descifrado_cesar(texto_plano_decodificado, clave)
                    dato="usuario2:   "+texto_plano +'\n'
                    self.txtChat.config(state = 'normal')
                    print('El codigo recibido es: '+texto_recibido)
                    print('El texto decodificado y descifrado es: '+texto_plano)
                    self.txtChat.insert(tk.INSERT, dato, 'black')
                    self.txtChat.see("end")
                    self.txtChat.config(state = 'disable')
                    self.ser.reset_input_buffer()
                elif string[-2][-1]=='p':
                    tipocifrado="RECIBIENDO : CIFRADO PROPIO"
                    self.lblcifrado.config(text = tipocifrado)
                    print('ha recibido texxto cifrado en  propio')
                    #mensaje_recibido= self.texto_cifrado
                    codigo_ruido=Generar_ruido.aleatorio(texto_recibido)
                    texto_plano_decodificado=decodificar_hamming.decodificacion(codigo_ruido)
                    texto_plano = propio.descifrado_propio(texto_plano_decodificado)
                    self.txtChat.config(state = 'normal')
                    dato="usuario2:   "+texto_plano +'\n'
                    print('El codigo recibido es:  '+texto_recibido)
                    print('El texto decodificado y descifrado es: '+texto_plano)
                    self.txtChat.insert(tk.INSERT, dato, 'black')
                    self.txtChat.see("end")
                    self.txtChat.config(state = 'disable')
                    self.ser.reset_input_buffer()
                # else:
                #     print("ocurrio un error")
                #     string="Reenvie el mensaje porfavor"
                #     data = string.encode("utf-8")
                #     self.lblcifrado.config(text="OCURRIO UN ERROR, SE SOLICITO EL TEXTO ")
                #     self.ser.write(data)

            elif self.cierre == True:
                break


###################################################################################3333333333333333333333###################################################################################3333333333333333333333
if __name__ == "__main__":
    root = tk.Tk()
    caesar = Interfaz(root)
    root.mainloop()