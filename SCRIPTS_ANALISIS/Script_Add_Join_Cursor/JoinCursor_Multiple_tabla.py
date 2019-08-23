#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      carlos.cano
#
# Created:     31/08/2016
# Copyright:   (c) carlos.cano 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#=====================Librerias==============================#
import arcpy, multiprocessing, random, time,os,subprocess
from arcpy import env
#=========Variables Globales y de Entorno=====================#
env.overwriteOutput = True
t_inicio=time.clock()# captura el tiempo de inicio del proceso
arcpy.env.workspace = "in_memory"
rasters_de_entrada=[]
src=arcpy.SpatialReference(3116)
ws=arcpy.env.workspace
#=================Parametros de entrada======================#
fcentrada = r"%s"%arcpy.GetParameterAsText(0)
llave_objetivo = arcpy.GetParameterAsText(1)
tablajoin = r"%s"%arcpy.GetParameterAsText(2)
llave_tabla = arcpy.GetParameterAsText(3)
campo_a_unir=[]
##for fc in arcpy.GetParameterAsText(4).split(";"):
##    campo_a_unir.append(fc)
campo_a_unir=arcpy.GetParameterAsText(4)
campo_a_unir = campo_a_unir.split(";")

##ruta_salida=r"%s"%arcpy.GetParameterAsText(5)
##nombre_salida=arcpy.GetParameterAsText(6)
#-------------------------------------------------------------

