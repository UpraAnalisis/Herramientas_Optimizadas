# -*- coding: utf-8 -*-
import arcpy
import os,time,exceptions,sys
from arcpy.sa import *
# sys.setdefaultencoding() does not exist, here!
reload(sys) # Reload does the trick!
sys.setdefaultencoding('UTF8')
try:
    t_inicio=time.clock()# captura el tiempo de inicio del proceso
    #arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3116)
    arcpy.env.overwriteOutput = True

    tipo=arcpy.GetParameterAsText(4)

    if tipo in ('FeatureClass','FeatureLayer'):

        in_table =r"%s"%(arcpy.GetParameterAsText(0))
        out_table =r"%s"%(arcpy.GetParameterAsText(1))
        statistics_fields =r"%s"%(arcpy.GetParameterAsText(2))
        case_field =r"%s"%(arcpy.GetParameterAsText(3))
        ruta_txt_fids1=arcpy.GetParameterAsText(5)
        entorno=arcpy.GetParameterAsText(6)


    else:

        in_table =r"%s"%(arcpy.GetParameterAsText(0))
        out_table =r"%s"%(arcpy.GetParameterAsText(1))
        statistics_fields =r"%s"%(arcpy.GetParameterAsText(2))
        case_field =r"%s"%(arcpy.GetParameterAsText(3))
        entorno=arcpy.GetParameterAsText(5)


    if case_field!="---":
        case_field=case_field
    else:
        case_field=""


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
##            print fid_Set
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
        print "Ejecutando Summary Statistics a 64bits ...."
        recibe_environ(variables,entorno)
        if tipo in ('FeatureClass','FeatureLayer','TableView'):
            in_table=cambia_caracteres(in_table)
            ruta_txt_fids1=cambia_caracteres(ruta_txt_fids1)
            lista_fids1=leer_text(ruta_txt_fids1.decode('utf-8'))
            in_table = recibir_seleccion(lista_fids1,in_table)
        else:
            in_table=cambia_caracteres(in_table)
        statistics_fields=cambia_caracteres(statistics_fields)
        case_field=cambia_caracteres(case_field)
        out_table=cambia_caracteres(out_table)
        print  in_table, out_table, statistics_fields, case_field
        arcpy.Statistics_analysis (in_table, out_table, statistics_fields, case_field)



except exceptions.Exception as e:
    print e.__class__, e.__doc__, e.message
    os.system("pause")



