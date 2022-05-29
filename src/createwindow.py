import datamanager
from tkinter import *
from datamanager import Product
from tkinter import messagebox
from tkinter import ttk
import editwindow

def open():
    windowForCreate = Toplevel()
    windowForCreate.grab_set()
    windowForCreate.title('Ingresar Producto')

    mainFrame = LabelFrame(windowForCreate, text='Información de Producto', borderwidth=4)
    mainFrame.pack(padx=10, pady=10)

    productName = StringVar()
    nameLabel = Label(mainFrame, text="Nombre")
    nameLabel.grid(row=1, column=1, padx=5, pady=5)
    nameInput = Entry(mainFrame, textvariable=productName)
    nameInput.grid(row=1, column=2, padx=5, pady=5)

    txtCostPrice = StringVar()
    costPriceLabel = Label(mainFrame, text="Costo")
    costPriceLabel.grid(row=2, column=1, padx=5, pady=5)
    costPriceInput = Entry(mainFrame, textvariable=txtCostPrice)
    costPriceInput.grid(row=2, column=2, padx=5, pady=5)

    txtPrice = StringVar()
    priceLabel = Label(mainFrame, text="Precio de Venta")
    priceLabel.grid(row=3, column=1, padx=5, pady=5)
    priceInput = Entry(mainFrame, textvariable=txtPrice)
    priceInput.grid(row=3, column=2, padx=5, pady=5)

    txtQuantity = StringVar()
    quantityLabel = Label(mainFrame, text="Existencia")
    quantityLabel.grid(row=4, column=1, padx=5, pady=5)
    quantityInput = Entry(mainFrame, textvariable=txtQuantity)
    quantityInput.grid(row=4, column=2, padx=5, pady=5)

    def doubleClickOnTableItem(event):
        item = dataSet.item(dataSet.selection()[0], 'values')
        producto = Product()
        producto.codigo = int(item[0])
        producto.name = item[1]
        producto.cost =  float(item[2]) if item[2] != 'None' else 0
        producto.price = float(item[3]) if item[3] != 'None' else 0
        producto.quantity = int(item[4]) if item[4] != 'None' else 0
        producto.lastInventary = item[5]
        editwindow.open(producto, updateTableFromOutside)

    def updateTable(dataSet):
        dataSet.delete(*dataSet.get_children())
        index = 0
        for row in datamanager.getLastInserted(20):
            dataSet.insert(parent='',index='end',iid=index,text='',
                values=row)
            index = index + 1
        dataSet.bind("<Double-1>", doubleClickOnTableItem)
        return
    
    def updateTableFromOutside():
        updateTable(dataSet)

    def clickCrear():
        if(createProduct(windowForCreate, productName.get(), txtCostPrice.get(), txtPrice.get(), txtQuantity.get())):
            productName.set('')
            productName.set('')
            txtCostPrice.set('')
            txtPrice.set('')
            txtQuantity.set('')
            updateTable(dataSet)
            return

    btnCrear = Button(mainFrame, text='Ingresar', command=clickCrear)
    btnCrear.grid(row=5, column=2, padx=5, pady=5)


    #table frame
    tableFrame = LabelFrame(windowForCreate, text='Últimos Productos Ingresados', borderwidth=4)
    tableFrame.pack(padx=10, pady=10)
    dataSet = ttk.Treeview(tableFrame)
    dataSet.pack()
    dataSet['columns']=('codigo', 'nombre', 'precio_costo', 'precio_venta', 'existencia', 'ultimo_inventario')
    dataSet.column("#0", width=0,  stretch=NO)
    dataSet.column("codigo",anchor=CENTER, width=50)
    dataSet.column("nombre",anchor=CENTER, width=300)
    dataSet.column("precio_costo",anchor=CENTER, width=80)
    dataSet.column("precio_venta",anchor=CENTER, width=80)
    dataSet.column("existencia",anchor=CENTER, width=80)
    dataSet.column("ultimo_inventario",anchor=CENTER, width=100)

    dataSet.heading("#0",text="",anchor=CENTER)
    dataSet.heading("codigo",text="Codigo",anchor=CENTER)
    dataSet.heading("nombre",text="Nombre",anchor=CENTER)
    dataSet.heading("precio_costo",text="Precio Costo",anchor=CENTER)
    dataSet.heading("precio_venta",text="Precio Venta",anchor=CENTER)
    dataSet.heading("existencia",text="Existencia",anchor=CENTER)
    dataSet.heading("ultimo_inventario",text="Fecha Inventario",anchor=CENTER)
    updateTable(dataSet)

    windowForCreate.resizable(False, False)
    windowForCreate.mainloop()

def createProduct(windowForCreate, name, txtCost, txtPrice, txtquantity):
    product:Product = Product()
    if name == '':
        messagebox.showerror('Error', 'El producto debe de tener un nombre válido.', parent=windowForCreate)
        return False
    product.name = name
    try: 
        product.price = float(txtPrice)
        if(product.price < 0):
            messagebox.showerror('Error', 'El precio de venta debe de ser un número válido.', parent=windowForCreate)
            return False
    except ValueError:
        messagebox.showerror('Error', 'El precio de venta debe de ser un número válido.', parent=windowForCreate)
        return False

    try:
        product.cost = float(txtCost)
        if(product.cost < 0):
            messagebox.showerror('Error', 'El costo del producto debe de ser un número válido.', parent=windowForCreate)
            return False      
    except ValueError:
        messagebox.showerror('Error', 'El precio de venta debe de ser un número válido.', parent=windowForCreate)
        return False
        
    try:
        product.quantity = int(txtquantity)
        if(product.quantity < 0 or product.quantity % 1 > 0):
            messagebox.showerror('Error', 'La cantidad del producto debe de ser un número entero válido.', parent=windowForCreate)
            return False      
    except ValueError:
        if txtquantity != '':
            messagebox.showerror('Error', 'La cantidad del producto debe de ser un número entero válido.', parent=windowForCreate)
            return False
        product.quantity = 0
    
    datamanager.saveProduct(product)
    return True

