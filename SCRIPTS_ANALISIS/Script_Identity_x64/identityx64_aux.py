# -*- coding: utf-8 -*-
import arcpy,os,time,exceptions
try:
    t_inicio=time.clock()# captura el tiempo de inicio del proceso
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3116)
    arcpy.env.overwriteOutput = True


    infea=arcpy.GetParameterAsText(0)
    segunda_capa= arcpy.GetParameterAsText(1)
    join_attributes=arcpy.GetParameterAsText(2)
    gdb_salida=arcpy.GetParameterAsText(3)
    capa_salida=arcpy.GetParameterAsText(4)

    arcpy.env.workspace = gdb_salida
    ##output=""


    if __name__ == '__main__':
        print "Ejecutando identity a 64bits ...."
        print infea , segunda_capa,capa_salida,gdb_salida
##        if arcpy.Exists(gdb_salida+"\\"+capa_salida):
##            arcpy.Delete_management(gdb_salida+"\\"+capa_salida)
        arcpy.Identity_analysis(in_features=infea,identity_features=segunda_capa, out_feature_class=gdb_salida+"\\"+capa_salida,join_attributes=join_attributes)

except exceptions.Exception as e:
    print e.__class__, e.__doc__, e.message
    os.system("pause")

