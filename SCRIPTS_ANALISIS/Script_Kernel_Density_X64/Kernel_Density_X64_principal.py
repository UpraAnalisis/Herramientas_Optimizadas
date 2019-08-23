# -*- coding: utf-8 -*-
# --------------------------------------------------------------------
# Kernel_Density_X64_principal.py
# Fecha de creacion: 2017-05-17 16:50:16.00000
# Author: Carlos Mario Cano Campillo
# Email: carlos.cano@upra.gov.co / kanocampillo@gmail.com
# Propietario: Unidad de Planificación Rural Agropecuaria
#
# ---------------------------------------------------------------------
#=====================Librerias==============================#
import arcpy,os,subprocess,time,inspect,sys
# ------------------------------------------------------------

#=========Variables Globales y de Entorno=====================#
t_inicio=time.clock()# captura el tiempo de inicio del proceso
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3116)
arcpy.env.overwriteOutput = True

in_features = r"%s"%(arcpy.GetParameterAsText(0))
in_features = arcpy.Describe(in_features).catalogPath
population_field = r"%s"%(arcpy.GetParameterAsText(1))
capa_salida = r"%s"%(arcpy.GetParameterAsText(2))
cell_size = r"%s"%(arcpy.GetParameterAsText(3))
search_radius = r"%s"%(arcpy.GetParameterAsText(4))
area_unit_scale_factor = r"%s"%(arcpy.GetParameterAsText(5))
out_cell_values = r"%s"%(arcpy.GetParameterAsText(6))
method = r"%s"%(arcpy.GetParameterAsText(7))


if population_field!="":
    population_field=population_field
else:
    population_field="NONE"

if cell_size!="":
    cell_size=cell_size
else:
    cell_size="---"

if search_radius!="":
    search_radius=search_radius
else:
    search_radius="---"

if area_unit_scale_factor!="":
    area_unit_scale_factor=area_unit_scale_factor
else:
    area_unit_scale_factor="---"

if out_cell_values!="":
    out_cell_values=out_cell_values
else:
    out_cell_values="DENSITIES"

if method!="":
    method=method
else:
    method="PLANAR"


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

# ------------------------------------------------------------

#=========Validación de reuqerimientos=====================#

pyexe = getPythonPath()

if not "x64" in r"%s"%(pyexe):
    pyexe=pyexe.replace("ArcGIS","ArcGISx64")
if not arcpy.Exists(pyexe):
    arcpy.AddError("Usted no tiene instalado el Geoprocesamiento en segundo plano (64 bits)")
    raise RuntimeError("Usted no tiene instalado el Geoprocesamiento en segundo plano (64 bits) {0}".format(pyexe))
else:
    verPython64=pyexe
    scriptAuxiliar="Kernel_Density_X64_aux.py"
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
        comando=r"start %s %s %s %s %s %s %s %s %s %s %s"%(verPython,script,in_features,population_field,capa_salida, cell_size,search_radius,area_unit_scale_factor,out_cell_values,method,entorno)
        ff=subprocess.Popen(comando,stdin=None,stdout=subprocess.PIPE,shell=True,env=dict(os.environ, PYTHONHOME=verPythonDir))
        astdout, astderr = ff.communicate()
        arcpy.AddMessage("proceso Completado en %s Minutos." % ((time.clock() - t_inicio)/60))