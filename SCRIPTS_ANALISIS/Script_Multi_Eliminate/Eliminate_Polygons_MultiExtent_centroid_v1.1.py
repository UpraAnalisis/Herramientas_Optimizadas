# -*- coding: utf-8 -*-
import arcpy,random,exceptions
from arcpy import env
import os.path
import time
env.overwriteOutput = True
import datetime


ruta = arcpy.CreateFolder_management(os.path.expanduser("~")+"\\"+r"AppData\Local\Temp",str(random.randrange(0,500000)))
print ruta
env.scratchWorkspace = r"%s"%(ruta)
try:
    ##Parametros

    fcEntrada = arcpy.GetParameterAsText(0) # Capa que se va a procesar.
    grilla = arcpy.GetParameterAsText(1) # Grilla de apoyo. El proceso se hará de forma individual por cada uno de los cuadros.
    capa_exclusion = arcpy.GetParameterAsText(2)
    if capa_exclusion=="----":
        capa_exclusion=""
    rango=arcpy.GetParameterAsText(3) # captura los cuadros que se van a procesar
    ruta_raiz = arcpy.GetParameterAsText(4) # captura la ruta donde se van a crear los directorios de salida y finales
    expresion = arcpy.GetParameterAsText(5) # captura la expresión a usar por el eliminate
    dic={"__":" ","igual":"=", "menor":"<", "mayor": ">"} # diccionario que en este convierte las letras en caracteres especiales

    for i in dic:# ciclo que reemplaza las letras por los carateres especiales
        expresion=expresion.replace(i,dic[i])
    print expresion
    t_inicio=time.clock()


    def recuperalista(lista): # función que
        b=[]
        rango=lista.replace("[","")
        rango=rango.replace("]","")
        rango = rango.split("_")
        b=map(int,rango)
        return b

    # Set local variables
    inFeatures = fcEntrada
    templGrilla = "blocklayer"
    templfeatures = "blocklayer2"
    templfeatures2 = "blocklayer3"
    expression = expresion

    def creadirs(numero): # crea los dierctorios de salida del programa
        nombre="Partes"
        if not os.path.exists(ruta_raiz+"\\%s"%(nombre+"\\"+str(numero))):
            os.makedirs(ruta_raiz+"\\%s"%(nombre+"\\"+str(numero)))
        return ruta_raiz+"\\%s"%nombre+"\\"+str(numero)

    def crearFGDB(ruta,numero):
        arcpy.CreateFileGDB_management(ruta, "bd"+str(numero)+".gdb")
        return ruta+"\\"+"bd"+str(numero)+".gdb"

    def Eliminate(inFeatures,outFeatureClass,expression,numero):
        nombre = arcpy.ValidateTableName("M" + str(datetime.datetime.now().strftime("%b_%S"))+str(random.randrange(0,50000))+str(numero),"in_memory")
        templfeatures=arcpy.ValidateTableName("blocklayer2"+"_"+str(datetime.datetime.now().strftime("%b_%S"))+str(random.randrange(0,50000))+str(numero),"in_memory")
        print inFeatures
##        arcpy.MakeFeatureLayer_management(inFeatures, templfeatures)
##        if ciclo==1:
##            nombre =  arcpy.ValidateTableName("M" + str(random.randrange(0,50000)),"in_memory")

##        path = nombre
        arcpy.MakeFeatureLayer_management(grilla, templGrilla)
        arcpy.MakeFeatureLayer_management(inFeatures, templfeatures)
##        arcpy.CopyFeatures_management(templfeatures, path)

        print "layer temporal1"
        fc_grilla=arcpy.SelectLayerByAttribute_management(templGrilla, "NEW_SELECTION", "PageNumber  = %s"%str(numero))
        print "selecionando grilla"
        fc_select=arcpy.SelectLayerByLocation_management(templfeatures, "have_their_center_in", templGrilla)
        print "seleccionando por centroides"

        arcpy.CopyFeatures_management(templfeatures, "in_memory"+"\\"+nombre)
        arcpy.MakeFeatureLayer_management( "in_memory"+"\\"+nombre, "in_memory"+"\\"+nombre+"_lyr")
        arcpy.AddField_management(in_table="in_memory"+"\\"+nombre+"_lyr", field_name="Area", field_type="DOUBLE")
        arcpy.CalculateField_management (in_table="in_memory"+"\\"+nombre+"_lyr", field="Area", expression="!SHAPE.area!",expression_type="PYTHON")
        print "layer temporal2"
        print "layer seleccione"
        fc_filtro=arcpy.SelectLayerByAttribute_management("in_memory"+"\\"+nombre+"_lyr", "NEW_SELECTION", expression)
        print "corriendo eliminate primer ciclo"
##            try:
        arcpy.Eliminate_management (in_features="in_memory"+"\\"+nombre+"_lyr", out_feature_class=outFeatureClass, selection="LENGTH", ex_where_clause="", ex_features=capa_exclusion)
