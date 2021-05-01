import sys
import datetime
import sqlite3
from sqlite3 import Error



import pandas as pd
import time
import datetime
import csv


venta = {}
menu = True
separador = ("-" * 60)
id = 0



while menu:
    print(separador)
    print(separador)
    print("**MENÚ PRINCIPAL**")
    print("1- Registro de venta")
    print("2- Consultar venta ")
    print("3- Reporte de venta por medio de fecha")
    print("4- Salir                ")

    opcion = int(input("¿Qué proceso desea ejecutar? "))

    if opcion == 1:
        opcion1 = True

        while opcion1:
            descripcion = input("Dame su Descripcion Producto: ")
            cantidad_piezas = int(input("Cantidad de piezas: "))
            precio = float(input("Precio del articulo: "))
            total = cantidad_piezas * precio
            print(f"El monto total a pagar es de $ {total}")
            fecha_venta = datetime.date.today()
            id = id + 1
            venta[id] = [fecha_venta,descripcion,cantidad_piezas,precio,total]
            print("Venta registrada correctamente")

            try:
                with sqlite3.connect("ventas.db") as conexion:
                    mi_cursor = conexion.cursor()
                    mi_cursor.execute("CREATE TABLE ventas (Clave INTEGER PRIMARY KEY, descripcion TEXT NOT NULL, cantidad_de_piezas NUMBER NOT NULL, precio NUMBER NOT NULL, fecha_de_venta timestamp);")                
                    fecha_actual = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
                    valores = {"Clave": id, "descripcion": descripcion, "cantidad_de_piezas": cantidad_piezas, "precio": precio, "fecha_de_venta": fecha_actual}
                    mi_cursor.execute("INSERT INTO ventas VALUES(:clave, :descripcion, :cantidad_piezas, :precio, :fecha_actual)", valores)
                    registros = mi_cursor.fetchall()
                    print("Tabla creada")

            except sqlite3.Error as e:
                print (e)
            except Exception:
                print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
            finally:
                if (conexion):
                    conexion.close()
                    print("Se ha cerrado la conexión")


            reg_products = int(input("¿Desea seguir registrando productos? 1-SI / 2-NO: "))

            if reg_products == 2:
                opcion1 = False



    elif opcion == 2:
        ventas = pd.DataFrame(venta,index = ["Fecha de venta","Descripcion","Cantidad de piezas","Precio de articulo","Total de la venta"])
        print(ventas)
        ventas.to_csv (r'Registro-Ventas.csv',index=True, header=True)

    elif opcion == 3:

        materiales_tm = ventas
        montototal=0
        fecha_buscar = input("Cual es la fecha de venta que desea buscar (DD/MM/YYYY): ")
        fecha_resultado = datetime.datetime.strptime(fecha_buscar,"%d/%m/%Y").date()
        FechaDeVenta = materiales_tm.loc["Fecha de venta"]
        print(FechaDeVenta)
        for x in FechaDeVenta:
            if fecha_resultado == x:
                monto = materiales_tm.loc["Total de la venta"]

                print(f"El Monto Total de {fecha_buscar} fue de {monto}")

    elif opcion == 4:
        Alder = False
        print("Salida exitosa del programa")
    else:
        print("La opcion indicada no es valida")


