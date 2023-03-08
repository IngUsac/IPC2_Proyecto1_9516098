import tkinter as tk
import xml.etree.ElementTree as ET
from ClassMuestra import Muestras
from ClassCeldas import Celdas
from MatrizMuestra import MatrizMuestras
import sys
import os
import random
from tkinter import messagebox
from tkinter import filedialog
from idlelib.tooltip import Hovertip
from os import system, startfile
from tkinter import *       #Interfas Grafica
from tkinter.ttk import *
from tkinter.messagebox import *
from escrituraxml import Escritor
from Graficar import GeneradorGrafico

def globales():
    global archEntrada
    archEntrada={}
    global arch1
    arch1=tk.StringVar()
    global arch

vPrincipal = tk.Tk()
vPrincipal.title("Menu Principal")
vPrincipal.geometry("500x250")

class msj_emergente(Hovertip):
    def showcontents(self):
        lbl = tk.Label(
            self.tipwindow, text=f' "{self.text}" ', justify=tk.LEFT, bg="gray", fg="black", relief=tk.SOLID, borderwidth=1,font=("Times New Roman", 10)
            )
        lbl.pack()

arch1=tk.StringVar()

def Color():
        no=random.randint(1,15777215)
        aleatory=str(hex(no))
        return "#"+aleatory[2:]

def GetColor(listamuestras,muestra):
        for item in listamuestras:
            if muestra==item.codigo:
                return item.color

def cargaXML():    # Carga archivo XML de entrada
    global archEntrada
    global arch1
    archEntrada={}
    arch1=filedialog.askopenfilename(initialdir = "/",title = "Seleccione el Archivo de Entrada XML",filetypes = (("extension .xml ","*.xml"),("Todos los Archivos","*.*")))
    ListaEspecimenes=[]
    ListaMatrices=[]
    os.system('cls')
    try:
        archxml=open(arch1)
        #print(archxml.read()) #imprime la estructura del xml
        if archxml.readable():
            datoxml= ET.parse(arch1).getroot()
            organ=datoxml.iter('organismo')
            for element in organ:
                ListaEspecimenes.append(Muestras(element.findtext('codigo'),element.findtext('nombre'),Color()))
            
            listaMuestras=datoxml.iter('muestra')
            for muestra in listaMuestras:
                temporal=MatrizMuestras()
                temporal.DefinirTamano(int(muestra.findtext('filas')),int(muestra.findtext('columnas')))
                celdasvivas=muestra.iter('celdaViva')
                for viva in celdasvivas:
                    temporal.AgregarInformacion(int(viva.findtext('fila')),int(viva.findtext('columna')),Celdas(viva.findtext('codigoOrganismo'),GetColor(ListaEspecimenes,viva.findtext('codigoOrganismo'))))
                diccionario={
                    "filas":muestra.findtext('filas'),
                    "columnas":muestra.findtext('columnas'),
                    "codigo":muestra.findtext('codigo'),
                    "descripcion":muestra.findtext('descripcion'),
                    "matriz":temporal
                }
                
                ListaMatrices.append(diccionario)

        else:
            print(False)
    except Exception as err:
        print("Error:",err)
    finally:
            archxml.close()
    if arch1!="":
        Label(vPrincipal,text ="El archivo actual cargado en Memoria es :",foreground="blue").place(x=20,y=160)
        Label(vPrincipal,text =arch1,foreground="green").place(x=20,y=190)
        Label(vPrincipal,text ="Puede seleccionar otro archivo de entrada cuando lo desee...",foreground="blue").place(x=20,y=220)
        messagebox.showinfo(title="Cargando Archivo...",message="El archivo fue cargado con exito !!!")
    archEntrada= {"ListaEspecimenes":ListaEspecimenes,"ListaMatrices":ListaMatrices}
    


def GeneraXML():
 
     Escritor.Escritura(archEntrada)

def graficaResultados():
  
    GeneradorGrafico.Graficar(archEntrada)

def salir():
    messagebox.showinfo("Finalizando...","Fue un gusto servirle !!!")  
    sys.exit()    


globales()

lbl=Label(vPrincipal,text ="Menu Principal\n",foreground="blue").place(x=100,y=10)
btn1 = tk.Button(vPrincipal, text="Cargar Archivo",command=cargaXML)
btn1.place(x=30,y=40)
msj_emergente(btn1, text="Carga archivo XML de entrada", hover_delay=100)

btn2 = tk.Button(vPrincipal, text="Guardar resultados en archivo",command=GeneraXML)
btn2.place(x=30,y=70)
msj_emergente(btn2, text="Genera Archivo XML de Salida", hover_delay=100)

btn3 = tk.Button(vPrincipal, text="Ver Resultados",command=graficaResultados)
btn3.place(x=30,y=100)
msj_emergente(btn3, text="Genera grafica de los resultados", hover_delay=100)

btn4 = tk.Button(vPrincipal, text="Salir",command=salir)
btn4.place(x=30,y=130)
msj_emergente(btn4, text="Se cierra la aplicación", hover_delay=100)


vPrincipal.mainloop()