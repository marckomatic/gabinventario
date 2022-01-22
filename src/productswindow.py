from cProfile import label
from turtle import bgcolor, color, position
from matplotlib.pyplot import text
from sklearn import datasets
import datamanager
from tkinter import *
from datamanager import Product
from tkinter import messagebox
from tkinter import ttk
import editwindow

def open():
    def doubleClickOnTableItem(event):
        item = dataSet.item(dataSet.selection()[0], 'values')
        producto = Product()
        producto.codigo = int(item[0])
        producto.name = item[1]
        producto.cost = float(item[2])
        producto.price = float(item[3])
        producto.quantity = int(item[4])
        producto.output = float(item[5])
        producto.entry = float(item[6])
        producto.total = float(item[7])
        editwindow.open(producto, updateTable)

    def updateTable():
        dataSet.delete(*dataSet.get_children())
        index = 0
        for row in datamanager.searchByName(txtNameSearch.get()):
            dataSet.insert(parent='',index='end',iid=index,text='',
                values=row)
            index = index + 1
        dataSet.bind("<Double-1>", doubleClickOnTableItem)
        return

    def searchCallback(*args):
        updateTable()

    windowForProducts = Toplevel()
    windowForProducts.grab_set()
    windowForProducts.title('Adminsitrar Productos')
    mainFrame = LabelFrame(windowForProducts, text='Productos Ingresados', borderwidth=4)
    mainFrame.pack(padx=10, pady=10)

    txtNameSearch = StringVar()
    txtNameSearch.trace_add("write", searchCallback)
    nameSearchLabel = Label(mainFrame, text='Buscar por Nombre')
    nameSearchLabel.pack(padx=10, pady=5)
    nameSearchInput = Entry(mainFrame, textvariable=txtNameSearch)
    nameSearchInput.pack(padx=10, pady=5)

    #table frame
    tableFrame = LabelFrame(windowForProducts, text='Últimos Productos Ingresados', borderwidth=4)
    tableFrame.pack(padx=10, pady=10)
    dataSet = ttk.Treeview(tableFrame)
    dataSet.pack()
    dataSet['columns']=('codigo', 'nombre', 'precio_costo', 'precio_venta', 'existencia', 'venta', 'entrada', 'total')
    dataSet.column("#0", width=0,  stretch=NO)
    dataSet.column("codigo",anchor=CENTER, width=50)
    dataSet.column("nombre",anchor=CENTER, width=300)
    dataSet.column("precio_costo",anchor=CENTER, width=80)
    dataSet.column("precio_venta",anchor=CENTER, width=80)
    dataSet.column("existencia",anchor=CENTER, width=80)
    dataSet.column("venta",anchor=CENTER, width=80)
    dataSet.column("entrada",anchor=CENTER, width=80)
    dataSet.column("total",anchor=CENTER, width=80)

    dataSet.heading("#0",text="",anchor=CENTER)
    dataSet.heading("codigo",text="Codigo",anchor=CENTER)
    dataSet.heading("nombre",text="Nombre",anchor=CENTER)
    dataSet.heading("precio_costo",text="Precio Costo",anchor=CENTER)
    dataSet.heading("precio_venta",text="Precio Venta",anchor=CENTER)
    dataSet.heading("existencia",text="Existencia",anchor=CENTER)
    dataSet.heading("venta",text="Venta",anchor=CENTER)
    dataSet.heading("entrada",text="Entrada",anchor=CENTER)
    dataSet.heading("total",text="Total",anchor=CENTER)
    updateTable()

    optionsFrame = LabelFrame(windowForProducts, text='Opciones', borderwidth=4)
    optionsFrame.pack(padx=10, pady=10)
    btnGuardar = Button(optionsFrame, text="Guardar en Excel", bg="blue", fg="white")
    btnGuardar.pack(side="left",padx=10, pady=10)
    btnLimpiar = Button(optionsFrame, text="BORRAR TODO", bg="red", fg="white")
    btnLimpiar.pack(side="left",padx=10, pady=10)


    windowForProducts.mainloop()