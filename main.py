from tkinter import *
import os
import sqlite3
from tkinter import messagebox
from datetime import datetime
from datetime import timedelta
from datetime import date
import time
from threading import Thread
from tkinter.messagebox import showinfo
import xlsxwriter

#Nombre la Base de Datos
db = "timerSIAT.db"

top = Tk()
top.iconbitmap('selftimer.ico')
top.title("Timmer SIAT")
top.geometry("330x250")

def Crear_DB():
    conexion = sqlite3.connect(db)
    cursor = conexion.cursor()

    try:
        cursor.execute('''CREATE TABLE NumPartes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parte VARCHAR(100) UNIQUE NOT NULL,
                tiempo INTEGER)''')
    except sqlite3.OperationalError:
        print("La tabla de NumPartes ya existe.")
    else:
        print("La tabla de NumPartes se ha creado correctamente.")

    try:
        cursor.execute('''CREATE TABLE log(
                wk VARCHAR(10) ,
                fechahora VARCHAR(100) PRIMARY KEY,
                parte VARCHAR(100), 
                serie VARCHAR(100),
                empleado VARCHAR(100),
                tiempo VARCHAR(10)) ''')
    except sqlite3.OperationalError:
        print("La tabla de log ya existe.")
    else:
        print("La tabla de log se ha creado correctamente.")

    conexion.close()

def Save_NP():
    os.system ("start Num_Parts.exe")
    
def Busca_NP():
    conexion = sqlite3.connect(db)
    cursor = conexion.cursor()
    data = NP.get()
    valor = int
    # Recuperamos un registro de la tabla de usuarios
    cursor.execute(f"SELECT tiempo FROM NumPartes WHERE parte='{data}'")

    usuario = cursor.fetchone()
    if usuario:
        for x in usuario:
            valor = x

        conexion.close()
        time.sleep(1)

        EjecutarTempo(valor)
    else:
        messagebox.showerror("Error", "No se encontro Numero de Parte")
        NP.set("")
        NS.set("")
        NE.set("")
        conexion.close()

    
def EjecutarTempo(minutos):
    if NP.get() == '' or NS.get() == '' or NE.get() == '':
        messagebox.showerror("Error", "Ningún campo debe estar vacio")
    else:
        conexion = sqlite3.connect(db)
        cursor = conexion.cursor()

        now = datetime.now()
        guardarfecha = now.strftime('%d/%m/%Y,%H:%M:%S')
        year = int(now.strftime('%Y'))
        month = int(now.strftime('%m'))
        day = int(now.strftime('%d'))
        week = str(date(year,month,day).isocalendar()[1])
        valorminutos = str(minutos)

        try:
            cursor.execute("INSERT INTO log(wk,fechahora,parte,serie,empleado,tiempo)VALUES(?,?,?,?,?,?)",(week,guardarfecha,NP.get(),NS.get(),NE.get(),valorminutos,))
        except sqlite3.IntegrityError:
            print(f"La categoría 'todo' ya existe.")
        else:
            print(f"Categoría 'todo' creada correctamente.")

            conexion.commit()
        conexion.close()

        NP.set("")
        NS.set("")
        NE.set("")

        if minutos == 9:
            os.system ("start t9.exe")
        elif minutos == 18:
            os.system ("start t18.exe")
        elif minutos == 21:
            os.system ("start t21.exe")
        elif minutos == 60:
            os.system ("start t60.exe")
        else:
            messagebox.showerror("Error", "Ese tiempo no se encuentra registrado, Favor de Contactar a Desarrollo de Pruebas")

def Buscar():
    os.system ("start Buscar_Serie.exe")
    

def reporte():
    report = Tk()
    report.title("Generar Reporte")
    report.iconbitmap('reporte.ico')
    report.geometry("330x250")

    Label(report, text = "Semana   ").place(x = 60, y = 70) 
    semana = StringVar()
    txt=Entry(report, textvariable=semana)
    txt.place(x = 155, y = 70) 

    now = datetime.now()
    year = int(now.strftime('%Y'))

    def reportes():
        conexion = sqlite3.connect(db)
        pas=int(txt.get())

        cursorObj = conexion.cursor()
        cursorObj.execute(f"SELECT fechahora,parte,serie,empleado,tiempo FROM log WHERE wk={pas}")

        usuario = cursorObj.fetchall()

        if usuario:
            workbook = xlsxwriter.Workbook("C:\\ReportesTIMER-SIAT\\Semana_{}_{}.xlsx".format(pas,year))
            worksheet = workbook.add_worksheet()

            row = 1
            col = 0

            worksheet.write(0,0,'Fecha de Prueba')
            worksheet.write(0,1,'Numero de Parte')
            worksheet.write(0,2,'Numero de Serie')
            worksheet.write(0,3,'Empleado')
            worksheet.write(0,4,'Tiempo de Prueba')

            for fec, par, ser, emp, tie in usuario:
                worksheet.write(row, col, fec)
                worksheet.write(row, col +1, par)
                worksheet.write(row, col +2, ser)
                worksheet.write(row, col +3, emp)
                worksheet.write(row, col +4, tie)
                row +=1

            workbook.close()
            respuesta=messagebox.showinfo("Reporte", "Reporte Generado Correctamente en C:\ReportesTIMER-SIAT")
            if respuesta == 'ok':
                report.destroy()
        else:
            negativo=messagebox.showerror("Error", "No se encontro registro de esa Semana")
            if negativo == 'ok':
                report.destroy()

        semana.set("")
        conexion.close()

    Button(report,  text = "GENERAR ARCHIVO",
                command = reportes,
                activebackground = "red", 
                activeforeground = "white").place(x = 110, y = 150,)

    # Mostrar la ventana
    report.mainloop() 

# Crear el menu principal
menubarra = Menu(top)
top.config(menu=menubarra)
menubarra.add_command(label="Agregar NP ", command=Save_NP)
menubarra.add_command(label=" Buscar Serie ", command=Buscar)
menubarra.add_command(label=" Reporte", command=reporte)    


Label(top, text = "Número de Parte   ").place(x = 30,y = 30)  
Label(top, text = "Número de Serie   ").place(x = 30, y = 70)   
Label(top, text = "Número de Empleado").place(x = 30, y = 110)

Button(top,  text = "INICIAR",
            command = Busca_NP,
            activebackground = "red", 
            activeforeground = "white").place(x = 120, y = 150,)  

NP = StringVar()
NS = StringVar()
NE = StringVar()

Entry(top, textvariable=NP).place(x = 155, y = 30)    
Entry(top, textvariable=NS).place(x = 155, y = 70)   
Entry(top, textvariable=NE).place(x = 155, y = 110)  

Crear_DB()

# Mostrar la ventana
top.mainloop()