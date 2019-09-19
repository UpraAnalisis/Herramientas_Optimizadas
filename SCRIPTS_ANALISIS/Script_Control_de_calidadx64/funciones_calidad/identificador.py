#-*- coding: 'utf-8' -*-
import arcpy
import collections


def identificador(capa,campo):
    valores = [x[0] for x in arcpy.da.SearchCursor(capa,campo)]
    repetidos = [item for item, conteo in collections.Counter(valores).items() if conteo >1]
    return repetidos