# -*- coding: utf-8 -*-
import arcpy
from arcpy.sa import *
import os,time,exceptions

try:
    t_inicio=time.clock()# captura el tiempo de inicio del proceso
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3116)
    arcpy.env.overwriteOutput = True


    in_source_data=arcpy.GetParameterAsText(0)
    in_cost_raster=arcpy.GetParameterAsText(1)
    maximum_distance=arcpy.GetParameterAsText(2)
    if maximum_distance!="---":
        maximum_distance=int(arcpy.GetParameterAsText(2))
    else:
        maximum_distance=""
    out_backlink_raster=arcpy.GetParameterAsText(3)
    capa_extent=arcpy.GetParameterAsText(4)
    print capa_extent
    capa_salida=arcpy.GetParameterAsText(5)
    if "....." in capa_extent:
        capa_extent=capa_extent.replace("....."," ")
    if "," not in capa_extent:
        if "MAXOF" in capa_extent or "MINOF"in capa_extent:
            arcpy.env.extent=capa_extent
        else:
            arcpy.env.extent=arcpy.Describe(capa_extent).extent

    else:
##        print capa_extent
        arcpy.env.extent=capa_extent

##    print capa_extent
##    os.system("pause")

##    in_source_data=r"U:\SCRIPTS_ANALISIS\Script_Cost_Distance_x64\Datos_Demo.gdb\Puntos_Nodos"
##    in_cost_raster=r"U:\SCRIPTS_ANALISIS\Script_Cost_Distance_x64\Datos_Demo.gdb\Extract_COST11"
##    maximum_distance=4300000
##    out_backlink_raster="---"
##    capa_salida=r"C:\Users\carlos.cano\Documents\ArcGIS\Default.gdb\dddd"
    if out_backlink_raster=="---":
        out_backlink_raster=""
##    if maximum_distance=="---":
##        maximum_distance=""
    ##output=""

    if arcpy.CheckOutExtension("Spatial"):
        1+1
    else:
        print "Usted no tiene habilitada la extensión Spatial Analyst"
        os.system("pause")


    if __name__ == '__main__':
        print "Ejecutando cost distance a 64bits ...."
        print in_source_data ,in_cost_raster,maximum_distance,out_backlink_raster
        outCostDistance = CostDistance(in_source_data=in_source_data, in_cost_raster=in_cost_raster, maximum_distance=maximum_distance, out_backlink_raster=out_backlink_raster)
        outCostDistance.save(capa_salida)

except exceptions.Exception as e:
    print e.__class__, e.__doc__, e.message
    os.system("pause")