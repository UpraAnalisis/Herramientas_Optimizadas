#-*- coding: 'utf-8' -*-
import arcpy
import sys
import os
import datetime

def geometria_check(capa,ruta):
    nombre = "errores_%s"%(datetime.datetime.now().strftime("%b_%d_%Y_%H_%M_%S"))
    nombre = nombre.replace(".","")
    gdb=arcpy.CreateFileGDB_management(ruta,nombre)
    registros = int(arcpy.GetCount_management(arcpy.management.CheckGeometry(capa,"%s\\geometria"%(gdb)))[0])
    return str(registros)+";"+"%s\\geometria"%(gdb)

