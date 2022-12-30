from tkinter import Tk, Label, Entry, Button
from tkinter.ttk import Combobox, Labelframe
from tkinter.scrolledtext import ScrolledText
import serial.tools.list_ports
import serial
import threading
from tkinter import *
import time
import textwrap
import tkinter as tk
from unidecode import unidecode
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from operator import xor
#importamos la funcion "xor" del modulo "operator", "xor" se utiliza para realizar una operacion de "o exclusivo" en dos operandos booleanos.
import random
import serial
from tkinter import scrolledtext
from serial.tools import list_ports
import threading
import os
import io
from io import open
from tkinter import filedialog
import hamming, decodificar_hamming, hill, cesar ,propio, Generar_ruido,  crear,comunicacionserial

class Chat_personal:
    close_serial = False
    def __init__(self,master):  
        self.master = master
        self.master.title("CHAT PRIVADO/SEGURO COM2")
        self.master.geometry("850x520+100+100")
        self.master.resizable(0, 0)
        self.cont = 0
        self.cont2 = 0        
        
        
        #objetos
        self.chat1 = ''
        self.port_select1 = StringVar()
        self.baud_select1=StringVar()
        self.envia1 = StringVar()
        self.puertoconectado = StringVar()
        self.nickname = StringVar()
        self.namemodificado = StringVar()
        self.status = StringVar()
        self.labelestado = StringVar()
        self.hora = StringVar()        
        self.fecha = StringVar()  
        self.datas=StringVar()

        
        self.namemodificado.set("Nickname")
        self.nickname.set("Nickname")
        self.puertoconectado.set("Ninguno")
        self.status.set("Sin conexión")
        self.labelestado.set("Desconectado")
        
        
        ports = serial.tools.list_ports.comports()
        self.port_list = []
        for port in ports:
            self.port_list.append(port.device)
        
        self.frmperfil = Frame(self.master, bg = "#338203",height=50,width=600)
        self.frmperfil.place(height=500, width=300, x=0, y=0)
            #SELECCIONAR PUERTO
        self.lblPort1 = Label(self.frmperfil, text="Puerto:", bg = "#338203", fg = "white", font='Verdana 10')
        self.lblPort1.place(height=23, width=75, x=20, y=5)
        self.cboCOM1 = Combobox(self.frmperfil, values=self.port_list, textvariable=self.port_select1)
        self.cboCOM1.place(height=23, width=80, x=100, y=5)        
        self.cboCOM1.set("Ninguno")
                              #BAUDRATE 
        baudlist=['9600','19200','38400','57600']
        self.lblbaud = Label(self.frmperfil, text="BAUDRATE:", bg = "#338203", fg = "white", font='Verdana 10')
        self.lblbaud.place(height=23, width=75, x=20, y=30)
        self.baud=Combobox(self.frmperfil,values=baudlist)
        self.baud.place(height=23,width=80,x=100,y=30)

              #CIFRADO 
        cifrado=['HILL','CESAR','PROPIO']
        self.tipcifr = Label(self.frmperfil, text="CIFRADO:", bg = "#338203", fg = "white", font='Verdana 10')
        self.tipcifr.place(height=23, width=75, x=20, y=55)
        self.tipocifrado=Combobox(self.frmperfil,values=cifrado)
        self.tipocifrado.place(height=23,width=80,x=100,y=55)

        #NICKNAME
        self.lblname = Label(self.frmperfil, textvariable = self.namemodificado, bg = "#338203", fg = "white", font='Verdana 14', anchor=W)
        self.lblname.place(height=25, width=150, x=20, y=80)

        self.btntitulo = Button(self.frmperfil, text = "Cambiar", bg = "#338203", fg = "white", font='Verdana 9', command=self.cambiar_nombre_Username)
        self.btntitulo.place(height=23, width=76, x=172, y=80)        
               #BUTTON CONECTAR
        #self.btnConn1 = Button(self.frmperfil, text="CONECTAR", width=12, command=self.conectar1, bg = "#338203", fg = "white", font='Verdana 10')
        #self.btnConn1.place(height=23, width=80, x=100, y=110)
                       #BUTTON CONECTAR
        self.btnConn1 = Button(self.frmperfil, text="CONECTAR", width=12, command=self.conectar1, bg = "#338203", fg = "white", font='Verdana 10')
        self.btnConn1.place(height=23, width=80, x=100, y=110)

        #SABER PUERTO CONECTADO
        self.lblmore = Label(self.frmperfil, text="Puerto conectado: ", bg = "#338203", fg = "white", font='Verdana 8',height=1,width=5, anchor=W)
        self.lblmore.place(height=25, width=108, x=20, y=150)
        
        self.lblcom = Label(self.frmperfil, textvariable=self.puertoconectado, bg = "#338203", fg = "white", font='Verdana 8',height=1,width=5)
        self.lblcom.place(height=25, width=50, x=120, y=150)     
        
  

        #BUTTON ABRIR FICHERO
        self.txtabrir = Button(self.frmperfil, text="ABRIR ARCHIVO de TEXTO", width=12, command=self.AbrirFicher, bg = "#338203", fg = "white", font='Verdana 10',state='disabled')
        self.txtabrir.place(height=23, width=80, x=100, y=230)

        #LEYENDA TEXTO RECIBIDO EN CIFRADO TAL
        self.lblcifrado1= Label(self.frmperfil, text="CIFRADO RECIBIENDO: ", bg = "#338203", fg = "white", font='Verdana 8',height=1,width=5, anchor=W)
        self.lblcifrado1.place(height=25, width=200, x=20, y=270)
        
        self.lblcifrado = Label(self.frmperfil, text="NINGUNO", bg = "#338203", fg = "white", font='Verdana 8',height=1,width=5)
        self.lblcifrado.place(height=25, width=80, x=160, y=270) 



        #ESTADO DE CONEXION SERIAL   
        self.lbltitulo = Label(self.frmperfil, text = "Estado", bg = "#338203", fg = "white", font='Verdana 14', anchor=W)
        self.lbltitulo.place(height=30, width=100, x=20, y=180)
        self.lblestado = Label(self.frmperfil, textvariable=self.labelestado, bg = "#338203", fg = "white", font='Verdana 8',height=1,width=5, anchor=W)
        self.lblestado.place(height=30, width=150, x=21, y=205)           


  


        self.frmchat = Frame(self.master, bg = "#F0F0EF")
        self.frmchat.place(height=450, width=600, x=250, y=0)
            
        self.text1 = ScrolledText(self.frmchat, width=70, height=20, state='disabled')
        self.text1.place(height=450, width=600, x=0, y=0)        

        self.frmescribe = Frame(self.master,  bg = "#8FF94F")
        self.frmescribe.place(height=50, width=600, x=250, y=450)
        
        
        self.inText1 = Entry(self.frmescribe, width=40, textvariable=self.envia1)
        self.inText1.place(height=28, width=480, x=28, y=11)

        
        self.btnEnviar1 = Button(self.frmescribe, text="Enviar", width=12, command=self.sendButton, font='Verdana 8',  bg = "#4EBD4C",  fg = "white",state='disabled')
        self.btnEnviar1.place(height=28, width=70, x=508, y=11)
        
        self.text1.insert(tk.END, self.chat1)
                
        # Manejo del boton "X" de la ventana en Windows
        self.master.protocol("WM_DELETE_WINDOW", self.closing)
        
        self.status_bar = Label(self.master, textvariable=self.status,anchor=W, font='Verdana 8',  bg = "#175417",  fg = "white")
        self.status_bar.place(height=20, width=850, x=0, y=500)
        

