from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button


class InventoryItem(BoxLayout):
    """Fila de inventario con nombre y checkbox"""
    def __init__(self, name, on_select, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=40, **kwargs)
        self.name = name
        self.on_select = on_select

        # Etiqueta con el nombre del producto
        self.add_widget(Label(text=name, size_hint_x=0.8))

        # Checkbox para seleccionar
        checkbox = CheckBox(size_hint_x=0.2)
        checkbox.bind(active=self.checkbox_changed)
        self.add_widget(checkbox)

    def checkbox_changed(self, checkbox, value):
        """Llama a la función de selección cuando cambia el estado"""
        self.on_select(self.name, value)


class InventoryApp(App):
    def build(self):
        self.selected_items = set()  # Guardar productos seleccionados

        root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Scroll con lista de productos
        scroll = ScrollView(size_hint=(1, 0.8))
        product_list = GridLayout(cols=1, spacing=5, size_hint_y=None)
        product_list.bind(minimum_height=product_list.setter('height'))

        # Lista de ejemplo (puedes cargar desde SQLite)
        products = ["Laptop", "Mouse", "Teclado", "Monitor", "Impresora"]

        for product in products:
            item = InventoryItem(product, self.toggle_item)
            product_list.add_widget(item)

        scroll.add_widget(product_list)
        root.add_widget(scroll)

        # Botón para mostrar seleccionados
        btn_show = Button(text="Mostrar seleccionados", size_hint=(1, 0.2))
        btn_show.bind(on_press=self.show_selected)
        root.add_widget(btn_show)

        return root

    def toggle_item(self, name, is_selected):
        """Agrega o quita productos de la selección"""
        if is_selected:
            self.selected_items.add(name)
        else:
            self.selected_items.discard(name)

    def show_selected(self, instance):
        """Muestra en consola los productos seleccionados"""
        print("Seleccionados:", list(self.selected_items))


if __name__ == '__main__':
    InventoryApp().run()