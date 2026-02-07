from abc import ABC, abstractmethod
#from static.image import logotaller

class Factura:
    def __init__(self):
     self.partes = []

    def agregar_partes(self, parte: str):
        self.partes.append(parte)

    def mostrar(self):
       return"\n".join(self.partes)
    

class Recibo(ABC):
   @abstractmethod
   def icono(self):
      pass

   @abstractmethod
   def encabezado(self):
      pass
   
   @abstractmethod
   def descripcion(self):
      pass

   @abstractmethod
   def costo(self):
      pass
   
   @abstractmethod
   def pie_pagina(self):
      pass
   
   @abstractmethod
   def obtener(self):
      pass
   
class ReciboBasico(Recibo):
   def __init__(self):
      self.recibo = Factura()

   def icono(self):
       self.recibo.agregar_partes(f"")

   def encabezado(self):
       self.recibo.agregar_partes("Moto Servicios A y N")

   def descripcion(self, Nombre, cantidad, mano_obra):
      self.recibo.agregar_partes(f"Repuestos: {Nombre}")
      self.recibo.agregar_partes(f"cantidad: {cantidad}")
      self.recibo.agregar_partes(f"mano de obra: {mano_obra}")

   def costo(self, precio):
       self.recibo.agregar_partes(f"precio: {precio}")

   def pie_pagina(self):
      self.recibo.agregar_partes("Gracias por su compra")

   def obtener(self):
       return self.recibo
   

class Creator_Factura:
   def __init__(self, Builder: Recibo):
      self.Builder = Builder

   def crear_recibo(self,Nombre, cantidad, mano_obra, precio):
      self.Builder.icono()
      self.Builder.encabezado()
      self.Builder.descripcion(Nombre, cantidad, mano_obra)
      self.Builder.costo(precio)
      self.Builder.pie_pagina()
      return self.Builder.obtener()
