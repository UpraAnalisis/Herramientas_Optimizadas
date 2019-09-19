#-*- coding: 'utf-8' -*-
import arcpy
import sys
import os
from funciones_calidad.check_sde import *

def nombre_capa(capa):
    mensaje =""
    errores = []
    if checkSDE(capa) == True: ##FUNCION PARA VALIDAR SI ESTA EN GEODATABASE CORPORATIVA
        tamanio = len(arcpy.Describe(capa).name.split("."))
        ubication_name = tamanio - 1
        nombre = [x for x in arcpy.Describe(capa).name.split(".")[ubication_name]]

    else:
        nombre = [x for x in arcpy.Describe(capa).name]

    diccionario ='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_0123456789'
    if len(nombre) > 30:
        mensaje =mensaje +"El nombre de la capa excede los 30 caracteres\n"

    [errores.append(x) for x in nombre if x not in diccionario]

    if len(errores) > 0:
       mensaje =mensaje +"Los siguientes caracteres no están permitidos %s"%((" ".join(errores)))
    return mensaje