##            arcpy.Eliminate_management(path+".lyr", outFeatureClass, "LENGTH","")
##            except arcpy.ExecuteError as e:
##                    if "000210" in str(e.message):
##                        nombre=str(random.randrange(3000,50000))
##                        try:
##                            arcpy.Eliminate_management (in_features=path+"_lyr", out_feature_class=outFeatureClass+nombre, selection="LENGTH", ex_where_clause="", ex_features=capa_exclusion)
##                            if arcpy.Exists(outFeatureClass+nombre):
##                                arcpy.Rename_management(outFeatureClass+nombre,outFeatureClass)
##
##                        except:
##                            arcpy.Eliminate_management (in_features=path+"_lyr", out_feature_class=outFeatureClass+nombre, selection="LENGTH", ex_where_clause="", ex_features=capa_exclusion)
##                            if arcpy.Exists(outFeatureClass+nombre):
##                                    arcpy.Rename_management(outFeatureClass+nombre,outFeatureClass)

##        if ciclo==0:
##            arcpy.MakeFeatureLayer_management(templfeatures, templfeatures+".lyr")
##            arcpy.AddField_management(in_table=templfeatures+".lyr", field_name="Area", field_type="DOUBLE")
##            arcpy.CalculateField_management (in_table=templfeatures+".lyr", field="Area", expression="!SHAPE.area!",expression_type="PYTHON")
##            print "seleccionando ciclos alternos"
##            fc_filtro=arcpy.SelectLayerByAttribute_management(templfeatures, "NEW_SELECTION", expression)
##            print "corriendo eliminate ciclos alternos"
##            try:
##                arcpy.Eliminate_management (in_features=templfeatures, out_feature_class=outFeatureClass, selection="LENGTH", ex_where_clause="", ex_features=capa_exclusion)
####            arcpy.Eliminate_management(templfeatures, outFeatureClass, "LENGTH","")
##            except arcpy.ExecuteError as e:
##                    if "000210" in str(e.message):
####                        nombre=str(random.randrange(3000,50000))
##                        try:
##                            arcpy.Eliminate_management (in_features=templfeatures, out_feature_class=outFeatureClass, selection="LENGTH", ex_where_clause="", ex_features=capa_exclusion)
##                        except:
##                            arcpy.Eliminate_management (in_features=templfeatures, out_feature_class=outFeatureClass, selection="LENGTH", ex_where_clause="", ex_features=capa_exclusion)
##
##        if ciclo==2:
##            arcpy.MakeFeatureLayer_management(templfeatures, templfeatures+".lyr")
##            arcpy.CalculateField_management (in_table=templfeatures+".lyr", field="Area", expression="!SHAPE.area!",expression_type="PYTHON")
##            print "seleccionando ciclos alternos"
##            fc_filtro=arcpy.SelectLayerByAttribute_management(templfeatures, "NEW_SELECTION", expression)
##            print "corriendo eliminate ciclos alternos"
##            try:
##                arcpy.Eliminate_management (in_features=templfeatures, out_feature_class=outFeatureClass, selection="LENGTH", ex_where_clause="", ex_features=capa_exclusion)
####            arcpy.Eliminate_management(templfeatures, outFeatureClass, "LENGTH","")
##            except arcpy.ExecuteError as e:
##                    if "000210" in str(e.message):
##                        nombre=str(random.randrange(3000,50000))
##                        arcpy.Eliminate_management (in_features=templfeatures, out_feature_class=outFeatureClass+nombre, selection="LENGTH", ex_where_clause="", ex_features=capa_exclusion)

    if __name__ == '__main__':

            print "Procesando secciones "+str(recuperalista(rango))
            arcpy.Delete_management("in_memory")
            rango=recuperalista(rango)

            for numero in rango:

                print "ejecutandose la seccion #: %s "%numero
                ruta=creadirs(numero)
                ruta=crearFGDB(ruta,numero)
##                ciclo=1
####                print inFeatures
##                Eliminate(inFeatures,ruta+"\\"+"cuadrox_"+str(numero),expression,ciclo)
##                ciclo=0
                nombre = arcpy.ValidateTableName("f" + str(datetime.datetime.now().strftime("%b_%S"))+str(random.randrange(0,5000))+"_"+str(numero),"in_memory")
                path = r"in_memory\%s" % nombre
##                path1 = r"in_memory\%s" % nombre+"1"
##                path2 = r"in_memory\%s" % nombre+"2"
##                path3 = r"in_memory\%s" % nombre+"3"
##                path4 = r"in_memory\%s" % nombre+"4"
##                ciclo=2
##                Eliminate(ruta+"\\"+"cuadrox_"+str(numero),path,expression,ciclo)
##                Eliminate(path,path1,expression,ciclo)
##                Eliminate(path1,path2,expression,ciclo)
##                Eliminate(path2,path3,expression,ciclo)
##                Eliminate(path3,path4,expression,ciclo)

##                Eliminate(path4,ruta+"\\"+"cuadrox_"+str(numero)+"_Final",expression,ciclo)
                arcpy.CopyFeatures_management(inFeatures, path)
                Eliminate(path,ruta+"\\"+"cuadrox_"+str(numero)+"_Final",expression,numero)
except exceptions.Exception as e:
    print e.__class__, e.__doc__, e.message
    os.system("pause")




