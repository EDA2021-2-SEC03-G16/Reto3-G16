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

def Requerimiento1(catalogo, ciudad):
    city=c.AvistamientoCiudad(catalogo, ciudad.lower())
    primeros=c.primerosTres(city)
    ultimos=c.ultimosTres(city)
    total=c.sizeIndex(catalogo, "cityIndex")
    print("Hay en total " + str(total) + " ciudades diferentes con UFO sightings..." + "\n")
    print("En " +ciudad+ " hay " + str(lt.size(city)) + " avistamientos.")    
    print('Los 3 primeros: \n')
    printDatos(primeros)
    print('Los 3 ultimos: \n') 
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
        lst = catalogo['avistamientos']
        primeros=c.primerosCinco(lst)
        ultimos=c.ultimosCinco(lst)
        print('Archivos cargados: ' + str(c.size(catalogo)))
        print('\n')
        print('Primeros 5 datos: \n')
        printDatos(primeros)
        print('Ultimos 5 datos: \n') 
        printDatos(ultimos)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print("Tiempo empleado: " + str(elapsed_time_mseg))

    elif int(inputs[0]) == 2:
        ciudad = input("Ingrese la ciudad a consultar: ")
        start_time = time.process_time()
        Requerimiento1(catalogo, ciudad)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print("Tiempo de ejecución: " + str(elapsed_time_mseg))
    else:
        sys.exit(0)
sys.exit(0)
