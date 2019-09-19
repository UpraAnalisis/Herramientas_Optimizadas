#-*- coding: 'utf-8' -*-
import arcpy


def validador_area(capa, area_minima, unidades):
     valores = [x[0] for x in arcpy.da.SearchCursor(capa,["OID@","SHAPE@"]) if x[1].getArea("PLANAR",unidades) < area_minima]
     return valores



