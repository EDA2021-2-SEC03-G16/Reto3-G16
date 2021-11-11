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
assert cf
from DISClib.Algorithms.Sorting import mergesort as msort
from DISClib.ADT import orderedmap as ordmap
import datetime as dtime
from datetime import date, timedelta


def newCatalog():
    catalogo = {'avistamientos': None,
                'indexCiudad': None,
                'hourIndex': None}

    catalogo["avistamientos"]=lt.newList()
    catalogo["indexCiudad"]=ordmap.newMap(omaptype="RBT", comparefunction=cmpCiudades)
    catalogo["hourIndex"]=ordmap.newMap(omaptype="RBT", comparefunction= cmpHora)
    catalogo["coordIndex"]=ordmap.newMap(omaptype= "RBT", comparefunction= cmpLongitudes)
    catalogo["indexDuracion"]=ordmap.newMap(omaptype='RBT',comparefunction=cmpDuracion)
    catalogo['dateIndex']=ordmap.newMap(omaptype='RBT',comparefunction=cmpDate)
    return catalogo


def addAvistamiento(catalogo,avistamiento):
    lt.addLast(catalogo['avistamientos'], avistamiento)
    NuevaCiudad(catalogo, avistamiento)
    NuevaHora(catalogo, avistamiento)
    CoordIndex(catalogo, avistamiento)
    DuracionIndex(catalogo['indexDuracion'], avistamiento)
    FechaIndex(catalogo['dateIndex'],avistamiento)
    return catalogo

def NuevaCiudad(catalogo, avistamiento):
    ciudadIndex = catalogo["indexCiudad"]
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
    elongitud=ordmap.contains(coordIndex, longitud)
    if elongitud:
        nuevoEntry=ordmap.get(coordIndex, longitud)["value"]
    else:
        nuevoEntry = lt.newList("SINGLE_LINKED", cmpfunction= cmpLatitudes)
    lt.addLast(nuevoEntry, avistamiento)
    ordmap.put(coordIndex, longitud, nuevoEntry)

def DuracionIndex(arb, avistamiento):
    duracion=float(avistamiento['duration (seconds)']) 
    entrada=ordmap.get(arb, duracion)
    if entrada is None:
        fechaentry = lt.newList()
        ordmap.put(arb, duracion, fechaentry)
    else:
        fechaentry = me.getValue(entrada)
    lt.addLast(fechaentry,avistamiento)

def FechaIndex(arb, avistamiento):
    dato=avistamiento['datetime']
    fecha=dtime.datetime.strptime(dato, '%Y-%m-%d %H:%M:%S')
    entrada=ordmap.get(arb, fecha.date())
    if entrada is None:
        fechaentry = lt.newList()
        ordmap.put(arb, fecha.date(), fechaentry)
    else:
        fechaentry = me.getValue(entrada)
    lt.addLast(fechaentry,avistamiento)

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

def cmpTiempos(dato1, dato2):
    fecha1=dtime.datetime.strptime(dato1["datetime"], '%Y-%m-%d %H:%M:%S')
    fecha2=dtime.datetime.strptime(dato2["datetime"], '%Y-%m-%d %H:%M:%S')
    if (fecha1.time()>fecha2.time()):
        return 0
    else:
        return -1

def cmpLatitudes(dato1, dato2):
    latitud1 = round(float(dato1["latitude"]), 2)
    latitud2 = round(float(dato2["latitude"]), 2)
    if (latitud1<latitud2):
        return 0
    else:
        return -1
    
def cmpDuracion(duracion1, duracion2):
    if (duracion1==duracion2):
        return 0
    elif duracion1>duracion2:
        return 1
    return -1
    
def cmpDate(fecha1, fecha2):
    if (fecha1==fecha2):
        return 0
    elif fecha1>fecha2:
        return 1
    return -1

def cmpCountryCity(dato1,dato2):
    country1=str(dato1['country'])
    country2=str(dato2['country'])
    if country1=='':
        country1='z'
    if country2=='':
        country2='z'
    if (country1==country2):
        city1=str(dato1['city'])
        city2=str(dato2['city'])
        if city1=='':
            city1='z'
        if city2=='':
            city2='z'
        if (city1==city2):
            return 0
        elif (city1>city2):
            return 1
        elif (city1<city2):
            return -1
    elif country1>country2:
        return 1
    elif country1<country2:
        return -1

