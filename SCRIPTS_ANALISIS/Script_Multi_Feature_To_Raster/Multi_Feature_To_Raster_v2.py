# -*- coding: utf-8 -*-
# --------------------------------------------------------------------
# Multi_Dissolve.py
# Fecha de creacion: 2016-08-01 08:59:08.00000
# Author: Carlos Mario Cano Campillo
# Email: carlos.cano@upra.gov.co / kanocampillo@gmail.com
# Propietario: Unidad de Planificación Rural Agropecuaria
#
# ---------------------------------------------------------------------
#=====================Librerias==============================#
import arcpy,random, time,os,subprocess,time,inspect,shutil
import string
from arcpy.sa import *
# ------------------------------------------------------------
#=========Variables Globales y de Entorno=====================#

t_inicio=time.clock()# captura el tiempo de inicio del proceso
arcpy.env.workspace = "in_memory" # fija el espacio de trabajo en memoria
ws=arcpy.env.workspace # variable que almacena el espacio de trabajo
arcpy.env.overwriteOutput = True # fija la variable de entrorno para sobrescribir resultados
comandos=[] # arreglo que almacena los parámetros que se enviarán al script auxiliar
cuadros_no_prioritarios=[] # variable que se usará en desarrollos posteriores
cuadros_prioritarios=[] # variable que se usará en desarrollos posteriores
#=========parámetros de entrada=====================#
in_features=arcpy.GetParameterAsText(0)
in_features=arcpy.Describe(in_features).catalogPath
raster_salida=r"%s"%(arcpy.GetParameterAsText(1).encode("utf-8")) # parámetro que almacena el nombre del featureclass resultante
feaGrilla=arcpy.GetParameterAsText(2) # paráetro que almacena la feture class de la grilla auxiliar
ruta_raiz=arcpy.GetParameterAsText(3)
campo=arcpy.GetParameterAsText(4) # parámetro que almacena el campo por el cual se realizará el dissolve
cell_size=float(arcpy.GetParameterAsText(5))
##tipo=arcpy.GetParameterAsText(6)
numeroprocesos=int(str(arcpy.GetCount_management(feaGrilla)))# parámetro que almacena el número de cuadros de la grilla auxiliar
procesossimultaneos=int(arcpy.GetParameterAsText(6)) # parámetro que almcena el número de procesos que se ejecuatarán de forma paralela
datos_intermedios=arcpy.GetParameterAsText(7)
arcpy.env.extent=arcpy.Describe(in_features).extent




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

def chunkIt(seq, num): # realiza la división del numero de cuadros a procesar entre el número de procesos simultaneos
  avg = len(seq) / float(num)
  out = []
  last = 0.0

  while last < len(seq):
    out.append(seq[int(last):int(last + avg)])
    last += avg

  return out

def pasarlista(lista): # prepara los argumentos para ser enviados al script auxiliar
    lista=str(lista)
    lista=lista.replace(", ","_")
    return lista

def listaanidada(lista,separador): #convierte un arreglo en una lista anidada
    seq = tuple(lista)
    texto_anidado=separador.join( seq )
    return texto_anidado

def creadirs(): # crea los directorios de salida del programa
    nombre="unificado"
    if not os.path.exists(ruta_raiz+"\\%s"%(nombre)):
        os.makedirs(ruta_raiz+"\\%s"%(nombre))
    return ruta_raiz+"\\%s"%nombre


def crearFGDB(ruta): # crea una file geodatabase para almacenar el resultado unificado
    arcpy.CreateFileGDB_management(ruta, "bd_unificado.gdb")
    return ruta+"\\"+"bd_unificado.gdb"

#=========Validación de requerimientos=====================#

pyexe = getPythonPath()

if not "x64" in r"%s"%(pyexe):
    pyexe=pyexe.replace("ArcGIS","ArcGISx64")
if not arcpy.Exists(pyexe):
    arcpy.AddError("Usted no tiene instalado el Geoprocesamiento en segundo plano (64 bits)")
    raise RuntimeError("Usted no tiene instalado el Geoprocesamiento en segundo plano (64 bits) {0}".format(pyexe))
