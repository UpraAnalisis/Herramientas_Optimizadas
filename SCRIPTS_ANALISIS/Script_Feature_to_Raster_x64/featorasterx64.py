# -*- coding: utf-8 -*-
# --------------------------------------------------------------------
# featorasterx64.py
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
scriptAuxiliar="featorasterx64_aux.py"
verPythonfinal=verPython64

in_features=arcpy.GetParameterAsText(0)
in_features=arcpy.Describe(in_features).catalogPath
field= arcpy.GetParameterAsText(1)
out_raster=arcpy.GetParameterAsText(2)
cell_size=float(arcpy.GetParameterAsText(3))
gdb_salida=arcpy.GetParameterAsText(4)
extent=r"%s"%(arcpy.GetParameterAsText(5))
mask=arcpy.GetParameterAsText(6)

if mask!="":
    mask=arcpy.Describe(mask).catalogPath
else:
    mask="---"
arcpy.env.workspace = gdb_salida



def directorioyArchivo ():
    archivo=inspect.getfile(inspect.currentframe()) # script filename
    directorio=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
    return archivo, directorio

if __name__ == '__main__':
    verPython=verPythonfinal
    verPythonDir=verPython.replace("\\python.exe","")
##    arcpy.AddMessage(verPythonDir)

    if "," in extent:
        extent="{}".format(extent)
        extent=extent.replace(" ",".....")
    arcpy.AddMessage(out_raster)
    script=directorioyArchivo()
    script=script[1]+"\\"+scriptAuxiliar
    arcpy.AddMessage(script)
    comando=r"start %s %s %s %s %s %s %s %s %s"%(verPython,script,in_features,field,out_raster,cell_size,gdb_salida,extent,mask)

    ff=subprocess.Popen(comando,stdin=None,stdout=subprocess.PIPE,shell=True,env=dict(os.environ, PYTHONHOME=verPythonDir))
    astdout, astderr = ff.communicate()
    output=gdb_salida+"\\"+out_raster
    arcpy.AddMessage(output+" "+out_raster)


    if mask!="---":
        raster_salida_recorte=arcpy.MakeRasterLayer_management(in_raster=output+"_recorte",out_rasterlayer=out_raster+"_layer_recorte")
        arcpy.SetParameter(7, raster_salida_recorte)


    else:
        raster_salida=arcpy.MakeRasterLayer_management(in_raster=output,out_rasterlayer=out_raster+"_layer")
        arcpy.SetParameter(7, raster_salida)
    arcpy.AddMessage("proceso Completado en %s Minutos." % ((time.clock() - t_inicio)/60))



