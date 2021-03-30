from tkinter import *
import sqlite3
from tkinter import messagebox
from tkinter import ttk

#Nombre la Base de Datos
db = "timerSIAT.db"

parts = Tk()
parts.iconbitmap('part.ico')
parts.title("Guardar Numero de Parte")
parts.geometry("330x250")

def agregar_numPart():
    if PartNew.get() == '' or tiempoMin.get() == 0 or tiempoMin == '0':
        messagebox.showerror("Error", "Numero de parte no puede estar vacio.")
    else:
        conexion = sqlite3.connect(db)
        cursor = conexion.cursor()
        try:
            cursor.execute(f"INSERT INTO NumPartes VALUES (null, '{PartNew.get()}', {tiempoMin.get()})")
        except sqlite3.IntegrityError:
            respuesta=messagebox.showerror("Error", "Numero de parte ya existe, Desea actualizar el tiempo?")
            if respuesta=='ok':
                cursor.execute(f"UPDATE NumPartes SET tiempo={tiempoMin.get()} WHERE parte='{PartNew.get()}'")

        conexion.commit()
        conexion.close()

        PartNew.set("")
        tiempoMin.set("")  

Label(parts, text = "Numero de Parte  ").place(x = 30,y = 30)  
Label(parts, text = "Tiempo en minutos").place(x = 30, y = 70)

Button(parts,  text = "GUARDAR",
            command = agregar_numPart,
            activebackground = "pink", 
            activeforeground = "blue").place(x = 120, y = 150)  

PartNew = StringVar()
tiempoMin = IntVar()

Entry(parts, textvariable=PartNew ).place(x = 155, y = 30)
Entry(parts, textvariable=tiempoMin).place(x = 155, y = 70)   

# Mostrar la ventana
parts.mainloop()