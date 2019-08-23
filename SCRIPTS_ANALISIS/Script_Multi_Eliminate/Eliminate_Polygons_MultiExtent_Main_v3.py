# -*- coding: utf-8 -*-
import os
import arcpy
from arcpy import env
import subprocess
import inspect
import random ,string, shutil


#variables de entrorno y globales
dic={" ":"__","=":"igual", "<":"menor", ">": "mayor"} # diccionario que convierte los caracteres especiales en letras
comandos=[] # arreglo que almacena los comandos a ejecutar por el script auxiliar
dic_acentos={" ":"---","\xc3\xa1":"***a***","\xc3\xa9":"***e***", "\xc3\xad":"***i***",
"\xc3\xb3": "***o***","\xc3\xba": "***u***","\xc3\xb1": "***n***","\xc3\x81":"***A***","\xc3\x89":"***E***",
"\xc3\x8d":"***I***", "\xc3\x93": "***O***","***\xc3\x9a***":"Ú","\xc3\x91": "***N***"}

#=========Parámetros=====================#
fcEntrada =arcpy.Describe(arcpy.GetParameterAsText(0)).catalogpath.decode('utf-8') # Capa que se va a procesar.
grilla = arcpy.Describe(arcpy.GetParameterAsText(1)).catalogpath.decode('utf-8')
consulta = arcpy.GetParameterAsText(2).decode('utf-8') # Expresión que actua como un criterio, que aplicará el eliminate sobre los fetures que cumplan con lo especificado en dicha expresión.
for i in dic: # ciclo que reemplaza los carateres especiales
    consulta = consulta.replace(i,dic[i])

selection = arcpy.GetParameterAsText(3)
if selection == "true":
    selection = "LENGTH"
else:
    selection = "AREA"

FolderEntrada = r"%s"%arcpy.GetParameterAsText(4).decode('utf-8') # Folder donde se almacenarán los datos resultantes
capa_de_salida = arcpy.GetParameterAsText(5).decode('utf-8') # captura el feature class resultante del proceso
capa_exclusion = arcpy.GetParameterAsText(6).decode('utf-8')

if capa_exclusion == "":
    capa_exclusion="----"
else:
    capa_exclusion = arcpy.Describe(capa_exclusion).catalogpath.decode('utf-8')

expresion_de_exclusion = arcpy.GetParameterAsText(7).decode('utf-8')
if expresion_de_exclusion == "":
    expresion_de_exclusion = "----"
for i in dic: # ciclo que reemplaza los carateres especiales
    expresion_de_exclusion = expresion_de_exclusion.replace(i,dic[i])

procesossimultaneos = int(arcpy.GetParameterAsText(8)) # captura el número de procesos simultaneos que se van a ejecutar para procesar todas las secciones de la grilla
numeroprocesos = int(arcpy.GetCount_management(grilla)[0]) # captura el numero de secciones de la grilla
datos_intermedios = arcpy.GetParameterAsText(9)


#=========Funciones Auxiliares=====================#

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

def listaanidada(lista,separador): #convierte un arreglo en una lista anidada
    seq = tuple(lista)
    texto_anidado=separador.join( seq )
    return texto_anidado

def creadirs(): # crea los dierectorios de salida del programa
    nombre="unificado"
    if not os.path.exists(FolderEntrada+"\\%s"%(nombre)):
        os.makedirs(FolderEntrada+"\\%s"%(nombre))
    return FolderEntrada+"\\%s"%nombre

def crearFGDB(ruta): # crea la geodatabase que almacena el resultado final
    arcpy.CreateFileGDB_management(ruta, "bd_unificado.gdb")
    return ruta+"\\"+"bd_unificado.gdb"

def chunkIt(seq, num): # función que parte una secuencia en un número de partes
  avg = len(seq) / float(num)
  out = []
  last = 0.0

  while last < len(seq):
    out.append(seq[int(last):int(last + avg)])
    last += avg

  return out

def pasarlista(lista): # función que transforma el rango para transferirlo al script auxiliar
    lista=str(lista)
    lista=lista.replace(", ","_") # convierte los espacios en _
    return lista

def listaanidada(lista,separador): #convierte un arreglo en una lista anidada
    seq = tuple(lista)
    texto_anidado=separador.join( seq )
    return texto_anidado

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
    verPython64=pyexe
    scriptAuxiliar="Eliminate_Polygons_MultiExtent_Aux_v3.py" # script auxiliar que ejecuta el prceso de eliminate
    verPythonfinal=verPython64
# ------------------------------------------------------------


