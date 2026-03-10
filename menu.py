from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from Backend.Repuestos import Ventasclass, Add
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file("Backend/Repuestos.kv")
Builder.load_file("Backend/Add.kv")
Builder.load_file("Backend/View.kv")

class MenuScreen(Screen):
    def back(self):
        App.get_running_app().stop()

class VentaScreen(Screen):
    pass

class AgregarScreen(Screen):
    pass

class Screenview(Screen):
    pass

class Screenservice(Screen):
    pass

class Myscreenmanager(ScreenManager):
    pass