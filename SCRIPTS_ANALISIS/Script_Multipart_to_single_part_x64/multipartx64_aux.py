# -*- coding: utf-8 -*-
import arcpy,os,time
t_inicio=time.clock()# captura el tiempo de inicio del proceso
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3116)
arcpy.env.overwriteOutput = True


infea=arcpy.GetParameterAsText(0)
gdb_salida=arcpy.GetParameterAsText(1)
nombre_salida=arcpy.GetParameterAsText(2)

##infea=r"U:\SCRIPTS_ANALISIS\Script_Multi_Update_Union_Clip_Intersect\Datos_demo.gdb\Predios_demo"
##gdb_salida=r"C:\Users\carlos.cano\Documents\ArcGIS\Default.gdb"
##nombre_salida="test_multipart"

if __name__ == '__main__':
    print "Ejecutando Multi part to single part a 64bits ...."
##    if arcpy.Exists(gdb_salida+"\\"+capa_salida):
##            arcpy.Delete_management(gdb_salida+"\\"+nombre_salida)
    arcpy.MultipartToSinglepart_management (in_features=infea, out_feature_class=gdb_salida+"\\"+nombre_salida)

