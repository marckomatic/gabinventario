from tkinter import filedialog
import datamanager
from tkinter import *
from datamanager import Product
from tkinter import ttk
import editwindow
import pandas as pd

def open():
    def doubleClickOnTableItem(event):
        item = dataSet.item(dataSet.selection()[0], 'values')
        producto = Product()
        producto.codigo = int(item[0])
        producto.name = item[1]
        producto.cost = float(item[2]) if item[2] != 'None' else 0
        producto.price = float(item[3]) if item[3] != 'None' else 0
        producto.quantity = int(item[4]) if item[4] != 'None' else 0
        producto.lastInventary = item[5]
        editwindow.open(producto, updateTable)

    def updateTable(type):
        dataSet.delete(*dataSet.get_children())
        index = 0
        result = None
        if type == 'name':
            result = datamanager.searchByName(txtNameSearch.get())
        elif type == 'coincidence': 
            result = datamanager.searchByCoincidence(txtCoincidenceSearch.get())
        else:
            result = datamanager.searchNones()
        for row in result:
            dataSet.insert(parent='',index='end',iid=index,text='',
                values=row)
            index = index + 1
        dataSet.bind("<Double-1>", doubleClickOnTableItem)
        return

    def searchCallback(*args):
        updateTable("name")
    
    def coincidenceSearchCallback(*args):
        updateTable("coincidence")

    def saveToExcel():
        filetypes = (
            ('Archivo de excel', '*.xls'),
        )
        excelFilePath = filedialog.asksaveasfilename(title='Guardar en archivo de excel.', filetypes=filetypes, defaultextension=".xls")
        query = datamanager.searchByName('')
        cols = [column[0] for column in query.description]
        dataFrame = pd.DataFrame.from_records(data = query.fetchall(), columns=cols, index='codigo')
        dataFrame.to_excel(excelFilePath, 'productos')    
    

    windowForProducts = Toplevel()
    windowForProducts.grab_set()
    windowForProducts.title('Adminsitrar Productos')
    mainFrame = LabelFrame(windowForProducts, text='B??squeda', borderwidth=4)
    mainFrame.pack(padx=10, pady=10)

    txtNameSearch = StringVar()
    txtNameSearch.trace_add("write", searchCallback)
    nameSearchLabel = Label(mainFrame, text='Buscar por Nombre')
    nameSearchLabel.grid(row=1, column=1, padx=10, pady=10)
    nameSearchInput = Entry(mainFrame, textvariable=txtNameSearch)
    nameSearchInput.grid(row=2, column=1, padx=10, pady=10)

    txtCoincidenceSearch = StringVar()
    txtCoincidenceSearch.trace_add("write", coincidenceSearchCallback)
    coincidenceSearchLabel = Label(mainFrame, text='Buscar por Coincidencia')
    coincidenceSearchLabel.grid(row=1, column=3, padx=10, pady=10)
    coincidenceSearchInput = Entry(mainFrame, textvariable=txtCoincidenceSearch)
    coincidenceSearchInput.grid(row=2, column=3, padx=10, pady=10)

    btnLimpiar = Button(mainFrame, text="Buscar Incompletos",command=lambda: updateTable('nones'))
    btnLimpiar.grid(row=3, column=2,padx=10, pady=10)

    #table frame
    tableFrame = LabelFrame(windowForProducts, text='Productos Disponibles', borderwidth=4)
    tableFrame.pack(padx=10, pady=10)
    dataSet = ttk.Treeview(tableFrame)
    dataSet.pack()
    dataSet['columns']=('codigo', 'nombre', 'precio_costo', 'precio_venta', 'existencia', 'fecha_inventario',)
    dataSet.column("#0", width=0,  stretch=NO)
    dataSet.column("codigo",anchor=CENTER, width=50)
    dataSet.column("nombre",anchor=CENTER, width=300)
    dataSet.column("precio_costo",anchor=CENTER, width=80)
    dataSet.column("precio_venta",anchor=CENTER, width=80)
    dataSet.column("existencia",anchor=CENTER, width=80)
    dataSet.column("fecha_inventario",anchor=CENTER, width=80)

    dataSet.heading("#0",text="",anchor=CENTER)
    dataSet.heading("codigo",text="Codigo",anchor=CENTER)
    dataSet.heading("nombre",text="Nombre",anchor=CENTER)
    dataSet.heading("precio_costo",text="Precio Costo",anchor=CENTER)
    dataSet.heading("precio_venta",text="Precio Venta",anchor=CENTER)
    dataSet.heading("existencia",text="Existencia",anchor=CENTER)
    dataSet.heading("fecha_inventario",text="??ltimo Inventario",anchor=CENTER)
    updateTable('name')

    optionsFrame = LabelFrame(windowForProducts, text='Opciones', borderwidth=4)
    optionsFrame.pack(padx=10, pady=10)
    btnGuardar = Button(optionsFrame, text="Guardar en Excel", bg="blue", fg="white", command=saveToExcel)
    btnGuardar.pack(side="left",padx=10, pady=10)
    btnLimpiar = Button(optionsFrame, text="BORRAR TODO", bg="red", fg="white")
    btnLimpiar.pack(side="left",padx=10, pady=10)

    windowForProducts.resizable(width=False, height=False)
    windowForProducts.mainloop()