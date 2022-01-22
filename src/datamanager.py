from math import prod
import sqlite3

class Product:
    def __init__(self):
        self.codigo = 0
        self.name = ''
        self.cost = 0
        self.price = 0
        self.quantity = 0
        self.output = 0
        self.entry = 0
        self.total = 0


connection = sqlite3.connect('tucancito.db')
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS PRODUCTO(
        codigo INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio_costo real,
        precio_venta real, 
        existencia INTEGER,
        venta INTEGER,
        entrada INTEGER,
        total INTEGER

    );
""")
connection.commit()

def saveProduct(product: Product):
    cursor.execute("""
        INSERT INTO PRODUCTO(nombre, precio_costo, precio_venta, existencia, venta,
            entrada, total) values (?, ?, ?, ?, ?, ?, ?)
    """, (product.name, product.cost, product.price, product.quantity, product.output, 
    product.entry, product.total))
    connection.commit()

def updateProduct(producto: Product):
    script = """
        UPDATE PRODUCTO 
        SET nombre = ?,
            precio_costo = ?,
            precio_venta = ?,
            existencia = ?,
            venta = ?,
            entrada = ?,
            total = ?
        WHERE codigo = %i
    """ %(producto.codigo)
    cursor.execute(script, (producto.name, producto.cost, producto.price, producto.quantity, producto.output, 
    producto.entry, producto.total))
    connection.commit()

def listProductsInConsole():
    for row in cursor.execute('SELECT * FROM PRODUCTO;'):
        print(row)

def getLastInserted(size):
    return cursor.execute('SELECT * FROM PRODUCTO ORDER BY CODIGO DESC LIMIT ' + str(size))

def searchByName(name):
    return cursor.execute("SELECT * FROM PRODUCTO WHERE nombre LIKE '" + name + "%'")

def deleteProduct(codigo):
    cursor.execute("DELETE FROM PRODUCTO WHERE CODIGO = " + str(codigo))
    connection.commit()