"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
from DISClib.ADT import map as mp
from DISClib.Algorithms.Sorting import mergesort as msort
from DISClib.ADT import orderedmap as ordmap
import datetime as dtime
from datetime import date, timedelta


def newCatalog():
    catalogo = {'avistamientos': None,
                'cityIndex': None,
                'hourIndex': None}

    catalogo["avistamientos"] = lt.newList()
    catalogo["cityIndex"] = ordmap.newMap(omaptype="RBT", comparefunction=cmpCiudades)
    catalogo["hourIndex"] = ordmap.newMap(omaptype="RBT", comparefunction= cmpHora)
    catalogo["coordIndex"] = ordmap.newMap(omaptype= "RBT", comparefunction= cmpLongitudes)
    catalogo["durationIndex"] = ordmap.newMap(omaptype='RBT',comparefunction=cmpDuracion)
    catalogo['dateIndex'] = ordmap.newMap(omaptype='RBT',comparefunction=cmpDate)
    return catalogo


def addAvistamiento(catalogo,avistamiento):
    lt.addLast(catalogo['avistamientos'], avistamiento)
    NuevaCiudad(catalogo, avistamiento)
    NuevaHora(catalogo, avistamiento)
    CoordIndex(catalogo, avistamiento)
    DuracionIndex(catalogo['durationIndex'], avistamiento)
    FechaIndex(catalogo['dateIndex'],avistamiento)
    return catalogo

def NuevaCiudad(catalogo, avistamiento):
    ciudadIndex = catalogo["cityIndex"]
    ciudad = avistamiento["city"]
    existcity = ordmap.contains(ciudadIndex, ciudad)
    if existcity:
        c_entry = ordmap.get(ciudadIndex, ciudad)["value"]
    else:
        c_entry = lt.newList()
    lt.addLast(c_entry, avistamiento)
    ordmap.put(ciudadIndex, ciudad, c_entry)

def NuevaHora(catalogo, avistamiento):
    horaIndex = catalogo["hourIndex"]
    fecha = dtime.datetime.strptime(avistamiento["datetime"], '%Y-%m-%d %H:%M:%S')
    hora = str(fecha.time())
    existhour = ordmap.contains(horaIndex, hora)
    if existhour:
        h_entry = ordmap.get(horaIndex, hora)["value"]
    else:
        h_entry = lt.newList("SINGLE_LINKED", cmpfunction= cmpTiempos)
    lt.addLast(h_entry, avistamiento)
    ordmap.put(horaIndex, hora, h_entry)

def CoordIndex(catalogo, avistamiento):
    coordIndex=catalogo["coordIndex"]
    longitud=str(round(float(avistamiento["longitude"]), 2)) 
    existlongitud=ordmap.contains(coordIndex, longitud)
    if existlongitud:
        nuevoEntry=ordmap.get(coordIndex, longitud)["value"]
    else:
        nuevoEntry = lt.newList("SINGLE_LINKED", cmpfunction= cmpLatitudes)
    lt.addLast(nuevoEntry, avistamiento)
    ordmap.put(coordIndex, longitud, nuevoEntry)

def DuracionIndex(arb, avistamiento):
    duracion=float(avistamiento['duration (seconds)']) 
    entry=ordmap.get(arb, duracion)
    if entry is None:
        datentry = lt.newList()
        ordmap.put(arb, duracion, datentry)
    else:
        datentry = me.getValue(entry)
    lt.addLast(datentry,avistamiento)

def FechaIndex(arbol, avistamiento):
    dato = avistamiento['datetime']
    fecha = dtime.datetime.strptime(dato, '%Y-%m-%d %H:%M:%S')
    entry = ordmap.get(arbol, fecha.date())
    if entry is None:
        datentry = lt.newList()
        ordmap.put(arbol, fecha.date(), datentry)
    else:
        datentry = me.getValue(entry)
    lt.addLast(datentry,avistamiento)

def cmpLongitudes(longitud1, longitud2):
    if (float(longitud1)==float(longitud2)):
        return 0
    elif (float(longitud1)>float(longitud2)):
        return 1
    else:
        return -1
    
def cmpCiudades(ciudad1, ciudad2):
    if (ciudad1==ciudad2):
        return 0 
    elif (ciudad1>ciudad2):
        return 1
    else:
        return -1

def cmpFechas2(av1, av2):
    fecha1=dtime.datetime.strptime(av1["datetime"], '%Y-%m-%d %H:%M:%S')
    fecha2=dtime.datetime.strptime(av2["datetime"], '%Y-%m-%d %H:%M:%S')
    if (fecha1>fecha2):
        return 0
    else:
        return -1

