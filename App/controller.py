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
 """

import config as cf
import model as m
import csv

def initCatalog():
    catalog = m.newCatalog()
    return catalog

def loadData(catalogo):
    file = cf.data_dir + 'UFOS-utf8-small.csv'
    input_file = csv.DictReader(open(file, encoding="utf-8"),
                                delimiter=",")
    for avistamiento in input_file:
        m.addAvistamiento(catalogo, avistamiento)
    return catalogo

def primerosCinco(lista):
    return m.primerosCinco(lista)
    
def ultimosCinco(lista):
    return m.ultimosCinco(lista)

def size(catalog):
    return m.size(catalog)