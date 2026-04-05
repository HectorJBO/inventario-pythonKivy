from kivy.uix.boxlayout import BoxLayout
from Backend.Repuestos import View
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

class Servis_item(BoxLayout):
    def __init__(self, name, on_select, **kwargs):
        super().__init__(orientation='horizontal',size_hint_y=None, height=40, **kwargs)
        self.name = name
        self.on_select = on_select

        self.add_widget(Label(text=name, size_hint_x=0.8))

        checkbox = CheckBox(size_hint_max=0.2)
        checkbox.bind(active=self.checkbox_changed)
        self.add_widget(checkbox)

    def checkbox_changed(self, checkbox , value):
        self.on_select(self.name , value)
class Servicios(BoxLayout, View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def servis_list(self):
        caja = self.ids.servis
        caja.clear_widgets()

        self.selected = set()

        root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Scroll con lista de productos
        scroll = ScrollView(size_hint=(1, 0.8))
        product_list = GridLayout(cols=1, spacing=5, size_hint_y=None)
        product_list.bind(minimum_height=product_list.setter('height'))

        for titulo in ["===SERVIVOS==="]:
            caja.add_widget(titulo)

        servicios = ["Lavado", "Mantenimiento"]

        for servicio in servicios:
            item = Servis_item(servicio, self.togglet_item)
            product_list.add_widget(item)

        scroll.add_widget(product_list)
        root.add_widget(scroll)


    def togglet_item(self, name, is_select):

        if is_select:
            self.selected_items.add(name)
        else: 
            self.selected.discard(name)