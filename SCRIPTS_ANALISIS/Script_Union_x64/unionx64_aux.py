# -*- coding: utf-8 -*-
import arcpy,os,time,exceptions
try:
    t_inicio=time.clock()# captura el tiempo de inicio del proceso
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3116)
    arcpy.env.overwriteOutput = True


    infea=arcpy.GetParameterAsText(0)
    segunda_capa= arcpy.GetParameterAsText(1)
    join_attributes=arcpy.GetParameterAsText(2)
    gaps=arcpy.GetParameterAsText(3)
    gdb_salida=arcpy.GetParameterAsText(4)
    capa_salida=arcpy.GetParameterAsText(5)

    arcpy.env.workspace = gdb_salida
    ##output=""


    if __name__ == '__main__':
        print "Ejecutando union a 64bits ...."
        print infea , segunda_capa,capa_salida,gdb_salida
        arcpy.Union_analysis (in_features=[infea,segunda_capa], out_feature_class=gdb_salida+"\\"+capa_salida,join_attributes=join_attributes,gaps=gaps)

except exceptions.Exception as e:
    print e.__class__, e.__doc__, e.message
    os.system("pause")

