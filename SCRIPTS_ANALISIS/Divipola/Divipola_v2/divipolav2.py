# -*- coding: utf-8 -*-

from Tkinter import *  
import Tkinter
import tkMessageBox
import tkMessageBox
import sqlite3 as lite
import os.path
import tkFileDialog
from xlutils.copy import copy
import xlsxwriter
import sys
import os
from xlrd import open_workbook
import Tkinter, Tkconstants, tkFileDialog
import xlrd
import time, multiprocessing
from multiprocessing import Pool

######## interfaz gráfica ######
root = Tk()
######## interfaz gráfica ######
outrow_idx = 0


lst = []
folder_archivos = ""

def getdir():
    global folder_archivos
    path = tkFileDialog.askdirectory(parent=root, initialdir='.')
    folder_archivos = path
    ruta_archivos_entry.insert(0, folder_archivos)
    # ruta_archivos_entry.packt()  

def dane(depto,mpio):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "divipola.sqlite")
    code = ""
    with lite.connect(db_path) as db:
    #con = lite.connect('divipola.sqlite')
   
    #with con:
        cur = db.cursor()
        cur.execute(str("SELECT cod_mpio FROM divipola WHERE depto=\"{0}\" AND mpio=\"{1}\"".format(depto.encode('utf-8'),mpio.encode('utf-8'))))
        rows = cur.fetchall()
        for row in rows:
            code = row[0]
    return code

def listar_xls(path):
    for file in os.listdir(path):
        if file.endswith(".xls") or file.endswith(".xlsx"):
            lst.append(os.path.join(path, file))
    return lst

def add_danecod(f):
    outrow_idx = 0
    rb = open_workbook(f)
    rs = rb.sheet_by_index(0)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    filename, file_extension = os.path.splitext(f)
    new = filename + r'_divipola.xlsx'
    workbook  = xlsxwriter.Workbook(new)
    #worksheet = workbook.add_worksheet(ws.name)
    for s in rb.sheets():
        print 'Processing Sheet:',s.name
        #ws.add_sheet(s.name,cell_overwrite_ok=True)
        ws = wb.get_sheet(s.number)
        worksheet = workbook.add_worksheet(s.name)
        for row_idx in xrange(s.nrows):
            for col_idx in xrange(s.ncols):
                worksheet.write(outrow_idx, col_idx,s.cell_value(row_idx, col_idx))
            worksheet.write(outrow_idx, col_idx+1,dane(s.cell_value(row_idx, 0),s.cell_value(row_idx, 1)))
            outrow_idx += 1
        outrow_idx = 0
    workbook.close()

def finalizado():
    mensaje = "Proceso finalizado con éxito".decode('utf-8')
    tkMessageBox.showinfo(message=mensaje, title="Proceso finalizado")

def error():
    mensaje = "Por favor escriba una ruta válida".decode('utf-8')
    tkMessageBox.showinfo(message=mensaje, title="Error")

def error2():
    mensaje = "Por favor revise que exitan archivos y que tengan estructura descrita en la ayuda".decode('utf-8')
    tkMessageBox.showinfo(message=mensaje, title="Error")

def abrir_ayuda():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ruta_ayuda = os.path.join(BASE_DIR, "img","Manual_divipola.png")
    os.system(os.path.join(ruta_ayuda))

def run():
    try:
        if os.path.exists(str(ruta_archivos_entry.get())):
            jobs = []
            xlsfiles = listar_xls(str(ruta_archivos_entry.get()))
            #p = Pool(7)
            #print(p.map(fusion, xlsfiles))
            for i in xlsfiles:
                print("procesando %s" %(unicode(i)))
                #add_danecod(i)
                p = multiprocessing.Process(target=add_danecod, args=(unicode(i),))
                jobs.append(p)
                p.start()
            for i in jobs:
                i.join()
            finalizado()
        else:
            error()
    except :
        error2()



if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    ######## interfaz gráfica ######
    root.title("Divipola_v2")
    label_archivos = Label(text ="Escriba la ruta de los archivos a procesar: ")
    label_archivos.grid(column = 0, row =1)
    ruta_archivos_entry = Entry(root,width= 50, borderwidth = 5)
    ruta_archivos_entry.grid(column = 1, row =1)

    icon_image_path = os.path.join(BASE_DIR, "img","folder_icon.gif")
    icon_image = PhotoImage(file= icon_image_path)

    btn_directorio= Button(root, width=20,height=20,command=getdir)
    btn_directorio.grid(column = 2, row =1)
    btn_directorio.image = icon_image
    btn_directorio.config(image=icon_image)
    btn_directorio.image = icon_image

    btn_convertir = Button(root,text = "procesar", command=run)
    btn_convertir.grid(row=4,column=1)
    btn_ayuda = Button(root,text = "ayuda", command=abrir_ayuda)
    btn_ayuda.grid(row=0,column=0, sticky="w")
    ######## interfaz gráfica ######
    
    root.mainloop()