else:
    verPython64=pyexe
    scriptAuxiliar="Multi_Feature_To_Raster_Aux_V2.py" # almacena la ruta del script auxiliar
    verPythonfinal=verPython64
# ------------------------------------------------------------


#=====================funciones principal=====================#
if __name__ == '__main__':
    unicos=[]
    dicti={}

##    arcpy.AddField_management(in_features,campo+"_aux")
##    campo_aux=campo+"_aux"
##    with arcpy.da.SearchCursor(in_features,campo)as cursor:
##        for row in cursor:
##            valor=row[0]
##            if valor not in unicos:
##                unicos.append(valor)
##    for x in xrange(0,len(unicos)):
##        dicti.update({'%s'%(unicos[x]): x})
##    campox=[campo,campo_aux]
##
##    with arcpy.da.UpdateCursor(in_features,campox)as cursor1:
##     for row in cursor1:
##        row[1]=dicti[row[0]]
##        cursor1.updateRow(row)


    verPython=verPython64  # define la versión de python de 64 para ser empleada en el procesamiento
    verPythonDir=verPython.replace("\\python.exe","") # obtiene la ruta del ejecutable de python definido
    script=directorioyArchivo() # almacena la ruta del archivo del script actual
    script=script[1]+"\\"+scriptAuxiliar # almacena la ruta del script auxiliar
    arcpy.AddMessage(script) # imprime la ruta del script
    cuadros=[num for num in xrange(1,numeroprocesos+1)] # define los cuadros que van a ser procesados
    for i in xrange(len(cuadros)): # les quita a la lista de cuadros aquellos cuadros que son prioritarios
        if cuadros[i] not in cuadros_prioritarios:
            cuadros_no_prioritarios.append(cuadros[i])
    # terminar el arreglo de cuadros prioritarios
    arcpy.AddMessage("generando cuadros")
    cuadros_ram=cuadros
    random.shuffle(cuadros_ram)
    partes=chunkIt(cuadros_ram,procesossimultaneos)
    arcpy.AddMessage( r"start %s %s %s"%(verPython,script,pasarlista(partes)))
    arcpy.AddMessage("iniciando subproceso")

    if procesossimultaneos!= len(partes): # valida que los procesos coincidad con el numero de partes
        partes1=partes[:]
        partes1.pop(-1)
        partes1[-1].extend(partes[-1])
        del partes
        partes=partes1[:]

    for a in partes: # almacena los comandos en un arreglo
         comandos.append(r"start %s %s %s %s %s %s %s %s %s"%(verPython,script,in_features,raster_salida,feaGrilla,ruta_raiz,campo,cell_size,pasarlista(a)))
##         comandos.append(r"start %s %s %s %s %s %s %s %s %s"%(verPython,script,in_features,nombreSalida,rutasalida,feaGrilla,campo_aux,cell_size,pasarlista(a)))
    for a in comandos:
        arcpy.AddMessage(a)
    letras=string.ascii_letters # almacena un listado de letras
    instrucciones="" # variable que almacena las instrucciones a enviar al script auxiliar
    instrucciones_espera="" # variable que almacena el comando que espera por la ejecución de los procesos en paralelo
    for x in xrange(0,procesossimultaneos): # realiza la contruccion de las intrucciones para ejecutar los procesos en paralelo en el script auxiliar
        if x==procesossimultaneos-1 :
            instrucciones+='%s = subprocess.Popen(comandos[%s],stdin=None,stdout=subprocess.PIPE,shell=True,env=dict(os.environ, PYTHONHOME=verPythonDir))'%(letras[x],str(x))
        else:
            instrucciones+='%s = subprocess.Popen(comandos[%s],stdin=None,stdout=subprocess.PIPE,shell=True,env=dict(os.environ, PYTHONHOME=verPythonDir));'%(letras[x],str(x))
    for x in xrange(0,procesossimultaneos):
        if x==procesossimultaneos-1 :
         instrucciones_espera+='astdout, astderr = %s.communicate()'%(letras[x])
        else:
         instrucciones_espera+='astdout, astderr = %s.communicate();'%(letras[x])
    instrucciones=compile(instrucciones, '<string>', 'exec')
    instrucciones_espera=compile(instrucciones_espera, '<string>', 'exec')
    exec(instrucciones)
    exec(instrucciones_espera)
    arreglo_features=[r"%s"%ruta_raiz+"\\Partes\\"+str(numero)+"\\bd"+str(numero)+".gdb\\cuadrox_"+str(numero) for numero in xrange(1,numeroprocesos+1)] # crea el listado de las partes del proceso