def cmpHora(hora1, hora2):
    if (hora1==hora2):
        return 0
    elif (hora1>hora2):
        return 1
    else:
        return -1

def cmpTiempos(av1, av2):
    fecha1=dtime.datetime.strptime(av1["datetime"], '%Y-%m-%d %H:%M:%S')
    fecha2=dtime.datetime.strptime(av2["datetime"], '%Y-%m-%d %H:%M:%S')
    if (fecha1.time()>fecha2.time()):
        return 0
    else:
        return -1

def cmpLatitudes(av1, av2):
    l1 = round(float(av1["latitude"]), 2)
    l2 = round(float(av2["latitude"]), 2)
    if (l1 < l2):
        return 0
    else:
        return -1
def cmpDuracion(d1, d2):
    if (d1 == d2):
        return 0
    elif d1 > d2:
        return 1
    return -1
    
def cmpDate(f1, f2):
    if (f1 == f2):
        return 0
    elif f1 > f2:
        return 1
    return -1

def cmpCountryCity(a1,a2):
    c1 = str(a1['country'])
    c2 = str(a2['country'])
    if c1 == '':
        c1 = 'z'
    if c2 == '':
        c2 = 'z'
    if (c1 == c2):
        city1 = str(a1['city'])
        city2 = str(a2['city'])
        if city1 == '':
            city1 = 'z'
        if city2 == '':
            city2 = 'z'
        if (city1 == city2):
            return 0
        elif (city1 > city2):
            return 1
        elif (city1 < city2):
            return -1
    elif c1 > c2:
        return 1
    elif c1 < c2:
        return -1

def primerosCinco(lista):
    return lt.subList(lista,1,5)
    
def ultimosCinco(lista):
    return lt.subList(lista,lt.size(lista)-4,5)

def size(analyzer):
    return lt.size(analyzer['avistamientos'])

def sizeIndex(analyzer, tipo):
    return ordmap.size(analyzer[tipo])

def AvistamientoCiudad(catalog, ciudad_entry):
    exist=ordmap.contains(catalog["cityIndex"], ciudad_entry)
    if exist:
        avist=ordmap.get(catalog["cityIndex"], ciudad_entry)["value"]
    msort.sort(avist, cmpfunction= cmpFechas2)
    return avist

def primerosTres(lista):
    return lt.subList(lista,1,3)
    
def ultimosTres(lista):
    return lt.subList(lista,lt.size(lista)-2,3)

def primerosn(lista,n):
    return lt.subList(lista,1,n)
    
def ultimosn(lista,n):
    return lt.subList(lista,lt.size(lista)-(n-1),n)

def requerimiento2(catalog,minimo,maximo):
    datos=catalog['durationIndex']
    llaves=ordmap.keys(datos,float(minimo),float(maximo))
    i=0
    for llave in lt.iterator(llaves):
        pareja=ordmap.get(datos,llave)
        lista=me.getValue(pareja)
        i+= lt.size(lista)
    primeros=lt.newList()
    j=0
    while j<3:
        llave2=lt.removeFirst(llaves)
        pareja2=ordmap.get(datos,llave2)
        lista2=me.getValue(pareja2)
        msort.sort(lista2,cmpCountryCity)
        for e in lt.iterator(lista2):
            lt.addLast(primeros,e)
        j+=1
    ultimos=lt.newList("LINKED_LIST")
    conteo=0
    while conteo<3:
        llave3=lt.removeLast(llaves)
        pareja3=ordmap.get(datos,llave3)
        lista3=me.getValue(pareja3)
        msort.sort(lista3,cmpCountryCity)
        for el in lt.iterator(lista3):
            lt.addLast(ultimos,el)
        conteo+=1      
    respuesta=lt.newList("LINKED_LIST")
    lt.addLast(respuesta,i)
    lt.addLast(respuesta,primerosn(primeros,3))
    lt.addLast(respuesta,primerosn(ultimos,3))
    return respuesta

def maxKey(analyzer, tipo):
    return ordmap.maxKey(analyzer[tipo])

def maximaDuracion(catalog):
    mapa=catalog['durationIndex']
    llave=ordmap.maxKey(mapa)
    pareja=ordmap.get(mapa,llave)
    valor=me.getValue(pareja)
    num=lt.size(valor)
    respuesta=lt.newList("LINKED_LIST")
    lt.addLast(respuesta,llave)
    lt.addLast(respuesta,num)
    return respuesta