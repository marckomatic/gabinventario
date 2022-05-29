from datetime import datetime
import datamanager
from tkinter import *
from datamanager import Product
from tkinter import messagebox

def open(product:Product, updateTableFunction):
    windowForCreate = Toplevel()
    windowForCreate.grab_set()
    windowForCreate.title('Editar Producto')

    mainFrame = LabelFrame(windowForCreate, text= 'Información de Producto No. ' + str(product.codigo), borderwidth=4)
    mainFrame.pack(padx=10, pady=10)

    productName = StringVar()
    productName.set(product.name)
    nameLabel = Label(mainFrame, text="Nombre")
    nameLabel.grid(row=1, column=1, padx=5, pady=5)
    nameInput = Entry(mainFrame, textvariable=productName)
    nameInput.grid(row=1, column=2, padx=5, pady=5)

    txtCostPrice = StringVar()
    txtCostPrice.set(str(product.cost))
    costPriceLabel = Label(mainFrame, text="Costo")
    costPriceLabel.grid(row=2, column=1, padx=5, pady=5)
    costPriceInput = Entry(mainFrame, textvariable=txtCostPrice)
    costPriceInput.grid(row=2, column=2, padx=5, pady=5)

    txtPrice = StringVar()
    txtPrice.set(str(product.price))
    priceLabel = Label(mainFrame, text="Precio de Venta")
    priceLabel.grid(row=3, column=1, padx=5, pady=5)
    priceInput = Entry(mainFrame, textvariable=txtPrice)
    priceInput.grid(row=3, column=2, padx=5, pady=5)

    txtQuantity = StringVar()
    txtQuantity.set(str(product.quantity))
    quantityLabel = Label(mainFrame, text="Existencia")
    quantityLabel.grid(row=4, column=1, padx=5, pady=5)
    quantityInput = Entry(mainFrame, textvariable=txtQuantity)
    quantityInput.grid(row=4, column=2, padx=5, pady=5)
    
    txtLastInventary = StringVar()
    txtLastInventary.set(str(product.lastInventary))
    dateLabel = Label(mainFrame, text="Último Inventario")
    dateLabel.grid(row=5, column=1, padx=5, pady=5)
    lastInventaryLabel = Label(mainFrame, textvariable=txtLastInventary)
    lastInventaryLabel.grid(row=5, column=2, padx=5, pady=5)


    def clickGuardar():
        if(updateProduct(windowForCreate, product.codigo, productName.get(), txtCostPrice.get(), txtPrice.get(), txtQuantity.get())):
            updateTableFunction('name') 
            txtLastInventary.set(str(datetime.now().date()))
 
    def clickBorrar():
        response = messagebox.askokcancel("Cuidado!", "¿Está seguro de que desea borrar este producto?", parent=windowForCreate)
        if(response):
            datamanager.deleteProduct(product.codigo)
            updateTableFunction('name')
            windowForCreate.destroy()

    btnGuardar = Button(mainFrame, text='Guardar Cambios', command=clickGuardar)
    btnGuardar.grid(row=6, column=1, padx=5, pady=5)

    btnEliminar = Button(mainFrame, text='Eliminar Producto', command=clickBorrar)
    btnEliminar.grid(row=6, column=2, padx=5, pady=5)
    
    btnCancelar = Button(mainFrame, text='Cancelar', command=windowForCreate.destroy)
    btnCancelar.grid(row=6, column=3, padx=5, pady=5)


    windowForCreate.resizable(width=False, height=False)
    windowForCreate.mainloop()

def updateProduct(windowForCreate, codigo, name, txtCost, txtPrice, txtquantity):
    product:Product = Product()
    if name == '':
        messagebox.showerror('Error', 'El producto debe de tener un nombre válido.', parent=windowForCreate)
        return False
    product.codigo = codigo
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
    datamanager.updateProduct(product)
    return True

