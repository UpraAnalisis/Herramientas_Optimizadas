# -*- coding: utf-8 -*-
import arcpy
import string
from funciones_calidad.check_sde import *


################funciones##################

def validar_carac(capa):
    if checkSDE(capa) == True:
        lista =[f.name for f in arcpy.ListFields (capa) if f.name not in ("OBJECTID","Objectid","Shape","SHAPE","Shape_Length","SHAPE_LENGTH","Shape_Area","SHAPE_AREA")]
        campos_mal = []
        errores_campos = []
        diccionario = 'abcdefghijklmnopqrstuvwxyz(_)0123456789'  ## se crea diccionario con los caracteres permitidos
        for campo in lista:
            campo_tem = []
            validar_car_espe = True
            [campo_tem.append(caracter) for caracter in campo if caracter in diccionario] ## se crea una lista denominada campo_temp, con los caracteres permitidos

            if "".join(campo_tem) == campo: ## se hace un join para volver cadena la lista, y comparar con el nombre real del campo
                validar_car_espe = True ## si campo_temp y campo, son iguales, el campo no tiene caracteres prohibidos.
            else:
                validar_car_espe = False
                campos_mal.append(campo)
    ##    print  str(campos_mal) + str(len(campos_mal)) + "campos con caracteres no permitidos"


    ######Errores para cada uno de los campos mal###################
        for campo in campos_mal:
            mensaje  = []

            ### VERIFICAR SI TIEne ESPACIOS####
            espacio = 0
            for caracter in campo:
                if caracter == " ":
                    espacio += 1
                else:
                    espacio = espacio
            if espacio > 0:
                mensaje.append('Espacio')

           ##VERIFICAR SI TIENE MAYUSCUCULAS###
            if campo.islower()== False:
                mensaje.append('Mayúscula')

            ####CARACTERES ESPECIALES#####
            diccionario2 = 'abcdefghijklmnopqrstuvwxyz_0123456789 ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            carac_especial = 0
            for caracter in campo:
                if caracter not in diccionario2:
                    carac_especial += 1
                else:
                    carac_especial = carac_especial
            if carac_especial > 0 :
                mensaje.append('Caracteres especiales')
            errores_campos.append('El campo %s contiene los siguientes errores: %s'%(campo, str(",".join(mensaje))))
        return errores_campos
    else:
        lista =[f.name for f in arcpy.ListFields (capa) if f.name not in ("OBJECTID","Objectid","Shape","SHAPE","Shape_Length","SHAPE_LENGTH","Shape_Area","SHAPE_AREA")]
        campos_mal = []
        errores_campos = []
        diccionario = 'abcdefghijklmnopqrstuvwxyz_0123456789'  ## se crea diccionario con los caracteres permitidos
        for campo in lista:
            campo_tem = []
            validar_car_espe = True
            [campo_tem.append(caracter) for caracter in campo if caracter in diccionario] ## se crea una lista denominada campo_temp, con los caracteres permitidos

            if "".join(campo_tem) == campo: ## se hace un join para volver cadena la lista, y comparar con el nombre real del campo
                validar_car_espe = True ## si campo_temp y campo, son iguales, el campo no tiene caracteres prohibidos.
            else:
                validar_car_espe = False
                campos_mal.append(campo)
    ##    print  str(campos_mal) + str(len(campos_mal)) + "campos con caracteres no permitidos"


    ######Errores para cada uno de los campos mal###################
        for campo in campos_mal:
            mensaje  = []

            ### VERIFICAR SI TIEne ESPACIOS####
            espacio = 0
            for caracter in campo:
                if caracter == " ":
                    espacio += 1
                else:
                    espacio = espacio
            if espacio > 0:
                mensaje.append('Espacio')

           ##VERIFICAR SI TIENE MAYUSCUCULAS###
            if campo.islower()== False:
                mensaje.append('Mayúscula')

            ####CARACTERES ESPECIALES#####
            diccionario2 = 'abcdefghijklmnopqrstuvwxyz_0123456789 ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            carac_especial = 0
            for caracter in campo:
                if caracter not in diccionario2:
                    carac_especial += 1
                else:
                    carac_especial = carac_especial
            if carac_especial > 0 :
                mensaje.append('Caracteres especiales')
            errores_campos.append('El campo %s contiene los siguientes errores: %s'%(campo, str(",".join(mensaje))))
        return errores_campos




def num_carac(capa):
    lista =[f.name for f in arcpy.ListFields (capa)]
    campo_max=[]
    [campo_max.append(campo) for campo in lista if len(campo) > 16 ]
    if len(campo_max)>0:
        return r'%s Estos campos presentan más caracteres de los permitidos'%((",").join(campo_max))
    else:
        return 0
