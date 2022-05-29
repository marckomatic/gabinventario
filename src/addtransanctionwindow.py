from tkinter import ttk
import datamanager
from tkinter import *
from datamanager import Product
from tkinter import messagebox

def open(product:Product):
    def updateTable():
        dataSet.delete(*dataSet.get_children())
        index = 0
        result = datamanager.searchTransactionsByProduct(product.codigo)
        for row in result:
            dataSet.insert(parent='',index='end',iid=index,text='',
                values=row)
            index = index + 1
        return

    def clickGuardar():
        precio = 0
        cantidad = 0
        try: 
            precio = float(ctoToSellInput.get())
            if(product.price < 0):
                messagebox.showerror('Error', 'El precio debe de ser una cantidad mayor o igual a 0.', parent=windowForCreate)
                return
        except ValueError:
            messagebox.showerror('Error', 'El precio debe de ser un número válido.', parent=windowForCreate)
            return
        try:
            cantidad = int(qtyToSellInput.get())
            if(cantidad > product.quantity and tipoCbox.get() == "venta"):
                messagebox.showerror('Error', 'La cantidad a vender debe de ser menor o igual a la que se tiene en existencia.', parent=windowForCreate)
                return
        except: 
            messagebox.showerror('Error', 'La cantidad debe de ser un número válido.', parent=windowForCreate)
            return
        try: 
            datamanager.saveTransaccion(product.codigo, precio, cantidad, tipoCbox.get())
        except: 
            messagebox.showerror('Error', 'Error al ingresar la transacción a la base de datos.', parent=windowForCreate)
            return   
        qty.set('')
        cto.set(str(product.price))
        updateTable()
        return


    windowForCreate = Toplevel()
    windowForCreate.grab_set()
    windowForCreate.title('Menú de Transacción De Producto')

    mainframe = LabelFrame(windowForCreate, borderwidth=0)
    mainframe.pack(padx=1, pady=1)

    infoFrame = LabelFrame(mainframe, text= 'Información de Producto No. ' + str(product.codigo), borderwidth=4)
    infoFrame.grid(row=1, column=1, padx=5, pady=5)

    nameLabel = Label(infoFrame, text="Nombre")
    nameLabel.grid(row=1, column=1, padx=5, pady=5)
    name = Label(infoFrame, text=product.name)
    name.grid(row=1, column=2, padx=5, pady=5)

    costPriceLabel = Label(infoFrame, text="Costo")
    costPriceLabel.grid(row=2, column=1, padx=5, pady=5)
    costPrice = Label(infoFrame, text=product.cost)
    costPrice.grid(row=2, column=2, padx=5, pady=5)

    priceLabel = Label(infoFrame, text="Precio de Venta Sugerido")
    priceLabel.grid(row=3, column=1, padx=5, pady=5)
    price = Label(infoFrame, text=product.price)
    price.grid(row=3, column=2, padx=5, pady=5)

    quantityLabel = Label(infoFrame, text="Existencia")
    quantityLabel.grid(row=4, column=1, padx=5, pady=5)
    quantity = Label(infoFrame, text=product.quantity)
    quantity.grid(row=4, column=2, padx=5, pady=5)


    transactionFrame = LabelFrame(mainframe, text= 'Nueva Transacción', borderwidth=4)
    transactionFrame.grid(row=1, column=2, padx=5, pady=5)

    qty = StringVar()
    qty.set('')
    qtyToSellLabel = Label(transactionFrame, text="Cantidad")
    qtyToSellLabel.grid(row = 5, column=1, padx=5, pady=5)
    qtyToSellInput = Entry(transactionFrame, textvariable=qty)
    qtyToSellInput.grid(row=5, column=2, padx=5, pady=5)

    cto = StringVar()
    cto.set(str(product.price))
    ctoToSell = Label(transactionFrame, text="Precio de transaccion")
    ctoToSell.grid(row = 6, column=1, padx=5, pady=5)
    ctoToSellInput = Entry(transactionFrame, textvariable=cto)
    ctoToSellInput.grid(row=6, column=2, padx=5, pady=5)

    tipoLbl = Label(transactionFrame, text="Tipo de transaccion")
    tipoLbl.grid(row=7, column=1, padx=5, pady=5)
    tipoCbox = ttk.Combobox(transactionFrame, values = ["compra", "venta"], state="readonly")
    tipoCbox.current(1)
    tipoCbox.grid(row=7, column=2,  padx=5, pady=5)

    btnGuardar = Button(transactionFrame, text='Agregar', command=clickGuardar)
    btnGuardar.grid(row=20, column=1, padx=5, pady=5)
    
    btnCancelar = Button(transactionFrame, text='Cancelar', command=windowForCreate.destroy)
    btnCancelar.grid(row=20, column=2, padx=5, pady=5)

    #Tabla de transacciones
    tableFrame = LabelFrame(windowForCreate, text="Transacciones de Producto", borderwidth=4)
    tableFrame.pack(padx=6, pady=6)

    dataSet = ttk.Treeview(tableFrame)
    dataSet.pack()
    dataSet['columns']=('fecha', 'tipo', 'cantidad', 'precio', 'total',)
    dataSet.column("#0", width=0,  stretch=NO)
    dataSet.column("fecha",anchor=CENTER, width=300)
    dataSet.column("tipo",anchor=CENTER, width=50)
    dataSet.column("cantidad",anchor=CENTER, width=50)
    dataSet.column("precio",anchor=CENTER, width=80)
    dataSet.column("total",anchor=CENTER, width=80)

    dataSet.heading("#0",text="",anchor=CENTER)
    dataSet.heading("fecha",text="Fecha",anchor=CENTER)
    dataSet.heading("tipo",text="Tipo",anchor=CENTER)
    dataSet.heading("cantidad",text="Cantidad",anchor=CENTER)
    dataSet.heading("precio",text="Precio",anchor=CENTER)
    dataSet.heading("total",text="Total",anchor=CENTER)

    updateTable()
    windowForCreate.resizable(width=False, height=False)
    windowForCreate.mainloop()


