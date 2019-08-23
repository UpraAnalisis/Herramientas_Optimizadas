# -*- coding: utf-8 -*-
import arcpy,os,time,exceptions

try:
    t_inicio=time.clock()# captura el tiempo de inicio del proceso
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3116)
    arcpy.env.overwriteOutput = True
    infea=arcpy.GetParameterAsText(0)
    nombre_salida=arcpy.GetParameterAsText(1)

    if __name__ == '__main__':
        print "Ejecutando Multi part to single part a 64bits ...."
        arcpy.MultipartToSinglepart_management (in_features=infea, out_feature_class=nombre_salida)

except exceptions.Exception as e:
    print e.__class__, e.__doc__, e.message
    os.system("pause")
