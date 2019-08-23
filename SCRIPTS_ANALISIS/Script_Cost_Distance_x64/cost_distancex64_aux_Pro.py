# -*- coding: utf-8 -*-
import arcpy
from arcpy.sa import *
import os,time #exceptions
arcpy.env.parallelProcessingFactor = 0
try:
    t_inicio=time.clock()# captura el tiempo de inicio del proceso
    arcpy.env.overwriteOutput = True


    in_source_data=arcpy.GetParameterAsText(0)
    sp=int(arcpy.Describe(in_source_data).spatialreference.factoryCode)
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(sp)

    in_cost_raster=arcpy.GetParameterAsText(1)
    maximum_distance=arcpy.GetParameterAsText(2)
    if maximum_distance!="---":
        maximum_distance=int(arcpy.GetParameterAsText(2))
    else:
        maximum_distance=""
    out_backlink_raster=arcpy.GetParameterAsText(3)
    capa_extent=arcpy.GetParameterAsText(4)
    capa_salida=arcpy.GetParameterAsText(5)
    if "....." in capa_extent:
        capa_extent=capa_extent.replace("....."," ")
    if "," not in capa_extent:
        if "MAXOF" in capa_extent or "MINOF"in capa_extent:
            arcpy.env.extent=capa_extent
        else:
            arcpy.env.extent=arcpy.Describe(capa_extent).extent

    else:

        arcpy.env.extent=capa_extent

    if out_backlink_raster=="---":
        out_backlink_raster=""

        if arcpy.CheckOutExtension("Spatial"):
            1+1
        else:
            arcpy.AddMessage ("Usted no tiene habilitada la extensión Spatial Analyst")
            os.system("pause")


    if __name__ == '__main__':
        print("Ejecutando cost distance a 64bits ....")
        print(in_source_data ,in_cost_raster,maximum_distance,out_backlink_raster)
        outCostDistance = CostDistance(in_source_data=in_source_data, in_cost_raster=in_cost_raster, maximum_distance=maximum_distance, out_backlink_raster=out_backlink_raster)
        outCostDistance.save(capa_salida)

except Exception as e:
    print(type(inst))
    print(inst.args)
    print(inst)
    os.system("pause")