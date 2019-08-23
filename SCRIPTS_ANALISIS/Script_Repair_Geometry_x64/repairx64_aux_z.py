# -*- coding: utf-8 -*-
import arcpy,os,time,exceptions
try:
    t_inicio=time.clock()# captura el tiempo de inicio del proceso
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3116)
    arcpy.env.overwriteOutput = True


    infea=arcpy.GetParameterAsText(0)
    delete_null= arcpy.GetParameterAsText(1)


    if __name__ == '__main__':
        print "Ejecutando repair geometry a 64bits ...."
        print infea , delete_null
        arcpy.RepairGeometry_management(in_features=infea, delete_null=delete_null)

except exceptions.Exception as e:
    print e.__class__, e.__doc__, e.message
    os.system("pause")

