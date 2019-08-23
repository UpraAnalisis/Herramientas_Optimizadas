# -*- coding: utf-8 -*-
# --------------------------------------------------------------------
# Fecha de creacion: 2017-11-15 08:59:08.00000
# Author: Carlos Mario Cano Campillo
# Email: carlos.cano@upra.gov.co / kanocampillo@gmail.com
# Propietario: Unidad de Planificación Rural Agropecuaria
#
# ---------------------------------------------------------------------
# sys.setdefaultencoding() does not exist, here!
reload(sys) # Reload does the trick!
sys.setdefaultencoding('UTF8')


import arcpy

capa_entrada = arcpy.GetParameterAsText(0)
capa_salida = arcpy.Describe(capa_entrada).catalogpath
arcpy.SetParameter(1,capa_salida)