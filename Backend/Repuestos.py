from Models import Productos , sess
from Facturacion import Factura, ReciboBasico , Recibo, Creator_Factura
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from functools import partial

class Add(BoxLayout):
   def __init__(self, **kwargs):
      super().__init__(**kwargs)

   def agregar_repuestos(self):
    self.add_widget(Label(text="producto agregado exitosamente"))
    nombre = self.ids.nombre.text.strip()
    precio = self.ids.precio.text.strip()
    cantidad_texto = self.ids.cantidad.text.strip()

    cantidad = int(cantidad_texto)
    precio = float(precio)

    if not nombre:
       print("no puedes dejar el producto sin nombre")
       return

    Nuevo_producto = Productos(Nombre=nombre, precio=precio, cantidad=cantidad)
    sess.add(Nuevo_producto)
    sess.commit()

class View(BoxLayout):
   def __init__(self, **kwargs):
      super().__init__(**kwargs)
      self.sess = sess

   def ver_repuestos(self):
    contenedor = self.ids._inventario_
    contenedor.clear_widgets()
    
    self.seleccionador = None
    Repuestos = self.sess.query(Productos).all()

    for titulo in [ "id","Nombre", "precio", "cantidad" ]:
       contenedor.add_widget(Label(text=titulo))

    if not Repuestos:
        contenedor.add_widget(
        Label(text="No hay Repuestos agregados aun..."))
    else:
        for Producto in Repuestos:
         contenedor.add_widget(Label(text=str(Producto.id)))
         contenedor.add_widget(Label(text=str(Producto.Nombre)))
         contenedor.add_widget(Label(text=str(Producto.precio)))
         contenedor.add_widget(Label(text=str(Producto.cantidad)))

         boton = Button(text="seleccionar", size_hint_y = None, width = 10)
         boton.bind(on_press=lambda boton, prod=Producto: self.seleccecionador_productos(prod))
        contenedor.add_widget(boton)

   def seleccecionador_productos(self , Producto):
      self.seleccionador = Producto
      self.ids._inventario_.add_widget(
         Label(text=f"seleccionado: {Producto.Nombre}")
      )

      if self.seleccionador == True:
         self.ids._inventario.add_widget(
            Label(text="Ya hay un repuesto seleccionado")
         )
      elif self.seleccionador == False:
         self.ids._inventario.add_widget(
            Label(text="No hay Repuesto seleccionado")
         ) 
         return
      
   def delete_items(self):
      if not self.seleccionador:
         self.ids._inventario_.add_widget(
            Label(text="No hay producto seleccionado")
         )
         return
      
      nombre = self.seleccionador.Nombre

      self.sess.delete(self.seleccionador)
      self.sess.commit() 

      self.ids._inventario_.clear_widgets()
      self.ids._inventario_.add_widget(
         Label(text=f" {nombre} eliminado correctamente")
      )
   def buscador(self):
      lookfor = self.ids._inventario_
      lookfor.clear_widgets()
      Buscador = self.ids.nombre.text.strip()
      
      if not Buscador:
         lookfor.add_widget(Label(text="Escribe el nombre del repuesto que buscas."))
         return
      
      Resultados = self.sess.query(Productos).filter(Productos.Nombre.ilike(f"%{Buscador}")).all()
      
      if Resultados:
         lookfor.add_widget(Label(text=f"{Buscador}"))
      for i in Resultados:
       lookfor.add_widget(Label(text=str(i.id)))
       lookfor.add_widget(Label(text=str(i.Nombre)))
       lookfor.add_widget(Label(text=str(i.precio)))
       lookfor.add_widget(Label(text=str(i.cantidad)))
      else:
         lookfor.add_widget(Label(text="producto no encontrado"))
   
   def agregar_cantidad(self):
     agregador = self.ids._inventario
     agregador.clear_widgets()
     self.seleccionador
     agregar = int(input("cantidad a agregar:"))

      repuaa = self.sess.query(Productos).filter_by(Nombre=Busca_repuesto).first()

      if not repuaa:
        print("NO encontrado")
        return
   
     repuaa.cantidad += agregar
     sess.commit()

     agregador.add_widget(Label(text="se han agregado "))


class Ventasclass(BoxLayout):
   def __init__(self, **Kwargs):
      super().__init__(**Kwargs)
      self.sess = sess

   def realizar_venta(self):
        nombre = self.ids.nombre.text.strip()
        cantidad_texto = self.ids.cantidad.text.strip()
        mano_obra_texto = self.ids.mano_obra.text.strip()

        # VALIDACIONES
        if not nombre:
            self.ids.resultado.text = "Ingresa el nombre del producto"
            return

        if not cantidad_texto.isdigit():
            self.ids.resultado.text = "Cantidad inválida"
            return

        cantidad = int(cantidad_texto)
        mano_obra = float(mano_obra_texto) if mano_obra_texto else 0

        # BUSCAR PRODUCTO
        producto = (
            self.sess.query(Productos)
            .filter(Productos.Nombre == nombre)
            .first()
        )

        if not producto:
            self.ids.resultado.text = "El producto no existe"
            return

        if producto.cantidad < cantidad:
            self.ids.resultado.text = "Stock insuficiente"
            return

        # REALIZAR VENTA
        producto.cantidad -= cantidad
        total = producto.precio * cantidad + mano_obra

        self.sess.commit()

        self.ids.resultado.text = f"Venta realizada\nTotal: {total}"

