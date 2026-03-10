from Models import Productos , sess
from Facturacion import Factura, ReciboBasico , Recibo, Creator_Factura
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from functools import partial
from kivy.properties import BooleanProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior

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

class inventario_list(BoxLayout):
   """Fila de inventario con nombre y checkbox"""
   def __init__(self, name, on_select, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=40, **kwargs)
        self.name = name
        self.on_select = on_select

        # Etiqueta con el nombre del producto
        self.add_widget(Label(text=str(name), size_hint_x=0.8))

        # Checkbox para seleccionar
        checkbox = CheckBox(size_hint_x=0.2)
        checkbox.bind(active=self.checkbox_changed)
        self.add_widget(checkbox)

   def checkbox_changed(self, checkbox, value):
        """Llama a la función de selección cuando cambia el estado"""
        self.on_select(self.name, value)

class View(BoxLayout):
   def __init__(self, **kwargs):
      super().__init__(**kwargs)
      self.sess = sess

   def ver_repuestos(self):
    contenedor = self.ids._inventario_
    contenedor.clear_widgets()

    root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Scroll con lista de productos
    scroll = ScrollView(size_hint=(1, 0.8))

    product_list = GridLayout(cols=1, spacing=5, size_hint_y=None)
    product_list.bind(minimum_height=product_list.setter('height'))
    
    self.selected_item = set()
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

    for Repuesto in Repuestos:
       item = inventario_list(Repuesto, self.togglet_item)
       product_list.add_widget(item)


    scroll.add_widget(product_list)
    root.add_widget(scroll)
      # Botón para mostrar seleccionados
    btn_show = Button(text="Mostrar seleccionados", size_hint=(1, 0.2))
    btn_show.bind(on_press=self.show_selected)
    root.add_widget(btn_show)
   
   def togglet_item(self, name , is_selected):
      if is_selected:
         self.selected_item.add(name)
      else: 
         self.selected_item.discard(name)
      
   def show_selected(self, instance):
        """Muestra en consola los productos seleccionados"""
        print("Seleccionados:", list(self.selected_items))
       
   """def seleccecionador_productos(self , Producto):
      self.seleccionador = Producto

      if self.seleccionador == True:
         self.ids._inventario.add_widget(
            Label(text="Ya hay un repuesto seleccionado")
         )
      elif self.seleccionador == False:
         self.ids._inventario.add_widget(
            Label(text="No hay Repuesto seleccionado")
         ) 
         return"""
      
   def delete_items(self,):
      if not self.seleccecionador_productos(Producto=Productos):
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
      
      for titulo in [ "id","Nombre", "precio", "cantidad" ]:
       lookfor.add_widget(Label(text=titulo))
      
      if Resultados:
         for i in Resultados:
           lookfor.add_widget(Label(text=str(i.id)))
           lookfor.add_widget(Label(text=str(i.Nombre)))
           lookfor.add_widget(Label(text=str(i.precio)))
           lookfor.add_widget(Label(text=str(i.cantidad)))
      else:
         lookfor.add_widget(Label(text="producto no encontrado"))
   
   def agregar_cantidad(self):
     agregador = self.ids._inventario_
     agregador.clear_widgets()

     select = self.lookfor.cantidad
     agregar = self.ids.cantidad.text.strip()

     if not agregar:
        agregador.add_widget(Label(text='agrega la cantidad'))
        return

     CANTIDAD = int(agregar)

     select = self.sess.query(Productos).filter_by(cantidad=select).first()

     if not select:
        agregador.add_widget(Label(text="No hay un producto seleccionado aun"))
     elif select is True:
        agregador.add_widget(Label(text="Ya hay un producto seleccionado"))
        return
     
     select.cantidad += CANTIDAD
     self.sess.commit()

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

