# -*- coding: utf-8 -*-
import arcpy,os,time
t_inicio=time.clock()# captura el tiempo de inicio del proceso
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3116)
arcpy.env.overwriteOutput = True


infea=arcpy.GetParameterAsText(0)
feaUpdate= arcpy.GetParameterAsText(1)
capa_salida=arcpy.GetParameterAsText(3)
gdb_salida=arcpy.GetParameterAsText(2)
##output=""


if __name__ == '__main__':
    print "Ejecutando update a 64bits ...."
    print infea , feaUpdate,capa_salida,gdb_salida
    arcpy.Update_analysis(in_features=infea, update_features=feaUpdate, out_feature_class=gdb_salida+"\\"+capa_salida, keep_borders="BORDERS", cluster_tolerance="")

