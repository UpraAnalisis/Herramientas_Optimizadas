#-*- coding: 'utf-8' -*-
import arcpy
import collections

def multipartes(capa):
    oid_campo= [f.name for f in arcpy.Describe(capa).fields if f.type == "OID"][0]
    multi_arreglo = []
    with arcpy.da.SearchCursor(capa,["OID@","SHAPE@"]) as cursor:
        for fila in cursor:
            if fila[1].partCount>1:
                multi_arreglo.append(fila[0])
    if len(multi_arreglo) >0:
        if len(multi_arreglo)==1:
            return 'Los siguientes OID son multipartes %s in %s'%(oid_campo,str(tuple(multi_arreglo)).replace(",",""))
        else:
            return 'Los siguientes OID son multipartes %s in %s'%(oid_campo,str(tuple(multi_arreglo)))
    else:
        return 0