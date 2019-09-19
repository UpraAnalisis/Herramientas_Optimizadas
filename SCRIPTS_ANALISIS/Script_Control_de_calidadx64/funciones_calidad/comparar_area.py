#-*- coding: utf-8 -*-

import arcpy

def comparar_areas(capa_original, capa_validacion,area_val,unidades):
    datos_area_original = [x[0].getArea("PLANAR",unidades) for x in arcpy.da.SearchCursor(capa_original,"SHAPE@")]
    area_original = sum(datos_area_original)
    datos_area_validacion = [x[0].getArea("PLANAR",unidades) for x in arcpy.da.SearchCursor(capa_validacion,"SHAPE@")]
    area_validacion = sum(datos_area_validacion)
    diferencia = area_original - area_validacion
    return diferencia

