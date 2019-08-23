# -*- coding: utf-8 -*-
# --------------------------------------------------------------------
# Multi_buffer.py
# Fecha de creacion: 2016-08-01 08:59:08.00000
# Author: Carlos Mario Cano Campillo
# Email: carlos.cano@upra.gov.co / kanocampillo@gmail.com
# Propietario: Unidad de Planificación Rural Agropecuaria
#
# ---------------------------------------------------------------------
#=====================Librerias==============================#
import arcpy,random, time,os,subprocess,time,inspect,shutil
import string
# ------------------------------------------------------------
#=========Variables Globales y de Entorno=====================#

t_inicio=time.clock()# captura el tiempo de inicio del proceso
arcpy.env.workspace = "in_memory"
ws=arcpy.env.workspace
arcpy.env.overwriteOutput = True
ws=arcpy.env.workspace
lGrilla=""
campo_id_cuadro="PageNumber"

comandos=[]
cuadros_no_prioritarios=[]
cuadros_prioritarios=[]
#=========parámetros de entrada=====================#
infea=arcpy.GetParameterAsText(0)
infea=arcpy.Describe(infea).catalogPath
capa_salida=arcpy.GetParameterAsText(1)
rutasalida=arcpy.GetParameterAsText(2)
feaGrilla=arcpy.GetParameterAsText(3)

radio= arcpy.GetParameterAsText(4)
radio=radio.replace(" ","_")

disolve=arcpy.GetParameterAsText(5)
line_side=arcpy.GetParameterAsText(6)
line_end_type=arcpy.GetParameterAsText(7)
dissolve_field=arcpy.GetParameterAsText(8)
numeroprocesos=int(str(arcpy.GetCount_management(feaGrilla)))
procesossimultaneos=int(arcpy.GetParameterAsText(9))
datos_intermedios=arcpy.GetParameterAsText(10)



ruta_raiz=rutasalida

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
    scriptAuxiliar="Multi_buffer_Aux_v3.py"
    verPythonfinal=verPython64
# ------------------------------------------------------------

def chunkIt(seq, num):
  avg = len(seq) / float(num)
  out = []
  last = 0.0

  while last < len(seq):
    out.append(seq[int(last):int(last + avg)])
    last += avg

  return out

def pasarlista(lista):
    lista=str(lista)
    lista=lista.replace(", ","_")
    return lista

def listaanidada(lista,separador): #convierte un arreglo en una lista anidada
    seq = tuple(lista)
    texto_anidado=separador.join( seq )
    return texto_anidado

def creadirs(): # crea los dierctorios de salida del programa
    nombre="unificado"
    if not os.path.exists(ruta_raiz+"\\%s"%(nombre)):
        os.makedirs(ruta_raiz+"\\%s"%(nombre))
    return ruta_raiz+"\\%s"%nombre


def crearFGDB(ruta):
    arcpy.CreateFileGDB_management(ruta, "bd_unificado.gdb")
    return ruta+"\\"+"bd_unificado.gdb"

#=====================funciones principal=====================#
if __name__ == '__main__':
    verPython=verPython64
    verPythonDir=verPython.replace("\\python.exe","")
    script=directorioyArchivo()
    script=script[1]+"\\"+scriptAuxiliar
    arcpy.AddMessage(script)
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
         comandos.append(r"start %s %s %s %s %s %s %s %s %s %s %s"%(verPython,script,infea,feaGrilla,radio,disolve,rutasalida,line_side,line_end_type,dissolve_field,pasarlista(a)))
    for a in comandos:
        arcpy.AddMessage(a)

    letras=string.ascii_letters
    instrucciones=""
    instrucciones_espera=""
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
    instrucciones=compile(instrucciones, '<string>', 'exec')
    instrucciones_espera=compile(instrucciones_espera, '<string>', 'exec')
    exec(instrucciones)
    exec(instrucciones_espera)

    arreglo_features=[r"%s"%ruta_raiz+"\\Partes\\"+str(numero)+"\\bd"+str(numero)+".gdb\\cuadrox_"+str(numero) for numero in xrange(1,numeroprocesos+1)]
    ruta_unificado=creadirs()
    ruta_unificado,nombre_salida =os.path.split(capa_salida)
    output=ruta_unificado+"\\"+str(nombre_salida)

    capa_fuente=r"%s"%ruta_raiz+"\\Partes\\"+str(1)+"\\bd"+str(1)+".gdb\\cuadrox_1" # nuevo


    no_existen,existen,i=[],[],1


    for capa in arreglo_features:
        if arcpy.Exists(capa):
            existen.append(i)
        else:
            no_existen.append(i)
        i+=1


    if len(no_existen)==0:
        arreglo_features=listaanidada(arreglo_features,";")
        arcpy.CreateFeatureclass_management(ruta_unificado,nombre_salida ,
                "POLYGON", capa_fuente, "SAME_AS_TEMPLATE", "SAME_AS_TEMPLATE", capa_fuente)
        arcpy.AddMessage(arreglo_features)
        arcpy.AddMessage(output)
        arcpy.Append_management (inputs=arreglo_features, target=output, schema_type="NO_TEST") # nuevo
        if datos_intermedios == "false":
            shutil.rmtree(r"%s"%ruta_raiz)


    print "proceso Completado en %s Minutos." % ((time.clock() - t_inicio)/60)



##    arcpy.SetParameter(6, infea)