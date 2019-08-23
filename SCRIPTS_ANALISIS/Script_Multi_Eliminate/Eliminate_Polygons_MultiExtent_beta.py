# -*- coding: utf-8 -*-
import os
import arcpy
from arcpy import env
import subprocess
import time,inspect
import random ,string


#variables de entrorno y globales
sr = arcpy.SpatialReference(3116)
t_inicio=time.clock()# captura el tiempo de inicio del proceso


FolderEntrada = r"%s"%arcpy.GetParameterAsText(0) # Folder donde se almacenarán los datos resultantes
FolderEntrada=r"%s"%FolderEntrada
numeroprocesos = r"%s"%arcpy.GetParameterAsText(1) # Número de secciones o features en la grilla de procesamiento
numeroprocesos=int(numeroprocesos) # convierte en entero el parámetro que ingresa como texto
procesossimultaneos = r"%s"%arcpy.GetParameterAsText(2) # captura el número de procesos simultaneos que se van a ejecutar para procesar todas las secciones de la grilla
procesossimultaneos=int(procesossimultaneos) # convierte en entero el parámetro de procesos simultaneos
fcEntrada = r"%s"%arcpy.GetParameterAsText(3) # Capa que se va a procesar.
fcEntrada=arcpy.Describe(fcEntrada).catalogPath # captura la ruta del feature class representado por el layer
grilla = r"%s"%arcpy.GetParameterAsText(4) # Grilla de apoyo. El proceso se hará de forma individual por cada uno de los cuadros.
grilla=arcpy.Describe(grilla).catalogPath # captura la ruta del feature class representado por el layer
consulta = arcpy.GetParameterAsText(5) # Expresión que actua como un criterio, que aplicará el eliminate sobre los fetures que cumplan con lo especificado en dicha expresión.
nombreSalida=arcpy.GetParameterAsText(6) # captura el nombre de salida del feature class resultante del proceso

scriptAuxiliar="Eliminate_Polygons_MultiExtent_centroid.py" # script auxiliar que ejecuta el prceso de eliminate
verPythonfinal=r"C:\Python27\ArcGIS10.3\python.exe" # ruta del ejecutable de python

dic={" ":"__","=":"igual", "<":"menor", ">": "mayor"} # diccionario que convierte los caracteres especiales en letras
comandos=[] # arreglo que almacena los comandos a ejecutar por el script auxiliar

for i in dic: # ciclo que reemplaza los carateres especiales
    consulta=consulta.replace(i,dic[i])


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

if __name__ == '__main__':
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

    for a in partes: # almacena los comandos en un arreglo
         comandos.append(r"start %s %s %s %s %s %s %s"%(verPython,script,fcEntrada,grilla,pasarlista(a),dirSalida,consulta))

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
    print "Proceso de unificacion"
    print "borrando temporales"
    # la linea a continuación construye un arreglo de todos las partes procesadas
    arreglo_features=[r"%s"%FolderEntrada+"\\Partes\\"+str(numx)+"\\bd"+str(numx)+".gdb\\cuadrox_"+str(numx)+"_Final" for numx in xrange(1,numeroprocesos+1)]
    ruta_unificado=creadirs() # crea el directorio donde se almacenará la información final
    ruta_unificado=crearFGDB(ruta_unificado) # crea la gdb donse se almacenará la información final
    output=ruta_unificado+"\\"+str(nombreSalida) # almacena la ruta final
    # captura la ruta de la primera parte con el fin de realizar una copia de la misma
    capa_fuente=r"%s"%FolderEntrada+"\\Partes\\"+str(1)+"\\bd"+str(1)+".gdb\\cuadrox_"+str(1)+"_Final"

    no_existen,existen,i=[],[],1 # inicializa las variables que almacenarán las secciones procesadas y aquellas que no se pudieron procesar
    for capa in arreglo_features: # si la sección existe o fue procesada se almacena en el arreglo de existen sino en el de no existen
        if arcpy.Exists(capa):
            existen.append(i)
        else:
            no_existen.append(i)
        i+=1

    if len(no_existen)==0: # si el arreglo de no existen no tiene ningún elemento procesa la unificación
        arreglo_features=listaanidada(arreglo_features,";")
        arcpy.CopyFeatures_management(capa_fuente,output) # nuevo
        arcpy.TruncateTable_management(output) # nuevo
        arcpy.AddMessage(arreglo_features)
        arcpy.AddMessage(output)
        arcpy.Append_management (inputs=arreglo_features, target=output, schema_type="NO_TEST") # nuevo
        layer_salida=arcpy.MakeFeatureLayer_management(output,nombreSalida)
        arcpy.SetParameter(7, layer_salida)
    else: # en caso de que existan secciones que no pudieron ser procesadas se muestra el siguiente texto
        arcpy.AddError("no se pudieron procesar las secciones: "+str(no_existen))
    print "Proceso de unificacion terminado"
    print "Eliminate Polygon MultiExtent Completado en %s segundos." % (time.clock() - t_inicio)