#        self.inText1.bind("<Return>", self.envia_mensaje1)
        
    def AbrirFicher(self):
        tf = filedialog.askopenfilename(
        initialdir="", 
        title="Open Text file", 
        filetypes=(("Text Files", "*.txt"),)
        )
       
        tf = open(tf)  # or tf = open(tf, 'r')
        data = tf.read()
        data=unidecode(data)
        self.datas.set(data)
        
        self.inText1.insert(tk.END, self.datas.get())
        tf.close()

    def cambiar_nombre_Username(self):
        if (self.cont2==0):
            self.cont2 = 1
            self.btntitulo.config(text="Aceptar")
            self.lblname.destroy()
            self.entname = Entry(self.frmperfil)
            self.entname.place(height=25, width=130, x=20, y=80)            
 
        elif (self.cont2==1):
            self.cont2 = 0
            self.btntitulo.config(text="Cambiar")
            self.namemodificado.set(self.entname.get())
            self.entname.destroy()
            self.lblname = Label(self.frmperfil, textvariable = self.namemodificado, bg = "#338203", fg = "white", font='Verdana 14', anchor=W)
            self.lblname.place(height=30, width=100, x=20, y=80)

    def conectar1(self):
        self.baudrate_select=str(self.baud.get())
        #print("PUERTO Y BAUD: "+str(self.port_select1.get()+"-"+str(self.baudrate_select)))
        try:
            comunicacionserial.available_ports(self.port_select1.get(),str(self.baudrate_select))
            self.labelestado.set("Conexion establecida")
            self.status.set("CONECTADO")
            self.text1.config(state='normal')  
            self.cifrado_tipo =self.tipocifrado.get()
            #deshabilitamos todo
            self.baud.config(state='disable')
            self.cboCOM1.config(state='disable')
            self.tipocifrado.config(state='disable')
            self.btntitulo.config(state='disable')
            self.txtabrir.config(state='normal')
            self.btnEnviar1.config(state='normal')
            self.btnConn1.config(text="CONECTADO", width=12, bg = "#CF0303", fg = "white", font='Verdana 9', command=self.desconectar)
            #th = threading.Thread(target=self.Response_loop, daemon=True)
            #th.start()  
            self.rcv = threading.Thread(target=self.receive) 
            self.rcv.start()
        except:
            print("OCURRIO UN ERROR AL CONECTARSE AL PUERTO")
    
    def conectar(self):
        #if self.cont==0: 
        self.text1.tag_config('blue', foreground='blue')
        self.text1.tag_config('verde', foreground='green')
        try:
            self.baudrate_select=str(self.baud.get())
            self.ser1 = serial.Serial(port=self.port_select1.get(), baudrate=self.baudrate_select)
