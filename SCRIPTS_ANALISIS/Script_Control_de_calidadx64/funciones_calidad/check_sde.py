import arcpy
import os
import sys

def checkSDE(capa):
    tipo_dato = arcpy.Describe(os.path.split(arcpy.Describe(capa).catalogpath)[0]).datatype
    if tipo_dato == "Workspace":
        tipo_ws = arcpy.Describe(os.path.split(arcpy.Describe(capa).catalogpath)[0]).workspaceFactoryProgID
        if tipo_ws == "esriDataSourcesGDB.SdeWorkspaceFactory.1":
            return True
        else:
            return False

    else: # es un dataset
        tipo_ws = arcpy.Describe("\\".join(arcpy.Describe(capa).catalogpath.split("\\")[:-2])).workspaceFactoryProgID
        if tipo_ws == "esriDataSourcesGDB.SdeWorkspaceFactory.1":
             return True
        else:
            return False