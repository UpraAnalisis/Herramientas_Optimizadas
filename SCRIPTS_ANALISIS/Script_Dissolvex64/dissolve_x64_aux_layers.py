# -*- coding: utf-8 -*-
import arcpy,os,time,exceptions
t_inicio=time.clock()# captura el tiempo de inicio del proceso
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3116)
arcpy.env.overwriteOutput = True


infea=arcpy.GetParameterAsText(0)
campo= arcpy.GetParameterAsText(1)
capa_salida=arcpy.GetParameterAsText(2)
gdb_salida=arcpy.GetParameterAsText(3)
multi_part=arcpy.GetParameterAsText(4)
unsplit_lines=arcpy.GetParameterAsText(5)
##
if multi_part not in ('MULTI_PART','SINGLE_PART'):
    multi_part='MULTI_PART'
    print "##### POR FAVOR VERIFIQUE LOS ESPACIOS EN LA RUTA DE ENTRADA y salida"
if unsplit_lines not in ('DISSOLVE_LINES','UNSPLIT_LINES'):
    unsplit_lines='DISSOLVE_LINES'
    print "##### POR FAVOR VERIFIQUE LOS ESPACIOS EN LA RUTA DE ENTRADA y salida"
####output=""

try:
    if __name__ == '__main__':
        print "Ejecutando dissolve a 64bits ...."
        print infea , campo,multi_part,unsplit_lines,capa_salida,gdb_salida
##        if arcpy.Exists(gdb_salida+"\\"+capa_salida):
##            arcpy.Delete_management(gdb_salida+"\\"+capa_salida)
        arcpy.Dissolve_management (in_features=infea, out_feature_class=gdb_salida+"\\"+capa_salida, dissolve_field=campo,multi_part=multi_part, unsplit_lines=unsplit_lines)
except exceptions.Exception as e:
        print e.__class__, e.__doc__, e.message
        os.system("pause")