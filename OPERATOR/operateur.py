from tkinter import PhotoImage
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
import re

class OperateurWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cart = []
        self.qty = []
        self.total = 0.00

    def update_purchases(self):
        pcode = self.ids.code_inp.text
        product_container = self.ids.products

        if pcode == "1234" or pcode=="2345":
            details = BoxLayout(size_hint_y=None, height=30, pos_hint={'top': 1})
            product_container.add_widget(details)
            thumbnail = Image(size_hint_x=.3/2, source='./1.png')
            code = Label(text=pcode, size_hint_x=.2, color=(0, 0, 0, 1))
            name = Label(text='HP PROBOOK 640 G2 | Intel® i5‑5350H 3.7 Ghz\n16 RAM | 320 SSD | 15,6" | 90 %', size_hint_x=.6, color=(.06, .45, .45, 1), height=10)
            qty = Label(text="1000", size_hint_x=.1, color=(0, 0, 0, 1))
            disc = Label(text="12000.00", size_hint_x=.1, color=(0, 0, 0, 1))
            price = Label(text="12000.00", size_hint_x=.2, color=(0, 0, 0, 1))
            total = Label(text="12000.00", size_hint_x=.2, color=(0, 0, 0, 1))
            details.add_widget(thumbnail)
            details.add_widget(code)
            details.add_widget(qty)
            details.add_widget(name)
            details.add_widget(price)
            details.add_widget(disc)
            details.add_widget(total)

            # update receipt preview
            pname = "HP PROBOOK 640 G2"
            if pcode == "2345":
                pname = "DELL LATITUDE"
            pprice = 24000.00
            pqty = 1
            self.total += pprice
            purchase_total = f"`\n\nTotale:\t\t\t\t\t\t\t\t{self.total}"

            curprdct = self.ids.cur_product
            curprdct.text = pname

            curprdct = self.ids.cur_price
            curprdct.text = f'{pprice}'

            preview = self.ids.receipt_preview
            prev_text = preview.text
            _prev = prev_text.find('`')

            if _prev > 0:
                prev_text = prev_text[:_prev]

            ptarget = -1
            for i, c in enumerate(self.cart):
                if c == pcode:
                    ptarget = i

            if ptarget >= 0:
                expr = f'%s\t\tx{self.qty[ptarget]}\t'%pname
                pqty = self.qty[ptarget]+1
                self.qty[ptarget] = pqty
                rexpr = pname+'\t\tx'+str(pqty)+'\t'
                nu_text = re.sub(expr, rexpr, prev_text)
                preview.text = nu_text + purchase_total
            elif ptarget == -1:
                self.cart.append(pcode)
                self.qty.append(1)
                nu_preview = '\n'.join([prev_text, pname+f'\t\tx{pqty}\t\t'+str(pprice), purchase_total])
                preview.text = nu_preview


class OperateurApp(App):
    def build(self):
        return OperateurWindow()

if __name__=="__main__":
    oa = OperateurApp()
    oa.run()