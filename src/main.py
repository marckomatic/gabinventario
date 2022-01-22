from tkinter import *
from PIL import Image, ImageTk
import createwindow
import productswindow
import datamanager


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

btnAdministrar = Button(mainFrame, text='Administrar Productos', command=productswindow.open)
btnAdministrar.pack(pady=10)

btnCargar = Button(mainFrame, text='Cargar desde Excel')
btnCargar.pack(pady=10)




root.mainloop()