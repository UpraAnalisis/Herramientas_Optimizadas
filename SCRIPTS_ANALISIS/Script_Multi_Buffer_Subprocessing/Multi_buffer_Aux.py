# -*- coding: utf-8 -*-
# --------------------------------------------------------------------
# Multi_Dissolve_Aux.py
# Fecha de creacion: 2016-08-01 08:59:08.00000
# Author: Carlos Mario Cano Campillo
# Email: carlos.cano@upra.gov.co / kanocampillo@gmail.com
# Propietario: Unidad de Planificación Rural Agropecuaria
#
# ---------------------------------------------------------------------
#=====================Librerias==============================#
import arcpy,random, time,os,subprocess, inspect
from multiprocessing import Process
import string
# ------------------------------------------------------------

#=========Variables Globales y de Entorno=====================#

t_inicio=time.clock()# captura el tiempo de inicio del proceso
arcpy.env.workspace = "in_memory"
ws=arcpy.env.workspace
arcpy.env.overwriteOutput = True
verPython32="C:\\Python27\\ArcGIS10.3\\python.exe"
verPython64="C:\\Python27\\ArcGISx6410.3\\python.exe"
scriptAuxiliar="Multi_repair_aux.py"
verPythonfinal=verPython64
comandos=[]
cuadros_no_prioritarios=[]
cuadros_prioritarios=[]
#=========parámetros de entrada=====================#
infea=arcpy.GetParameterAsText(0)
feaGrilla=arcpy.GetParameterAsText(1)
radio=float(arcpy.GetParameterAsText(2))
dissolve_tipo=arcpy.GetParameterAsText(3)
ruta_raiz=arcpy.GetParameterAsText(4)
rango=arcpy.GetParameterAsText(5)

##
##infea=r"C:\Users\carlos.cano\Documents\ArcGIS\Default.gdb\Prediosx"
##feaGrilla=r"C:\Users\carlos.cano\Documents\ArcGIS\Default.gdb\Grilla_prediosx"
##campo="CondicionPredial"
##ruta_raiz=r"X:\Organizacion\borrame\camilo_diss"
##rango="[[1]_[2]_[3]]"

#=====================funciones auxiliares=====================#

def recuperalista(lista):
    b=[]
    rango=lista.replace("[","")
    rango=rango.replace("]","")
    rango = rango.split("_")
    b=map(int,rango)
    return b

def creadirs(numero): # crea los dierctorios de salida del programa
    nombre="Partes"
    if not os.path.exists(ruta_raiz+"\\%s"%(nombre+"\\"+str(numero))):
        os.makedirs(ruta_raiz+"\\%s"%(nombre+"\\"+str(numero)))
    return ruta_raiz+"\\%s"%nombre+"\\"+str(numero)

def crearFGDB(ruta,numero):
    arcpy.CreateFileGDB_management(ruta, "bd"+str(numero)+".gdb")
    return ruta+"\\"+"bd"+str(numero)+".gdb"

def obtenerExtension1(FC,num):
	rows = arcpy.SearchCursor(FC)
	for row in rows:
		if row.getValue("PageNumber")==num:
			extent = row.shape.extent
			return extent

def dissolve(infea,capaSalida,ruta_salida,cuadro):
    capasalidax=(arcpy.Dissolve_management (in_features=infea, out_feature_class=capaSalida,dissolve_field=campo, multi_part="SINGLE_PART"))
    arcpy.CopyFeatures_management(capasalidax,ruta_salida+"\\"+"cuadrox_"+str(cuadro))

def buffer(infea,capaSalida,ruta_salida,cuadro):
    capasalidax=(arcpy.Buffer_analysis (in_features=infea, out_feature_class=capaSalida, buffer_distance_or_field=radio,dissolve_option=dissolve_tipo))
    arcpy.CopyFeatures_management(capasalidax,ruta_salida+"\\"+"cuadrox_"+str(cuadro))



def funcion_principal(rango):
##    nombre_featureEntrada=ws+"\\"+"capaEntrada_"+str(random.randrange(40,5555000))
    nombre_layerEntrada=ws+"\\"+"capaEntrada_"+str(random.randrange(40,5555000))+".lyr"
    layerEntrada=arcpy.MakeFeatureLayer_management(infea,nombre_layerEntrada)
    nombreCapaUpdated=ws+"\\"+"capaUpdated_"+str(random.randrange(0,5000))

    for cuadro in rango:
        print "procesando seccion "+str(cuadro)
        ruta=creadirs(cuadro)
        ruta=crearFGDB(ruta,cuadro)

##        arcpy.env.extent=obtenerExtension1(feaGrilla,cuadro)
        expresion="PageNumber = %s"%str(cuadro)
        nombre_layer_cuadro=ws+"\\"+"cuadro_"+str(random.randrange(0,555555555000))+".lyr"
        cuadroCapa=arcpy.MakeFeatureLayer_management(feaGrilla,nombre_layer_cuadro,expresion)
        seleccionadas=arcpy.SelectLayerByLocation_management(layerEntrada, "HAVE_THEIR_CENTER_IN", cuadroCapa)
        buffer(seleccionadas,nombreCapaUpdated,ruta,cuadro)

#=====================funciones principal=====================#

if __name__ == '__main__':
    print t_inicio
    print "Procesando secciones "+str(recuperalista(rango))
    arcpy.Delete_management("in_memory")
    rango=recuperalista(rango)

##    print rango
    funcion_principal(rango)
    ws=arcpy.env.workspace
    arcpy.Delete_management("in_memory")
    print "proceso Completado en %s Minutos." % ((time.clock() - t_inicio)/60)
