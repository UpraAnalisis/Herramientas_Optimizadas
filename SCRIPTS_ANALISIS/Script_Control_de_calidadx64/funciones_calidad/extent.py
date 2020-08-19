#-*- coding: 'utf-8' -*-
import arcpy
import datetime
import random
arcpy.env.overwriteOutput = 1

def crea_capa_extent(capa):
    pre_ti = datetime.datetime.now().strftime("%b_%d_%Y_%H_%M_%S") +str(random.randint(400,800))
    pre_ti = pre_ti.replace(".","")
    nueva_capa=arcpy.ValidateTableName(arcpy.Describe(capa).name+"%s_gg"%pre_ti,"in_memory")
    sr=arcpy.SpatialReference(arcpy.Describe(capa).spatialReference.factoryCode)
    extension = arcpy.Describe(capa).extent
    xmax = extension.XMax
    ymax = extension.YMax
    xmin = extension.XMin
    ymin = extension.YMin
    capa_ext = arcpy.CreateFeatureclass_management (out_path = "in_memory", out_name = nueva_capa,
    geometry_type ="POLYGON", has_m = "DISABLED", has_z = "DISABLED", spatial_reference  = sr)
    cuadro = arcpy.Polygon(arcpy.Array([arcpy.Point(xmin,ymax),arcpy.Point(xmax,ymax),arcpy.Point(xmax,ymin),arcpy.Point(xmin,ymin)]))
##    cursor = arcpy.da.InsertCursor(nueva_capa,"SHAPE@")
##    cursor.insertRow([cuadro])
    return cuadro

def distancia(capa1,capa2):
    c_capa1 = [x[0] for x in arcpy.da.SearchCursor(capa1,"SHAPE@")][0]
    c_capa2 = [x[0] for x in arcpy.da.SearchCursor(capa2,"SHAPE@")][0]
    return c_capa1.distanceTo(c_capa2)

def compara_capas(capa1,capa2):
    cuadro_capa1 = crea_capa_extent(capa1)
    cuadro_capa2 = crea_capa_extent(capa2)
    cen_capa1 = arcpy.FeatureToPoint_management(cuadro_capa1,"in_memory\\cp1s").getOutput(0)
    cen_capa2 = arcpy.FeatureToPoint_management(cuadro_capa2,"in_memory\\cp2s").getOutput(0)
    return distancia(cen_capa1,cen_capa2)
