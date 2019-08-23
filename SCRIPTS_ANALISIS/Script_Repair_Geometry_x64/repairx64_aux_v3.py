# -*- coding: utf-8 -*-
import arcpy,os,time,exceptions
try:
    t_inicio=time.clock()# captura el tiempo de inicio del proceso
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3116)
    arcpy.env.overwriteOutput = True


    infea=arcpy.GetParameterAsText(0)
    delete_null= arcpy.GetParameterAsText(1)
    en_memoria= arcpy.GetParameterAsText(2)
    num_ciclos= arcpy.GetParameterAsText(3)


    if __name__ == '__main__':
        print "Ejecutando repair geometry a 64bits ...."
        print infea , delete_null
        if en_memoria == "true":
            arcpy.CopyFeatures_management(infea, "in_memory\\"+arcpy.Describe(infea).name)
            capa_salida="in_memory\\"+arcpy.Describe(infea).name
            for x in xrange(int(num_ciclos)):
                print "procesando ciclo {}".format(x+1)
                arcpy.RepairGeometry_management(in_features=capa_salida, delete_null=delete_null)
            arcpy.CopyFeatures_management("in_memory\\"+arcpy.Describe(infea).name, arcpy.Describe(infea).catalogpath)

        else:
            capa_salida=infea
            for x in xrange(int(num_ciclos)):
                print "procesando ciclo {}".format(x+1)
                arcpy.RepairGeometry_management(in_features=capa_salida, delete_null=delete_null)

except exceptions.Exception as e:
    print e.__class__, e.__doc__, e.message
    os.system("pause")