##    parte_demo=arreglo_features.pop()
##    arreglo_features.append(parte_demo)
##    arreglo_features.reverse()
##    ruta_unificado=creadirs() # crea el directorio final
##    ruta_unificado=crearFGDB(ruta_unificado) # crea la file  geodatabase que almacena el resultado unificado
    output=raster_salida
##    output=ruta_unificado+"\\"+str(nombreSalida) # almacena la ruta del archivo final
    no_existen,existen,i=[],[],1 # crea las varibales que almacenarán los arreglo de la comprobación de procesos completados y fallidos

    for capa in arreglo_features: # verifica cuales fueron los procesos completados con exito y los fallidos
        if arcpy.Exists(capa):
            existen.append(i)
        else:
            no_existen.append(i)
        i+=1

    if len(no_existen)==0: # si todos los procesos fueron completados con exito
        arreglo_features=listaanidada(arreglo_features,";") # almacena el listado de los archivos generados por lo procesos exitosos
##        arcpy.MosaicToNewRaster_management(input_rasters=arreglo_features, output_location=ruta_unificado,
##        raster_dataset_name_with_extension=nombreSalida,pixel_type="8_BIT_UNSIGNED",cellsize=cell_size, number_of_bands=1, mosaic_colormap_mode= tipo)
##        raster_final=arcpy.MakeRasterLayer_management (output, nombreSalida)

        ruta_final,nombre_salida =os.path.split(raster_salida) # variable que almacena la ruta de salida y el nombre
##        arcpy.AddMessage(arreglo_features+"__"+ str(ruta_unificado)+"__"+str(nombreSalida)+"__"+str(cell_size)+"__"+str(tipo))

        arcpy.MosaicToNewRaster_management (input_rasters=arreglo_features, output_location=ruta_final,
        raster_dataset_name_with_extension=nombre_salida, coordinate_system_for_the_raster = arcpy.SpatialReference(3116),
        pixel_type="8_BIT_UNSIGNED", cellsize=cell_size, number_of_bands=1, mosaic_colormap_mode="")
        arcpy.BuildRasterAttributeTable_management (ruta_final+"\\"+nombre_salida, "Overwrite")

##        raster_final=arcpy.MakeRasterLayer_management (ruta_final, nombre_salida)

##        dicti_inv= {v: k for k, v in dicti.iteritems()}################################
##        arcpy.AddField_management(raster_final,campo,"TEXT")
##        campox=[campo,"value"]
##        with arcpy.da.UpdateCursor(raster_final,campox)as cursor2:
##         for row in cursor2:
##            row[0]=dicti_inv[row[1]]
##            cursor2.updateRow(row)



        arcpy.AddMessage(arreglo_features) # imprime el listado de los features que seran unificados
        arcpy.AddMessage(output) # imprime la ruta de la salida final
##        arcpy.SetParameter(9, raster_final)
        if datos_intermedios == "false":
            shutil.rmtree(r"%s"%ruta_raiz)

        del output
    else:
        arcpy.AddError("no se puedieron procesar las secciones: "+str(no_existen)) # en caso de que algúna sección no se procesó muestra cual o cuales son en un mesnaje de error
    print "proceso Completado en %s Minutos." % ((time.clock() - t_inicio)/60)
