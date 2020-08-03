#-*- coding: utf-8 -*-
import easygui
import arcpy,os,exceptions
import xlsxwriter
import sys
import time
import datetime
from TableToExcel import *

# sys.setdefaultencoding() does not exist, here!
reload(sys) # Reload does the trick!
sys.setdefaultencoding('UTF8')

def create_gdb(outfolder):
    gdb_nombre = "base_%s"%(datetime.datetime.now().strftime("%b_%d_%Y_%H_%M_%S"))
    gdb_salida = "%s\\%s.gdb"%(outfolder, gdb_nombre)
        # Process: Create File GDB
    if not arcpy.Exists(gdb_salida):
       arcpy.CreateFileGDB_management(outfolder, gdb_nombre)
       return gdb_salida


def fracciona_tabla(tabla,base):
    nombre_tabla = arcpy.Describe(tabla).name
    table_view =arcpy.MakeTableView_management(tabla ,nombre_tabla ).getOutput(0)
    if int(arcpy.GetCount_management(tabla).getOutput(0)) > 1000000:

        arcpy.TableSelect_analysis(in_table =table_view,
        out_table = os.path.join(base,nombre_tabla + "_px_1")
        ,where_clause = "OBJECTID <= 1000000")

        arcpy.TableSelect_analysis(in_table = table_view,
        out_table = os.path.join(base,nombre_tabla + "_px2_2")
        ,where_clause = "OBJECTID > 1000000")

    else:
       arcpy.TableSelect_analysis(in_table = table_view,
       out_table = os.path.join(base,nombre_tabla))

def listar(base):
    arcpy.env.workspace = base
    tablas=arcpy.ListTables()
    ws=arcpy.env.workspace
    feature_classes = []
    for dirpath, dirnames, filenames in arcpy.da.Walk(ws, datatype="FeatureClass"):
        for filename in filenames:
            feature_classes.append(os.path.join(dirpath, filename))

    ruta_tablas = [os.path.join(arcpy.env.workspace, t) for t in tablas]
    return feature_classes + ruta_tablas


def convierte_excel(lista):
    for archivo in lista:
        export_to_xls(archivo, os.path.join(outfolder,arcpy.Describe(archivo).name + ".xlsx"))



try:
    t_inicio=time.clock()# captura el tiempo de inicio del proceso
    arcpy.env.overwriteOutput = True
    infea = sys.argv[1]
    outfolder = sys.argv[2]
    filename = sys.argv[3]

    _GDB = create_gdb(outfolder)
    fracciona_tabla(infea,_GDB)
    lista_archivos = listar(_GDB)
    convierte_excel(lista_archivos)

    print(os.path.join(outfolder,filename + ".xlsx"))
##    export_to_xls(infea, os.path.join(outfolder,filename + ".xlsx"))



    if __name__ == '__main__':
        print ("Ejecutando Super Export a 64bits ....")
        print (outfolder)


except exceptions.Exception as e:
    print e.__class__, e.__doc__, e.message
    os.system("pause")
