# -*- coding: utf-8 -*-
# --------------------------------------------------------------------
# JoinCursor_Multiple_v3_x64_feature_aux.py
# Fecha de creacion: 2017-11-15 08:59:08.00000
# Author: Carlos Mario Cano Campillo
# Email: carlos.cano@upra.gov.co / kanocampillo@gmail.com
# Propietario: Unidad de Planificación Rural Agropecuaria
#
# ---------------------------------------------------------------------
#=====================Librerias==============================#
import arcpy,os,random,time,exceptions,inspect

# sys.setdefaultencoding() does not exist, here!
reload(sys) # Reload does the trick!
sys.setdefaultencoding('UTF8')


try:
    from arcpy import env
    #=========Variables Globales y de Entorno=====================#
    env.overwriteOutput = True # habilita la opcion de sobrescribir datos
    t_inicio=time.clock() # captura el tiempo de inicio del proceso
    arcpy.env.workspace = "in_memory" # fija el espacio de trabajo en memoria
    src=arcpy.SpatialReference(3116) # fija el sistema de coordenadas en magna bogota
    ws=arcpy.env.workspace
    #=================Parametros de entrada======================#
    fcentrada = r"%s"%arcpy.GetParameterAsText(0) # almacena la capa objetivo del join
    llave_objetivo = arcpy.GetParameterAsText(1) # almacena la llave de la capa objetivo
    tablajoin = r"%s"%arcpy.GetParameterAsText(2) # almacena la tabla desde donde se traeran los atributos
    llave_tabla = arcpy.GetParameterAsText(3) # almacena la llave de la tabla de donde bienen los atributos
    campo_a_unir=[]  # almacena los campos a unir en el join
    campo_a_unir=arcpy.GetParameterAsText(4)
    campo_a_unir = campo_a_unir.split("__")
    #-------------------------------------------------------------

    dic_acentos={"---":" ","***a***":"\xc3\xa1","***e***":"\xc3\xa9", "***i***":"\xc3\xad", "***o***":"\xc3\xb3","***u***":"\xc3\xba","***n***": "\xc3\xb1",
    "***A***":"\xc3\x81","***E***":"\xc3\x89", "***I***":"\xc3\x8d", "***O***":"\xc3\x93","***Ú***":"\xc3\x9a","***N***":"\xc3\x91"}

    def cambia_caracteres(infea):
        for xx in dic_acentos:# ciclo que reemplaza las letras por los carateres especiales
            infea=infea.replace(xx,dic_acentos[xx])
        return infea

    class Layer(object):

        def __init__(self,inFeature,campos_visibles,ws):  # funcion que incializa la clase e instancia el objeto de tipo layer
            self.feature=r"%s"%inFeature # esta propiedad almacena el feature clas del objeto
            self.ruta="" # almacena la ruta del feature layer
            self.nombre=arcpy.Describe(self.feature).name # almacena el nombre de la capa
            self.camposFeature=arcpy.ListFields(self.feature) # almacena los campos del feature class
            self.camposLayer="" # almacena los campos del layer
            self.toLayer(campos_visibles) # almacena el workspace que en este caso es en memoria

        def toLayer(self,campos_visibles): # crea un objeto a partir del feature de entrada y los campos visibles
            fields= arcpy.ListFields(self.feature)
            fieldinfo = arcpy.FieldInfo() ##proporciona  metodos y propiedades a los campos de un layer

            if campos_visibles!=[]:
                for field in fields:
                    if field.name in campos_visibles:
                        fieldinfo.addField(field.name, field.name, "VISIBLE", "")
                    else:
                        fieldinfo.addField(field.name, field.name, "HIDDEN", "")
            else:
                for field in fields:
                        fieldinfo.addField(field.name, field.name, "VISIBLE", "")

            if "in_memory" in ws:
                self.ruta=arcpy.MakeTableView_management(self.feature, self.nombre+"_"+str(random.randrange(0,5000))+".lyr",field_info=fieldinfo).getOutput(0)
            else:
                self.ruta=arcpy.MakeTableView_management(self.feature, self.nombre+".lyr",field_info=fieldinfo).getOutput(0)
            self.camposLayer=arcpy.ListFields(self.feature)


        def addjoinCursorMultiple(self,capajoin,llaveobjetivo,llavetabla,camposjoin): # realiza una add join entre dos capas empleando cursores, pero uniendo multiples campos
            arcpy.AddMessage(capajoin)
            arcpy.AddMessage(camposjoin)
            arcpy.AddMessage(llaveobjetivo)
            arcpy.AddMessage(llavetabla)
            targshp =self.ruta
            joinshp=capajoin
            joinfields =camposjoin
            joindict = {}
            campo_tipo={}
            camposjoin1=[]
            camposjoin1.append(llavetabla)
            for i in xrange(0,len(camposjoin)):
                    camposjoin1.append(camposjoin[i])
            camposjoin=camposjoin1
            with arcpy.da.SearchCursor(capajoin,camposjoin) as cursor:
             for row in cursor:
                llave=row[0]
                valor=[]
                for i in xrange(1,len(camposjoin)):
                    valor.append(row[i])
                joindict[llave]=valor
            camposupdate=[]
            camposupdate.append(llaveobjetivo)
            for i in xrange(1,len(camposjoin)):
                    camposupdate.append(camposjoin[i])
            campos_feature=arcpy.ListFields(capajoin)
            for campo in campos_feature:
                campo_tipo[campo.name]=[campo.type]

            clon=self.feature

            for i in xrange(1,len(camposupdate)):

                arcpy.AddField_management(clon, camposupdate[i],str(campo_tipo[camposupdate[i]][0]))
                with arcpy.da.UpdateCursor(clon, [camposupdate[0], camposupdate[i]]) as recs:
                    for rec in recs:
                        keyval = rec[0]

                        if joindict.has_key(keyval):
                            rec[1] = joindict[keyval][i-1]
                        recs.updateRow(rec)

                print "Se agregaron los datos del campo " + camposupdate[i]

    if __name__ == '__main__':
        print "Ejecutando Add join a 64bits ...."
        fcentrada=cambia_caracteres(fcentrada)
        llave_objetivo=cambia_caracteres(llave_objetivo)
        tablajoin=cambia_caracteres(tablajoin)
        llave_tabla=cambia_caracteres(llave_tabla)
        print tablajoin,llave_objetivo,llave_tabla,[cambia_caracteres(x) for x in campo_a_unir]
        capa=Layer(fcentrada,[],ws)# instancia un objeto de la clase Layer para aceder a sus propiedades
        capa.addjoinCursorMultiple(tablajoin,llave_objetivo,llave_tabla,[cambia_caracteres(x) for x in campo_a_unir]) # realiza un addjoin cursor multiple entre las capas especificadas


except exceptions.Exception as e:
    print e.__class__, e.__doc__, e.message
    os.system("pause")