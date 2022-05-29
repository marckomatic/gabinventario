import sqlite3
from datetime import datetime

class Product:
    def __init__(self):
        self.codigo = 0
        self.name = ''
        self.cost = 0
        self.price = 0
        self.quantity = 0
        self.lastInventary = ''


connection = sqlite3.connect('tucancito.db')
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS PRODUCTO(
        codigo INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio_costo real,
        precio_venta real, 
        existencia INTEGER,
        fecha_inventario TEXT
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS TRANSACCION(
        codigo INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_producto INTEGER NOT NULL,
        tipo TEXT NOT NULL,
        total real,
        cantidad INTEGER,
        precio real,
        fecha TEXT,

        CONSTRAINT fk_codigo_producto
            FOREIGN KEY (codigo_producto)
            REFERENCES PRODUCTO (codigo)
            ON DELETE CASCADE
    );
""")

connection.commit()

def saveProduct(product: Product):
    cursor.execute("""
        INSERT INTO PRODUCTO(nombre, precio_costo, precio_venta, existencia, fecha_inventario) values (?, ?, ?, ?, ?)
    """, (product.name, product.cost, product.price, product.quantity, datetime.now().date() if product.lastInventary == 'si' else '2020-03-13'))
    connection.commit()

def updateProduct(producto: Product):
    script = """
        UPDATE PRODUCTO 
        SET nombre = ?,
            precio_costo = ?,
            precio_venta = ?,
            existencia = ?,
            fecha_inventario = ?
        WHERE codigo = %i
    """ %(producto.codigo)
    cursor.execute(script, (producto.name, producto.cost, producto.price, producto.quantity, datetime.now().date()))
    connection.commit()

def listProductsInConsole():
    for row in cursor.execute('SELECT * FROM PRODUCTO;'):
        print(row)

def getLastInserted(size):
    return cursor.execute('SELECT * FROM PRODUCTO ORDER BY CODIGO DESC LIMIT ' + str(size))

def searchByName(name):
    return cursor.execute("SELECT * FROM PRODUCTO WHERE nombre LIKE '" + name + "%'")

def searchByCoincidence(coincidence):
    return cursor.execute("SELECT * FROM PRODUCTO WHERE nombre LIKE '%" + coincidence + "%' "
    + " or precio_costo LIKE '%" + coincidence + "%' "
    + " or precio_venta LIKE '%" + coincidence + "%' "
    + " or existencia LIKE '%" + coincidence + "%' "
    + " or fecha_inventario LIKE '%" + coincidence + "%' ")

def searchNones():
    return cursor.execute("SELECT * FROM PRODUCTO WHERE precio_costo is null"
    + " or precio_venta is null "
    + " or existencia is null ")

def searchTransactionsByProduct(productCode):
    return cursor.execute("SELECT FECHA, TIPO, CANTIDAD, PRECIO, TOTAL FROM TRANSACCION WHERE codigo_producto = '" + str(productCode) + "' order by codigo desc")

def saveTransaccion(codigoProducto, precio, cantidad, tipo):
    cursor.execute("""
        INSERT INTO TRANSACCION(codigo_producto, tipo, total, cantidad, precio, fecha) values (?, ?, ?, ?, ?, ?)
    """, (codigoProducto, tipo, cantidad * precio, cantidad, precio,  datetime.now()))
    connection.commit()


def deleteProduct(codigo):
    cursor.execute("DELETE FROM PRODUCTO WHERE CODIGO = " + str(codigo))
    connection.commit()

def deleteAll(codigo):
    cursor.execute("DELETE FROM PRODUCTO")

def dropTableProducto():
    cursor.execute("DROP TABLE PRODUCTO")

def dropTableTransaccion():    
    cursor.execute("DROP TABLE TRANSACCION")
