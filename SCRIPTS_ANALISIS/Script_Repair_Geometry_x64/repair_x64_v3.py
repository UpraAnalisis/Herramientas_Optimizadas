# -*- coding: utf-8 -*-
# --------------------------------------------------------------------
# repair_x64_v2.py
# Fecha de creacion: 2017-08-09 09:21:08.00000
# Author: Carlos Mario Cano Campillo
# Email: carlos.cano@upra.gov.co / kanocampillo@gmail.com
# Propietario: Unidad de Planificación Rural Agropecuaria
#
# ---------------------------------------------------------------------
#=====================Librerias==============================#
import arcpy,os,subprocess,time,inspect,exceptions
# ------------------------------------------------------------

#=========Variables Globales y de Entorno=====================#
t_inicio=time.clock()# captura el tiempo de inicio del proceso

arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3116)
arcpy.env.overwriteOutput = True
infea=arcpy.GetParameterAsText(0)
infea=arcpy.Describe(infea).catalogPath
nombre=arcpy.Describe(infea).name
delete_null= arcpy.GetParameterAsText(1)
en_memoria= arcpy.GetParameterAsText(2)
num_ciclos= arcpy.GetParameterAsText(3)

try:


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
        scriptAuxiliar="repairx64_aux_v3.py"
        verPythonfinal=verPython64
    # ------------------------------------------------------------

    if __name__ == '__main__':
        verPython=verPythonfinal
        verPythonDir=verPython.replace("\\python.exe","")
        script=directorioyArchivo()
        script=script[1]+"\\"+scriptAuxiliar
        arcpy.AddMessage(script)
        comando=r"start %s %s %s %s %s %s"%(verPython,script,infea,delete_null,en_memoria,num_ciclos)

        ff=subprocess.Popen(comando,stdin=None,stdout=subprocess.PIPE,shell=True,env=dict(os.environ, PYTHONHOME=verPythonDir))
        astdout, astderr = ff.communicate()

        if en_memoria == "true":
            capa_copia =arcpy.Describe(infea).catalogpath
            arcpy.SetParameter(4, capa_copia)
        else:
            arcpy.SetParameter(4, infea)
        arcpy.AddMessage("proceso Completado en %s Minutos." % ((time.clock() - t_inicio)/60))

except exceptions.Exception as e:
    print e.__class__, e.__doc__, e.message
    os.system("pause")


