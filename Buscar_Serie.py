import sqlite3
from tkinter import *
from tkinter import messagebox

#Nombre la Base de Datos
db = "timerSIAT.db"

busca = Tk()
busca.iconbitmap('buscar.ico')
busca.title("Buscar Numero de Serie")
busca.geometry("330x250")

uno=Label(busca, text=" ")
uno.place(x = 30, y = 70)
dos=Label(busca, text=" ")
dos.place(x = 155, y = 70)   
tres=Label(busca, text=" " )
tres.place(x = 30, y = 110)
cuatro=Label(busca, text=" ")
cuatro.place(x = 155, y = 110)
cinco=Label(busca, text=" " )
cinco.place(x = 30, y = 150)
seis=Label(busca, text=" ")
seis.place(x = 155, y = 150)

def Busca_Serial():
    if NSerie.get() == '':
        messagebox.showerror("Error", "Ingresa un Numero de Serie")
    else:
        conexionbuscar = sqlite3.connect(db)
        cursorbuscar = conexionbuscar.cursor()
        data = NSerie.get()

        cursorbuscar.execute(f"SELECT fechahora,empleado,tiempo FROM log WHERE serie='{data}'")
        usuario = cursorbuscar.fetchone()
        if usuario:
            uno.configure(text="Fecha de Prueba")
            dos.configure(text="  "+str(usuario[0]))
            tres.configure(text="Numero de Empleado")
            cuatro.configure(text="  "+str(usuario[1]))
            cinco.configure(text="Tiempo de Prueba")
            seis.configure(text="  "+str(usuario[2]))
        else:
            uno.configure(text=" ")
            dos.configure(text=" ")
            tres.configure(text=" ")
            cuatro.configure(text=" ")
            cinco.configure(text=" ")
            seis.configure(text=" ")
            messagebox.showerror("Error", "No se encontro Numero de Serie")
            
        conexionbuscar.close()
        busca.mainloop()
    
def Limpiar():
    uno.configure(text=" ")
    dos.configure(text=" ")
    tres.configure(text=" ")
    cuatro.configure(text=" ")
    cinco.configure(text=" ")
    seis.configure(text=" ")

NSerie = StringVar()

Label(busca, text = "Numero de Serie   ").place(x = 30,y = 30)
Entry(busca, textvariable=NSerie).place(x = 155, y = 30)

Button(busca, text = "BUSCAR",
            command = Busca_Serial,
            activebackground = "green", 
            activeforeground = "white").place(x = 50, y = 190)  
Button(busca,text = "BORRAR",
            command = Limpiar,
            activebackground = "RED", 
            activeforeground = "white").place(x = 250, y = 190) 

   
Label(busca).place(x = 155, y = 70)   
Label(busca).place(x = 155, y = 110)   

# Mostrar la ventana
busca.mainloop()