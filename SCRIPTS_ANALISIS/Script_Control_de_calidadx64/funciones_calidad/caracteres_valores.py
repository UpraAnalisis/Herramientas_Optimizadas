# -*- coding: utf-8 -*-
import arcpy
import sys

reload(sys) # Reload does the trick!
sys.setdefaultencoding('UTF8')

def valores_campo(capa):
    oid_campo= [f.name for f in arcpy.Describe(capa).fields if f.type == "OID"][0]
    campos =[f.name for f in arcpy.ListFields (capa) if f.name not in ("Shape","SHAPE") and f.type in ("String")]
    diccionario = 'abcdefghijklmnñopqrstuvwxyz_0123456789 ABCDEFGHIJKLMNÑOPQRSTUVWXYZ.,-áéíóúüÁÉÍÓÚÜ()'
    valores_mal = []
    for campo in campos:
        item_car_esp = []
        for item in arcpy.da.SearchCursor(capa,["OID@",campo]):
            campo_tem = []
            [campo_tem.append(caracter) for caracter in str(item[1]).decode('utf-8') if caracter in diccionario] ## se crea una lista denominada campo_temp, con los caracteres permitidos

            if "".join(campo_tem) == str(item[1]): ## se hace un join para volver cadena la lista, y comparar con el nombre real del campo
                continue
            else:
                item_car_esp.append(item[0])
        if len(item_car_esp) > 0 :
            if len(item_car_esp) == 1:
                valores_mal.append( 'El campo %s tiene caracteres especiales en los valores con los siguientes OID: %s In %s;'%(campo,oid_campo,str(tuple(item_car_esp)).replace(",","")))
            else:
                valores_mal.append( 'El campo %s tiene caracteres especiales en los valores con los siguientes OID: %s In %s;'%(campo,oid_campo,str(tuple(item_car_esp))))

    if len(valores_mal) != 0:
       return valores_mal
    else:
        return 0




