from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from pymongo import MongoClient
from kivy.uix.modalview import ModalView
import itertools
import os
from  random import choice
from string import digits, ascii_uppercase
import yaml
import shutil
from datetime import datetime
import sys

from kivy.lang import Builder


Builder.load_file('./OPERATOR/operateur.kv')



class OperateurWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        client = MongoClient()
        db = client.pos
        self.stocks = db.stocks
        self.products = db.stocks
        self.transactions = db.transactions
        self.clients = db.clients
        
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
        
        self.transaction_id = self.gen_transaction_ref()
        self.client_id = self.gen_client_ref()
        
    
    def logout(self):
        self.parent.parent.current = "scrn_si"
          
    def success_popup(self, operation):
        box = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)        
        error_img = Image(source='./utils/2.png', size=(150, 150))
        error_msg = Label(text=f'{operation} avec succès', bold=True)
        
        
        popup = ModalView(size_hint=(None, None), size=(400, 300))
        box.add_widget(error_img)
        box.add_widget(error_msg)
        
        popup.add_widget(box)
        
        popup.open()
        
        return 0
        

    def transaction_exist(self, ref):
        tr = self.transactions.find({'Ref': f'{ref}'})
        try:
            tr = tr[0]
            return True 
        except IndexError:
            return False 
 
        
    def gen_transaction_ref(self):
        numbers = digits
        letters = ascii_uppercase

        g = True

        while g == True:
            one = ''.join(choice(numbers) for i in range(5))
            two = ''.join(choice(letters) for i in range(1))
            ref = f"TR-{one}{two}"
            g = self.transaction_exist(ref)
        
        return ref
    
 
    def client_exist(self, ref):
        tr = self.clients.find({'Ref': f'{ref}'})
        try:
            tr = tr[0]
            return True 
        except IndexError:
            return False 

    
    def gen_client_ref(self):
        numbers = digits
        letters = ascii_uppercase

        g = True

        while g == True:
            one = ''.join(choice(numbers) for i in range(5))
            two = ''.join(choice(letters) for i in range(1))
            ref = f"C-{two}{one}"
            g = self.client_exist(ref)
        
        return ref

   
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
        
        if self.ids.disc_inp.text == '':
            self.ids.disc_inp.text = '0'
        
        if self.ids.disc_perc_inp.text == '':
            self.ids.disc_perc_inp.text == '0'
        
        if float(self.ids.disc_inp.text) > float(self.ids.price_inp.text):
            self.error_popup("la remise ne peut pas être\nsupérieure au prix de vente")
            self.ids.disc_inp.focus = True
            return 0
        
        if int(self.ids.disc_perc_inp.text) > 100:
            self.error_popup("la remise ne peut pas être\nsupérieure à 100 %")
            self.ids.disc_perc_inp.focus = True
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
                self.error_popup("Champ Manquant")
                self.ids.price_inp.focus = True
                return 0
            else:
                self.error_popup("Entrée Invalide")
                return 0
        try:
            discount = float(self.ids.disc_inp.text)
        except:
            if self.ids.disc_inp.text == '':
                discount = 0  
            else:
                self.error_popup("Entrée Invalide")
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
        discount = discount + discount_per
        tvap = tva
        tva = (price-discount)*tva/100
        total = price-discount+tva
        
        
        
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
                    prdct.append(tvap)
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
                    prdct.append(tvap)
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
        
        #print(self.cartsummary)
        #print(total)
        self.ids.code_inp.text = ''
        self.ids.code_inp.focus = True
        #print("done")
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
        name = Label(text=designation, size_hint_x=.6, color=(0.678, 0, 0, 1), height=10)
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

        pprice = float(price.text)
        #self.total += pprice

        curprdct = self.ids.cur_product
        curprdct.text = pname

        curprdct = self.ids.cur_price
        curprdct.text = f'{pprice}'

        return 0


    def update_reciept(self):
        ttl = []
        tva = []
        preview = self.ids.receipt_preview
        #(ref, designation, quantity, discount, vat, price, totall)
        new = self.previewheader
        today = datetime.today().strftime("%d-%m-%Y")
        new = f"{new}\nReçu N°: {self.transaction_id}\nDate: {today}\n\n"
        for c, item in enumerate(self.purchases):
            #print(self.purchases)
            new = new + f"\n({c+1})\t" + str(item[1]).lower()+ "\n"
            new = f"{new}\n{str(item[0])}\t{str(float(item[5])-float(item[3]))}\tx\t{str(item[2])}\n"
            ttl.append(float(item[5])-float(item[3]))
            tva.append(float(item[6]))

        self.total = sum(ttl)
        new = new + "\n" + "\n" + F"Totale HT: {self.total}"
        new = new + "\n" + F"Totale TTC: {sum(tva)}"

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
        self.transaction_id = self.gen_transaction_ref()
        self.client_id = self.gen_client_ref()
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
        
        self.ids.rs.text = ''
        self.ids.rc.text = ''
        self.ids.idf.text = ''
        self.ids.ice.text = ''
        
        self.ids.code_inp.focus = True
        
        return 0
    
    
    def update_product(self, ref, price, minus, last_purchase):
        prdct = self.products.find({'Ref': f'{ref}'})
        prdct = prdct[0]
        if prdct['vendu'] == '':
            prdct['vendu'] = 0
        if prdct['en_stock'] == '':
            prdct['en_stock'] = 0
        new_en_stock = int(prdct['en_stock']) - int(minus)
        sold = int(prdct['vendu']) + int(minus)
        self.products.update_one({'Ref':ref}, {'$set':{'prix': price, 'en_stock': new_en_stock, 'vendu': sold, 'dernier_achat': last_purchase}})    
        return 0
    
    
    def validate_transaction(self):
        today = datetime.today().strftime("%d-%m-%Y")
        if len(self.purchases) < 1:
            self.error_popup("Le Panier est vide")
            self.clear()
            return 0
        positions = []
        item = {}
        
        
        #[ref, 'designation', quantity, réduction, tva, price, price-reduction+tva]
        sumht = []
        sumtva = []
        sumttc = []
        for element in self.purchases:
            item['ref'] = element[0]
            item['text'] = element[1]
            if element[2] == '' or '1':
                element[2] = 1
            item['amount'] = int(element[2])
            if element[7] == 0 or '':
                item['tax_rate'] = 0
            else:
                item['tax_rate'] = float(element[7])
            item['netto_price'] = float(float(element[5]))-int(float(element[3]))
            
            # calculate to add to transactions table
            
            httemp = item['netto_price']*item['amount']
            sumht.append(httemp)
            tvatemp = httemp*item['tax_rate']/100
            sumtva.append(tvatemp)
            sumttc.append(httemp+tvatemp)
            
            self.transactions.insert_one({'Ref': self.transaction_id, 'Totale_HT': sum(sumht), 'TVA': sum(sumtva), 'Totale_TTC': sum(sumttc), 'date': today})
            self.update_product(item['ref'], item['netto_price'], item['amount'], today)
            
            positions.append(item)
            item = {} 
        
        
        original_stdout = sys.stdout
        
        
        with open(f"./recu/{self.transaction_id}.txt", 'w') as txtfile:
            sys.stdout = txtfile
            print(self.ids.receipt_preview.text)
        
        
        
        if self.ids.rs.text != '':
            self.clients.insert_one({'Ref': self.client_id, 'RS': self.ids.rs.text, 'RC': self.ids.rc.text, 'IF': self.ids.idf.text, 'ICE': self.ids.ice.text, 'date': today})
            shutil.copy('./utils/data.yml', './documents/invoice/data.yml')
            with open("./documents/invoice/data.yml", 'a') as yamlfile:
                data = yaml.dump(positions, yamlfile)
                sys.stdout = yamlfile
                print("invoice:")
                print(f"  number: {self.transaction_id}")
                print(f"  date: {today}")
                print("\n")
                print(f'customer_number: {self.client_id}')
                print("\n")
                print("to:")
                print(f"    name: 'Raison Sociale: {self.ids.rs.text}'")
                print(f"    street: 'RC: {self.ids.rc.text}'")
                print(f"    postcode: 'IF: {self.ids.idf.text}'")
                print(f"    city: 'ICE: {self.ids.ice.text}'")
        
                os.system(f"wsl python3 buildpdf.py --output_pdf ./factures/{self.transaction_id}.pdf")
                os.startfile(f".\\factures\\{self.transaction_id}.pdf")
    
                #os.remove('./documents/invoice/data.yml')
        
        sys.stdout = original_stdout
        
        self.clear()
        
        self.success_popup("Transaction Enregistré")
        
        return 0
                         
        
class OperateurApp(App):
    def build(self):
        return OperateurWindow()

if __name__=="__main__":
    oa = OperateurApp()
    oa.run()
