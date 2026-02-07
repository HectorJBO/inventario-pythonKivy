from Models import Productos, sess
import pandas as pd

def exportacion_excel():
    productos = sess.query(Productos).all()

    data=[{
        "id": p.id,
        "Nombre": p.Nombre,
        "precio": p.precio,
        "cantidad": p.cantidad
    }for p in productos]

    df = pd.DataFrame(data)
    df.to_excel("Repuestos.xlsx",index=False)
    print("reporte exitoso")