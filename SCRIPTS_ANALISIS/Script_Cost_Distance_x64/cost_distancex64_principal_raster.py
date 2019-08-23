# -*- coding: utf-8 -*-
# --------------------------------------------------------------------
# crear_folder_nombre_capa.py
# Fecha de creacion: 2016-08-01 08:59:08.00000
# Author: Carlos Mario Cano Campillo
# Email: carlos.cano@upra.gov.co / kanocampillo@gmail.com
# Propietario: Unidad de Planificación Rural Agropecuaria
#
# ---------------------------------------------------------------------
#=====================Librerias==============================#
import arcpy,os,subprocess,time,inspect
# ------------------------------------------------------------

#=========Variables Globales y de Entorno=====================#
t_inicio=time.clock()# captura el tiempo de inicio del proceso

arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3116)
arcpy.env.overwriteOutput = True
verPython64="C:\\Python27\\ArcGISx6410.3\\python.exe"
scriptAuxiliar="cost_distancex64_aux_raster.py"
verPythonfinal=verPython64

in_source_raster=r"%s"%(arcpy.GetParameterAsText(0))

in_source_vector=r"%s"%(arcpy.GetParameterAsText(1))


if in_source_vector!="":
    in_source_vector=arcpy.Describe(in_source_vector).catalogPath
    in_source_data=in_source_vector
if in_source_raster!="":
    in_source_raster=arcpy.Describe(in_source_raster).catalogPath
    in_source_data=in_source_raster

in_cost_raster=r"%s"%(arcpy.GetParameterAsText(2))
maximum_distance=arcpy.GetParameterAsText(3)
out_backlink_raster=r"%s"%(arcpy.GetParameterAsText(4))
extent=r"%s"%(arcpy.GetParameterAsText(5))
if out_backlink_raster!="":
    out_backlink_raster=arcpy.Describe(out_backlink_raster).catalogPath
else:
    out_backlink_raster="---"
if maximum_distance!="":
    maximum_distance=maximum_distance
else:
    maximum_distance="---"
capa_salida=r"%s"%(arcpy.GetParameterAsText(6))


directoriox,nombre =os.path.split(capa_salida)

arcpy.env.workspace = directoriox


def directorioyArchivo ():
    archivo=inspect.getfile(inspect.currentframe()) # script filename
    directorio=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
    return archivo, directorio

if __name__ == '__main__':
    verPython=verPythonfinal
    verPythonDir=verPython.replace("\\python.exe","")
##    arcpy.AddMessage(verPythonDir)
##    arcpy.AddMessage(verPython)
    script=directorioyArchivo()
    script=script[1]+"\\"+scriptAuxiliar
##    arcpy.AddMessage(script)
##    arcpy.AddMessage("extent %s"%extent)
    extentx=""
##    try:
##        arcpy.Exists(extent)
##    except:
    if "," in extent:
        extent="{}".format(extent)
        extent=extent.replace(" ",".....")

##    arcpy.AddMessage("{}".format(extent))

    comando=r"start %s %s %s %s %s %s %s %s"%(verPython,script,in_source_data,in_cost_raster,maximum_distance,out_backlink_raster,extent,capa_salida)
    ff=subprocess.Popen(comando,stdin=None,stdout=subprocess.PIPE,shell=True,env=dict(os.environ, PYTHONHOME=verPythonDir))
    astdout, astderr = ff.communicate()

##    layer_salida=arcpy.MakeRasterLayer_management(capa_salida,nombre+"_salida")
##    arcpy.SetParameter(6, layer_salida)
    arcpy.SetParameter(7, capa_salida)
    arcpy.AddMessage("proceso Completado en %s Minutos." % ((time.clock() - t_inicio)/60))



