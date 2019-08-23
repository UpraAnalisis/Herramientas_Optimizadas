# -*- coding: utf-8 -*-
import arcpy
from arcpy.sa import *
import os,time,exceptions

try:
    t_inicio=time.clock()# captura el tiempo de inicio del proceso
    #arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3116)
    arcpy.env.overwriteOutput = True

    in_features = arcpy.GetParameterAsText(0)
    population_field = arcpy.GetParameterAsText(1)
    capa_salida = arcpy.GetParameterAsText(2)
    cell_size = arcpy.GetParameterAsText(3)
    search_radius = arcpy.GetParameterAsText(4)
    area_unit_scale_factor = arcpy.GetParameterAsText(5)
    out_cell_values = arcpy.GetParameterAsText(6)
    method = arcpy.GetParameterAsText(7)
    entorno=arcpy.GetParameterAsText(8)
    arcpy.env.outputCoordinateSystem = arcpy.Describe(in_features).spatialReference
	

    if cell_size!="---":
        cell_size=cell_size
    else:
        cell_size=""

    if search_radius!="---":
        search_radius=search_radius
    else:
        search_radius=""

    if area_unit_scale_factor!="---":
        area_unit_scale_factor=area_unit_scale_factor
    else:
        area_unit_scale_factor=""




    variables =[var for var in dir(arcpy.env) if "_" not in var and "packageWorkspace" not in var and "scratch" not in var]

    def recibe_environ(palabras_entorno,valores_entorno):
        valores_entorno=valores_entorno.split("***")
        for i in xrange(len(palabras_entorno)):
            if "geoprocessing._base.GPEnvironment" in valores_entorno[i]:
                valores_entorno[i]= None
            pivote="arcpy.env.%s"%(palabras_entorno[i])
            exec("""tipo= type(%s)"""%(pivote))
            if "\\" in (valores_entorno[i]):
                    valores_entorno[i]=valores_entorno[i].replace("\\","\\\\")

            if unicode == tipo:
                instruc_a="""arcpy.env.%s = %s"""%(palabras_entorno[i],valores_entorno[i].replace("....."," "))
                if "None" not in instruc_a:
                    instruc_a="""arcpy.env.%s = """%(palabras_entorno[i].replace("....."," "))+'"'+"%s"%(valores_entorno[i].replace("....."," "))+'"'
                    exec(instruc_a)

                else:
                    instruc_a="""arcpy.env.%s = %s"""%(palabras_entorno[i],valores_entorno[i].replace("....."," "))
                    exec(instruc_a)

            if int == tipo:
                instruc_a="""arcpy.env.%s = %s"""%(palabras_entorno[i],valores_entorno[i].replace("....."," "))
                exec(instruc_a)

            if float == tipo:
                instruc_a="""arcpy.env.%s = %s"""%(palabras_entorno[i],valores_entorno[i].replace("....."," "))
                exec(instruc_a)


            if long == tipo:
                instruc_a="""arcpy.env.%s = %s"""%(palabras_entorno[i],valores_entorno[i].replace("....."," "))
                exec(instruc_a)


            if type(None) == tipo:
                instruc_a="""arcpy.env.%s = %s"""%(palabras_entorno[i],valores_entorno[i].replace("....."," "))
                if "None" not in instruc_a:
                    instruc_a="""arcpy.env.%s = """%(palabras_entorno[i].replace("....."," "))+'"'+"%s"%(valores_entorno[i].replace("....."," "))+'"'
                    exec(instruc_a)

                else:
                    instruc_a="""arcpy.env.%s = %s"""%(palabras_entorno[i],valores_entorno[i].replace("....."," "))
                    exec(instruc_a)

            if bool == tipo:
                instruc_a="""arcpy.env.%s = %s"""%(palabras_entorno[i],valores_entorno[i].replace("....."," "))
                if "isCancelled" not in instruc_a:
                    exec(instruc_a)



    if arcpy.CheckOutExtension("Spatial"):
        1+1
    else:
        print "Usted no tiene habilitada la extensión Spatial Analyst"
        os.system("pause")


    if __name__ == '__main__':
        print "Ejecutando Kernel Density a 64bits ...."
        print in_features,population_field,capa_salida, cell_size,search_radius,area_unit_scale_factor,out_cell_values,method,entorno
        valores_entorno=entorno.split("***")
	print "#######" +str(arcpy.env.outputCoordinateSystem)
	print [str(variables[x]) +"_"+str(valores_entorno[x]) for x in xrange(len(valores_entorno))]
	recibe_environ(variables,entorno)
	


        in_layer=arcpy.MakeFeatureLayer_management(in_features,arcpy.Describe(in_features).name)
        outKernelDensity = KernelDensity (in_features = in_layer, population_field = population_field, cell_size = cell_size, search_radius = search_radius
        , area_unit_scale_factor = area_unit_scale_factor, out_cell_values = out_cell_values, method = method)
        outKernelDensity.save(capa_salida)

except exceptions.Exception as e:
    print e.__class__, e.__doc__, e.message
    os.system("pause")