class Layer(object):

    def __init__(self,inFeature,campos_visibles,ws):
        self.feature=r"%s"%inFeature
        self.ruta=""
        self.nombre=arcpy.Describe(self.feature).name
        self.camposFeature=arcpy.ListFields(self.feature)
        self.camposLayer=""
        self.toLayer(campos_visibles)

    def toLayer(self,campos_visibles):
        fields= arcpy.ListFields(self.feature)
        fieldinfo = arcpy.FieldInfo()

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

    def nuevoCampoCal(self,nombre,tipocampo,expresion,tipocod):
        listaTipo={'texto': "TEXT",'flotante': 'FLOAT','doble': 'DOUBLE','entero_corto': 'SHORT','entro_largo': 'LONG','fecha': 'DATE'}
        listaExpre={'py':'PYTHON_9.3','vb':'VB'}
        print nombre,"%s"%self.ruta,listaTipo[tipocampo]
        arcpy.AddField_management(self.ruta,nombre,"%s"%listaTipo[tipocampo])
        self.camposLayer=arcpy.ListFields(self.feature)
        arcpy.CalculateField_management(self.ruta, field=nombre, expression=expresion,expression_type=listaExpre[tipocod])

    def nuevoCampo(self,nombre,tipocampo):
        listaTipo={'texto': "TEXT",'flotante': 'FLOAT','doble': 'DOUBLE','entero_corto': 'SHORT','entro_largo': 'LONG','fecha': 'DATE'}
        arcpy.AddField_management(self.ruta,nombre,"%s"%listaTipo[tipocampo])


    def calcularCampo(self,nombre,expresion,tipocod):
        listaExpre={'py':'PYTHON_9.3','vb':'VB'}
        arcpy.CalculateField_management(self.ruta, field=nombre, expression=expresion,expression_type=listaExpre[tipocod])

    def calcularCampoCode(self,nombre,expresion,tipocod,codeblock):
        listaExpre={'py':'PYTHON_9.3','vb':'VB'}
        print (nombre, expresion,listaExpre[tipocod],codeblock)
        arcpy.CalculateField_management(in_table=self.ruta, field=nombre, expression=expresion,expression_type=listaExpre[tipocod],code_block=codeblock)


    def sistemacoordenado(self):
        return arcpy.Describe(self.feature).SpatialReference.name


    def seleccionaAtributo(self, tiposel,expresion):
        listaTipo={'nueva': 'NEW_SELECTION','adicion': 'ADD_TO_SELECTION','remover': 'REMOVE_FROM_SELECTION','subconjunto': 'SUBSET_SELECTION','intercambio':'SWITCH_SELECTION','borrar': 'CLEAR_SELECTION'}
        in_layer_or_view=self.ruta
        selection_type=listaTipo[tiposel]
        where_clause=expresion
        arcpy.SelectLayerByAttribute_management(in_layer_or_view,selection_type,where_clause)


    def seleccionaLocalizacion(self,fseleccionar,fforma,radio,tiposobrepos,tiposel,espacial):
        listaTipoOverlap={'inter': 'INTERSECT','inter3d': 'INTERSECT_3D','dentrodistacia': 'WITHIN_A_DISTANCE','dentrodistacia3d': 'WITHIN_A_DISTANCE_3D'
        ,'dentrodistaciageo': 'WITHIN_A_DISTANCE_GEODESIC','contiene': 'CONTAINS','contienecompletamente': 'COMPLETELY_CONTAINS','contieneclementini': 'CONTAINS_CLEMENTINI'
        ,'dentro': 'WITHIN','completamentedentro': 'COMPLETELY_WITHIN','dentroclementini': 'WITHIN_CLEMENTINI','identico': 'ARE_IDENTICAL_TO'
        ,'tocaborde': 'BOUNDARY_TOUCHES','compartesegmento': 'SHARE_A_LINE_SEGMENT_WITH','cruzalinea': 'CROSSED_BY_THE_OUTLINE_OF','centroide': 'HAVE_THEIR_CENTER_IN'}
        listaTipoSelec={'nueva': 'NEW_SELECTION','adicion': 'ADD_TO_SELECTION ','remover': 'REMOVE_FROM_SELECTION','subconjunto': 'SUBSET_SELECTION','intercambio': 'SWITCH_SELECTION','borrar': 'CLEAR_SELECTION'}
        listaTipoEspacial={'invertida':'INVERT','noinvertida':'NOT_INVERT'}
        in_layer=fseleccionar
        overlap_type=listaTipoOverlap[tiposobrepos]
        select_features=fforma
        search_distance=radio
        selection_type=listaTipoSelec[tiposel]
        invert_spatial_relationship=listaTipoEspacial[espacial]
        arcpy.SelectLayerByLocation_management (in_layer, overlap_type, select_features, search_distance, selection_type, invert_spatial_relationship)

    def valoresCampo(self,campo):
        cursor=arcpy.SearchCursor(self.ruta)
        return [cur.getValue(campo) for cur in cursor]

    def nuevoCampoCode(self,nombre,tipocampo,expresion,tipocod,codeblock):
        listaTipo={'texto': 'TEXT','flotante': 'FLOAT','doble': 'DOUBLE','entero_corto': 'SHORT','entro_largo': 'LONG','fecha': 'DATE'}
        listaExpre={'py':'PYTHON_9.3','vb':'VB'}
        arcpy.AddField_management(self.ruta,nombre,"%s"%listaTipo[tipocampo])
        arcpy.CalculateField_management(self.ruta, field=nombre, expression=expresion,expression_type=listaExpre[tipocod],code_block=codeblock)

    def materializar(self,rutasalida):
        arcpy.CopyFeatures_management(self.ruta, rutasalida)
        return self.ruta

    def truncar(self):
        arcpy.TruncateTable_management(self.feature)

    def cuentaFeatures(self):
        name="myTableView"+"_"+str(random.randrange(0,5000))
        arcpy.MakeTableView_management(self.ruta, name)
        count = int(arcpy.GetCount_management(name).getOutput(0))
        return count

    def select(self,capa,feaSalida,query):
        arcpy.Select_analysis(in_features = capa, out_feature_class= feaSalida, where_clause = query)
        return feaSalida

    def joinField(self,TablaEntrada,LlaveEntrada,TablaCampos,Llavedestino,listaCampos):
        inFeatures = TablaEntrada
        in_field=LlaveEntrada
        joinField = Llavedestino
        joinTable = TablaCampos
        fieldList = listaCampos
        arcpy.JoinField_management (inFeatures, in_field, joinTable, joinField, fieldList)

    def addjoin(self,TablaEntrada,LlaveEntrada,TablaCampos,Llavedestino,listaCampos):
        lista_tipo={'todo':'KEEP_ALL','comunes':'KEEP_COMMON'}
        in_layer=TablaEntrada
        in_field=LlaveEntrada
        join_table=TablaCampos
        join_field=Llavedestino
        join_type=lista_tipo[listaCampos]
        arcpy.AddJoin_management(in_layer,in_field, join_table,join_field,join_type)

    def addjoinCursor(self,capajoin,llaveobjetivo,camposjoin,tipo):
        targshp =self.ruta
        joinshp=capajoin
        joinfields =camposjoin
        joindict = {}

        with arcpy.da.SearchCursor(capajoin,camposjoin) as cursor:
         for row in cursor:
            llave= row[0]
            valor= row[1]
            joindict[llave]=[valor]
        print len(joindict)

        camposupdate=['%s'%(llaveobjetivo),'%s'%(camposjoin[1])]

        arcpy.AddField_management(self.ruta, camposjoin[1],tipo)
        with arcpy.da.UpdateCursor(self.ruta, camposupdate) as recs:
            for rec in recs:
                keyval = rec[0]
                if joindict.has_key(keyval):
                    rec[1] = joindict[keyval][0]
                recs.updateRow(rec)
    def addjoinCursorMultiple(self,capajoin,llaveobjetivo,llavetabla,camposjoin):
        arcpy.AddMessage(capajoin)
        arcpy.AddMessage(camposjoin)
        arcpy.AddMessage(llaveobjetivo)
        arcpy.AddMessage(llavetabla)

        targshp =self.ruta
        joinshp=capajoin
        joinfields =camposjoin
        joindict = {}
        campo_tipo={}
        campo_tipo_nombre=[]
        campo_tipo_tipo=[]
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

        print joindict
        camposupdate=[]
        camposupdate.append(llaveobjetivo)
        for i in xrange(1,len(camposjoin)):
                camposupdate.append(camposjoin[i])
        print camposupdate

        campos_feature=arcpy.ListFields(capajoin)
        for campo in campos_feature:
            campo_tipo[campo.name]=[campo.type]

