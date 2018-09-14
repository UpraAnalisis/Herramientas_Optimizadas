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
in_features=arcpy.GetParameterAsText(0)
in_features=arcpy.Describe(in_features).catalogPath
field= arcpy.GetParameterAsText(1)
out_raster=arcpy.GetParameterAsText(2)
cell_size=float(arcpy.GetParameterAsText(3))
gdb_salida,out_raster =os.path.split(out_raster)
extent=r"%s"%(arcpy.GetParameterAsText(4))
mask=arcpy.GetParameterAsText(5)


if mask!="":
    mask=arcpy.Describe(mask).catalogPath
else:
    mask="---"
arcpy.env.workspace = gdb_salida



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

pyexe = getPythonPath()

if not "x64" in r"%s"%(pyexe):
    pyexe=pyexe.replace("ArcGIS","ArcGISx64")
if not arcpy.Exists(pyexe):
    arcpy.AddError("Usted no tiene instalado el Geoprocesamiento en segundo plano (64 bits)")
    raise RuntimeError("Usted no tiene instalado el Geoprocesamiento en segundo plano (64 bits) {0}".format(pyexe))
else:
    verPython64=pyexe
    scriptAuxiliar="featorasterx64_aux_v3.py"
    verPythonfinal=verPython64
# ------------------------------------------------------------

if __name__ == '__main__':
    verPython=verPythonfinal
    verPythonDir=verPython.replace("\\python.exe","")
    arcpy.AddMessage(mask)

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
        arcpy.SetParameter(5, output+"_recorte")


    else:
        arcpy.SetParameter(5, output)
    arcpy.AddMessage("proceso Completado en %s Minutos." % ((time.clock() - t_inicio)/60))



