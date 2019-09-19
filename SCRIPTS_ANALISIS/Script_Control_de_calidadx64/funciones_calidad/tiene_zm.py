#-*- coding: 'utf-8' -*-
import arcpy


def tiene_z(capa):
    return arcpy.Describe(capa).hasZ

def tiene_m(capa):
    return arcpy.Describe(capa).hasM
