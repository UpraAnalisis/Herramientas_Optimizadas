# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------
# JoinCursor_Multiple_v3_x64_feature.py
# Fecha de creacion: 2017-11-15 08:59:08.00000
# Author: Carlos Mario Cano Campillo
# Email: carlos.cano@upra.gov.co / kanocampillo@gmail.com
# Propietario: Unidad de Planificación Rural Agropecuaria
#
# ---------------------------------------------------------------------
#=====================Librerias==============================#
import arcpy, random, time,os,subprocess,inspect
from arcpy import env

# sys.setdefaultencoding() does not exist, here!
reload(sys) # Reload does the trick!
sys.setdefaultencoding('UTF8')

#=========Variables Globales y de Entorno=====================#
env.overwriteOutput = True # habilita la opcion de sobrescribir datos
t_inicio=time.clock() # captura el tiempo de inicio del proceso
arcpy.env.workspace = "in_memory" # fija el espacio de trabajo en memoria
src=arcpy.SpatialReference(3116) # fija el sistema de coordenadas en magna bogota
ws=arcpy.env.workspace
#=================Parametros de entrada======================#
fcentrada = r"%s"%arcpy.GetParameterAsText(0) # almacena la capa objetivo del join
llave_objetivo = arcpy.GetParameterAsText(1) # almacena la llave de la capa objetivo
tablajoin = r"%s"%arcpy.GetParameterAsText(2) # almacena la tabla desde donde se traeran los atributos
llave_tabla = arcpy.GetParameterAsText(3) # almacena la llave de la tabla de donde bienen los atributos
campo_a_unir=[]  # almacena los campos a unir en el join
campo_a_unir=arcpy.GetParameterAsText(4)
campo_a_unir = campo_a_unir.split(";")
#-------------------------------------------------------------

dic_acentos={" ":"---","\xc3\xa1":"***a***","\xc3\xa9":"***e***", "\xc3\xad":"***i***", "\xc3\xb3": "***o***","\xc3\xba": "***u***","\xc3\xb1": "***n***",
"\xc3\x81":"***A***","\xc3\x89":"***E***", "\xc3\x8d":"***I***", "\xc3\x93": "***O***","***\xc3\x9a***":"Ú","\xc3\x91": "***N***"}


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

def cambia_caracteres(infea):
    for xx in dic_acentos:# ciclo que reemplaza las letras por los carateres especiales
        infea=infea.replace(xx,dic_acentos[xx])
    return infea

#=========Validación de requerimientos=====================#

pyexe = getPythonPath()

if not "x64" in r"%s"%(pyexe):
    pyexe=pyexe.replace("ArcGIS","ArcGISx64")
if not arcpy.Exists(pyexe):
    arcpy.AddError("Usted no tiene instalado el Geoprocesamiento en segundo plano (64 bits)")
    raise RuntimeError("Usted no tiene instalado el Geoprocesamiento en segundo plano (64 bits) {0}".format(pyexe))
else:
    verPython64=pyexe
    scriptAuxiliar="JoinCursor_Multiple_v5_x64_feature_tabla_aux.py"
    verPythonfinal=verPython64
# ------------------------------------------------------------


if __name__ == '__main__':
    verPython=verPythonfinal
    verPythonDir=verPython.replace("\\python.exe","")
    script=directorioyArchivo()
    script=script[1]+"\\"+scriptAuxiliar
    arcpy.AddMessage(script)
    fcentrada_con_acentos=fcentrada
    fcentrada=cambia_caracteres(arcpy.Describe(fcentrada).catalogPath)
    llave_objetivo=cambia_caracteres(llave_objetivo)
    tablajoin=cambia_caracteres(arcpy.Describe(tablajoin).catalogPath)
    llave_tabla=cambia_caracteres(llave_tabla)
    comando=r"start %s %s %s %s %s %s %s"%(verPython,script,fcentrada,llave_objetivo,tablajoin,llave_tabla,("__").join([x for x in campo_a_unir]))
    ff=subprocess.Popen(comando,stdin=None,stdout=subprocess.PIPE,shell=True,env=dict(os.environ, PYTHONHOME=verPythonDir))
    astdout, astderr = ff.communicate()
    arcpy.SetParameter(5,arcpy.Describe(fcentrada_con_acentos).catalogpath) # retorna como un parametro la capa resultante


