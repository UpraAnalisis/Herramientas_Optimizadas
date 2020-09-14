# -*- coding: utf-8 -*-
import arcpy






#arcpy.CalculateField_management(inputFC,'Vertices','!shape!.pointcount',"PYTHON_9.3")
def VertexCount(inputFC,limit):
    fields = ['OID@', 'SHAPE@']
    oidList = []
    with arcpy.da.SearchCursor(inputFC, fields) as cursor:
        # For each row, evaluate the WELL_YIELD value (index position
        # of 0), and update WELL_CLASS (index position of 1)
        for row in cursor:
            numVertex = row[1].pointCount-row[1].partCount
            if (numVertex >= limit):
                oidList.append(row[0])

    fieldName = [x.name for x in arcpy.Describe(inputFC).fields if x.type == 'OID'][0]
    if len(oidList) > 0:
        return   "#### En la capa hay %s poligonos que tienen mas de %s vertices \n %s in %s"%(len(oidList),limit,fieldName, str(tuple(oidList)))

    else:
        return None