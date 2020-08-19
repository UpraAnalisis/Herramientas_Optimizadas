#-*- coding:'utf-8' -*-
# nueva

import arcpy
import datetime

def duplicados(capa,ruta):
    global gdb
    nombre_gdb = "duplicados_%s"%(datetime.datetime.now().strftime("%b_%d_%Y_%H_%M_%S"))
    nombre_gdb = nombre_gdb.replace(".","")
    gdb=arcpy.CreateFileGDB_management(ruta,nombre_gdb)
    ##capa_copia=arcpy.CopyFeatures_management(in_features=capa,out_feature_class="in_memory\\%s"%(arcpy.ValidateTableName(arcpy.Describe(capa).name)))
    capa_copia=arcpy.CopyFeatures_management(in_features=capa,out_feature_class="%s\\%s"%(gdb,arcpy.ValidateTableName(arcpy.Describe(capa).name)))
    arcpy.AddField_management(capa_copia, "dupli", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    with arcpy.da.UpdateCursor(capa_copia,["SHAPE@Y","SHAPE@X","SHAPE@AREA","dupli"]) as cursor:
      for fila in cursor:
##       x=str(fila[1])[0:len(str(fila[1]))-2]
##       y=str(fila[0])[0:len(str(fila[0]))-2]
       Cx=float(str(fila[1])[0:len(str(fila[1]))])
       Cy=float(str(fila[0])[0:len(str(fila[0]))])
       CArea = float(str(fila[2])[0:len(str(fila[2]))])
       x = "{0:.2f}".format(Cx) ###funcion para dejar solo dos decimales
       y = "{0:.2f}".format(Cy) ###funcion para dejar solo dos decimales
       Area = "{0:.2f}".format(CArea)
       fila[3]= str(x)+"_"+str(y)+"_"+str(Area)
       cursor.updateRow(fila)

    arcpy.FindIdentical_management(in_dataset=capa_copia,out_dataset=str(gdb) + "\\duplicados",fields=["dupli"],output_record_option="ONLY_DUPLICATES")
    arcpy.Delete_management("%s\\%s"%(gdb,arcpy.ValidateTableName(arcpy.Describe(capa).name)))
    registros = int(arcpy.GetCount_management(str(gdb) + "\\duplicados")[0])
    return str(registros)+";"+"%s\\duplicados"%(gdb)

def duplicados_OID(capa):
    tabla = str(gdb) + "\\duplicados"
    duplicados = []
    oid_campo = [f.name for f in arcpy.Describe(capa).fields if f.type == "OID"][0]
    cursor = arcpy.da.SearchCursor(tabla,["IN_FID"])
    for fila in cursor:
        duplicados.append(cursor[0])
    return oid_campo + " In " +str(tuple(duplicados))

