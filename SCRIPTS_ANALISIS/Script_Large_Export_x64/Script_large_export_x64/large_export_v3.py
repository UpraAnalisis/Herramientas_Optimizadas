#-*- coding: utf-8 -*-
import easygui

import sys
import arcpy,os,subprocess,time,inspect
sys.argv = [""]
# sys.setdefaultencoding() does not exist, here!
reload(sys) # Reload does the trick!
sys.setdefaultencoding('UTF8')
#Definición parametros auxiliares
verPython64="C:\\Python27\\ArcGISx6410.7\\python.exe"
scriptAuxiliar="large_exportx64v3_aux.py"

infea=arcpy.GetParameterAsText(0)
folder=arcpy.GetParameterAsText(1)
nombre=arcpy.GetParameterAsText(2)

t_inicio=time.clock()#

try:
    import xlsxwriter
except:
     os.system(r'{} -m pip install xlsxwriter'.format(verPython64))


def directorioyArchivo ():
    archivo=inspect.getfile(inspect.currentframe()) # script filename
    directorio=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
    return archivo, directorio

if __name__ == '__main__':
    verPython=verPython64
    verPythonDir=verPython.replace("\\python.exe","")
##    arcpy.AddMessage(verPythonDir)
##    arcpy.AddMessage(verPython)
    script=directorioyArchivo()
    script=script[1]+"\\"+scriptAuxiliar
    arcpy.AddMessage(script)
    comando=r'start %s %s "%s" "%s" "%s"'%(verPython,script,infea,folder,nombre)

    ff=subprocess.Popen(comando,stdin=None,stdout=subprocess.PIPE,shell=True,env=dict(os.environ, PYTHONHOME=verPythonDir))
    astdout, astderr = ff.communicate()
##    output=gdb_salida+"\\"+capa_salida
##    layer_salida=arcpy.MakeFeatureLayer_management(output,capa_salida)
    #arcpy.SetParameter(5, layer_salida)
    start = t_inicio
    end = time.clock()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    arcpy.AddMessage("proceso Completado en {:0>2} H {:0>2} M {:05.2f} S.".format(int(hours),int(minutes),seconds))
