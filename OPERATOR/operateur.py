from tkinter import PhotoImage
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
import re
from pymongo import MongoClient
from kivy.uix.modalview import ModalView
from collections import OrderedDict
import itertools

class OperateurWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        client = MongoClient()
        db = client.pos
        self.stocks = db.stocks

        self.cart = []
        self.cartsummary = {}
        self.detailedsummary = {}
        self.qty = []
        self.total = 0.00
        self.mastertotal = []
        self.stock = []
        self.stockindex = []
        self.purchases = []
        
        self.get_stocks()
        
        self.previewheader = self.ids.receipt_preview.text
        

    def error_popup(self, message):
        box = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)        
        error_img = Image(source='./utils/1.png', size=(150, 150))
        error_msg = Label(text=f'{message}', bold=True)
        
        popup = ModalView(size_hint=(None, None), size=(400, 300))
        box.add_widget(error_img)
        box.add_widget(error_msg)
        
        popup.add_widget(box)
        
        popup.open()
        
        return 0
     
        
    def get_stocks(self):
        product = []
        self.stock = []
        self.stockindex = []
    
        for element in self.stocks.find():
            self.stockindex.append(element['Ref'])
            product.append(f"{element['marque']} {element['modele']} | {element['cpu']} | {element['ram']}\n{element['stockage']} | {element['gpu']} | {element['batterie']}")
            product.append(element['en_stock'])
            self.stock.append(product)
            product = []
    
        for element in self.stock:
            if (int(element[1]) < 1) or element[1] == '':
                element[1] = 'Out of stock'
        
        print(self.stockindex)


    def add_to_cart(self):
        ref = self.ids.code_inp.text
        try:
            add = int(self.ids.qty_inp.text)
        except:
            if self.ids.qty_inp.text == '':
                add = 1
            else:
                self.error_popup("Invalid Input")
                self.ids.qty_inp.focus = True
                return 0
        
        # check if the product exists
        try:
            if  self.stock[self.stockindex.index(ref)][1] == 'Out of stock':
                self.error_popup('Rupture de stock')
                self.ids.code_inp.focus = True
                return 0
            qty = int(self.stock[self.stockindex.index(ref)][1])
            indice = self.stockindex.index(ref)
        except ValueError:
            self.error_popup("Référence Invalide")
            self.ids.code_inp.text = ''
            self.ids.code_inp.focus = True
            return 0
        
        # calculate price
        try:
            price = float(self.ids.price_inp.text)
        except:
            if self.ids.price_inp.text == '':
                print("Champ Manquant")
                self.ids.price_inp.focus = True
                return 0
            else:
                print("Invalid Input")
                return 0
        try:
            discount = float(self.ids.disc_inp.text)
        except:
            if self.ids.disc_inp.text == '':
                discount = 0
            else:
                self.error_popup("Invalid Input")
                return 0
        
        try:
            discount_per = float(self.ids.disc_perc_inp.text)
        except:
            if self.ids.disc_perc_inp.text == '':
                discount_per = 0
            else:
                self.error_popup("Invalid Input")
                self.ids.disc_perc_inp.focus = True
                return 0
        
        try:
            tva = float(self.ids.vat_inp.text)
        except:
            if self.ids.vat_inp.text == '':
                tva = 0
            else:
                self.ids.vat_inp.focus = True
                self.error_popup('Invalid Input')
        
        discount_per = price*discount_per/100
        tva = price*tva/100
        total = price-discount-discount_per+tva
        discount = discount + discount_per
        
        
        # check if there  is enough stock
        prdct = []
        try:
            if self.cartsummary[ref] + add <= qty:
                for i in range(0, add):
                    self.cart.append(self.stockindex[indice])
                    prdct.append(self.stockindex[indice])
                    prdct.append(self.stock[indice][0])
                    prdct.append(add)
                    prdct.append(discount)
                    prdct.append(tva)
                    prdct.append(price)
                    prdct.append(total)
                    self.purchases.append(prdct)
                    prdct = []
            else:
                self.error_popup("stock insuffisant")
                self.ids.qty_inp.focus = True
                return 0
        except KeyError:
            if add <= qty:
                for i in range(0, add):
                    self.cart.append(self.stockindex[indice])
                    prdct.append(self.stockindex[indice])
                    prdct.append(self.stock[indice][0])
                    prdct.append(add)
                    prdct.append(discount)
                    prdct.append(tva)
                    prdct.append(price)
                    prdct.append(total)
                    self.purchases.append(prdct)
                    prdct = []
                    #self.detailedsummary[f"{ref}"] = self.stock[indice]
            else:
                self.error_popup("stock insuffisant")
                self.ids.qty_inp.focus = True
                return 0
        
        self.purchases = list(k for k,_ in itertools.groupby(self.purchases))

        
        for c, element in enumerate(self.purchases):
            if c == 0:
                self.update_purchases(element[0], element[1], element[2], element[3], element[4], element[5], element[6], clear=True)
            else:
                self.update_purchases(element[0], element[1], element[2], element[3], element[4], element[5], element[6], clear=False)
        
        self.cartsummary = dict((item, self.cart.count(item)) for item in self.cart)
        self.update_reciept()
        
        print(self.cartsummary)
        print(total)
        self.ids.code_inp.text = ''
        self.ids.code_inp.focus = True
        print("done")
        return 0
        
        
    def update_purchases(self, ref, designation, quantity, discount, vat, price, totall, clear=False):
        pcode = ref
        product_container = self.ids.products
        
        if clear ==  True:
            product_container.clear_widgets()

        details = BoxLayout(size_hint_y=None, height=30, pos_hint={'top': 1})
        product_container.add_widget(details)
        #thumbnail = Image(size_hint_x=.3/2, source='./1.png')
        code = Label(text=pcode, size_hint_x=.2, color=(0, 0, 0, 1))
        name = Label(text=designation, size_hint_x=.6, color=(.06, .45, .45, 1), height=10)
        qty = Label(text=str(quantity), size_hint_x=.1, color=(0, 0, 0, 1))
        disc = Label(text=str(discount), size_hint_x=.1, color=(0, 0, 0, 1))
        tva = Label(text=str(vat), size_hint_x=.1, color=(0, 0, 0, 1))
        price = Label(text=str(price), size_hint_x=.2, color=(0, 0, 0, 1))
        total = Label(text=str(totall), size_hint_x=.2, color=(0, 0, 0, 1))
        #details.add_widget(thumbnail)
        details.add_widget(code)
        details.add_widget(qty)
        details.add_widget(name)
        details.add_widget(price)
        details.add_widget(disc)
        details.add_widget(tva)
        details.add_widget(total)

        pname = designation

        pprice = float(totall)
        self.total += pprice

        curprdct = self.ids.cur_product
        curprdct.text = pname

        curprdct = self.ids.cur_price
        curprdct.text = f'{pprice}'

        return 0


    def update_reciept(self):
        preview = self.ids.receipt_preview
        #(ref, designation, quantity, discount, vat, price, totall)
        new = self.previewheader
        for c, item in enumerate(self.purchases):
            new = new + f"\n({c+1})\t" + str(item[1]).lower()+ "\n"
            new = f"{new}\n{str(item[0])}\t{str(item[5])}\tx\t{str(item[2])}\n"

        new = new + "\n" + "\n" + F"Totale: {self.total}"

        preview.text = new

        self.ids.code_inp.text = ''
        self.ids.qty_inp.text = ''
        self.ids.price_inp.text = ''
        self.ids.disc_inp.text = ''
        self.ids.disc_perc_inp.text = ''
        self.ids.vat_inp.text = ''
        self.ids.code_inp.focus = True

        return 0

 
    def clear(self):
        preview = self.ids.receipt_preview
        preview.text = self.previewheader
        self.ids.products.clear_widgets()
        self.cart = []
        self.cartsummary = {}
        self.detailedsummary = {}
        self.qty = []
        self.total = 0.00
        self.mastertotal = []
        self.stock = []
        self.stockindex = []
        self.purchases = []
        
        self.get_stocks()
        
        self.ids.cur_product.text = 'Désignation'
        self.ids.cur_price.text = '0.00'
        self.ids.code_inp.text = ''
        self.ids.qty_inp.text = ''
        self.ids.price_inp.text = ''
        self.ids.disc_inp.text = ''
        self.ids.disc_perc_inp.text = ''
        self.ids.vat_inp.text = ''
        self.ids.code_inp.focus = True
        
        return 0
        
class OperateurApp(App):
    def build(self):
        return OperateurWindow()

if __name__=="__main__":
    oa = OperateurApp()
    oa.run()
