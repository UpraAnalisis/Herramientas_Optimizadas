# -*- coding: utf-8 -*-
# --------------------------------------------------------------------
# Eliminate_x64.py
# Fecha de creacion: 2017-07-10 14:00:08.00000
# Author: Carlos Mario Cano Campillo
# Email: carlos.cano@upra.gov.co / kanocampillo@gmail.com
# Propietario: Unidad de Planificación Rural Agropecuaria
#
# ---------------------------------------------------------------------
#=====================Librerias==============================#
import arcpy,os,subprocess,time,inspect
import sys


# sys.setdefaultencoding() does not exist, here!
reload(sys) # Reload does the trick!
sys.setdefaultencoding('UTF8')
# ------------------------------------------------------------

#=========Variables Globales y de Entorno=====================#
t_inicio=time.clock()# captura el tiempo de inicio del proceso
#arcpy.env.workspace = "in_memory"
#arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3116)
arcpy.env.overwriteOutput = True
# ------------------------------------------------------------


#=========Parámetros=====================#

in_table =r"%s"%(arcpy.GetParameterAsText(0))
out_table =r"%s"%(arcpy.GetParameterAsText(1))
statistics_fields =r"%s"%(arcpy.GetParameterAsText(2))
case_field =r"%s"%(arcpy.GetParameterAsText(3))

# ------------------------------------------------------------

dic_acentos={" ":"---","\xc3\xa1":"***a***","\xc3\xa9":"***e***", "\xc3\xad":"***i***", "\xc3\xb3": "***o***","\xc3\xba": "***u***","\xc3\xb1": "***n***",
"\xc3\x81":"***A***","\xc3\x89":"***E***", "\xc3\x8d":"***I***", "\xc3\x93": "***O***","***\xc3\x9a***":"Ú","\xc3\x91": "***N***"}
comandos=[] # arreglo que almacena los comandos a ejecutar por el script auxiliar


if case_field!="":
    case_field=case_field
else:
    case_field="---"


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


variables =[var for var in dir(arcpy.env) if "_" not in var and "packageWorkspace" not in var and "scratch" not in var]

def enviar_environ(palabras_entorno):
    var_entorno=[]
    for palabra in palabras_entorno:
        if palabra == "mask" or palabra == "workspace" :
            if arcpy.env.mask is not None:
                intruc_a="""if arcpy.env.%s !="" and "object" not in str(arcpy.env.%s): var_entorno.append(str(arcpy.Describe(arcpy.env.%s).catalogpath).replace(" ","....."))"""%(palabra,palabra,palabra)
            else:
                intruc_a="""if arcpy.env.%s !="" and "object" not in str(arcpy.env.%s): var_entorno.append(str(arcpy.env.%s).replace(" ","....."))"""%(palabra,palabra,palabra)
            instruc_b="""else: var_entorno.append("----")"""
        if palabra == "extent":
            intruc_a="""if arcpy.env.%s !="" and "object" not in str(arcpy.env.%s): var_entorno.append((" ").join([value for value in str(arcpy.env.%s).split(" ") if "NaN" not in value]).replace(" ","....."))"""%(palabra,palabra,palabra)
            instruc_b="""else: var_entorno.append("----")"""
        if palabra != "extent" and palabra != "mask":
            intruc_a="""if arcpy.env.%s !="" and "object" not in str(arcpy.env.%s): var_entorno.append(str(arcpy.env.%s).replace(" ","....."))"""%(palabra,palabra,palabra)
            instruc_b="""else: var_entorno.append("----")"""
        exec(intruc_a+"\n"+instruc_b)
    return ("***").join(var_entorno)


def cambia_caracteres(infea):
    for xx in dic_acentos:# ciclo que reemplaza las letras por los carateres especiales
        infea=infea.replace(xx,dic_acentos[xx])
    return infea

def enviar_seleccion(capa):
    fid_Set = [str(r[0]) for r in arcpy.da.SearchCursor(capa,"OID@")]
    if str(len(fid_Set))!=str(int(arcpy.GetCount_management(arcpy.Describe(capa).catalogpath)[0])):
        fid_Set=("_").join(fid_Set)
        fid_Set= fid_Set.replace("; ","_")
        return fid_Set
    else:
        fid_Set = "---"
        return fid_Set

def escribe_txt(capa_entrada,capa_salida,lista_fids):
    ruta_salida,archivo_salida=os.path.split(capa_salida)
    ruta_entrada,archivo_entrada=os.path.split(arcpy.Describe(capa_entrada).catalogpath)
    carpeta=("\\").join(ruta_salida.split('\\')[:-1])
    ruta_txt = (r"%s\%s.txt"%(carpeta,archivo_entrada))
    txt = open("%s"%(ruta_txt),"w")
    txt.write(lista_fids)
    txt.close()
    return ruta_txt


# ------------------------------------------------------------

#=========Validación de requerimientos=====================#

pyexe = getPythonPath()


if not "x64" in r"%s"%(pyexe):
    pyexe=pyexe.replace("ArcGIS","ArcGISx64")
if not arcpy.Exists(pyexe):
    arcpy.AddError("Usted no tiene instalado el Geoprocesamiento en segundo plano (64 bits)")
    raise RuntimeError("Usted no tiene instalado el Geoprocesamiento en segundo plano (64 bits) {0}".format(pyexe))
else:
    verPython64=pyexe
    scriptAuxiliar="Script_Summary_Statistics_x64_auxiliar_v4.py"
    verPythonfinal=verPython64
# ------------------------------------------------------------

    if __name__ == '__main__':
        verPython=verPythonfinal
        verPythonDir=verPython.replace("\\python.exe","")
        script=directorioyArchivo()
        script=script[1]+"\\"+scriptAuxiliar
        arcpy.AddMessage(script)
        entorno = enviar_environ(variables)


        arcpy.AddMessage("######### VARIABLES DE ENTORNO #########")
        arcpy.AddMessage(entorno)
        arcpy.AddMessage("######### VARIABLES DE ENTORNO #########")
        arcpy.AddMessage(verPython)
        if arcpy.Describe(arcpy.Describe(in_table).catalogPath).dataType in ('FeatureClass','FeatureLayer','TableView'):
            tipo= arcpy.Describe(in_table).dataType
            lista_fids1 = enviar_seleccion(in_table)
            ruta_txt_fids1=escribe_txt(in_table,out_table,lista_fids1)
            in_table=cambia_caracteres(arcpy.Describe(in_table).catalogPath)
            statistics_fields=cambia_caracteres(statistics_fields)
            case_field=cambia_caracteres(case_field)
            out_table=cambia_caracteres(out_table)
            ruta_txt_fids1=cambia_caracteres(ruta_txt_fids1)
            comando=r"start %s %s %s %s %s %s %s %s %s"%(verPython,script,in_table,out_table, statistics_fields,case_field, tipo,ruta_txt_fids1,entorno)

        else:
            tipo= arcpy.Describe(in_table).dataType
            in_table = cambia_caracteres(arcpy.Describe(in_table).catalogPath)
            statistics_fields=cambia_caracteres(statistics_fields)
            case_field=cambia_caracteres(case_field)
            out_table=cambia_caracteres(out_table)
            comando=r"start %s %s %s %s %s %s %s %s"%(verPython,script,in_table,out_table, statistics_fields,case_field, tipo,entorno)

        ff=subprocess.Popen(comando,stdin=None,stdout=subprocess.PIPE,shell=True,env=dict(os.environ, PYTHONHOME=verPythonDir))
        astdout, astderr = ff.communicate()
        arcpy.AddMessage("proceso Completado en %s Minutos." % ((time.clock() - t_inicio)/60))




