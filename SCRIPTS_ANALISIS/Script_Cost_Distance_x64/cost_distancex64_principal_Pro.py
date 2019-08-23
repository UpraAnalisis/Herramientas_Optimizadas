# -*- coding: utf-8 -*-
# --------------------------------------------------------------------
# cost_distancex64_principal_raster_z.py
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


arcpy.env.overwriteOutput = True
in_source_raster=r"%s"%(arcpy.GetParameterAsText(0))
in_source_raster=arcpy.Describe(in_source_raster).catalogPath
sp=int(arcpy.Describe(in_source_raster).spatialreference.factoryCode)
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(sp)
in_cost_raster=r"%s"%(arcpy.GetParameterAsText(1))
in_cost_raster=arcpy.Describe(in_cost_raster).catalogPath

maximum_distance=arcpy.GetParameterAsText(2)
out_backlink_raster=r"%s"%(arcpy.GetParameterAsText(3))
extent=r"%s"%(arcpy.GetParameterAsText(4))

if out_backlink_raster=="":
    out_backlink_raster="---"

if maximum_distance!="":
    maximum_distance=maximum_distance
else:
    maximum_distance="---"

capa_salida=r"%s"%(arcpy.GetParameterAsText(5))

directoriox,nombre =os.path.split(capa_salida)

arcpy.env.workspace = directoriox


#=========Funciones Auxiliares=====================#
def getPythonPath():
    pydir = sys.exec_prefix
    pyexe = os.path.join(pydir, "python.exe")
    if os.path.exists(pyexe):
        return pyexe
    else:
        raise RuntimeError("python.exe no se encuentra instalado en {0}".format(pydir))

def directorioyArchivo ():
    archivo=inspect.getfile(inspect.currentframe()) # script filename
    directorio=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
    return archivo, directorio

#=========Validación de requerimientos=====================#

pyexe = r"C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe"
verPythonDir = r"C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3"

verPython64=pyexe
scriptAuxiliar="cost_distancex64_aux_Pro.py"
verPythonfinal=verPython64
# ------------------------------------------------------------

if __name__ == '__main__':
    verPython=verPythonfinal
    #verPythonDir=getPythonPath()
    script=directorioyArchivo()
    script=script[1]+"\\"+scriptAuxiliar
    extentx=""

    if "," in extent:
        extent="{}".format(extent)
        extent=extent.replace(" ",".....")

    comando=r""""%s" %s %s %s %s %s %s %s"""%(verPython,script,in_source_raster,in_cost_raster,maximum_distance,out_backlink_raster,extent,capa_salida)
    arcpy.AddMessage(comando)
    #os.system("ECHO %s"%comando)
    #os.system("PAUSE")
    ff=subprocess.Popen(comando,stdin=None,stdout=subprocess.PIPE,shell=False,env=dict(os.environ, PYTHONHOME=verPythonDir))
    astdout, astderr = ff.communicate()
    arcpy.AddMessage("proceso Completado en %s Minutos." % ((time.clock() - t_inicio)/60))