def primerosCinco(lista):
    return lt.subList(lista,1,5)
    
def ultimosCinco(lista):
    return lt.subList(lista,lt.size(lista)-4,5)

def size(analyzer):
    return lt.size(analyzer['avistamientos'])

def sizeIndex(analyzer, tipo):
    return ordmap.size(analyzer[tipo])

def AvistamientoCiudad(catalogo, ciudad):
    existe=ordmap.contains(catalogo["indexCiudad"], ciudad)
    if existe:
        avistamiento=ordmap.get(catalogo["indexCiudad"], ciudad)["value"]
    msort.sort(avistamiento, cmpfunction= cmpFechas2)
    return avistamiento

def primerosTres(lista):
    return lt.subList(lista,1,3)
    
def ultimosTres(lista):
    return lt.subList(lista,lt.size(lista)-2,3)

def primerosn(lista,n):
    return lt.subList(lista,1,n)

def requerimiento2(catalogo,min,max):
    datos=catalogo['indexDuracion']
    llaves=ordmap.keys(datos,float(min),float(max))
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

def maximaDuracion(catalogo):
    map=catalogo['indexDuracion']
    llave=ordmap.maxKey(map)
    pareja=ordmap.get(map,llave)
    valor=me.getValue(pareja)
    numero=lt.size(valor)
    respuesta=lt.newList("LINKED_LIST")
    lt.addLast(respuesta,llave)
    lt.addLast(respuesta,numero)
    return respuesta

def avistamientoHora(catalogo, hora):
    existe=ordmap.contains(catalogo["hourIndex"], hora)
    if existe:
        i=ordmap.get(catalogo["hourIndex"], hora)["value"]
    return i

def avistamientoHora2(catalogo, hora, orden):
    existe=ordmap.contains(catalogo["hourIndex"], hora)
    if existe:
        avist=ordmap.get(catalogo["hourIndex"], hora)["value"]
        for i in lt.iterator(avist):
            lt.addLast(orden, i)

def avistamientoOrdenadoHora(catalogo, hora_i, hora_f):
    orden=lt.newList()
    hora1=dtime.datetime.strptime(hora_i,"%H:%M")
    hora2=dtime.datetime.strptime(hora_f,"%H:%M")
    tiempototal=(hora2-hora1)
    h=str(tiempototal)
    hh, mm, ss = h.split(':')
    delta=int(hh)*60+int(mm)+int(ss)*0
    for minute in range(delta + 1):
        dia_nuevo=hora1+dtime.timedelta(minutes=minute)
        hora_nueva=dia_nuevo.strftime("%H:%M:%S")
        avistamientoHora2(catalogo, str(hora_nueva), orden)
    return orden

def requerimiento4(catalogo,minimo,maximo):
    datos=catalogo['dateIndex']
    llaves=ordmap.keys(datos,date.fromisoformat(minimo),date.fromisoformat(maximo))
    i=0
    for llave in lt.iterator(llaves):
        pareja=ordmap.get(datos,llave)
        lista=me.getValue(pareja)
        i+=lt.size(lista)
    primeros=lt.newList()
    j=0
    while j<3:
        llave2=lt.removeFirst(llaves)
        pareja2=ordmap.get(datos,llave2)
        lista2=me.getValue(pareja2)
        for e in lt.iterator(lista2):
            lt.addLast(primeros,e)
        j+=1
    ultimos=lt.newList("LINKED_LIST")
    contador=0
    while contador<3:
        llave3=lt.removeLast(llaves)
        pareja3=ordmap.get(datos,llave3)
        lista3=me.getValue(pareja3)
        for el in lt.iterator(lista3):
            lt.addLast(ultimos,el)
        contador+=1      
    respuesta=lt.newList("LINKED_LIST")
    lt.addLast(respuesta,i)
    lt.addLast(respuesta,primerosn(primeros,3))
    lt.addLast(respuesta,primerosn(ultimos,3))
    return respuesta

def minKey(analyzer, tipo):
    return ordmap.minKey(analyzer[tipo])

def fechaAntigua(catalogo):
    mapa=catalogo['dateIndex']
    llave=ordmap.minKey(mapa)
    pareja=ordmap.get(mapa,llave)
    valor=me.getValue(pareja)
    num=lt.size(valor)
    respuesta = lt.newList("LINKED_LIST")
    lt.addLast(respuesta,llave)
    lt.addLast(respuesta,num)
    return respuesta