##        clon=arcpy.CopyFeatures_management(self.feature, ws+"\\"+self.nombre)
        clon=self.feature

        for i in xrange(1,len(camposupdate)):

            arcpy.AddField_management(clon, camposupdate[i],str(campo_tipo[camposupdate[i]][0]))

        with arcpy.da.UpdateCursor(clon, camposupdate) as recs:
            lim_i=len(joinfields)
            j=0
            for rec in recs:
                keyval = rec[0]

                if joindict.has_key(keyval):
                    print "hola"

                    for i in xrange(0,lim_i):
                        print rec[i+1] ,joindict[keyval][i]
                        print i+1, i
                        rec[i+1] = joindict[keyval][i]

                recs.updateRow(rec)

##        arcpy.CopyFeatures_management(clon, ruta_salida+"\\"+nombre_salida)
##        arcpy.CopyFeatures_management(clon, ruta_salida+"\\"+nombre_salida)


    def imprimeAtr(self):
        print self.feature
        print self.ruta
        print self.nombre
        print [x.name for x in self.camposFeature]
        print [x.name for x in self.camposLayer]

if __name__ == '__main__':
##    fcentrada=r"C:\Users\carlos.cano\Documents\ArcGIS\Default.gdb\Prediosx"
##    tITR=r"C:\Users\carlos.cano\Documents\ArcGIS\Default.gdb\demo_itr33"   [x for x in campo_a_unir]
##    tITR=r"X:\opt_test_k\Pruebas_Formalizacion\Insumos\Insumos_valorizacion.gdb\ITR"
    capa=Layer(fcentrada,[],ws)# parte1
    capa.addjoinCursorMultiple(tablajoin,llave_objetivo,llave_tabla,[x for x in campo_a_unir])
##    capa_salida_final=MakeTableView_managementin_features=ruta_salida+"\\"+nombre_salida, out_layer=ruta_salida+"\\"+nombre_salida+".lyr")
##    arcpy.SetParameter(7,capa_salida_final)
    arcpy.SetParameter(5,capa.feature)


