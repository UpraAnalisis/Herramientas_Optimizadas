# -*- coding: utf-8 -*-
import arcpy
import sys

reload(sys) # Reload does the trick!
sys.setdefaultencoding('UTF8')

def valores_vacios(capa):
    oid_campo= [f.name for f in arcpy.Describe(capa).fields if f.type == "OID"][0]
    campos =[f.name for f in arcpy.ListFields (capa)]
    oid_valores_vacios = []
    for campo in campos:
        valores = []
        for item in arcpy.da.SearchCursor(capa,["OID@",campo]):
            if item[1] is None:
                valores.append(item[0])
            elif str(item[1]).isspace() == True:
                valores.append(item[0])
            else:
                lon_item = []
                [lon_item.append(caracter) for caracter in str(item[1])]
                if len(lon_item) == 0:
                    valores.append(item[0])
        if len(valores) >0 :
            if len(valores) == 1:
                oid_valores_vacios.append('En el campo %s, se encuentran vacíos los valores con los siguientes OID: %s In %s ;'%(campo, oid_campo, str(tuple(valores)).replace(",","")))
            else:
                oid_valores_vacios.append('En el campo %s, se encuentran vacíos los valores con los siguientes OID: %s In %s ;'%(campo, oid_campo, str(tuple(valores))))
    if len(oid_valores_vacios) != 0:
        return oid_valores_vacios
    else:
        return 0










