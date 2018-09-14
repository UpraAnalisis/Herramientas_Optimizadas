# -*- coding: utf-8 -*-
import arcpy
import os,time,exceptions,sys
import datetime

# sys.setdefaultencoding() does not exist, here!
reload(sys) # Reload does the trick!
sys.setdefaultencoding('UTF8')
try:
    t_inicio=time.clock()# captura el tiempo de inicio del proceso
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3116)
    arcpy.env.overwriteOutput = True

    infea=r"%s"%(arcpy.GetParameterAsText(0))
    capa_salida=r"%s"%(arcpy.GetParameterAsText(1))
    selection= "%s"%(arcpy.GetParameterAsText(2))
    expresion_exclusion= "%s"%(arcpy.GetParameterAsText(3))
    exfeatures=r"%s"%(arcpy.GetParameterAsText(4))
    lista_fids=r"%s"%(arcpy.GetParameterAsText(5))
    entorno=arcpy.GetParameterAsText(6)

    if exfeatures!="---":
        exfeatures=arcpy.Describe(exfeatures).catalogPath

    else:
        exfeatures =""

    dic={"__":" ","igual":"=", "menor":"<", "mayor": ">"} # diccionario que en este convierte las letras en caracteres especiales
    dic_acentos={"---":" ","***a***":"\xc3\xa1","***e***":"\xc3\xa9", "***i***":"\xc3\xad", "***o***":"\xc3\xb3","***u***":"\xc3\xba","***n***": "\xc3\xb1",
    "***A***":"\xc3\x81","***E***":"\xc3\x89", "***I***":"\xc3\x8d", "***O***":"\xc3\x93","***Ú***":"\xc3\x9a","***N***":"\xc3\x91"}


    if selection!="---":
        selection=selection
    else:
        selection=""


    if expresion_exclusion!="---":
        expresion_exclusion=expresion_exclusion
    else:
        expresion_exclusion=""

    if exfeatures!="---":
        exfeatures=exfeatures
    else:
        exfeatures=""



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

    def cambia_caracteres1(expresion_exclusion):

        for i in dic: # ciclo que reemplaza los carateres especiales
            expresion_exclusion=expresion_exclusion.replace(i,dic[i])
        return expresion_exclusion

    def recibir_seleccion(fid_Set,capa):
        if fid_Set != "---":
            for campo in [x for x in arcpy.Describe(capa).fields]:
                if campo.type=="OID":
                    campo_oid=campo.name
            oids=fid_Set.replace("_"," , ")
            expre_seleccion="%s in (%s)"%(campo_oid,oids)
            layer_capa=arcpy.MakeFeatureLayer_management(capa,arcpy.Describe(capa).name+datetime.datetime.now().strftime("%b_%d_%Y_%H_%M_%S"))
            arcpy.SelectLayerByAttribute_management(in_layer_or_view=layer_capa,selection_type="NEW_SELECTION",where_clause=expre_seleccion)
            return layer_capa
        else:
            layer_capa=arcpy.MakeFeatureLayer_management(capa,arcpy.Describe(capa).name+datetime.datetime.now().strftime("%b_%d_%Y_%H_%M_%S"))
            return layer_capa

    def leer_txt(ruta_txt):
        txt = open("%s"%(ruta_txt),"r")
        fid_Set=txt.read()
        txt.close()
        return fid_Set

    if __name__ == '__main__':
        print "Ejecutando Eliminate a 64bits ...."
        recibe_environ(variables,entorno)
        infea = cambia_caracteres(arcpy.Describe(infea).catalogPath)
        capa_salida =cambia_caracteres(capa_salida)
        expresion_exclusion = cambia_caracteres1(expresion_exclusion)
        exfeatures=cambia_caracteres(exfeatures)
        print infea,capa_salida,expresion_exclusion
        carpeta_txt=lista_fids
        lista_fids=leer_txt(carpeta_txt)
        arcpy.Delete_management(carpeta_txt)
        layer_entrada = recibir_seleccion(lista_fids,infea)

        print "procesando ciclo..."
        arcpy.Eliminate_management (in_features=layer_entrada, out_feature_class=capa_salida, selection=selection, ex_where_clause=expresion_exclusion, ex_features=exfeatures)



except exceptions.Exception as e:
    print e.__class__, e.__doc__, e.message
    os.system("pause")

