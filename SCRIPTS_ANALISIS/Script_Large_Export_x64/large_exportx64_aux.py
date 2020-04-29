#-*- coding: utf-8 -*-
import easygui
import arcpy,os,exceptions
import xlsxwriter
import sys
import time
# sys.setdefaultencoding() does not exist, here!
reload(sys) # Reload does the trick!
sys.setdefaultencoding('UTF8')

def a(path):
    field_names = []
    fields = arcpy.ListFields(path)
    for field in fields:
        field_names.append(field.name)
    return tuple(field_names)

def summari(capa):
    #out = r'' + easygui.diropenbox("Save Folder","Hojas Generadas",".")
    out = outex
    campos =[i.name for i in arcpy.ListFields(capa)]
    st_flds = easygui.multchoicebox("Seleccione campos estadisticas","Select Fields",campos)
    fun = ["SUM","MEAN","MIN","MAX","RANGE","STD","COUNT","FIRST","LAST"]
    st_exp=[[i,easygui.choicebox("Selecione operacion para %s"%i,"Select Fields",fun)] for i in st_flds]
    case_flds = easygui.multchoicebox("Seleccione campos de grupos","Select Fields",campos)
    arcpy.Statistics_analysis(capa,arcpy.Describe(capa).Path+r"\tmp_"+arcpy.Describe(capa).name,st_exp,case_flds)
    array = arcpy.da.TableToNumPyArray(arcpy.Describe(capa).Path+r"\tmp_"+arcpy.Describe(capa).name,'*')
    workbook = xlsxwriter.Workbook(r''+out+'\Summary_%s.xlsx'%(arcpy.Describe(capa).name),{'nan_inf_to_errors': True,'constant_memory': True})
    worksheet = workbook.add_worksheet()
    col = 0
    data = a(arcpy.Describe(capa).Path+r"\tmp_"+arcpy.Describe(capa).name)
    worksheet.write_row('A1', data)
    for row, data in enumerate(array):
        worksheet.write_row(row+1, col, data)
    workbook.close()

def export(capa):
    #out = r'' + easygui.diropenbox("Save Folder","Hojas Generadas",".")
    out = outex
    try:
        if arcpy.Describe(capa).dataType == 'FeatureClass' or arcpy.Describe(capa).dataType == 'FeatureLayer':
            print "Export Feature Class or Layer"
            arcpy.CopyRows_management(capa,arcpy.Describe(capa).Path+r"\tmp_"+arcpy.Describe(capa).name)
            print "Copy rows OK"
            array = arcpy.da.TableToNumPyArray(arcpy.Describe(capa).Path+r"\tmp_"+arcpy.Describe(capa).name,'*')
            data = a(arcpy.Describe(capa).Path+r"\tmp_"+arcpy.Describe(capa).name)
        else:
            print "In is not a Feature Layer"
            array = arcpy.da.TableToNumPyArray(capa,'*')
            data = a(capa)
    except:
        array = arcpy.da.TableToNumPyArray(capa,'*')
        data = a(capa)
    workbook = xlsxwriter.Workbook(r''+out+'\Export_%s.xlsx'%(arcpy.Describe(capa).name),{'nan_inf_to_errors': True,'constant_memory': True})
    worksheet = workbook.add_worksheet()
    col = 0
    worksheet.write_row('A1', data)
    for row, data in enumerate(array):
        worksheet.write_row(row+1, col, data)
    workbook.close()

try:
    t_inicio=time.clock()# captura el tiempo de inicio del proceso
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3116)
    arcpy.env.overwriteOutput = True
    infea = sys.argv[1]
    lyr = sys.argv[1]
    outex = sys.argv[2]

    if __name__ == '__main__':
        print "Ejecutando Super Export a 64bits ...."
        s = easygui.choicebox("Seleccione una opción:","Multiple Large Export Support",["Tables","Layers","Summary"])
        print infea
        if s == 'Layers':
                export(lyr)
        elif s == 'Tables':
                export(lyr)
        elif s == 'Summary':
                summari(lyr)
        else:
            easygui.msgbox("Sorry, This not found!!!","Error de Arcgis")
        start = t_inicio
        end = time.clock()
        hours, rem = divmod(end-start, 3600)
        minutes, seconds = divmod(rem, 60)
        print("proceso Completado en {:0>2} H {:0>2} M {:05.2f} S.".format(int(hours),int(minutes),seconds))

except exceptions.Exception as e:
    print e.__class__, e.__doc__, e.message
    os.system("pause")
