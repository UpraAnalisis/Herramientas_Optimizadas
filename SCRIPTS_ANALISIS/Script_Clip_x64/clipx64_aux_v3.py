# -*- coding: utf-8 -*-
import arcpy,os,time,exceptions
try:
    t_inicio=time.clock()# captura el tiempo de inicio del proceso
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3116)
    arcpy.env.overwriteOutput = True


    infea=arcpy.GetParameterAsText(0)
    segunda_capa= arcpy.GetParameterAsText(1)
    capa_salida=arcpy.GetParameterAsText(2)


    if __name__ == '__main__':
        print "Ejecutando clip a 64bits ...."
        print infea ,segunda_capa,capa_salida
        arcpy.arcpy.Clip_analysis(in_features=infea, clip_features=segunda_capa, out_feature_class=capa_salida)

except exceptions.Exception as e:
    print e.__class__, e.__doc__, e.message
    os.system("pause")

