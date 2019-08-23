# -*- coding: utf-8 -*-
# --------------------------------------------------------------------
# asignar_simbologia.py
# Fecha de creacion: 2017-05-23 01:45:08.00000
# Author: Carlos Mario Cano Campillo, Wilmar Fernando Pineda Rojas
# Email: carlos.cano@upra.gov.co / wilmar.pineda@upra.gov.co
# Propietario: Unidad de Planificación Rural Agropecuaria
#######################################################################
##Este Script tienen como objetivo realizar una clasificación por medio de intervalos geométricos.
##El usuario debe especificar el campo de valores para construir los intervalos, un
##conjunto de nombres de clases separados por ";" (sin comillas) y por último,
##el campo en donde se asignarán estas clases.
##Este script debe usarse dentro de ArcMap, ya que necesita la interfaz de mapa para contruir una simbología.
# ---------------------------------------------------------------------
#=====================Librerias==============================#
import arcpy, os ,inspect, sys
# ------------------------------------------------------------

#=====================Parámetros==============================#
layer = arcpy.GetParameterAsText(0).encode("utf-8") # FeatureLayer sobre el cual se construirán los intervalos de clases geométricos y se asignarán las clases.
campo_clasificacion = arcpy.GetParameterAsText(1) # Este es el campo del cual se extraerán los valores para crear los intervalos de clase geométricos.
tipo_clasificacion = arcpy.GetParameterAsText(2)
clases =  arcpy.GetParameterAsText(3).encode("utf-8").split(";") # En este campo se deben escribir los nombres que recibirán los intervalos de clases. Ejemplo: Alta;Media;Baja
intervalos = arcpy.GetParameterAsText(4)
if intervalos!="":
    intervalos = [float(x) for x in arcpy.GetParameterAsText(4).split(";")]
calcular_categoria=arcpy.GetParameterAsText(5)
campo_calculate = arcpy.GetParameterAsText(6) # En este campo se asignarán los nombres de los intrevalos de clases de acuerdo con el valor del campo de valores
num_clases = len(clases) # variable que alamcena el número de clases

if calcular_categoria == "true":
    if campo_calculate =="":
     arcpy.AddError("###################################")
     arcpy.AddError("debe elegir un campo de asignacion ")
     arcpy.AddError("###################################")
     sys.exit()
# ------------------------------------------------------------

#=====================funciones auxiliares==============================#

def directorioyArchivo (): # función que devuelve el nombre del archivo del script y su ruta
    archivo=inspect.getfile(inspect.currentframe()) # captura el nombre de archivo
    directorio=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # captura la ruta del archivo
    return archivo, directorio


def asignasimbologia(layer,campo,num_clases,clases,tipo_clasificacion,ruta): # asigna la simbología y devuelve los intervalos
    tipo_dict={"Intervalos_Geometricos":"intervalos_geometricos_alta_media_baja",
    "Intervalos_Iguales":"intervalos_iguales_3clases",
    "Quantiles":"quantiles_3clases",
    "Natural_Breaks_(jenks)":"natural_breaks_jenks_3clases",
    "Intervalos_Manuales":"natural_breaks_jenks_3clases"}
    mxd = arcpy.mapping.MapDocument("current") # captura el mxd abierto
    df = arcpy.mapping.ListDataFrames(mxd)[0] # captura el dataframe
    addlayer = arcpy.mapping.Layer(layer) # instancia el objeto layer de mapping
    arcpy.mapping.AddLayer(df, addlayer) # añade el layer al mapa o mxd
    lyr = arcpy.mapping.ListLayers(mxd, "*"+arcpy.Describe(layer).name+"*")[0] # captura el layer cargado en el mapa
    sourceLayer = arcpy.mapping.Layer(ruta+"\\layers\\"+tipo_dict[tipo_clasificacion]+".lyr") # captura el layer de ejemplo que define la simbología
    arcpy.mapping.UpdateLayer(df, lyr, sourceLayer, True) # asigna la simbologia del layer de ejemplo al layer a actualizar
    arcpy.RefreshTOC() # refresca la tabla de contenido
    arcpy.RefreshActiveView() # refresca la vista activa
    if lyr.symbologyType == "GRADUATED_COLORS": # si se tiene simbología de colores graduados
        lyr.symbology.valueField = campo # asigna el campo para hacer los intervalos
        lyr.symbology.numClasses = num_clases # asigna el número de clases
        if tipo_clasificacion in ("Intervalos_Manuales"):
            if len(intervalos)<num_clases+1:

                arcpy.AddError("###################################")
                if len(intervalos)==0:
                    arcpy.AddError("Debe introducir los intervalos")
                else:
                    arcpy.AddError("Debe introducir %s intervalos"%(str(len(intervalos)+1)))
                arcpy.AddError("###################################")
                sys.exit()
            lyr.symbology.numClasses = num_clases # asigna el número de clases
            lyr.symbology.classBreakValues =intervalos # captura los intervalos
            lyr.symbology.classBreakLabels = clases # asigna los nombre de las
        else:
            lyr.symbology.classBreakLabels = clases # asigna los nombre de las

    arcpy.RefreshActiveView() # refresca la tabla de contenido
    arcpy.RefreshTOC() # refresca la vista activa
    rangos = lyr.symbology.classBreakValues # captura los intervalos
    return rangos # devuelve los intervalos

def asignacategoria(capa,campo_clasificacion,intervalos,clases,campo_calculate): # asigna el nombre de clase acorde con los intervalos
    diccio ={} # crea un diccionario
    valores=[x[0]for x in arcpy.da.SearchCursor(capa,campo_clasificacion)] # captura todos los valores del campo de valores
    for valor in valores:
        for x in xrange(len(intervalos)-1):
            if valor >= intervalos[x] and valor <= intervalos[x+1]: # asigna la clase acorde con el intervalo definido en el diccionario
                diccio.update({"%s"%valor:clases[x]}) # actualiza el diccionario
    with arcpy.da.UpdateCursor(capa,[campo_clasificacion,campo_calculate]) as cursor:# actualiar el campo del layer
        for fila in cursor:
            try:
                fila[1] = diccio[str(fila[0])]
            except:
                pass
            cursor.updateRow(fila)
# ------------------------------------------------------------

if __name__ == '__main__':
    nombre,ruta=directorioyArchivo () # captura el nombre del archivo del script y la ruta
    rangos = asignasimbologia(layer,campo_clasificacion,num_clases,clases,tipo_clasificacion,ruta) # asigna la simbología y devuelve los intervalos

    if calcular_categoria == "true":
        asignacategoria(arcpy.Describe(layer).catalogpath,campo_clasificacion,rangos,clases,campo_calculate) # asigna el nombre de clase acorde con los intervalos
    arcpy.SetParameter(7,arcpy.Describe(layer).catalogpath) # fija el parámetro de salida que es un feature class

