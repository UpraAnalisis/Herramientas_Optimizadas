# -*- coding: utf-8 -*-
import arcpy,random,exceptions
from arcpy import env
import os.path
import time
env.overwriteOutput = True


try:
    ##Parametros

    fcEntrada = arcpy.GetParameterAsText(0) # Capa que se va a procesar.
    grilla = arcpy.GetParameterAsText(1) # Grilla de apoyo. El proceso se hará de forma individual por cada uno de los cuadros.
    rango=arcpy.GetParameterAsText(2) # captura los cuadros que se van a procesar
    ruta_raiz = arcpy.GetParameterAsText(3) # captura la ruta donde se van a crear los directorios de salida y finales
    expresion = arcpy.GetParameterAsText(4) # captura la expresión a usar por el eliminate
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

    def Eliminate(inFeatures,outFeatureClass,expression,ciclo):
        nombre = "M" + str(random.randrange(0,5000))
        templfeatures="blocklayer2"+"_"+str(random.randrange(0,5000))
        print inFeatures
        arcpy.MakeFeatureLayer_management(inFeatures, templfeatures)
        if ciclo==1:
            nombre = "M" + str(random.randrange(0,5000))
            arcpy.MakeFeatureLayer_management(grilla, templGrilla)
            arcpy.MakeFeatureLayer_management(inFeatures, templfeatures)
            path = r"in_memory\%s" % nombre
            print "layer temporal1"
            fc_grilla=arcpy.SelectLayerByAttribute_management(templGrilla, "NEW_SELECTION", "PageNumber  = %s"%str(numero))
            print "selecionando grilla"
            fc_select=arcpy.SelectLayerByLocation_management(templfeatures, "have_their_center_in", templGrilla)
            print "seleccionando por centroides"
            arcpy.CopyFeatures_management(templfeatures, path)

            arcpy.MakeFeatureLayer_management(path, path+".lyr")
            arcpy.AddField_management(in_table=path+".lyr", field_name="Area_ha", field_type="DOUBLE")
            arcpy.CalculateField_management (in_table=path+".lyr", field="Area_ha", expression="!SHAPE.area!",expression_type="PYTHON")
            print "layer temporal2"
            print "layer seleccione"
            fc_filtro=arcpy.SelectLayerByAttribute_management(path+".lyr", "NEW_SELECTION", expression)
            print "corriendo eliminate primer ciclo"
            arcpy.Eliminate_management(path+".lyr", outFeatureClass, "LENGTH","")

        if ciclo==0:
            arcpy.MakeFeatureLayer_management(templfeatures, templfeatures+".lyr")
            arcpy.AddField_management(in_table=templfeatures+".lyr", field_name="Area_ha", field_type="DOUBLE")
            arcpy.CalculateField_management (in_table=templfeatures+".lyr", field="Area_ha", expression="!SHAPE.area!",expression_type="PYTHON")
            print "seleccionando ciclos alternos"
            fc_filtro=arcpy.SelectLayerByAttribute_management(templfeatures, "NEW_SELECTION", expression)
            print "corriendo eliminate ciclos alternos"
            arcpy.Eliminate_management(templfeatures, outFeatureClass, "LENGTH","")

        if ciclo==2:
            arcpy.MakeFeatureLayer_management(templfeatures, templfeatures+".lyr")
            arcpy.CalculateField_management (in_table=templfeatures+".lyr", field="Area_ha", expression="!SHAPE.area!",expression_type="PYTHON")
            print "seleccionando ciclos alternos"
            fc_filtro=arcpy.SelectLayerByAttribute_management(templfeatures, "NEW_SELECTION", expression)
            print "corriendo eliminate ciclos alternos"
            arcpy.Eliminate_management(templfeatures, outFeatureClass, "LENGTH","")

    if __name__ == '__main__':

            print "Procesando secciones "+str(recuperalista(rango))
            arcpy.Delete_management("in_memory")
            rango=recuperalista(rango)

            for numero in rango:

                print "ejecutandose la seccion #: %s "%numero
                ruta=creadirs(numero)
                ruta=crearFGDB(ruta,numero)
                ciclo=1
##                print inFeatures
                Eliminate(inFeatures,ruta+"\\"+"cuadrox_"+str(numero),expression,ciclo)
                ciclo=0
                nombre = "f" + str(random.randrange(0,5000))
                path = r"in_memory\%s" % nombre
                path1 = r"in_memory\%s" % nombre+"1"
                path2 = r"in_memory\%s" % nombre+"2"
                path3 = r"in_memory\%s" % nombre+"3"
                path4 = r"in_memory\%s" % nombre+"4"
                ciclo=2
                Eliminate(ruta+"\\"+"cuadrox_"+str(numero),path,expression,ciclo)
                Eliminate(path,path1,expression,ciclo)
                Eliminate(path1,path2,expression,ciclo)
                Eliminate(path2,path3,expression,ciclo)
                Eliminate(path3,path4,expression,ciclo)

                Eliminate(path4,ruta+"\\"+"cuadrox_"+str(numero)+"_Final",expression,ciclo)
except exceptions.Exception as e:
    print e.__class__, e.__doc__, e.message
    os.system("pause")