#                self.text1.insert(END, "Conexion establecida"+ '\n')
            self.labelestado.set("Conexion establecida")
            self.status.set("CONECTADO")
            self.text1.config(state='normal')  
            self.cifrado_tipo =self.tipocifrado.get()
            #deshabilitamos todo
            self.baud.config(state='disable')
            self.cboCOM1.config(state='disable')
            self.tipocifrado.config(state='disable')
            self.btntitulo.config(state='disable')
            self.txtabrir.config(state='normal')
            self.btnEnviar1.config(state='normal')
            self.namemodificado.set(self.entname.get())
            self.btnConn1.config(text="CONECTADO", width=12, bg = "#CF0303", fg = "white", font='Verdana 9', command=self.desconectar)
            #th = threading.Thread(target=self.Response_loop, daemon=True)
            #th.start()    
            self.rcv = threading.Thread(target=self.recibiendo) 
            self.rcv.start()

            return True
        except:
            self.namemodificado.set(self.cboCOM1.get()) 
            self.puertoconectado.set(self.cboCOM1.get())
            self.namemodificado.set("Nickname")  
            self.cont=1
            self.labelestado.set("No se pudo realizar la conexion")
            self.text1.config(state='disabled')                
#                self.text1.insert(END, "No se pudo realizar la conexion"+ '\n')
            self.status.set("Desconectado")
            return False
                

    def desconectar(self):          
            #elif self.cont==1:
            try:
                
                self.ser1.close()
    #            self.text1.insert(END, "Conexion cerrada"+ '\n')
                self.labelestado.set("Conexion cerrada")
                self.puertoconectado.set("Ninguno")
                self.namemodificado.set("Nickname") 
                self.status.set("Desconectado")
                self.text1.config(state='disable') 
                #deshabilitamos todo
                self.baud.config(state='enable')
                self.cboCOM1.config(state='enable')
                self.tipocifrado.config(state='enable')
                self.btntitulo.config(state='normal')
                self.btnEnviar1.config(state='disable')
                self.btnConn1.config(text="CONECTAR", width=12, bg = "#338203", fg = "white", font='Verdana 10',command=self.conectar)
            except:
                print("ocurrio un error al cerrar")


      
    def envia_mensaje1(self):
        try:
            self.hora.set(time.strftime("%H:%M:%S") )
            self.fecha.set(time.strftime("%d/%m/%y"))
            texto_plano = ("  "+ self.namemodificado.get() +": "+self.envia1.get())
            #se envia la data por el puerto

                #ser = serial.Serial(port='COM3',baudrate=str(self.inbaud.get()))
            #ser.close()
            
            if self.cifrado_tipo == 'CESAR':
                texto_plano=unidecode(texto_plano)
                print("ha seleccionado cifrado cesar")
                clave = 3
                print(texto_plano)
                texto_cifrado_cesar = cesar.cifrado_cesar(texto_plano, clave) #self.texto_cifrado_entry.get()
                print('el texto cifrado en cesar es:   '+texto_cifrado_cesar)
                mensaje_cifrado_y_codificado= hamming.hamming(texto_cifrado_cesar)
                encriptado_codificado=" ".join(mensaje_cifrado_y_codificado)+'c'
                print(encriptado_codificado)
                #Estraccion de datos
                data = encriptado_codificado.encode("utf8")
                print(data)
                self.ser1.write(data)
                #print(data)
                self.status.set("Enviado")
    #            self.status.set("Connected")
                cadena=str(self.fecha.get())+" - "+str(self.hora.get()) + '\n'+str(texto_plano)+'\n'+ '\n'
                print(cadena)
                self.text1.insert(tk.END,cadena,'verde')
                #self.text1.insert(tk.END, str(self.fecha.get())+" - "+str(self.hora.get())+ "\n"+ "  "+ self.namemodificado.get() +": "+self.chat1 + self.envia1.get() + '\n'+ '\n','verde')  
                #   Recibir
                self.envia1.set('')
                

            if self.cifrado_tipo=='HILL': 
                #ser.open()
                texto_plano=unidecode(texto_plano)
                print("ha seleccionado cifrado Hill")
                clave = [[13, 17], [10, 16]]
                texto_cifrado_hill= hill.cifradohill(texto_plano, clave)
                print('el texto cifrado en hill es:   '+texto_cifrado_hill)
                mensaje_cifrado_y_codificado= hamming.hamming(texto_cifrado_hill)
                encriptado_codificado=" ".join(mensaje_cifrado_y_codificado)+'h'
                print(encriptado_codificado)
                #Estraccion de datos
                data = encriptado_codificado.encode("utf8")
                print(data)
                self.ser1.write(data)
                #print(data)
                self.status.set("Enviado")
    #            self.status.set("Connected")
                cadena=str(self.fecha.get())+" - "+str(self.hora.get()) + '\n'+str(texto_plano)+'\n'+ '\n'
                print(cadena)
                self.text1.insert(tk.END,cadena,'verde')
                #self.text1.insert(tk.END, str(self.fecha.get())+" - "+str(self.hora.get())+ "\n"+ "  "+ self.namemodificado.get() +": "+self.chat1 + self.envia1.get() + '\n'+ '\n','verde')  
                #   Recibir
                self.envia1.set('')


            if self.cifrado_tipo =='PROPIO':
                texto_plano=unidecode(texto_plano)
                print("ha seleccionado cifrado propio")
                texto_cifrado_propio = propio.cifradopropio(texto_plano)
                mensaje_cifrado_y_codificado=hamming.hamming(texto_cifrado_propio)
                encriptado_codificado=" ".join(mensaje_cifrado_y_codificado)+'p'
                print(encriptado_codificado)
                #Estraccion de datos
                data = encriptado_codificado.encode("utf8")
                print(data)
                self.ser1.write(data)
                #print(data)
                self.status.set("Enviado")
    #            self.status.set("Connected")
                cadena=str(self.fecha.get())+" - "+str(self.hora.get()) + '\n'+str(texto_plano)+'\n'+ '\n'
                print(cadena)
                self.text1.insert(tk.END,cadena,'verde')
                #self.text1.insert(tk.END, str(self.fecha.get())+" - "+str(self.hora.get())+ "\n"+ "  "+ self.namemodificado.get() +": "+self.chat1 + self.envia1.get() + '\n'+ '\n','verde')  
                #   Recibir
                self.envia1.set('')
               
        except:
            #self.text1.insert(END, "No hay conexion a puertos"+ '\n')
            self.labelestado.set("No hay conexion a puertos")

    
    
    def Response_loop(self):
        self.Recibe_dato()
    
     
    
    def Recibe_dato(self):   
        while True:    
            try:
                
                if self.ser1.in_waiting > 0:
                    self.hora.set(time.strftime("%H:%M:%S") )
                    self.fecha.set(time.strftime("%d/%m/%y"))
                    self.data2 = self.ser1.readline()
                    print("MENSAJE : "+str(self.data2))
                    self.status.set("Recibido")
                    #DESCIFRADO CESAR
                    data = self.data2
                    print("el texto es: "+str(data))
                    #La data recibida son bytes y hay que convertirlos
                    string = data.decode('utf-8')
                    print("codigo recibido" +string)
                    texto_recibido=string[:-2]+'\n'
                    print(texto_recibido)
                    print(string[-2])     

                    if string[-2][-1]=='c':
                        print('ha recibido texxto cifrado en cesar')
                        tipocifrado="CESAR"
                        self.lblcifrado.config(text = tipocifrado)
                        #mensaje_recibido= self.texto_cifrado
                        clave = 3
                        codigo_ruido=Generar_ruido.aleatorio(texto_recibido) #mensaje con ruido
                        texto_plano_decodificado=decodificar_hamming.decodificacion(codigo_ruido)
                        texto_plano = cesar.descifrado_cesar(texto_plano_decodificado, clave)
                        dato="usuario2:   "+texto_plano +'\n'
                        print('El codigo recibido es: '+texto_recibido)
                        print('El texto decodificado y descifrado es: '+texto_plano)
                        cadena=str(self.fecha.get())+" - "+str(self.hora.get()) + '\n'+str(texto_plano)+'\n'+ '\n'
                        self.text1.insert(tk.END,cadena,'blue')
                        if len(texto_plano)>=200:
                                print("longitud de texto: "+str(len(texto_plano)))
                                crear.creararchivo(texto_plano)
                    elif string[-2][-1]=='h':
                        print('ha recibido texxto cifrado en hill')
                        tipocifrado="HILL"
                        self.lblcifrado.config(text = tipocifrado)
                        #mensaje_recibido= self.texto_cifrado
                        clave = [[13, 17], [10, 16]]
                        codigo_ruido=Generar_ruido.aleatorio(texto_recibido)
                        texto_plano_decodificado=decodificar_hamming.decodificacion(codigo_ruido)
                        texto_plano=hill.descifrado_hill(texto_plano_decodificado,clave)
                        print('El codigo recibido es: '+texto_recibido)
                        print('El texto decodificado y descifrado es: '+texto_plano)
                        cadena=str(self.fecha.get())+" - "+str(self.hora.get()) + '\n'+str(texto_plano)+'\n'+ '\n'
                        self.text1.insert(tk.END,cadena,'blue')
                        if len(texto_plano)>=200:
                                print("longitud de texto: "+str(len(texto_plano)))
                                crear.creararchivo(texto_plano)
                    elif string[-2][-1]=='p':
                        tipocifrado="PROPIO"
                        self.lblcifrado.config(text = tipocifrado)
                        print('ha recibido texxto cifrado en  propio')
                        #mensaje_recibido= self.texto_cifrado
                        codigo_ruido=Generar_ruido.aleatorio(texto_recibido)
                        texto_plano_decodificado=decodificar_hamming.decodificacion(codigo_ruido)
                        texto_plano=propio.descifrado_propio(texto_plano_decodificado)
                        print('El codigo recibido es: '+texto_recibido)
                        print('El texto decodificado y descifrado es: '+texto_plano)
                        cadena=str(self.fecha.get())+" - "+str(self.hora.get()) + '\n'+str(texto_plano)+'\n'+ '\n'
                        self.text1.insert(tk.END,cadena,'blue')
                        if len(texto_plano)>=200:
                                print("longitud de texto: "+str(len(texto_plano)))
                                crear.creararchivo(texto_plano)
                        else:
                            tipocifrado="OCURRIO UN ERROR"
                            self.text1.insert(tk.END,texto_recibido,'blue')
                            if len(texto_plano)>=200:
                                    print("longitud de texto: "+str(len(texto_plano)))
                                    crear.creararchivo(texto_plano)
                self.master.after(100, self.Response_loop)
                    
                    #strSerial = data2.decode('utf-8')
                    #self.text1.insert(str(self.fecha.get())+" - "+str(self.hora.get()) + "\n"+ self.chat1 + strSerial + '\n'+ '\n')
                #C:\Users\santo\Downloads\Proyecto_Comunicaciones-2version\Proyecto_Comunicaciones-2version\nuevomain.py
            except:
                print("OCURRIO UN ERROR AL RECIBIR EL MENSAJE")
            break
    
    

    def closing(self):
        #cierra puertos seriales
        try:
            if self.ser1.is_open==True:
                self.ser1.close()
            else:
                pass
            self.master.destroy()
        except:
            self.master.destroy()

    def sendButton(self, event=False):
        self.text1.config(state = DISABLED) 
        self.msg = self.envia1.get()
        self.envia1.set('')
        #self.envia1.delete(0, END)
        snd = threading.Thread(target = self.envia_mensaje11); snd.start()
		
	# function to receive messages 
    def receive(self): 
        self.com_port = comunicacionserial.COMPORT
        while True: 
            if not self.close_serial:
                try:
                    message = self.com_port.readline().decode('utf-8')
                    print(message)
                except UnicodeDecodeError:
                    continue
                    
                # insert message to text box
                if message != '':
                    #logging.info(message.strip())
                    self.text1.config(state = NORMAL) 
                    self.text1.insert(END, time.strftime('%d/%m/%Y %H:%M:%S')+' '+message+'\n') 
                    self.text1.config(state = DISABLED) 
                    self.text1.see(END)
                    message = ''
            else:
                print('close serial')
                self.com_port.close()
                break
		
	# function to send messages 
    def envia_mensaje11(self, event=False): 
        self.text1.config(state=DISABLED) 
        if self.msg != '':
            self.name="USUARIO 2"
            message = (f"{self.name}: {self.msg}") 
            self.text1.config(state = NORMAL) 
            self.text1.insert(END, time.strftime('%d/%m/%Y %H:%M:%S')+' '+message+'\n') 
            self.text1.config(state = DISABLED) 
            self.text1.see(END)
            #logging.info(message.strip())
            self.com_port.write(message.encode('UTF-8'))
            self.msg = ''
		
    def just_exit(self, event):
        print("CERRANDO")
        #res = ctypes.pythonapi.PyThreadState_SetAsyncExc(self.rcv.ident, ctypes.py_object(SystemExit))
        #sys.exit()   

root = Tk()
app = Chat_personal(root)
root.mainloop()


