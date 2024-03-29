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
arcpy.env.workspace = "in_memory"
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3116)
arcpy.env.overwriteOutput = True
verPython64="C:\\Python27\\ArcGISx6410.3\\python.exe"
scriptAuxiliar="updatex64_aux.py"
verPythonfinal=verPython64

infea=arcpy.GetParameterAsText(0)
feaUpdate= arcpy.GetParameterAsText(1)
gdb_salida=arcpy.GetParameterAsText(2)
capa_salida=arcpy.GetParameterAsText(3)





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
    arcpy.AddMessage(script)
    comando=r"start %s %s %s %s %s %s"%(verPython,script,infea,feaUpdate,gdb_salida,capa_salida)

    ff=subprocess.Popen(comando,stdin=None,stdout=subprocess.PIPE,shell=True,env=dict(os.environ, PYTHONHOME=verPythonDir))
    astdout, astderr = ff.communicate()
    output=gdb_salida+"\\"+capa_salida
    arcpy.SetParameter(4, output)
    arcpy.AddMessage("proceso Completado en %s Minutos." % ((time.clock() - t_inicio)/60))



