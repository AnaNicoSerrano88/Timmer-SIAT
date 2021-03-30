import sqlite3
import csv

#Abrimos el archivo CSV
f=open('SIAT.csv','r') 
#Omitimos la linea de encabezado
next(f, None)
reader = csv.reader(f, delimiter=',')

#Crea la BD en la carpeta donde se encuentra el script
sql = sqlite3.connect('timerSIAT.db')
cur = sql.cursor()

#Creamos la tabla si no existe
#cur.execute('''CREATE TABLE IF NOT EXISTS posiciones
#            (posicion int, nombre text, equipo text, tiempo text)''')
#Llenamos la BD con los datos del CSV
rower = 1
for row in reader:
    tempo=int(row[1])
    print (type(tempo))
    #cur.execute(f"INSERT INTO NumPartes (id, parte)VALUES ({rower},'{row[0]}'")
    cur.execute(f"INSERT INTO NumPartes (id, parte, tiempo)VALUES ({rower},{row[0]}, {tempo})")
    rower +=1
    
#Muestro las filas guardadas en la tabla
for row in cur.execute('SELECT * FROM NumPartes'):
    print(row)
'''
for row in reader:
    print(row[1])
    print(type(row[1]))
'''
#Cerramos el archivo y la conexion a la bd
f.close()
sql.commit()
sql.close()