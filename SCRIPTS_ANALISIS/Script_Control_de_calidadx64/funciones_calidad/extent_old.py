#-*- coding: 'utf-8' -*-
import arcpy
import math

def insular(capa):
    mensaje = ""
    extent_capa = arcpy.Describe(capa).extent

    colombia_x_min = 165290.19180000015
    colombia_x_max = 1806815.8903
    colombia_y_min = 23039.05169999972
    colombia_y_max = 1984871.0185000002

    san_andres_x_min = 165290.19180000015
    san_andres_x_max = 1806815.8903
    san_andres_y_min = 23039.05169999972
    san_andres_y_max = 1984871.0185000002

    ecolombia = arcpy.Extent(colombia_x_min, colombia_y_min, colombia_x_max, colombia_y_max, None, None, None, None)
    esan_andres = arcpy.Extent(san_andres_x_min, san_andres_y_min, san_andres_x_max, san_andres_y_max, None, None, None, None)
    ecolombia_width = ecolombia.width
    ecolombia_height = ecolombia.height
    ecolombia_ancho = math.floor(ecolombia_width * ecolombia_height)

    esan_andres_width = esan_andres.width
    esan_andres_height = esan_andres.height
    esan_andres_ancho = math.floor(esan_andres_width * esan_andres_height)

    capa_width = extent_capa.width
    capa_height = extent_capa.height
    capa_ancho = math.floor(capa_width * capa_height)

    if capa_ancho > ecolombia_ancho:
        mensaje = mensaje +"La capa comprende una extensión mayor al área oficial de Colombia,"
    elif capa_ancho == ecolombia_ancho or capa_ancho - ecolombia_ancho <= 2000 :
        mensaje = mensaje +"La capa comprende una extensión igual al área oficial de Colombia,"
    else:
        mensaje = mensaje +"La capa comprende una extensión menor al área oficial de Colombia,"

    if extent_capa.contains(esan_andres):
        mensaje = mensaje +"La capa comprende la extensión de San Andrés"
    else:
        mensaje = mensaje +"La capa no comprende la extensión de San Andrés"


    return mensaje

