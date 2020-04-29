#-*- coding: utf-8 -*-
import easygui
import xlsxwriter
import sys
import pythonaddins
import arcpy,os,subprocess,time,inspect
sys.argv = [""]
# sys.setdefaultencoding() does not exist, here!
reload(sys) # Reload does the trick!
sys.setdefaultencoding('UTF8')
#Definición parametros auxiliares
verPython64="C:\\Python27\\ArcGISx6410.5\\python.exe"
scriptAuxiliar=r"U:\SCRIPTS_ANALISIS\PRUEBAS\Large_Export_x64\large_exportx64_aux.py"
t_inicio=time.clock()#

def directorioyArchivo ():
    archivo=inspect.getfile(inspect.currentframe()) # script filename
    directorio=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
    return archivo, directorio

def mExporTable():
    verPython=verPython64
    verPythonDir=verPython.replace("\\python.exe","")
    #script=directorioyArchivo()
    #script=script[1]+"\\"+scriptAuxiliar
    script=scriptAuxiliar
    arcpy.AddMessage(script)
    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = arcpy.mapping.ListDataFrames(mxd, '')[0]
    lyrList = pythonaddins.GetSelectedTOCLayerOrDataFrame()
    try:
        outex = r'' + easygui.diropenbox("Save Folder","Hojas Generadas",".")
    except:
        outex = pythonaddins.OpenDialog("Ruta de Salida: ")
    

    for lyr in arcpy.mapping.ListLayers(mxd, '', df):
        for layer in lyrList:
            if lyr.name == layer.name:
                #pythonaddins.MessageBox("Exportando {} to PNG ".format(lyr.name),"Wait...",)
                print "Exportando {} to Excel ".format(lyr.name)
                lyr.visible = True
                arcpy.RefreshActiveView()
                infea = arcpy.Describe(lyr).catalogPath
                # print mxd, PNGPath+"\\" + lyr.name + ".png","",anHojaPulga,alHojaPulga,int(resolucionSalida)
                try:
                    print verPython,script,infea,outex
                    print infea
                    comando=r"start %s %s %s %s"%(verPython,script,infea,outex)
                    ff=subprocess.Popen(comando,stdin=None,stdout=subprocess.PIPE,shell=True,env=dict(os.environ, PYTHONHOME=verPythonDir))
                    astdout, astderr = ff.communicate()
                except:
                    try:
                        infea = r'' + arcpy.Describe(lyr).calalogPath
                        comando=r"start %s %s %s %s"%(verPython,script,infea,outex)
                        ff=subprocess.Popen(comando,stdin=None,stdout=subprocess.PIPE,shell=True,env=dict(os.environ, PYTHONHOME=verPythonDir))
                        astdout, astderr = ff.communicate()
                    except:
                        pythonaddins.MessageBox("AttributeError: PageLayoutObject \n\nPlease restart ArcMap and try again , If error persist call to ESRI support","ArcGIS Fatal Error",7)
                        raise SystemExit(0)

    start = t_inicio
    end = time.clock()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    arcpy.AddMessage("proceso Completado en {:0>2} H {:0>2} M {:05.2f} S.".format(int(hours),int(minutes),seconds))
