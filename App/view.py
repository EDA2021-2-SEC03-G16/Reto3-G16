"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import time
import sys
import controller as c
from DISClib.ADT import list as lt
assert cf


def printMenu():
    print("*******************************************")
    print("              Bienvenido                   ")
    print("1- Cargar información en el catálogo.")
    print("2- Contar avistamientos en una ciudad.")
    print("3- Contar los avistamientos por duración")
    print("4- Contar avistamientos por hora/minutos del día.")
    print("5- Contar avistamientos en un rango de fechas.")
    print("6- Contar avistamientos de una zona geografíca")
    print("0- Salir")
    print("*******************************************")
catalog = None


def printDatos(avistamientos):
    size = lt.size(avistamientos)
    if size>0:
        for avistamiento in lt.iterator(avistamientos):
            if avistamiento is not None:
                print (avistamiento)
                print('\n')
    else:
        print ("No se encontraron datos.")
    

def printReq1(catalogo, ciudad):
    city=c.AvistamientoCiudad(catalogo, ciudad.lower())
    primeros=c.primerosTres(city)
    ultimos=c.ultimosTres(city)
    total=c.sizeIndex(catalogo, "indexCiudad")
    print("Hay en total " + str(total) + " ciudades diferentes con UFO sightings..." + "\n")
    print("En " +ciudad+ " hay " + str(lt.size(city)) + " avistamientos.")    
    print('Los 3 primeros: \n')
    printDatos(primeros)
    print('Los 3 ultimos: \n') 
    printDatos(ultimos)


def printReq2(catalogo,minimo,maximo):
    max=c.maximaDuracion(catalogo)
    lmax=lt.removeFirst(max)
    nmax=lt.removeFirst(max)
    datos=c.requerimiento2(catalogo,minimo,maximo)
    rango=lt.removeFirst(datos)
    primeros=lt.removeFirst(datos)
    ultimos=lt.removeFirst(datos)
    print("El numero de avistamientos con la duracion (seg) mas larga registrada " + str(lmax) + " es: " + str(nmax))
    print("El numero de avistamientos en el rango " + str(minimo) + ", " + str(maximo) + " es: " + str(rango))
    print("Primeros 3 en el rango son: ")
    printDatos(primeros)
    print("Ultimos 3 en el rango son: ")
    printDatos(ultimos)


def printReq3(catalogo, hora_i, hora_f):
    hora=c.maxKey(catalogo, "hourIndex")
    tamanio=lt.size(c.avistamientoHora(catalogo, hora))
    orden=c.avistamientoOrdenadoHora(catalogo, hora_i, hora_f)
    primeros=c.primerosTres(orden)
    ultimos=c.ultimosTres(orden)
    print("Hay " + str(c.sizeIndex(catalogo, "hourIndex")) + " UFO en los tiempos consultados.\n")
    print("El último avistamiento en el tiempo es: " +str(hora) + ":" + str(tamanio) + "\n")
    print("Hay " + str(lt.size(orden)) + " avistamientos el rango " + hora_i + " y " + hora_f+'\n') 
    print('Primeros 3 en el rango: ')
    printDatos(primeros)
    print('Ultimos 3 en el rango: ') 
    printDatos(ultimos)

def printReq4(catalogo,fecha1,fecha2):
    fecha=c.fechaAntigua(catalogo)
    f1=lt.removeFirst(fecha)
    f2=lt.removeFirst(fecha)
    datos=c.requerimiento4(catalogo,fecha1,fecha2)
    rango=lt.removeFirst(datos)
    primeros=lt.removeFirst(datos)
    ultimos=lt.removeFirst(datos)
    print("Avistamientos con la fecha mas antigua registrada " + str(f1) + " es: " + str(f2))
    print("Hay " + str(rango)+" avistamientos en el rango " + str(fecha1) + " y " + str(fecha2))
    print("Primeros 3 avistamientos: ")
    printDatos(primeros)
    print("Ultimos 3 avistamientos: ")
    printDatos(ultimos)

def printReq5(catalogo, longitud1, longitud2, latitud1, latitud2):
    lista=c.avistamientoLatLong(catalogo, longitud1, longitud2, latitud1, latitud2)
    tamanio=lt.size(lista)
    primeros=c.primerosCinco(lista)
    ultimos=c.ultimosCinco(lista)
    print("Hay " + str(tamanio) + " avistamientos en la latitud y longitud seleccionadas.\n")
    print('Primeros 5 avistamientos: ')
    printDatos(primeros)
    print('Ultimos 5 avistamientos: ')
    printDatos(ultimos)


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        start_time = time.process_time()
        catalogo=c.initCatalog()
        c.loadData(catalogo)
        lista=catalogo['avistamientos']
        primeros=c.primerosCinco(lista)
        ultimos=c.ultimosCinco(lista)
        print('Archivos cargados: ' + str(c.size(catalogo)))
        print('\n')
        print('Primeros 5 datos: \n')
        printDatos(primeros)
        print('Ultimos 5 datos: \n') 
        printDatos(ultimos)
        stop_time=time.process_time()
        elapsed_time_mseg=(stop_time - start_time)*1000
        print("Tiempo empleado: " + str(elapsed_time_mseg))

    elif int(inputs[0]) == 2:
        ciudad=input("Ingrese la ciudad a consultar: ")
        start_time=time.process_time()
        printReq1(catalogo, ciudad)
        stop_time=time.process_time()
        elapsed_time_mseg=(stop_time - start_time)*1000
        print("Tiempo empleado: " + str(elapsed_time_mseg))

    elif int(inputs[0]) == 3:
        min=input("Ingrese la minima duración: ")
        max=input("Ingrese la maxima duración: ")
        start_time=time.process_time()
        printReq2(catalogo,min,max)
        stop_time=time.process_time()
        elapsed_time_mseg=(stop_time - start_time)*1000
        print("Tiempo empleado: " + str(elapsed_time_mseg))

    elif int(inputs[0]) == 4:
        hora_i=input("Hora minima (HH:MM): ")
        hora_f=input("Hora maxima (HH:MM): ")
        start_time=time.process_time()
        printReq3(catalogo, hora_i, hora_f)
        stop_time=time.process_time()
        elapsed_time_mseg=(stop_time - start_time)*1000
        print("Tiempo empleado: " + str(elapsed_time_mseg))

    elif int(inputs[0]) == 5:
        fecha1=input("Fecha inicial(YYYY-MM-DD): ")
        fecha2=input("Fecha final (YYYY-MM-DD): ")
        start_time=time.process_time()
        printReq4(catalogo,fecha1,fecha2)
        stop_time=time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print("Tiempo empleado: " + str(elapsed_time_mseg))
    
    elif int(inputs[0]) == 6:
        longitud1=input("Ingrese la longitud inicial: ")
        longitud2=input("Ingrese la longitud final: ")
        latitud1=input("Ingrese la latitud inicial: ")
        latitud2=input("Ingrese la latitud final: ")
        start_time=time.process_time()
        printReq5(catalogo, longitud1, longitud2, latitud1, latitud2)
        stop_time=time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print("Tiempo empleado: " + str(elapsed_time_mseg))
    else:
        sys.exit(0)
sys.exit(0)