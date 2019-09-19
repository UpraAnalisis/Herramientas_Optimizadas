#-*- coding: 'utf-8' -*-
import arcpy

def sistema_referencia(capa):
    if arcpy.Describe(capa).spatialReference.factoryCode == 3116:
        referencia = True
    else:
        referencia = False
    return referencia


