from tkinter import PhotoImage
from turtle import color
from unicodedata import name
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
class OperateurWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_purchases(self):
        code = self.ids.code_inp.text
        product_container = self.ids.products

        if code == "1234":
            details = BoxLayout(size_hint_y=None, height=30, pos_hint={'top': 1})
            product_container.add_widget(details)
            thumbnail = Image(size_hint_x=.1, source='./1.png')
            code = Label(text=code, size_hint_x=.3, color=(0, 0, 0, 1))
            name = Label(text="1er Produit", size_hint_x=.3, color=(0, 0, 0, 1))
            qty = Label(text="1", size_hint_x=.1, color=(0, 0, 0, 1))
            disc = Label(text="0.00", size_hint_x=.1, color=(0, 0, 0, 1))
            price = Label(text="0.00", size_hint_x=.1, color=(0, 0, 0, 1))
            total = Label(text="0.00", size_hint_x=.1, color=(0, 0, 0, 1))
            details.add_widget(thumbnail)
            details.add_widget(code)
            details.add_widget(name)
            details.add_widget(qty)
            details.add_widget(disc)
            details.add_widget(price)
            details.add_widget(total)

class OperateurApp(App):
    def build(self):
        return OperateurWindow()
if __name__=="__main__":
    oa = OperateurApp()
    oa.run()