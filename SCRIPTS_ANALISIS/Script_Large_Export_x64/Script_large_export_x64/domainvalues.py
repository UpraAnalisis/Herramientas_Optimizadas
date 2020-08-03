import os
import arcpy


def header_and_iterator(dataset_name):
    """Returns a list of column names and an iterator over the same columns"""
    fDict = {}
    if arcpy.GetInstallInfo()['Version'] != '10.0':
        try:
            transDom = arcpy.env.transferDomains
        except:
            pass
        if transDom:
            # check that the workspace can support domains
            allowableWorkspaces = ["LocalDatabase", "RemoteDatabase"]

            # get the workspace type
            try:
                # if stored in a gdb or folder
                dirname = os.path.dirname(dataset_name)
                wspacetype = arcpy.Describe(dirname).workspaceType
            except:
                try:
                    # if stored in a feature dataset
                    dirname = os.path.dirname(dirname)
                    wspacetype = arcpy.Describe(dirname).workspaceType
                except:
                    # if its a feature layer or tableview
                    dirname = os.path.dirname(arcpy.Describe(dataset_name).catalogPath)
                    wspacetype = arcpy.Describe(dirname).workspaceType

            # If workspace type is one that may have domains ('localDatabase' or
            # 'remoteDatabase'), start looking for domains
            if wspacetype in allowableWorkspaces:

                # get a list of domains from the selected table
                fields = arcpy.ListFields(dataset_name)
                domainlist = [f.domain for f in fields if len(f.domain) > 0]

                # if the table has domains associated with it, go on
                if domainlist:
                    # create lists to populate with domains and attributes
                    dDict = {}
                    domainlist2 = []
                    # narrow domain list to only coded value domains (domainlist2),
                    # from that list, get a dictionary of all cv domains and their
                    # associated coded values (as dDict)
                    for d in arcpy.da.ListDomains(dirname):
                        if d.domainType == "CodedValue" and d.name in domainlist:
                            dDict[d.name] = d.codedValues
                            domainlist2.append(d.name)

                    # use 'dDict' to create a dictionary of the fields with their
                    # associated domain values.
                    for f in fields:
                        if f.domain in domainlist2:
                            fDict[f.name] = dDict[f.domain]

    # get a list of the fields in the selected table that arent specialized
    # (not "Geometry", "Raster", "Blob")
    data_description = arcpy.Describe(dataset_name)
    fieldnames = [f.name for f in data_description.fields if f.type not in
    ["Geometry", "Raster", "Blob"]]
    count = len(fieldnames)

    def iterator_for_feature():
        # if using 10.0, use the old searchcursor
        if arcpy.GetInstallInfo()['Version'] == '10.0':
            cursor = arcpy.SearchCursor(dataset_name)
            for row in cursor:
                yield [getattr(row, col) for col in fieldnames]

        # otherwise use the new cursor
        else:
            cursor = arcpy.da.SearchCursor(dataset_name, fieldnames)
            # if the table has any cv domains, go about transfering them.
            if fDict:
                for row in cursor:
                    values = []
                    for i in range(0, count):
                        # if the column has a CV domain
                        if fieldnames[i] in fDict:
                            # get the codes and values of the CV domain
                            # associated with the current column
                            CVDict = fDict[fieldnames[i]]
                            # use that dictionary to write the actual value,
                            # instead of just the code
                            values.append(CVDict[row[i]]) # var3
                        else:
                            values.append(row[i])
                    yield values
            # otherwise, append the base values
            else:
                for row in cursor:
                    yield row
            del row, cursor
    return fieldnames, iterator_for_feature()


def _encode(x):
    """ Encodes input values into 'utf-8' format """
    if isinstance(x, unicode):
        return x.encode("utf-8", 'ignore')
    else:
        return str(x)


def _encodeHeader(x):
    """ Encodes input values into 'utf-8' format, performing some field name
    validation as well """
    return _encode(x.replace(".", "_"))


def validate(out_table, fieldnames):
    """ validates input csv or excel field names based on the output table's
    requirements """
    directory = os.path.dirname(out_table)
    out_name = os.path.basename(out_table)
    wspaceType = arcpy.Describe(directory).workspaceType

    # start a list of fields within the new table. the OID and default fields
    # are different, depending on the table type
    if wspaceType == "FileSystem":
        if out_name.endswith('.dbf'):
            tempFields = ['objectid', 'field1']
        else:
            tempFields = ['rowid', 'objectid', 'field1']
    else:
        tempFields = ['objectid']
    initialList = tempFields[:]

    for i in range(0, len(fieldnames)):
        # validate fieldnames
        if fieldnames[i] == "" or fieldnames[i] == None:
            new_field = "field_{0}".format(i + 1)
        else:
            new_field = arcpy.ValidateFieldName(fieldnames[i], directory)
        if new_field.lower() in initialList:
            if wspaceType == 'FileSystem':
                new_field = "{0}_{1}".format(new_field[:6], i + 1)
            else:
                new_field = "{0}_{1}".format(new_field, i + 1)

        # if the fieldname has been changed from its original name (through
        # validation or to prevent identical names), add a message, and change
        # the name in the fieldname list to the new name (used in the table)
        if new_field != fieldnames[i]:
            arcpy.AddWarning("  Field '{0}' is now '{1}'".format(fieldnames[i],
                             new_field))
            fieldnames[i] = new_field
        initialList.append(new_field)
    # remove the OID field (and any default fields from the list of fields,
    # which was only used to ensure no identical fields were added
    for field in tempFields:
        initialList.remove(field)
    # get the lower case values to make comparison easier
    initialList = [initial.lower() for initial in initialList]

    return initialList
