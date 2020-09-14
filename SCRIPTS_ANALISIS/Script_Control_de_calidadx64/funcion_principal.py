#-*- coding: utf-8 -*-

import arcpy
import os
import sys
import datetime
import subprocess
import exceptions
import inspect
import arceditor
##import easygui
from funciones_calidad.nombres_capas import *
from funciones_calidad.nombres_campos import *
from funciones_calidad.tiene_zm import *
from funciones_calidad.multipartes import *
from funciones_calidad.identificador import *
from funciones_calidad.validador_area import *
from funciones_calidad.coordenadas import *
from funciones_calidad.valores_vacios import *
from funciones_calidad.geometria import *
from funciones_calidad.caracteres_valores import *
from funciones_calidad.extent import *
from funciones_calidad.encontrar_duplicados import *
from funciones_calidad.comparar_area import *
from funciones_calidad.neighbors import *
from funciones_calidad.evaluar_topologia import *
from funciones_calidad.Vertex_Count import *

try:

    dic_acentos={"---":" ","***a***":"\xc3\xa1","***e***":"\xc3\xa9", "***i***":"\xc3\xad", "***o***":"\xc3\xb3","***u***":"\xc3\xba","***n***": "\xc3\xb1",
        "***A***":"\xc3\x81","***E***":"\xc3\x89", "***I***":"\xc3\x8d", "***O***":"\xc3\x93","***Ú***":"\xc3\x9a","***N***":"\xc3\x91"}

    #######################################funciones auxiliares##########################################################
    def cambia_caracteres(infea):
        for xx in dic_acentos:# ciclo que reemplaza las letras por los carateres especiales
            infea=infea.replace(xx,dic_acentos[xx])
        return infea

    def directorioyArchivo (): # captura el directorio donde se encuentra almacenado el script y el nombre del script
        archivo=inspect.getfile(inspect.currentframe()) # script filename
        directorio=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
        return archivo, directorio

    def funcion_principal(conteo_validador):
        capa_entrada = arcpy.Describe(cambia_caracteres(arcpy.GetParameterAsText(1))).catalogpath.decode('utf-8')
        nombre_del_identificador = cambia_caracteres(arcpy.GetParameterAsText(2))
        capa_area = cambia_caracteres(arcpy.GetParameterAsText(3)).decode('utf-8')

        if arcpy.Exists(capa_area):
            capa_area = arcpy.Describe(capa_area).catalogpath

        if cambia_caracteres(arcpy.GetParameterAsText(4)) != "":
            area_validacion , unidades_area = cambia_caracteres(arcpy.GetParameterAsText(4)).split(" ")
            area_validacion = float(area_validacion)
            unidades_area = unidades_area.upper()

        if cambia_caracteres(arcpy.GetParameterAsText(6)) != "":
            area_minima , unidades_aream = cambia_caracteres(arcpy.GetParameterAsText(6)).split(" ")
            area_minima = float(area_minima.replace(",","."))
            unidades_aream = unidades_aream.upper()

       #######################################funciones auxiliares##########################################################

        ruta_salida = cambia_caracteres(arcpy.GetParameterAsText(5)).decode('utf-8')
        archivo = cambia_caracteres(arcpy.GetParameterAsText(0)).decode('utf-8')
        tipo_validacion = cambia_caracteres(arcpy.GetParameterAsText(7)).decode('utf-8')

        reporte = open(archivo,"w")


        #####  Validaciones #######
        archivox,direc =directorioyArchivo()
        txt_logo_upra = open(r"%s\logo.txt"%(direc),"r")
        texto_logo_upra =txt_logo_upra.read()
        txt_logo_upra.close()
        reporte.write(texto_logo_upra)
        reporte.write('\n \n')

        reporte.write("Evaluación de calidad realizada a la capa: %s \n que se encuentra ubicada en: %s \n \n"% (str(arcpy.Describe(capa_entrada).name), str(arcpy.Describe(capa_entrada).path)))


        val_nombre_de_campos = arcpy.GetParameterAsText(8) # valida el nombre d elos campos
        if val_nombre_de_campos == "True":
            texto = validar_carac(capa_entrada)
            texto1 = num_carac(capa_entrada)
            if  texto1 !=0:
                reporte.write("###### Validación de número de caracteres en el nombre de los campos ###### \n")
                reporte.write('\n')
                reporte.write(str(texto1) + " \n")
                conteo_validador+=1
            if len(texto)>0:
                reporte.write("###### Validación de caracteres especiales en el nombre de los campos ###### \n")
                reporte.write('\n')
                for error in texto:
                    reporte.write(str(error) + " \n")
                    conteo_validador+=1
            reporte.write('\n')

        val_nombre_capa = arcpy.GetParameterAsText(9) # valida el nombre de la capa
        if val_nombre_capa == "True":
            if len(nombre_capa(capa_entrada))>0:
                reporte.write("###### Validación del nombre de capa ###### \n")
                reporte.write('\n')
                reporte.write(nombre_capa(capa_entrada) + " \n")
                reporte.write('\n')
                conteo_validador+=1

        val_zm = arcpy.GetParameterAsText(10)
        if val_zm == "True":
            if tiene_m(capa_entrada) and tiene_z(capa_entrada):
                reporte.write("###### Validación de geometrias Z y M ###### \n")
                reporte.write('\n')
                if tiene_m(capa_entrada):
                     reporte.write("La capa tiene M en su geometría" + " \n")
                     conteo_validador+=1
                if tiene_z(capa_entrada):
                     reporte.write("La capa tiene Z en su geometría" + " \n")
                     conteo_validador+=1
                reporte.write('\n')

        multipartesx = arcpy.GetParameterAsText(11)
        if multipartesx == "True":
            if multipartes(capa_entrada) != 0:
                reporte.write("###### Validación de multiples partes ###### \n")
                reporte.write('\n')
                reporte.write(str(multipartes(capa_entrada))+"\n")
                reporte.write('\n')
                conteo_validador+=1

        identificadores = arcpy.GetParameterAsText(12)
        if identificadores == "True":
            if len(identificador(capa_entrada,nombre_del_identificador)) >0:
                 reporte.write("###### Validación del identificador ###### \n")
                 reporte.write('\n')
                 reporte.write("Los siguientes identificadores están repetidos \n")
                 if len(identificador(capa_entrada,nombre_del_identificador)) == 1:
                    reporte.write("%s in %s"%(nombre_del_identificador,str(tuple(identificador(capa_entrada,nombre_del_identificador))).replace(",","")) + " \n")
                 else:
                    reporte.write("%s in %s"%(nombre_del_identificador,str(tuple(identificador(capa_entrada,nombre_del_identificador)))) + " \n")
                 reporte.write('\n')
                 conteo_validador+=1


        validar_area = arcpy.GetParameterAsText(13)
        if validar_area == "True":
            diferencia = comparar_areas(capa_entrada, capa_area,area_validacion,unidades_area)
            if abs(diferencia) > area_validacion:
                reporte.write("###### Validación del área ###### \n")
                reporte.write('\n')
                if diferencia >0:
                    reporte.write("la diferencia es de %s %s por encima del área de la capa de validación"%(str(abs(diferencia)),unidades_area))
                else:
                    reporte.write("la diferencia es de %s %s por debajo del área de la capa de validación"%(str(abs(diferencia)),unidades_area))
                reporte.write('\n')
                conteo_validador+=1
            reporte.write('\n')



        val_pol_areaMinima = arcpy.GetParameterAsText(14)
        oid_campo = [f.name for f in arcpy.Describe(capa_entrada).fields if f.type == "OID"][0] ###funcion para obtner el nombre del OID
        if val_pol_areaMinima == "True":
            if len(validador_area(capa_entrada, area_minima, unidades_aream)) >0:
                 reporte.write('\n')
                 reporte.write("###### Validación de polígonos de %s %s ###### \n"%(area_minima, unidades_aream))
                 reporte.write('\n')
                 reporte.write("Los siguientes elementos tienen área inferior a %s %s\n"%(area_minima, unidades_aream))
                 if len(validador_area(capa_entrada, area_minima, unidades_aream)) == 1:
                    reporte.write("%s in %s"%(oid_campo,str(tuple(validador_area(capa_entrada, area_minima, unidades_aream))).replace(",","")) + " \n")
                 else:
                    reporte.write("%s in %s"%(oid_campo,str(tuple(validador_area(capa_entrada, area_minima, unidades_aream)))) + " \n")
                 reporte.write('\n')
                 conteo_validador+=1


        val_extent = arcpy.GetParameterAsText(15)
        if val_extent == "True":
            distancia = compara_capas(capa_entrada,capa_area)
            if distancia >= 100:
                reporte.write("###### Validación de cubrimiento espacial ###### \n")
                reporte.write('\n')
                reporte.write("La extensión de la capa de entrada está desplazada %s %s de la capa de validación \n"%(str(distancia),arcpy.Describe(capa_area).spatialReference.linearUnitName))
                reporte.write('\n')
                conteo_validador+=1


        val_valores_vacios = arcpy.GetParameterAsText(16)
        if val_valores_vacios == "True":
             if valores_vacios(capa_entrada) != 0:
                reporte.write("###### Validación de valores vacíos en campos ######" + " \n")
                reporte.write('\n')
                reporte.write('Los campos se deben establecer como "Sin información" si no aplica o es vacio, "Desconocido" cuando no se conoce. \n' )
                reporte.write('\n')
                arreglo_val_vacios = valores_vacios(capa_entrada)
                for campo in arreglo_val_vacios:
                    reporte.write(str(campo.split(";")[0]) + '\n')
                    reporte.write('\n')
                reporte.write('\n')
                conteo_validador+=1

        val_geometria = arcpy.GetParameterAsText(17)
        if val_geometria == "True":
            try:
                dato = geometria_check(capa_entrada,ruta_salida)
                errores , ruta = dato.split(";")[0],dato.split(";")[1]
                if int(errores)>0:
                    reporte.write("###### Validación de geometría ######" + " \n")
                    reporte.write('\n')
                    reporte.write("La capa cuenta con %s errores geométricos, revise la información en:"%(errores))
                    reporte.write(r"%s"%(ruta))
                    reporte.write('\n')
                    conteo_validador+=1
                reporte.write('\n')
            except arcpy.ExecuteError as e:
                reporte.write("###### Validación de geometría ######" + " \n")
                reporte.write('\n')
                if ".sde" in str(e.message):
                    reporte.write('la función de check geometry no se puede ejecutar en bases de datos corporativas')
                    reporte.write('\n')
                    conteo_validador+=1

        val_caracteres_valores = arcpy.GetParameterAsText(18)
        if val_caracteres_valores == "True":
            if valores_campo(capa_entrada)!= 0:
                reporte.write('\n')
                reporte.write("###### Validación de caracteres en los valores de los campos ######" + " \n")
                reporte.write('\n')
                arreglo_caracter_mal = valores_campo(capa_entrada)
                for campo in arreglo_caracter_mal:
                    reporte.write(str(campo.split(";")[0]) + '\n')
                    reporte.write('\n')
                reporte.write('\n')
                conteo_validador+=1

        val_duplicados = arcpy.GetParameterAsText(19)
        if val_duplicados == "True":
            dato = duplicados(capa_entrada,ruta_salida)
            consulta = duplicados_OID(capa_entrada)
            errores , ruta = dato.split(";")[0],dato.split(";")[1]
            if int(errores)>0:
                reporte.write("###### Validación de duplicados ######" + " \n")
                reporte.write('\n')
                reporte.write("La capa cuenta con %s registros duplicados, revise la información en:"%(errores))
                reporte.write(r"%s"%(ruta))
                reporte.write('\n')
                reporte.write(str(consulta) + "\n")
                conteo_validador+=1
            reporte.write('\n')

        val_sis_referencia = arcpy.GetParameterAsText(20)
        if val_sis_referencia == "True":
             if not sistema_referencia(capa_entrada):
                reporte.write("###### Validación del Sistema de Referencia ###### \n")
                reporte.write('\n')
                reporte.write("La capa NO tiene el sistema de coordenadas Magna Colombia Bogota EPSG: 3116\n")
                conteo_validador+=1
                reporte.write('\n')

        val_polmenores_Vecinos = arcpy.GetParameterAsText(21)
        if val_polmenores_Vecinos == "True":
            try:
                pol_Vecinos  = Reporte_neigbors(capa_entrada, 250000, tipo_validacion, ruta_salida)
                reporte.write (os. linesep)
                reporte.write (os. linesep)
                reporte.write(pol_Vecinos)

                if tipo_validacion != "PERMITIDOS":
                    if len(pol_Vecinos) > 40: ###se deja de valor base 40 por que siempre se escribre cuantos poligonos hay, y ese texto tiene 40 caracteres, ver pol_Vecinos inicial
                        conteo_validador+=1
            except:
                pol_Vecinos  = "#####Validación polígonos de menos de 25 Ha ######\n\n La validación de polígonos permitidos y no permitidos con menos de 25 Ha, se realiza para las \n capas de  zonificación que cuentan con gridcode 1, 2, 3, 8, 0. Por favor, revise si la capa ingresada \n cumple con estas condiciones."
                reporte.write (os. linesep)
                reporte.write (os. linesep)
                reporte.write(pol_Vecinos)


        val_topologia = arcpy.GetParameterAsText(22)
        regla_topologica = cambia_caracteres(arcpy.GetParameterAsText(23)).decode('utf-8')
        if val_topologia == "True":
            resultadoTopologia = topologia(capa_entrada, ruta_salida, regla_topologica)
            if resultadoTopologia != None:
                reporte.write (os. linesep)
                reporte.write (os. linesep)
                reporte.write (str(resultadoTopologia))
                conteo_validador+=1


        val_Vertex = arcpy.GetParameterAsText(24)
        VertexLimit = arcpy.GetParameterAsText(25)
        if val_Vertex == "True":
            resultadoVertices = VertexCount(capa_entrada,int(VertexLimit))
            if resultadoVertices != None:
                reporte.write (os. linesep)
                reporte.write (os. linesep)
                reporte.write (resultadoVertices)
                conteo_validador+=1




        reporte.close()


    if __name__ == '__main__':
        archivo,direc =directorioyArchivo()
        txt_logo = open(r"%s\logo.txt"%(direc),"r")
        print txt_logo.read()
        print ""
        txt_logo.close()
        funcion_principal(0)
        print ""


except exceptions.Exception as e:
    print e.__class__, e.__doc__, e.message
    os.system("pause")