if __name__ == '__main__':
    ### codificando parametros #####
    fcEntrada= cambia_caracteres(fcEntrada)
    grilla = cambia_caracteres(grilla)
    consulta = cambia_caracteres(consulta)
    FolderEntrada = cambia_caracteres(FolderEntrada)
    if capa_exclusion != "----":
        capa_exclusion = cambia_caracteres(capa_exclusion)
    if expresion_de_exclusion != "----":
        expresion_de_exclusion = cambia_caracteres(capa_exclusion)
    ### codificando parametros #####
    verPython=verPythonfinal # asigna la versión de python que se va a usar 32 o 64 bits
    verPythonDir=verPython.replace("\\python.exe","") # obtiene la ruta del directorio que almacena el ejecutable de python
    script=directorioyArchivo() #
    script=script[1]+"\\"+scriptAuxiliar # almacena la ruta y nombre de archivo del script auxiliar
    #crea la base
    dirSalida= FolderEntrada
    cuadros=[num for num in xrange(1,numeroprocesos+1)] # define los cuadros que van a ser procesados
    cuadros_ram=cuadros
    random.shuffle(cuadros_ram)
    partes=chunkIt(cuadros_ram,procesossimultaneos)
    if procesossimultaneos!= len(partes): # valida que los procesos coincida con el numero de partes
        partes1=partes[:]
        partes1.pop(-1)
        partes1[-1].extend(partes[-1])
        del partes
        partes=partes1[:]

    for a in partes: # almacena los comandos en un arreglo+
##         comandos.append(r"start %s %s %s %s %s %s %s %s"%(verPython,script,fcEntrada,grilla,capa_exclusion,pasarlista(a),dirSalida,consulta))
         comandos.append(r"start %s %s %s %s %s %s %s %s %s %s"%(verPython, script, fcEntrada , grilla , consulta, selection, FolderEntrada,
          capa_exclusion , expresion_de_exclusion, pasarlista(a)))

    letras=string.ascii_letters # crea un listado de lestras que usará para almacenar la ejecución de los comandos
    instrucciones="" # incializa la cadena de texto que almacenará las instrucciones de ejecución de los multiples procesos
    instrucciones_espera="" # inicializa la variable que almacenará las instrucciones de espera de los procesos
    # este ciclo almacena las instrucciónes en una cadena de texto teniendo en cuenta el número de procesos simultaneos definidos
    for x in xrange(0,procesossimultaneos):
        if x==procesossimultaneos-1 :
            instrucciones+='%s = subprocess.Popen(comandos[%s],stdin=None,stdout=subprocess.PIPE,shell=True,env=dict(os.environ, PYTHONHOME=verPythonDir))'%(letras[x],str(x))
        else:
            instrucciones+='%s = subprocess.Popen(comandos[%s],stdin=None,stdout=subprocess.PIPE,shell=True,env=dict(os.environ, PYTHONHOME=verPythonDir));'%(letras[x],str(x))
    for x in xrange(0,procesossimultaneos):
        if x==procesossimultaneos-1 :
         instrucciones_espera+='astdout, astderr = %s.communicate()'%(letras[x])
        else:
         instrucciones_espera+='astdout, astderr = %s.communicate();'%(letras[x])

    instrucciones=compile(instrucciones, '<string>', 'exec') # compila el texto para que sea ejecutado de mejor forma por el interprete de python
    instrucciones_espera=compile(instrucciones_espera, '<string>', 'exec') # compila el texto para que sea ejecutado de mejor forma por el interprete de python
    exec(instrucciones) # ejecuta las instrucciones de ejecución compiladas
    exec(instrucciones_espera) # ejecuta las instrucciones compiladas de espera
    # la linea a continuación construye un arreglo de todos las partes procesadas
    arreglo_features=[r"%s"%FolderEntrada+"\\Partes\\"+str(numx)+"\\bd"+str(numx)+".gdb\\cuadrox_"+str(numx) for numx in xrange(1,numeroprocesos+1)]
    output=capa_de_salida
    capa_fuente=r"%s"%FolderEntrada+"\\Partes\\"+str(1)+"\\bd"+str(1)+".gdb\\cuadrox_1" # nuevo


    no_existen,existen,i=[],[],1

    for capa in arreglo_features:
        if arcpy.Exists(capa):
            existen.append(i)
        else:
            no_existen.append(i)
        i+=1

    if len(no_existen)==0:
        arreglo_features=listaanidada(arreglo_features,";")
        ruta_unificado,nombre_salida =os.path.split(capa_de_salida)
        arcpy.CreateFeatureclass_management(ruta_unificado,nombre_salida ,
                "POLYGON", capa_fuente, "SAME_AS_TEMPLATE", "SAME_AS_TEMPLATE", capa_fuente)
        arcpy.AddMessage(arreglo_features)
        arcpy.AddMessage(output)
        arcpy.Append_management (inputs=arreglo_features, target=output, schema_type="NO_TEST") # nuevo
        if datos_intermedios == "false":
            shutil.rmtree(r"%s"%FolderEntrada+"\\Partes")
    else:
        arcpy.AddError("no se pudieron procesar las secciones: "+str(no_existen))






