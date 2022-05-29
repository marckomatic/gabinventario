from cmath import isnan
from tkinter import *
from PIL import Image, ImageTk
import createwindow
from datamanager import Product, saveProduct
import productswindow
import transactionswindow
from tkinter import filedialog
import pandas as pd

def openFile():
    filetypes = (
        ('Excel CSV', '*.csv'),
    )
    csvFileName = filedialog.askopenfile(title='Abrir archivo de excel.', filetypes=filetypes).name
    print(csvFileName)
    csv = pd.read_csv(csvFileName, encoding='utf8')
    for tuple in csv.itertuples():
        print(tuple)
        producto = Product()
        producto.name = tuple.Nombre.replace("|", ",")
        producto.price = float(tuple.Venta)
        producto.cost = float(tuple.Costo)
        producto.lastInventary = tuple.Actualizacion
        if(not isnan(tuple.Existencia)):
            producto.quantity = int(tuple.Existencia)
        saveProduct(producto)



#Main window
root = Tk()
root.geometry('300x390')
root.title('Inventario El Tucancito')
root.resizable(False, False)

#Open Windows



#Main Window content
mainFrame = LabelFrame(root, text='Menú Principal', borderwidth=4)
mainFrame.pack(padx=10, pady=10)

iconImg = ImageTk.PhotoImage(Image.open('assets/inventary.png').resize((200,200), Image.ANTIALIAS))
imageLabel = Label(mainFrame, image=iconImg)
imageLabel.pack()

btnIngresar = Button(mainFrame, text='Ingresar Productos', command=createwindow.open)
btnIngresar.pack(pady=10)

btnAdministrar = Button(mainFrame, text='Productos', command=productswindow.open)
btnAdministrar.pack(pady=10)


btnTransacciones = Button(mainFrame, text='Transacciones', command=transactionswindow.open)
btnTransacciones.pack(pady=10)

btnCargar = Button(mainFrame, text='Cargar desde Excel', command=openFile)
btnCargar.pack(pady=10)

root.mainloop()
