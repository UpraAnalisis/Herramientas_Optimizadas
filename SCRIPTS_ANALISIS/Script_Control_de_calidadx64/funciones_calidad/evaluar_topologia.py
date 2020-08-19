#-*- coding:'utf-8' -*-


# Set the necessary product code
import arceditor
import arcpy
import sys
import os
import datetime


reload(sys) # Reload does the trick!
sys.setdefaultencoding('UTF8')

def topologia(capa, folder_salida, ruleTopology):
    global gdb_salida
    try:
        nombre_gdb = "topologia_%s"%(datetime.datetime.now().strftime("%b_%d_%Y_%H_%M_%S"))
        nombre_gdb = nombre_gdb.replace(".","")
        gdb_salida = "%s\\%s.gdb"%(folder_salida, nombre_gdb)
        nombre_dataset = "dt_topologia"


        arcpy.env.workspace = gdb_salida
        nombre_capa = arcpy.Describe(capa).name


        # Process: Create File GDB
        if not arcpy.Exists(gdb_salida):
           arcpy.CreateFileGDB_management(folder_salida, nombre_gdb)

        # Process: Create Feature Dataset
        arcpy.CreateFeatureDataset_management(gdb_salida, nombre_dataset, "PROJCS['MAGNA_Colombia_Bogota',GEOGCS['GCS_MAGNA',DATUM['D_MAGNA',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',1000000.0],PARAMETER['False_Northing',1000000.0],PARAMETER['Central_Meridian',-74.07750791666666],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',4.596200416666666],UNIT['Meter',1.0]];-4623200 -9510300 10000;-100000 10000;-100000 10000;0,001;0,001;0,001;IsHighPrecision")
        path_dataset = os.path.join(gdb_salida, nombre_dataset)
    ##    correc_topo = "\\%s"%(nombre_dataset)
        # Process: Feature Class to Feature Class

        arcpy.FeatureClassToFeatureClass_conversion(capa, path_dataset, nombre_capa)
        path_Feature = os.path.join(path_dataset, nombre_capa)
    ##    FeaClass = "%s\\%s"%(nombre_dataset, nombre_capa)
        # Process: Create Topology
        Capa_topologia ="topo_capa_%s"%(nombre_capa)
        arcpy.CreateTopology_management(path_dataset, Capa_topologia, "")
        path_topology = os.path.join(path_dataset, Capa_topologia )
    ##    Topology = "%s\\topo_capa_%s"%(nombre_dataset, nombre_capa)

        # Process: Add Feature Class To Topology
        arcpy.AddFeatureClassToTopology_management(path_topology,path_Feature , "1", "1")

           ###########################################################################################################################

        if ruleTopology == "Huecos y sobreposición":
            contador = 0
            arcpy.AddRuleToTopology_management(path_topology, "Must Not Overlap (Area)", path_Feature, "", "", "")

            # Process: Add Rule To Topology (2)
            arcpy.AddRuleToTopology_management(path_topology, "Must Not Have Gaps (Area)", path_Feature, "", "", "")

            # Process: Validate Topology
            arcpy.ValidateTopology_management(path_topology, "Full_Extent")

            # Process: Exportar error topology
            arcpy.ExportTopologyErrors_management(path_topology,path_dataset, "Errores")

            ErroresTopologia = "#####Validación de topología (Huecos - Sobreposición) ######\n\n"


            for fc in arcpy.ListFeatureClasses(feature_dataset = nombre_dataset):
                path = os.path.join(arcpy.env.workspace, nombre_dataset, fc)

                if  "Errores" in arcpy.Describe(path).name:
                    Ctd_contar = arcpy.GetCount_management(path)
                    Ctd = int(Ctd_contar.getOutput(0))

                    if Ctd > 0:

                        if "line" in str(arcpy.Describe(path).name):
                            if Ctd > 1:
                                contador = +1
                                ErroresTopologia = ErroresTopologia + "La capa presenta %s casos de huecos. \n"%(Ctd)
                        elif "poly" in str(arcpy.Describe(path).name):
                            contador = +1
                            ErroresTopologia = ErroresTopologia + "La capa presenta %s casos de sobreposición. \n"%(Ctd)

                            ####oid de los poligonos con sobreposicion
                            oid_campo= [f.name for f in arcpy.Describe(capa).fields if f.type == "OID"][0]
                            arreglo = []
                            with arcpy.da.SearchCursor(path,["OID@","OriginObjectID","DestinationObjectID"]) as cursor:
                                for fila in cursor:
                                    arreglo.append(fila[1])
                                    arreglo.append(fila[2])
                            if len(arreglo) >0:
                                if len(arreglo)==1:
                                    ErroresTopologia = ErroresTopologia + 'Los siguientes OID presentan sobreposición %s in %s \n'%(oid_campo,str(tuple(list(set(arreglo)))).replace(",",""))
                                else:
                                    ErroresTopologia = ErroresTopologia + 'Los siguientes OID presentan sobreposición  %s in %s \n'%(oid_campo,str(tuple(list(set(arreglo)))))

                else:
                    pass

            ErroresTopologia = ErroresTopologia + "\n\n Para validar los errores topológicos por favor consulte el siguente dataset %s"%(path_dataset)


            ###########################################################################################################################


        elif ruleTopology == "Huecos":
            contador = 0

            # Process: Add Rule To Topology (2)
            arcpy.AddRuleToTopology_management(path_topology, "Must Not Have Gaps (Area)", path_Feature, "", "", "")

            # Process: Validate Topology
            arcpy.ValidateTopology_management(path_topology, "Full_Extent")

            # Process: Exportar error topology
            arcpy.ExportTopologyErrors_management(path_topology,path_dataset, "Errores")

            ErroresTopologia = "#####Validación de topología (Huecos) ######\n\n"
            for fc in arcpy.ListFeatureClasses(feature_dataset = nombre_dataset):
                path = os.path.join(arcpy.env.workspace, nombre_dataset, fc)

                if  "Errores" in arcpy.Describe(path).name:
                    Ctd_contar = arcpy.GetCount_management(path)
                    Ctd = int(Ctd_contar.getOutput(0))
                    if Ctd > 1:

                        if "line" in str(arcpy.Describe(path).name):
                            contador = +1
                            ErroresTopologia = ErroresTopologia + "La capa presenta %s casos de huecos. \n"%(Ctd)
                else:
                    pass

            ErroresTopologia = ErroresTopologia + "\n\n Para validar los errores topológicos por favor consulte el siguente dataset %s"%(path_dataset)


        ###########################################################################################################################


        elif ruleTopology == "Sobreposición":
            contador = 0

             # Process: Add Rule To Topology
            arcpy.AddRuleToTopology_management(path_topology, "Must Not Overlap (Area)", path_Feature, "", "", "")

            # Process: Validate Topology
            arcpy.ValidateTopology_management(path_topology, "Full_Extent")

            # Process: Exportar error topology
            arcpy.ExportTopologyErrors_management(path_topology,path_dataset, "Errores")

            ErroresTopologia = "#####Validación de topología (Sobreposición) ######\n\n"

            for fc in arcpy.ListFeatureClasses(feature_dataset = nombre_dataset):
                path = os.path.join(arcpy.env.workspace, nombre_dataset, fc)

                if  "Errores" in arcpy.Describe(path).name:
                    Ctd_contar = arcpy.GetCount_management(path)
                    Ctd = int(Ctd_contar.getOutput(0))
                    if Ctd > 0:

                        if "poly" in str(arcpy.Describe(path).name):
                            contador = +1
                            ErroresTopologia = ErroresTopologia + "La capa presenta %s casos de sobreposición. \n"%(Ctd)

                            ####oid de los poligonos con sobreposicion
                            oid_campo= [f.name for f in arcpy.Describe(capa).fields if f.type == "OID"][0]
                            arreglo = []
                            with arcpy.da.SearchCursor(path,["OID@","OriginObjectID","DestinationObjectID"]) as cursor:
                                for fila in cursor:
                                    arreglo.append(fila[1])
                                    arreglo.append(fila[2])
                            if len(arreglo) >0:
                                if len(arreglo)==1:
                                    ErroresTopologia = ErroresTopologia + 'Los siguientes OID presentan sobreposición %s in %s \n'%(oid_campo,str(tuple(list(set(arreglo)))).replace(",",""))
                                else:
                                    ErroresTopologia = ErroresTopologia + 'Los siguientes OID presentan sobreposición  %s in %s \n'%(oid_campo,str(tuple(list(set(arreglo)))))


            ErroresTopologia = ErroresTopologia + "\n\n Para validar los errores topológicos por favor consulte el siguente dataset %s"%(path_dataset)
    except arcpy.ExecuteError:
        arcpy.AddMessage(arcpy.GetMessages())
        msg = arcpy.GetMessages()
        if msg.find("-2147467259") != -1:
            ErroresTopologia = "#######Evaluación Topología###### \n El Feature de entrada presenta demasiados errores topológicos, \n por lo que ArcGIS no puede crear la topología, se recomienda fraccionar en partes más pequeñas \n  e.x. sí es del territorio nacional, se puede dividir por departamentos, o emplear la herramienta Multitopology \n que se encuentra en U: \SCRIPTS_ANALISIS"
            contador = 1
    except:

        # By default any other errors will be caught here
        e = sys.exc_info()[1]
        msg = e.args[0]
        ErroresTopologia = "#######Evaluación Topología###### \n Se encontró el siguiente error %s"%(msg)
        contador = 1

    if contador > 0:
        return ErroresTopologia + "\n"
    elif contador == 0:
        return None




