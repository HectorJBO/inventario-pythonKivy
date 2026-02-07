from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from Backend.Repuestos import Ventasclass , Add
from kivy.lang import Builder
from menu import Myscreenmanager

Builder.load_file("Menu.kv")

class Ventana(App):
    title = 'Moto servicio A y N'
    def build(self):
        return Myscreenmanager()
