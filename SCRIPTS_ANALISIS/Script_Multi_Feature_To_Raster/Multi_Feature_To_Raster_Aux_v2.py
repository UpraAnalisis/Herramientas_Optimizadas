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
import arcpy,random, time,os,subprocess, inspect,exceptions
import string
# ------------------------------------------------------------

#=========Variables Globales y de Entorno=====================#
try:
    t_inicio=time.clock()# captura el tiempo de inicio del proceso
    arcpy.env.workspace = "in_memory" # fija el espacio de trabajo en memoria
    ws=arcpy.env.workspace # variable que almacena el espacio de trabajo
    arcpy.env.overwriteOutput = True # fija la variable de entrorno para sobrescribir resultados
    #=========parámetros de entrada=====================#
    in_features=arcpy.GetParameterAsText(0)
    raster_salida =arcpy.GetParameterAsText(1)
    feaGrilla=arcpy.GetParameterAsText(2) # paráetro que almacena la feture class de la grilla auxiliar
    ruta_raiz =arcpy.GetParameterAsText(3)
    campo=arcpy.GetParameterAsText(4) # parámetro que almacena el campo por el cual se realizará el dissolve
    cell_size=float(arcpy.GetParameterAsText(5))
    rango=arcpy.GetParameterAsText(6) # contiene los cuadros de la grilla qeu serán procesados
    #=====================funciones auxiliares=====================#

    def recuperalista(lista): # función que recupera el listado de los cuadros a procesar
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

    def crearFGDB(ruta,numero): # crea una file geodatabase de la sección procesada
        arcpy.CreateFileGDB_management(ruta, "bd"+str(numero)+".gdb")
        return ruta+"\\"+"bd"+str(numero)+".gdb"

    def obtenerExtension1(FC,num): # función que obtiene el extent del cuadro a procesar
    	rows = arcpy.SearchCursor(FC)
    	for row in rows:
    		if row.getValue("PageNumber")==num:
    			extent = row.shape.extent
    			return extent


    def featureToRaster(inFeature,outRaster,cellSize,field):
        raster_naturales=arcpy.FeatureToRaster_conversion(inFeature, field, outRaster, cellSize)


    def funcion_principal(rango): # función principal que unificatodo el proceso

        for cuadro in rango: # ciclo que realiza el procesamiento de cada uno de los cuadros del listado
                print "procesando seccion "+str(cuadro) # imprime el mensaje que indica la sección en proceso
                ruta=creadirs(cuadro) # crea el directorio de salida de la sección procesada
                ruta=crearFGDB(ruta,cuadro) # crea una file geodatabase de salida de la sección procesada

                arcpy.env.extent=obtenerExtension1(feaGrilla,cuadro) # captura la extensión del cuadro a procesar

                featureToRaster(in_features,ruta+"\\"+"cuadrox_"+str(cuadro),cell_size,campo)



    #=====================funciones principal=====================#

    if __name__ == '__main__':
        print t_inicio
        print "Procesando secciones "+str(recuperalista(rango)) # imprime el listado de secciones a procesar
        arcpy.Delete_management("in_memory") # fija el espacio de trabajo en memoria
        rango=recuperalista(rango) # recupera la lista de cuadros a procesar enviada por el script principal

        funcion_principal(rango) # ejecuta la función principal
        ws=arcpy.env.workspace # almacena el workspace
        arcpy.Delete_management("in_memory") # borra el espacio de trabajo en memoria
        print "proceso Completado en %s Minutos." % ((time.clock() - t_inicio)/60) # imprime el tiempo de ejecuación del script

except exceptions.Exception as e:
    print e.__class__, e.__doc__, e.message
    os.system("pause")

