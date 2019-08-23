# -*- coding: utf-8 -*-
import arcpy
import os,time,exceptions,sys

# sys.setdefaultencoding() does not exist, here!
reload(sys) # Reload does the trick!
sys.setdefaultencoding('UTF8')
try:
    t_inicio=time.clock()# captura el tiempo de inicio del proceso
    #arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3116)
    arcpy.env.overwriteOutput = True


    infea=r"%s"%(arcpy.GetParameterAsText(0))
    zone_fields=r"%s"%(arcpy.GetParameterAsText(1))
    in_class_features=r"%s"%(arcpy.GetParameterAsText(2))
    out_table=r"%s"%(arcpy.GetParameterAsText(3))
    class_fields=r"%s"%(arcpy.GetParameterAsText(4))
    sum_fields=r"%s"%(arcpy.GetParameterAsText(5))
    xy_tolerance=r"%s"%(arcpy.GetParameterAsText(6))
    out_units=r"%s"%(arcpy.GetParameterAsText(7))
    ruta_txt_fids1=r"%s"%(arcpy.GetParameterAsText(8))
    ruta_txt_fids2=r"%s"%(arcpy.GetParameterAsText(9))
    entorno=arcpy.GetParameterAsText(10)

    if class_fields!="---":
        class_fields=class_fields
    else:
        class_fields=""

    if sum_fields!="---":
        sum_fields=sum_fields
    else:
        sum_fields=""

    if xy_tolerance!="---":
        xy_tolerance=xy_tolerance
    else:
        xy_tolerance=""

    dic_acentos={"---":" ","***a***":"\xc3\xa1","***e***":"\xc3\xa9", "***i***":"\xc3\xad", "***o***":"\xc3\xb3","***u***":"\xc3\xba","***n***": "\xc3\xb1",
    "***A***":"\xc3\x81","***E***":"\xc3\x89", "***I***":"\xc3\x8d", "***O***":"\xc3\x93","***Ú***":"\xc3\x9a","***N***":"\xc3\x91"}


    variables =[var for var in dir(arcpy.env) if "_" not in var and "packageWorkspace" not in var and "scratch" not in var]

    def recibe_environ(palabras_entorno,valores_entorno):
        valores_entorno=valores_entorno.split("***")
        for i in xrange(len(palabras_entorno)):
            if "geoprocessing._base.GPEnvironment" in valores_entorno[i]:
                valores_entorno[i]= None
            pivote="arcpy.env.%s"%(palabras_entorno[i])
            exec("""tipo= type(%s)"""%(pivote))
            if "\\" in (valores_entorno[i]):
                    valores_entorno[i]=valores_entorno[i].replace("\\","\\\\")

            if unicode == tipo:
                instruc_a="""arcpy.env.%s = %s"""%(palabras_entorno[i],valores_entorno[i].replace("....."," "))
                if "None" not in instruc_a:
                    instruc_a="""arcpy.env.%s = """%(palabras_entorno[i].replace("....."," "))+'"'+"%s"%(valores_entorno[i].replace("....."," "))+'"'
                    exec(instruc_a)

                else:
                    instruc_a="""arcpy.env.%s = %s"""%(palabras_entorno[i],valores_entorno[i].replace("....."," "))
                    exec(instruc_a)

            if int == tipo:
                instruc_a="""arcpy.env.%s = %s"""%(palabras_entorno[i],valores_entorno[i].replace("....."," "))
                exec(instruc_a)

            if float == tipo:
                instruc_a="""arcpy.env.%s = %s"""%(palabras_entorno[i],valores_entorno[i].replace("....."," "))
                exec(instruc_a)


            if long == tipo:
                instruc_a="""arcpy.env.%s = %s"""%(palabras_entorno[i],valores_entorno[i].replace("....."," "))
                exec(instruc_a)


            if type(None) == tipo:
                instruc_a="""arcpy.env.%s = %s"""%(palabras_entorno[i],valores_entorno[i].replace("....."," "))
                if "None" not in instruc_a:
                    instruc_a="""arcpy.env.%s = """%(palabras_entorno[i].replace("....."," "))+'"'+"%s"%(valores_entorno[i].replace("....."," "))+'"'
                    exec(instruc_a)

                else:
                    instruc_a="""arcpy.env.%s = %s"""%(palabras_entorno[i],valores_entorno[i].replace("....."," "))
                    exec(instruc_a)

            if bool == tipo:
                instruc_a="""arcpy.env.%s = %s"""%(palabras_entorno[i],valores_entorno[i].replace("....."," "))
                if "isCancelled" not in instruc_a:
                    exec(instruc_a)


    def cambia_caracteres(infea):
        for xx in dic_acentos:# ciclo que reemplaza las letras por los carateres especiales
            infea=infea.replace(xx,dic_acentos[xx])
        return infea

    def recibir_seleccion(fid_Set,capa):
        if fid_Set != "---":
            for campo in [x for x in arcpy.Describe(capa).fields]:
                if campo.type=="OID":
                    campo_oid=campo.name
            oids=fid_Set.replace("_"," , ")
            expre_seleccion="%s in (%s)"%(campo_oid,oids)
            layer_capa=arcpy.MakeFeatureLayer_management(capa,arcpy.Describe(capa).name)
            arcpy.SelectLayerByAttribute_management(in_layer_or_view=layer_capa,selection_type="NEW_SELECTION",where_clause=expre_seleccion)
            return layer_capa
        else:
            layer_capa=arcpy.MakeFeatureLayer_management(capa,arcpy.Describe(capa).name)
            return layer_capa

    def leer_text(ruta_txt):
        txt = open("%s"%(ruta_txt),"r")
        fid_Set=txt.read()
        txt.close()
        arcpy.Delete_management(ruta_txt)
        return fid_Set


    if __name__ == '__main__':
        print "Ejecutando Tabulate Intersection a 64bits ...."
        print infea, zone_fields, in_class_features, out_table, class_fields, sum_fields, xy_tolerance, out_units
        recibe_environ(variables,entorno)
        ruta_txt_fids1 = cambia_caracteres(ruta_txt_fids1)
        ruta_txt_fids2 = cambia_caracteres(ruta_txt_fids2)
        lista_fids1=leer_text(ruta_txt_fids1.decode('utf-8'))
        lista_fids2=leer_text(ruta_txt_fids2.decode('utf-8'))
        infea=cambia_caracteres(infea)
        out_table=cambia_caracteres(out_table)
        in_class_features=cambia_caracteres(in_class_features)
        layer_infea = recibir_seleccion(lista_fids1,infea)
        layer_in_class_features = recibir_seleccion(lista_fids2,in_class_features)
        print layer_infea, zone_fields, layer_in_class_features, out_table, class_fields, sum_fields, xy_tolerance, out_units
        in_class_features =cambia_caracteres(in_class_features)
        arcpy.TabulateIntersection_analysis (in_zone_features=layer_infea, zone_fields=zone_fields, in_class_features=layer_in_class_features,
        out_table=out_table, class_fields=class_fields, sum_fields=sum_fields, xy_tolerance=xy_tolerance, out_units=out_units)




except exceptions.Exception as e:
    print e.__class__, e.__doc__, e.message
    os.system("pause")



