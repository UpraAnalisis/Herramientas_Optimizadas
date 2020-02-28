#-*- coding: utf-8 -*-

import arcpy
import os
import sys
import subprocess
import inspect
##import easygui

arcpy.env.overwriteOutput = 1
reload(sys)
sys.setdefaultencoding('UTF8')
##from funciones_calidad.funcion_principal import *



dic_acentos={" ":"---","\xc3\xa1":"***a***","\xc3\xa9":"***e***", "\xc3\xad":"***i***",
"\xc3\xb3": "***o***","\xc3\xba": "***u***","\xc3\xb1": "***n***","\xc3\x81":"***A***","\xc3\x89":"***E***",
"\xc3\x8d":"***I***", "\xc3\x93": "***O***","***\xc3\x9a***":"Ú","\xc3\x91": "***N***"}


def cambia_caracteres(infea):
    for xx in dic_acentos:# ciclo que reemplaza las letras por los carateres especiales
        infea=infea.replace(xx,dic_acentos[xx])
    return infea

def getPythonPath():
    pydir = sys.exec_prefix
    pyexe = os.path.join(pydir, "python.exe")
    if os.path.exists(pyexe):
        return pyexe
    else:
        raise RuntimeError("python.exe no se encuentra instalado en {0}".format(pydir))

def directorioyArchivo (): # captura el directorio donde se encuentra almacenado el script y el nombre del script
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
    verPythonfinal=pyexe
    scriptAuxiliar="funcion_principal.py" # script auxiliar que ejecuta el prceso
 # ------------------------------------------------------------

parametros = arcpy.GetParameterInfo()
ruta_salida = arcpy.GetParameterAsText(4).decode('utf-8')
archivo =r"%s\reporte_%s.txt"%(ruta_salida,datetime.datetime.now().strftime("%b_%d_%Y_%H_%M_%S"))
nuevos_parametros = []
for x in parametros:
    try:
        nuevos_parametros.append(cambia_caracteres(arcpy.Describe(str(x.value)).catalogpath.decode('utf-8')))
    except:
        nuevos_parametros.append(cambia_caracteres(str(x.value).decode('utf-8')))

parametros_array = [cambia_caracteres(archivo)] + nuevos_parametros


parametros_string = (" ").join(parametros_array)
verPython=verPythonfinal # asigna la versión de python que se va a usar 32 o 64 bits
verPythonDir=verPython.replace("\\python.exe","") # obtiene la ruta del directorio que almacena el ejecutable de python
script=directorioyArchivo() #
script=script[1]+"\\"+scriptAuxiliar # almacena la ruta y nombre de archivo del script auxiliar
comandos=r"start %s %s %s"%(verPython,script, parametros_string)
aa = subprocess.Popen(comandos, stdin=None,stdout=subprocess.PIPE,shell=True,env=dict(os.environ, PYTHONHOME=verPythonDir))
astdout, astderr = aa.communicate()
texto = open(r"%s"%(archivo),"r")
texto_anterior = texto.read()
if  "#" in texto_anterior:
    arcpy.AddError("Por favor realize las correcciones indicadas en el archivo de reporte : %s"%(archivo))


else:
    arcpy.AddWarning("No se encontraron errores en las características evaluadas.")
    archivox,direc =directorioyArchivo()
    txt_ok = open(r"%s\ok_ok.txt"%(direc),"r")
    texto_ok =txt_ok.read()
    txt_ok.close()
    txt_logo_upra = open(r"%s\logo.txt"%(direc),"r")
    texto_logo_upra =txt_logo_upra.read()
    txt_logo_upra.close()

    arcpy.AddWarning(texto_ok)
    arcpy.AddWarning( "")
    texto1 = open(r"%s"%(archivo),"w")
    texto1.write(texto_anterior)
    texto1.write('\n')
    texto1.write("No se encontraron errores en las características evaluadas.")
    texto1.write('\n')
    texto1.write(texto_ok)
    texto1.close()
texto.close()


