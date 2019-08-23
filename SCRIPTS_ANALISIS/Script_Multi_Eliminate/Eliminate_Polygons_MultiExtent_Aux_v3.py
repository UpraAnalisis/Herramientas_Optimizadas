# -*- coding: utf-8 -*-
import arcpy,random,exceptions
from arcpy import env
import os.path
import time
env.overwriteOutput = True
import datetime


ruta = arcpy.CreateFolder_management(os.path.expanduser("~")+"\\"+r"AppData\Local\Temp",str(random.randrange(0,500000)))
env.scratchWorkspace = r"%s"%(ruta)
dic={"__":" ","igual":"=", "menor":"<", "mayor": ">"} # diccionario que en este convierte las letras en caracteres especiales
dic_acentos={"---":" ","***a***":"\xc3\xa1","***e***":"\xc3\xa9", "***i***":"\xc3\xad", "***o***":"\xc3\xb3","***u***":"\xc3\xba","***n***": "\xc3\xb1",
    "***A***":"\xc3\x81","***E***":"\xc3\x89", "***I***":"\xc3\x8d", "***O***":"\xc3\x93","***Ú***":"\xc3\x9a","***N***":"\xc3\x91"}

try:
    ##Parametros
    fcEntrada = arcpy.GetParameterAsText(0) # Capa que se va a procesar.
    grilla = arcpy.GetParameterAsText(1) # Grilla de apoyo. El proceso se hará de forma individual por cada uno de los cuadros.
    expresion_seleccion = arcpy.GetParameterAsText(2)
    for i in dic:# ciclo que reemplaza las letras por los carateres especiales
        expresion_seleccion=expresion_seleccion.replace(i,dic[i])
    selection = arcpy.GetParameterAsText(3)
    ruta_raiz = arcpy.GetParameterAsText(4) # captura la ruta donde se van a crear los directorios de salida y finales
    capa_exclusion = arcpy.GetParameterAsText(5)
    if capa_exclusion=="----":
        capa_exclusion=""
    ex_where_clause = arcpy.GetParameterAsText(6)
    if ex_where_clause == "----":
        ex_where_clause = ""
    else:
        for i in dic:# ciclo que reemplaza las letras por los carateres especiales
            ex_where_clause = ex_where_clause.replace(i,dic[i])

    rango=arcpy.GetParameterAsText(7) # captura los cuadros que se van a procesar

    t_inicio=time.clock()

    def cambia_caracteres(infea):
        for xx in dic_acentos:# ciclo que reemplaza las letras por los carateres especiales
            infea=infea.replace(xx,dic_acentos[xx])
        return infea

    def recuperalista(lista): # función que
        b=[]
        rango=lista.replace("[","")
        rango=rango.replace("]","")
        rango = rango.split("_")
        b=map(int,rango)
        return b

    # Set local variables
##    inFeatures = fcEntrada
    templGrilla = "blocklayer"
    templfeatures = "blocklayer2"

    def creadirs(numero): # crea los dierctorios de salida del programa
        nombre="Partes"
        if not os.path.exists(ruta_raiz+"\\%s"%(nombre+"\\"+str(numero))):
            os.makedirs(ruta_raiz+"\\%s"%(nombre+"\\"+str(numero)))
        return ruta_raiz+"\\%s"%nombre+"\\"+str(numero)

    def crearFGDB(ruta,numero):
        arcpy.CreateFileGDB_management(ruta, "bd"+str(numero)+".gdb")
        return ruta+"\\"+"bd"+str(numero)+".gdb"

    def Eliminate(inFeatures,outFeatureClass,numero):
        nombre = arcpy.ValidateTableName("M" + str(datetime.datetime.now().strftime("%b_%S"))+str(random.randrange(0,50000))+str(numero),"in_memory")
        templfeatures=arcpy.ValidateTableName("blocklayer2"+"_"+str(datetime.datetime.now().strftime("%b_%S"))+str(random.randrange(0,50000))+str(numero),"in_memory")
        arcpy.MakeFeatureLayer_management(grilla, templGrilla)
        arcpy.MakeFeatureLayer_management(inFeatures, templfeatures)
        fc_grilla=arcpy.SelectLayerByAttribute_management(templGrilla, "NEW_SELECTION", "PageNumber  = %s"%str(numero))
        fc_select=arcpy.SelectLayerByLocation_management(templfeatures, "have_their_center_in", templGrilla)
        arcpy.CopyFeatures_management(templfeatures, "in_memory"+"\\"+nombre)
        arcpy.MakeFeatureLayer_management( "in_memory"+"\\"+nombre, "in_memory"+"\\"+nombre+"_lyr")
        arcpy.AddField_management(in_table="in_memory"+"\\"+nombre+"_lyr", field_name="Area", field_type="DOUBLE")
        arcpy.CalculateField_management (in_table="in_memory"+"\\"+nombre+"_lyr", field="Area", expression="!SHAPE.area!",expression_type="PYTHON")
        fc_filtro=arcpy.SelectLayerByAttribute_management("in_memory"+"\\"+nombre+"_lyr", "NEW_SELECTION", expresion_seleccion)
        arcpy.Eliminate_management (in_features="in_memory"+"\\"+nombre+"_lyr", out_feature_class=outFeatureClass, selection= selection, ex_where_clause = ex_where_clause, ex_features = capa_exclusion)


    if __name__ == '__main__':
            ### decodificando parametros #####
            fcEntrada= cambia_caracteres(fcEntrada)
            grilla = cambia_caracteres(grilla)
            expresion_seleccion = cambia_caracteres(expresion_seleccion)
            ruta_raiz = cambia_caracteres(ruta_raiz)
            if capa_exclusion != "":
                capa_exclusion = cambia_caracteres(capa_exclusion)
            if ex_where_clause != "":
                ex_where_clause = cambia_caracteres(ex_where_clause)
            ### decodificando parametros #####
            print "Seleccion : " + expresion_seleccion
            print "Exclusion : " +ex_where_clause
            print "Procesando secciones "+str(recuperalista(rango))
            arcpy.Delete_management("in_memory")
            rango=recuperalista(rango)
            for numero in rango:
                print "ejecutandose la seccion #: %s "%numero
                ruta=creadirs(numero)
                ruta=crearFGDB(ruta,numero)
                nombre = arcpy.ValidateTableName("f" + str(datetime.datetime.now().strftime("%b_%S"))+str(random.randrange(0,5000))+"_"+str(numero),"in_memory")
                path = r"in_memory\%s" % nombre
                arcpy.CopyFeatures_management(fcEntrada, path)
                Eliminate(path,ruta+"\\"+"cuadrox_"+str(numero),numero)
except exceptions.Exception as e:
    print e.__class__, e.__doc__, e.message
    os.system("pause")




