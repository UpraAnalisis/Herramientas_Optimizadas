# -*- coding: utf-8 -*-
# --------------------------------------------------------------------
# featorasterx64.py
# Fecha de creacion: 2016-08-01 08:59:08.00000
# Author: Carlos Mario Cano Campillo
# Email: carlos.cano@upra.gov.co / kanocampillo@gmail.com
# Propietario: Unidad de Planificación Rural Agropecuaria
#
# ---------------------------------------------------------------------
#=====================Librerias==============================#
import arcpy,os,subprocess,time,inspect,exceptions
from arcpy.sa import *
# ------------------------------------------------------------

#=========Variables Globales y de Entorno=====================#
t_inicio=time.clock()# captura el tiempo de inicio del proceso
try:
    def dict_raster(ras_entrada,ras_objetivo,campo):
        """ ras_entrada,ras_objetivo,campo"""
        unicos_values=[]
        unicos_campo=[]
        dicti1={}
        dicti2={}
        arcpy.AddField_management(in_table=ras_objetivo,field_name=campo,field_type="TEXT")

        with arcpy.da.SearchCursor(ras_entrada,["%s"%(campo),"Value"])as cursor:
            for row in cursor:
                value=row[0]
                campo_v=row[1]
                if value not in unicos_values:
                    unicos_values.append(value)
                    unicos_campo.append(campo_v)

        for x in xrange(0,len(unicos_values)):
            dicti1.update({'%s'%(unicos_values[x]): '%s'%(unicos_campo[x])})
            dicti2.update({'%s'%(unicos_campo[x]): '%s'%(unicos_values[x])})

        with arcpy.da.UpdateCursor(ras_objetivo,["Value","%s"%(campo)])as cursor1:
            for row in cursor1:
                row[1]=dicti2[str(row[0])]
                cursor1.updateRow(row)

    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3116)
    arcpy.env.overwriteOutput = True

    in_features=arcpy.GetParameterAsText(0)
    in_features=arcpy.Describe(in_features).catalogPath
    field= arcpy.GetParameterAsText(1)
    out_raster=arcpy.GetParameterAsText(2)
    cell_size=float(arcpy.GetParameterAsText(3))
    gdb_salida=arcpy.GetParameterAsText(4)
    capa_extent=arcpy.GetParameterAsText(5)
    mask=arcpy.GetParameterAsText(6)
    if "....." in capa_extent:
        capa_extent=capa_extent.replace("....."," ")
    if "," not in capa_extent:
        if "MAXOF" in capa_extent or "MINOF"in capa_extent:
            arcpy.env.extent=capa_extent
        else:
            arcpy.env.extent=arcpy.Describe(capa_extent).extent

    else:
        arcpy.env.extent=capa_extent


    if mask=="---":
        mask=""
    else:
         arcpy.env.mask =mask

    arcpy.env.workspace = gdb_salida

    if arcpy.CheckOutExtension("Spatial"):
        1+1
    else:
        print "Usted no tiene habilitada la extensión Spatial Analyst"
        os.system("pause")

    if __name__ == '__main__':
        print "Procesando el feature to raster a 64 bits"

        if mask!="":
            arcpy.FeatureToRaster_conversion (in_features=in_features, field=field, out_raster=out_raster+"_temp", cell_size=cell_size)
            outTimes = Raster(out_raster+"_temp") * 1
            outTimes.save(out_raster)
            dict_raster(gdb_salida+"\\"+out_raster+"_temp",gdb_salida+"\\"+out_raster,field)
            arcpy.Delete_management(gdb_salida+"\\"+out_raster+"_temp")
        else:
            arcpy.FeatureToRaster_conversion (in_features=in_features, field=field, out_raster=out_raster, cell_size=cell_size)

except exceptions.Exception as e:
    print e.__class__, e.__doc__, e.message
    os.system("pause")


