from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from pymongo import MongoClient
from utils.datatable import DataTable
from datetime import datetime
import hashlib
import openpyxl
import tkinter.filedialog
from datetime import datetime
from  random import choice
from string import digits, ascii_uppercase
from pandas import read_excel
from PIL import ImageFont, ImageDraw
import PIL.Image
import qrcode
import os



# TIDY UP CODE BY SCREEN


class AdminWindow(BoxLayout):
    # Add screen size to get_products
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        client = MongoClient()
        db = client.pos
        self.users = db.users
        self.products = db.stocks
        
        # display users
        content = self.ids.scrn_contents
        users = self.get_users()
        usertable  = DataTable(table=users)
        content.add_widget(usertable)
        
        # display products
        product_scrn = self.ids.scrn_product_contents
        products = self.get_products()
        prod_table  = DataTable(table=products)
        product_scrn.add_widget(prod_table)
        
        #scrn_order_content
        order_scrn = self.ids.scrn_order_contents
        products = self.get_products()
        prod_table  = DataTable(table=products)
        order_scrn.add_widget(prod_table)
        
        #scrn_search_content
        search_scrn = self.ids.scrn_search_contents
        products = self.get_products()
        prod_table  = DataTable(table=products)
        search_scrn.add_widget(prod_table)
        
        # scrn_supplier_contents
        supplier_scrn = self.ids.scrn_supplier_contents
        products = self.get_products()
        prod_table  = DataTable(table=products)
        supplier_scrn.add_widget(prod_table)
        
 
    def calculate_price(self):
        purchase = self.ids.purchase_price_calc.text
        transport = self.ids.transport_calc.text
        douane = self.ids.douane_calc.text
        transitaire = self.ids.transitaire_calc.text
        autres = self.ids.autres_calc.text
        nbr = self.ids.nbr_prdct_calc.text
        if purchase == '':
            self.error_popup('le champ "Prix D\'achat" manquant')
            return 0
        if nbr == '':
            self.error_popup('le champ "Nombre des Produits" manquant')
            return 0
        if transport == '':
            self.ids.transport_calc.text = "0"
            transport = 0
        if douane == '':
            self.ids.douane_calc.text = "0"
            douane = 0
        if transitaire == '':
            self.ids.transitaire_calc.text = "0"
            transitaire = 0
        if autres == '':
            self.ids.autres_calc.text = "0"
            autres = 0
        try:
            somme = float(purchase)+float(transport)+float(douane)+float(transitaire)+float(autres)
        except ValueError:
            self.error_popup("Entrée invalide")
            return 0
        result = somme/int(nbr)
        result = "{:.2f}".format(result)
        self.ids.result_calc.text = f"Résultat: {result} DH PAR PRODUIT"
        
        return 0
    
    
    def clear_calc(self):
        self.ids.purchase_price_calc.text = ''
        self.ids.transport_calc.text = ''
        self.ids.douane_calc.text = ''
        self.ids.transitaire_calc.text = ''
        self.ids.autres_calc.text = ''
        self.ids.nbr_prdct_calc.text = ''
        self.ids.result_calc.text = "Résultat: "
        
        return 0
    
             
    def create_label(self, ref):
        path = tkinter.filedialog.askdirectory()
        product = self.products.find({"Ref": f"{ref}"})
        try:
            product = product[0]
        except IndexError:
            self.error_popup("Référence Invalide")
            return 0
        prix = product['prix']
        marque = product['marque']
        modele = product['modele']
        cpu = product['cpu']
        ram = product['ram']
        stockage = product['stockage']
        gpu = product['gpu']
        batterie = product['batterie']
        commande = product['commande']

        font = ImageFont.truetype("Montserrat-Regular.ttf", 35)
        font2 = ImageFont.truetype("Montserrat-Regular.ttf", 54)

        img = PIL.Image.open("./utils/Label.jpg")

        draw = ImageDraw.Draw(img)

        draw.text((185, 547),f"{ref} | {prix} DH",(0,0,0),font=font2)

        draw.text((397, 1150),f"{marque} {modele}",(0,0,0),font=font)
        draw.text((397, 1224),f"{cpu}",(0,0,0),font=font)
        draw.text((397, 1298),f"{ram}",(0,0,0),font=font)
        draw.text((397, 1372),f"{stockage}",(0,0,0),font=font)
        draw.text((397, 1446),f"{gpu}",(0,0,0),font=font)
        draw.text((397, 1520),f"{batterie}",(0,0,0),font=font)
        draw.text((397, 1594),f"{commande}",(0,0,0),font=font)

        Logo_link = './utils/logo.jpg'

        logo = PIL.Image.open(Logo_link)    

        basewidth = 100 

        wpercent = (basewidth/float(logo.size[0]))
        hsize = int((float(logo.size[1])*float(wpercent)))
        logo = logo.resize((basewidth, hsize), PIL.Image.Resampling.LANCZOS)
        QRcode = qrcode.QRCode( 
	    error_correction=qrcode.constants.ERROR_CORRECT_H
        )
        
        QRcode.add_data(ref)    
        QRcode.make()
        QRcolor = '#000000'
        QRimg = QRcode.make_image(
        	fill_color=QRcolor, back_color="white").convert('RGB')

        QRimg = QRimg.resize((420, 420), PIL.Image.Resampling.NEAREST)
        pos = ((QRimg.size[0] - logo.size[0]) // 2,
        	(QRimg.size[1] - logo.size[1]) // 2)
        QRimg.paste(logo, pos)        
        img.paste(QRimg, (390, 680))

        img.save(f"{path}/{ref}.pdf")
        os.startfile(f"{path}/{ref}.pdf")
        return 0


    def create_order_labels(self, order):
        if order == '':
            return 0
        comm = self.products.find({"commande": f"{order}"})
        try:
            comm = comm[0]
            del(comm)
        except IndexError:
            return 0

        path = tkinter.filedialog.askdirectory()
        if path == '':
            return 0

        font = ImageFont.truetype("Montserrat-Regular.ttf", 35)
        font2 = ImageFont.truetype("Montserrat-Regular.ttf", 54)
        img = PIL.Image.open("./utils/Label.jpg")
        Logo_link = './utils/logo.jpg'
        images = []
        for product in self.products.find({"commande": f"{order}"}):
            ref = product['Ref']
            prix = product['prix']
            marque = product['marque']
            modele = product['modele']
            cpu = product['cpu']
            ram = product['ram']
            stockage = product['stockage']
            gpu = product['gpu']
            batterie = product['batterie']
            commande = product['commande']

            draw = ImageDraw.Draw(img)
            draw.text((185, 547),f"{ref} | {prix} DH",(0,0,0),font=font2)
            draw.text((397, 1150),f"{marque} {modele}",(0,0,0),font=font)
            draw.text((397, 1224),f"{cpu}",(0,0,0),font=font)
            draw.text((397, 1298),f"{ram}",(0,0,0),font=font)
            draw.text((397, 1372),f"{stockage}",(0,0,0),font=font)
            draw.text((397, 1446),f"{gpu}",(0,0,0),font=font)
            draw.text((397, 1520),f"{batterie}",(0,0,0),font=font)
            draw.text((397, 1594),f"{commande}",(0,0,0),font=font)

            logo = PIL.Image.open(Logo_link)    
            basewidth = 100 
            wpercent = (basewidth/float(logo.size[0]))
            hsize = int((float(logo.size[1])*float(wpercent)))
            logo = logo.resize((basewidth, hsize), PIL.Image.Resampling.LANCZOS)
            QRcode = qrcode.QRCode( 
            error_correction=qrcode.constants.ERROR_CORRECT_H
            )   
            QRcode.add_data(ref)    
            QRcode.make()
            QRcolor = '#000000'
            QRimg = QRcode.make_image(
                fill_color=QRcolor, back_color="white").convert('RGB')
            QRimg = QRimg.resize((420, 420), PIL.Image.Resampling.NEAREST)
            pos = ((QRimg.size[0] - logo.size[0]) // 2,
                (QRimg.size[1] - logo.size[1]) // 2)
            QRimg.paste(logo, pos)        
            img.paste(QRimg, (390, 680))
            images.append(img)
            img = PIL.Image.open("./utils/Label.jpg")

        images[0].save(
            f"{path}/{order}.pdf", "PDF" ,resolution=300.0, save_all=True, append_images=images[1:]
        )
        
        os.startfile(f"{path}/{order}.pdf")
        self.success_popup("Tickets Générées")
        return 0


    def get_order(self):
        orderref = self.ids.order_id.text
        if orderref == '':
            return 0
        
        stats = self.ids.scrn_order_stats
        order_scrn = self.ids.scrn_order_contents
        order_scrn.clear_widgets()
        stats.clear_widgets()
        
        _stocks = {}
        _stocks['Ref'] = {}
        _stocks['designation'] = {}
        _stocks['prix'] = {}
        _stocks['prix_achat'] = {}
        _stocks['en_stock'] = {}
        _stocks['vendu'] = {}
        _stocks['commande'] = {}
        _stocks['fournisseur'] = {}
        _stocks['dernier_achat'] = {}
        _stocks['commentaire'] = {}
        Ref = []
        prix = []
        prix_achat = []
        marque = []
        modele = []
        cpu = []
        ram = []
        gpu = []
        stockage = []
        batterie = []
        en_stock = []
        vendu = []
        commande = []
        fournisseur = []
        dernier_achat = []
        commentaire = []
        
        for product in self.products.find({"commande": f"{orderref}"}):
            Ref.append(product['Ref'])
            prix.append(float(product['prix']))

            try:
                prix_achat.append(float(product['prix_achat']))
            except KeyError:
                prix_achat.append(0)

            marque.append(product['marque'])
            modele.append(product['modele'])
            cpu.append(product['cpu'])
            ram.append(product['ram'])
            gpu.append(product['gpu'])
            stockage.append(product['stockage'])
            batterie.append(product['batterie'])

            try:    
                en_stock.append(product['en_stock'])
            except KeyError:
                en_stock.append('')

            try:    
                vendu.append(product['vendu'])
            except KeyError:
                vendu.append('')

            commande.append(product['commande'])
            
            try:    
                fournisseur.append(product['fournisseur'])
            except KeyError:
                fournisseur.append('')

            try:    
                dernier_achat.append(product['dernier_achat'])
            except KeyError:
                dernier_achat.append('')
                
            try:    
                commentaire.append(product['commentaire'])
            except KeyError:
                commentaire.append('')

        sum_purchase_price = []
        sum_sold_list = []
        sold_items = []
        in_stock_items = []
        in_stock_items_price = []
        
        for c, v in enumerate(Ref):
            if int(vendu[c]) >= 1:
                sum_sold_list.append(int(vendu[c])*float(prix[c]))
                sold_items.append(int(vendu[c]))
                sum_purchase_price.append(int(vendu[c])*float(prix_achat[c]))
            
            if int(en_stock[c]) >= 1:
                in_stock_items_price.append(int(en_stock[c])*float(prix_achat[c]))
                in_stock_items.append(int(en_stock[c]))
                sum_purchase_price.append(int(en_stock[c])*float(prix_achat[c]))
            
            _stocks['Ref'][c] = Ref[c]
            _stocks['designation'][c] = f"{marque[c]} {modele[c]} | {cpu[c]} | {ram[c]}GB\n{stockage[c]} | {gpu[c]} | {batterie[c]}"
            _stocks['prix'][c] = prix[c]
            _stocks['prix_achat'][c] = prix_achat[c]
            _stocks['en_stock'][c] = en_stock[c]
            _stocks['vendu'][c] = vendu[c]
            _stocks['commande'][c] = commande[c]
            _stocks['fournisseur'][c] = fournisseur[c]
            _stocks['dernier_achat'][c] = dernier_achat[c]
            _stocks['commentaire'][c] = commentaire[c]
        
        products = _stocks
        prod_table  = DataTable(table=products)
        order_scrn.add_widget(prod_table)
        
        # key numbers
        total_order_price = sum(sum_purchase_price)
        in_stock_items = sum(in_stock_items)
        in_stock_items_price = sum(in_stock_items_price)
        sold_items = sum(sold_items)
        sold_products_price = float(sum(sum_sold_list))
        profit = sold_products_price-total_order_price
        
        totalorderpricelabel = Label(text=f'Prix Du Commande:\n{total_order_price}', bold=True, color=(0,0,0,1))
        instockitemslabel = Label(text=f'Produits en stock:\n{in_stock_items}', bold=True, color=(0,0,0,1))
        instockitemspricelabel = Label(text=f'Prix des produits en stock:\n{in_stock_items_price}', bold=True, color=(0,0,0,1))
        solditemslabel = Label(text=f'Produits Vendu:\n{sold_items}', bold=True, color=(0,0,0,1))
        soldproductspricelabel = Label(text=f'Prix des produits Vendu:\n{sold_products_price}', bold=True, color=(0,0,0,1))
        profitlabel = Label(text=f'Profit:\n{profit}', bold=True, color=(0,0,0,1))
        
        stats.add_widget(totalorderpricelabel)
        stats.add_widget(instockitemslabel)
        stats.add_widget(instockitemspricelabel)
        stats.add_widget(solditemslabel)
        stats.add_widget(soldproductspricelabel)
        stats.add_widget(profitlabel)
        
        return _stocks


    def get_supp(self):
        supp = self.ids.supplier_id.text
        if supp == '':
            return 0
        
        stats = self.ids.scrn_supplier_stats
        order_scrn = self.ids.scrn_supplier_contents
        order_scrn.clear_widgets()
        stats.clear_widgets()
        
        _stocks = {}
        _stocks['Ref'] = {}
        _stocks['designation'] = {}
        _stocks['prix'] = {}
        _stocks['prix_achat'] = {}
        _stocks['en_stock'] = {}
        _stocks['vendu'] = {}
        _stocks['commande'] = {}
        _stocks['fournisseur'] = {}
        _stocks['dernier_achat'] = {}
        _stocks['commentaire'] = {}
        Ref = []
        prix = []
        prix_achat = []
        marque = []
        modele = []
        cpu = []
        ram = []
        gpu = []
        stockage = []
        batterie = []
        en_stock = []
        vendu = []
        commande = []
        fournisseur = []
        dernier_achat = []
        commentaire = []
        
        for product in self.products.find({"fournisseur": f"{supp}"}):
            Ref.append(product['Ref'])
            prix.append(float(product['prix']))

            try:
                prix_achat.append(float(product['prix_achat']))
            except KeyError:
                prix_achat.append(0)

            marque.append(product['marque'])
            modele.append(product['modele'])
            cpu.append(product['cpu'])
            ram.append(product['ram'])
            gpu.append(product['gpu'])
            stockage.append(product['stockage'])
            batterie.append(product['batterie'])

            try:    
                en_stock.append(product['en_stock'])
            except KeyError:
                en_stock.append('')

            try:    
                vendu.append(product['vendu'])
            except KeyError:
                vendu.append('')

            commande.append(product['commande'])
            
            try:    
                fournisseur.append(product['fournisseur'])
            except KeyError:
                fournisseur.append('')

            try:    
                dernier_achat.append(product['dernier_achat'])
            except KeyError:
                dernier_achat.append('')
                
            try:    
                commentaire.append(product['commentaire'])
            except KeyError:
                commentaire.append('')

        sum_purchase_price = []
        sum_sold_list = []
        sold_items = []
        in_stock_items = []
        in_stock_items_price = []
        
        for c, v in enumerate(Ref):
            if int(vendu[c]) >= 1:
                sum_sold_list.append(int(vendu[c])*float(prix[c]))
                sold_items.append(int(vendu[c]))
                sum_purchase_price.append(int(vendu[c])*float(prix_achat[c]))
            
            if int(en_stock[c]) >= 1:
                in_stock_items_price.append(int(en_stock[c])*float(prix_achat[c]))
                in_stock_items.append(int(en_stock[c]))
                sum_purchase_price.append(int(en_stock[c])*float(prix_achat[c]))
            
            _stocks['Ref'][c] = Ref[c]
            _stocks['designation'][c] = f"{marque[c]} {modele[c]} | {cpu[c]} | {ram[c]}GB\n{stockage[c]} | {gpu[c]} | {batterie[c]}"
            _stocks['prix'][c] = prix[c]
            _stocks['prix_achat'][c] = prix_achat[c]
            _stocks['en_stock'][c] = en_stock[c]
            _stocks['vendu'][c] = vendu[c]
            _stocks['commande'][c] = commande[c]
            _stocks['fournisseur'][c] = fournisseur[c]
            _stocks['dernier_achat'][c] = dernier_achat[c]
            _stocks['commentaire'][c] = commentaire[c]
        
        products = _stocks
        prod_table  = DataTable(table=products)
        order_scrn.add_widget(prod_table)
        
        # key numbers
        total_order_price = sum(sum_purchase_price)
        in_stock_items = sum(in_stock_items)
        in_stock_items_price = sum(in_stock_items_price)
        sold_items = sum(sold_items)
        sold_products_price = float(sum(sum_sold_list))
        profit = sold_products_price-total_order_price
        
        totalorderpricelabel = Label(text=f'Importé depuis ce fournisseur:\n{total_order_price} DH', bold=True, color=(0,0,0,1))
        instockitemslabel = Label(text=f'Produits en stock:\n{in_stock_items}', bold=True, color=(0,0,0,1))
        instockitemspricelabel = Label(text=f'Prix des produits en stock:\n{in_stock_items_price} DH', bold=True, color=(0,0,0,1))
        solditemslabel = Label(text=f'Produits Vendu:\n{sold_items}', bold=True, color=(0,0,0,1))
        soldproductspricelabel = Label(text=f'Prix des produits Vendu:\n{sold_products_price} DH', bold=True, color=(0,0,0,1))
        profitlabel = Label(text=f'Profit:\n{profit}', bold=True, color=(0,0,0,1))
        
        stats.add_widget(totalorderpricelabel)
        stats.add_widget(instockitemslabel)
        stats.add_widget(instockitemspricelabel)
        stats.add_widget(solditemslabel)
        stats.add_widget(soldproductspricelabel)
        stats.add_widget(profitlabel)
        
        return _stocks


    def get_product(self):
        orderref = self.ids.prod_id.text
        if orderref == '':
            return 0
        
        order_scrn = self.ids.scrn_search_contents
        order_scrn.clear_widgets()
        
        _stocks = {}
        _stocks['Ref'] = {}
        _stocks['designation'] = {}
        _stocks['prix'] = {}
        _stocks['prix_achat'] = {}
        _stocks['en_stock'] = {}
        _stocks['vendu'] = {}
        _stocks['commande'] = {}
        _stocks['fournisseur'] = {}
        _stocks['dernier_achat'] = {}
        _stocks['commentaire'] = {}
        Ref = []
        prix = []
        prix_achat = []
        marque = []
        modele = []
        cpu = []
        ram = []
        gpu = []
        stockage = []
        batterie = []
        en_stock = []
        vendu = []
        commande = []
        fournisseur = []
        dernier_achat = []
        commentaire = []
        for product in self.products.find({"Ref": f"{orderref}"}):
            Ref.append(product['Ref'])
            prix.append(product['prix'])

            try:
                prix_achat.append(product['prix_achat'])
            except KeyError:
                prix_achat.append('')

            marque.append(product['marque'])
            modele.append(product['modele'])
            cpu.append(product['cpu'])
            ram.append(product['ram'])
            gpu.append(product['gpu'])
            stockage.append(product['stockage'])
            batterie.append(product['batterie'])

            try:    
                en_stock.append(product['en_stock'])
            except KeyError:
                en_stock.append('')

            try:    
                vendu.append(product['vendu'])
            except KeyError:
                vendu.append('')

            commande.append(product['commande'])
            
            try:    
                fournisseur.append(product['fournisseur'])
            except KeyError:
                fournisseur.append('')

            try:    
                dernier_achat.append(product['dernier_achat'])
            except KeyError:
                dernier_achat.append('')
                
            try:    
                commentaire.append(product['commentaire'])
            except KeyError:
                commentaire.append('')

        for c, v in enumerate(Ref):
            _stocks['Ref'][c] = Ref[c]
            _stocks['designation'][c] = f"{marque[c]} {modele[c]} | {cpu[c]} | {ram[c]}GB\n{stockage[c]} | {gpu[c]} | {batterie[c]}"
            _stocks['prix'][c] = prix[c]
            _stocks['prix_achat'][c] = prix_achat[c]
            _stocks['en_stock'][c] = en_stock[c]
            _stocks['vendu'][c] = vendu[c]
            _stocks['commande'][c] = commande[c]
            _stocks['fournisseur'][c] = fournisseur[c]
            _stocks['dernier_achat'][c] = dernier_achat[c]
            _stocks['commentaire'][c] = commentaire[c]

        
        products = _stocks
        prod_table  = DataTable(table=products)
        order_scrn.add_widget(prod_table)
        
        return _stocks

    
    def missing_field_popup(self, field):
            box = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)        
            error_img = Image(source='./utils/1.png', size=(150, 150))
            error_msg = Label(text=f'champ obligatoire ({field}) manquant', bold=True)
            
            
            popup = ModalView(size_hint=(None, None), size=(400, 300))
            box.add_widget(error_img)
            box.add_widget(error_msg)
            
            popup.add_widget(box)
            
            popup.open()
            
            return 0
    
    
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


    def add_print_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
        crud_ref = TextInput(hint_text="Référence", multiline=False, width=100, height=10)
        crud_submit =  Button(text='Imprimer Le Ticket', size_hint_x=None, width=150, background_color=(0.184, 0.216, 0.231), background_normal='',
                            on_release=lambda x: self.create_label(crud_ref.text))
        crud_close =  Button(text='Fermer', size_hint_x=None, width=100, on_release=lambda x: self.ids.ops_fields_p.clear_widgets(),
                            background_color=(0.184, 0.216, 0.231), background_normal='')
        spacer = Label(text='', size_hint_x=.6)
        target.add_widget(crud_ref)
        target.add_widget(crud_submit)
        target.add_widget(crud_close)
        target.add_widget(spacer)
        

    def gen_ref(self, marque):
        numbers = digits
        letters = ascii_uppercase

        g = True

        while g == True:
            one = ''.join(choice(numbers) for i in range(4))
            two = ''.join(choice(letters) for i in range(1))
            ref = f"{marque[:3]}-{one}{two}"
            g = self.product_exist(ref)
        
        return ref
    

    def export_order_xlsx(self, enstock=False):
        orderref = self.ids.order_id.text
        if orderref == '':
            return 0
        
        path = tkinter.filedialog.askdirectory()
        if path == '':
            return 0
        
        
        _stocks = {}

        _stocks['Ref'] = {}
        _stocks['marque'] = {}
        _stocks['modele'] = {}
        _stocks['cpu'] = {}
        _stocks['ram'] = {}
        _stocks['stockage'] = {}
        _stocks['gpu'] = {}
        _stocks['batterie'] = {}
        _stocks['prix'] = {}
        _stocks['prix_achat'] = {}
        _stocks['en_stock'] = {}
        _stocks['vendu'] = {}
        _stocks['commande'] = {}
        _stocks['dernier_achat'] = {}

        Ref = []
        prix = []
        prix_achat = []
        marque = []
        modele = []
        cpu = []
        ram = []
        gpu = []
        stockage = []
        batterie = []
        en_stock = []
        vendu = []
        commande = []
        dernier_achat = []

        for product in self.products.find():
            Ref.append(product['Ref'])
            prix.append(product['prix'])
            try:
                prix_achat.append(product['prix_achat'])
            except KeyError:
                prix_achat.append('')
            marque.append(product['marque'])
            modele.append(product['modele'])
            cpu.append(product['cpu'])
            ram.append(product['ram'])
            gpu.append(product['gpu'])
            stockage.append(product['stockage'])
            batterie.append(product['batterie'])
            try:    
                en_stock.append(product['en_stock'])
            except KeyError:
                en_stock.append('')

            try:    
                vendu.append(product['vendu'])
            except KeyError:
                vendu.append('')

            commande.append(product['commande'])

            try:    
                dernier_achat.append(product['dernier_achat'])
            except KeyError:
                dernier_achat.append('')


        for c, v in enumerate(Ref):
            _stocks['Ref'][c] = Ref[c]

            _stocks['modele'][c] = modele[c]
            _stocks['marque'][c] = marque[c]
            _stocks['cpu'][c] = cpu[c]
            _stocks['ram'][c] = ram[c]
            _stocks['stockage'][c] = stockage[c]
            _stocks['gpu'][c] = gpu[c]
            _stocks['batterie'][c] = batterie[c]

            _stocks['prix'][c] = prix[c]
            _stocks['prix_achat'][c] = prix_achat[c]
            _stocks['en_stock'][c] = en_stock[c]
            _stocks['vendu'][c] = vendu[c]
            _stocks['commande'][c] = commande[c]
            _stocks['dernier_achat'][c] = dernier_achat[c]

        titles = _stocks.keys()
        titles = list(titles)

        titles2 = ['Réf', 'Marque', 'Modèle', 'CPU', 'RAM', 'Stockage', 'GPU', 'Batterie',
            'Prix', "Prix d'achat", 'En Stock', 'Vendu', 'Commande', 'Dernier Achat']

        product = []
        all_products = []

        for c, v in enumerate(_stocks['Ref']):
            product.append(_stocks[titles[0]][c])
            product.append(_stocks[titles[1]][c])
            product.append(_stocks[titles[2]][c])
            product.append(_stocks[titles[3]][c])
            product.append(_stocks[titles[4]][c])
            product.append(_stocks[titles[5]][c])
            product.append(_stocks[titles[6]][c])
            product.append(_stocks[titles[7]][c])
            product.append(_stocks[titles[8]][c])
            product.append(_stocks[titles[9]][c])
            product.append(int(_stocks[titles[10]][c]))
            product.append(_stocks[titles[11]][c])
            product.append(_stocks[titles[12]][c])
            product.append(_stocks[titles[13]][c])
            all_products.append(product)
            product = []


        if enstock == True:   
            filename = f'/en-stock-{orderref}-'
            filtered = []
            for i in all_products:
                if int(i[10]) >= 1 and i[12] == orderref:
                    filtered.append(i)
            all_products = filtered
        else:
            filtered = []
            for i in all_products:
                if i[12] == orderref:
                    filtered.append(i)
            all_products = filtered
            filename = f'/tous-{orderref}-'

        all_products.insert(0, titles2)

        wb = openpyxl.Workbook()
        ws_write = wb.worksheets[0]

        for p in all_products:
            ws_write.append(p)

        today = datetime.today().strftime("%d-%m-%Y")
        wb.save(filename=f'{path}{filename}{today}.xlsx')
        
        if enstock:
            self.success_popup('les produits en stock ont été exportés')
        else:
            self.success_popup('Tous les produits ont été exportés')
        
        return 0


    def rt_xlsx(self, enstock=False):
        path = tkinter.filedialog.askdirectory()
        if path == '':
            return 0
        
        _stocks = {}

        _stocks['Ref'] = {}
        _stocks['marque'] = {}
        _stocks['modele'] = {}
        _stocks['cpu'] = {}
        _stocks['ram'] = {}
        _stocks['stockage'] = {}
        _stocks['gpu'] = {}
        _stocks['batterie'] = {}
        _stocks['prix'] = {}
        _stocks['prix_achat'] = {}
        _stocks['en_stock'] = {}
        _stocks['vendu'] = {}
        _stocks['commande'] = {}
        _stocks['dernier_achat'] = {}

        Ref = []
        prix = []
        prix_achat = []
        marque = []
        modele = []
        cpu = []
        ram = []
        gpu = []
        stockage = []
        batterie = []
        en_stock = []
        vendu = []
        commande = []
        dernier_achat = []

        for product in self.products.find():
            Ref.append(product['Ref'])
            prix.append(product['prix'])
            try:
                prix_achat.append(product['prix_achat'])
            except KeyError:
                prix_achat.append('')
            marque.append(product['marque'])
            modele.append(product['modele'])
            cpu.append(product['cpu'])
            ram.append(product['ram'])
            gpu.append(product['gpu'])
            stockage.append(product['stockage'])
            batterie.append(product['batterie'])
            try:    
                en_stock.append(product['en_stock'])
            except KeyError:
                en_stock.append('')
    
            try:    
                vendu.append(product['vendu'])
            except KeyError:
                vendu.append('')

            commande.append(product['commande'])

            try:    
                dernier_achat.append(product['dernier_achat'])
            except KeyError:
                dernier_achat.append('')


        for c, v in enumerate(Ref):
            _stocks['Ref'][c] = Ref[c]

            _stocks['modele'][c] = modele[c]
            _stocks['marque'][c] = marque[c]
            _stocks['cpu'][c] = cpu[c]
            _stocks['ram'][c] = ram[c]
            _stocks['stockage'][c] = stockage[c]
            _stocks['gpu'][c] = gpu[c]
            _stocks['batterie'][c] = batterie[c]

            _stocks['prix'][c] = prix[c]
            _stocks['prix_achat'][c] = prix_achat[c]
            _stocks['en_stock'][c] = en_stock[c]
            _stocks['vendu'][c] = vendu[c]
            _stocks['commande'][c] = commande[c]
            _stocks['dernier_achat'][c] = dernier_achat[c]

        titles = _stocks.keys()
        titles = list(titles)

        titles2 = ['Réf', 'Marque', 'Modèle', 'CPU', 'RAM', 'Stockage', 'GPU', 'Batterie',
            'Prix', "Prix d'achat", 'En Stock', 'Vendu', 'Commande', 'Dernier Achat']

        product = []
        all_products = []

        for c, v in enumerate(_stocks['Ref']):
            product.append(_stocks[titles[0]][c])
            product.append(_stocks[titles[1]][c])
            product.append(_stocks[titles[2]][c])
            product.append(_stocks[titles[3]][c])
            product.append(_stocks[titles[4]][c])
            product.append(_stocks[titles[5]][c])
            product.append(_stocks[titles[6]][c])
            product.append(_stocks[titles[7]][c])
            product.append(_stocks[titles[8]][c])
            product.append(_stocks[titles[9]][c])
            product.append(int(_stocks[titles[10]][c]))
            product.append(_stocks[titles[11]][c])
            product.append(_stocks[titles[12]][c])
            product.append(_stocks[titles[13]][c])
            all_products.append(product)
            product = []
            
        if enstock == True:   
            filename = '/en-stock-'
            filtered = []
            for i in all_products:
                if int(i[10]) >= 1:
                    filtered.append(i)
            all_products = filtered
        else:
            filename = '/tous-'

        all_products.insert(0, titles2)

        wb = openpyxl.Workbook()
        ws_write = wb.worksheets[0]

        for p in all_products:
            ws_write.append(p)

        today = datetime.today().strftime("%d-%m-%Y")
        wb.save(filename=f'{path}{filename}{today}.xlsx')
        
        if enstock:
            self.success_popup('les produits en stock ont été exportés')
        else:
            self.success_popup('Tous les produits ont été exportés')
        
        return 0


    def import_xlsx(self):
        path = tkinter.filedialog.askopenfilename(initialdir="/", title="Sélectionnez un fichier Excel",
                                                filetypes=[("Fichiers Excel", ".xlsx")])
        if path == '':
            return 0
        
        
        order_scrn = self.ids.scrn_order_contents
        order_scrn.clear_widgets()
        content = self.ids.scrn_product_contents
        content.clear_widgets()
        
        
        df = read_excel(path)

        df['gpu'] = df['gpu'].fillna('STANDARD')
        df['prix_achat'] = df['prix_achat'].fillna(0)
        df['vendu'] = df['vendu'].fillna(0)
        df['dernier_achat'] = df['dernier_achat'].fillna('N/A')
        df['batterie'] = df['batterie'].fillna('Bien')

        data = df.to_dict(orient="records")

        for record in data:
            record['Ref'] = self.gen_ref(record['marque'])

        self.products.insert_many(data)
        
        products = self.get_products()
        product_table  = DataTable(table=products)
        product_table2  = DataTable(table=products)
        content.add_widget(product_table)
        order_scrn.add_widget(product_table2)
        
        self.success_popup(f"{len(data)} Produits Importés")

        return 0
    
    
    def product_exist(self, ref):
        i = 0
        product = self.products.find({'Ref': f'{ref}'})
        try:
            product = product[0]
            return True 
        except IndexError:
            return False 


    def user_exist(self, username):
        users = self.users
        i = 0
        for p in users.find():
            if p['user_name'] == f"{username}":
                i += 1
        if i == 0:
            return False
        else:
            return True
    
    
    def get_users(self):
        users = self.users
        
        _users = {}
        _users['first_names'] = {}
        _users['last_names'] = {}
        _users['user_names'] = {}
        _users['passwords'] = {}
        _users['designations'] = {}
        
        first_names = []
        last_names = []
        user_names = []
        passwords = []
        designations = []

        for user in users.find():
            first_names.append(user['first_name'])
            last_names.append(user['last_name'])
            user_names.append(user['user_name'])
            pwd = user['password']
            if len(pwd) > 10:
                pwd  = f"{pwd[:10]}..."
            passwords.append(pwd)
            designations.append(user['designation'])

        for c, v in enumerate(first_names):
            _users['first_names'][c] = first_names[c]
            _users['last_names'][c] = last_names[c]
            _users['user_names'][c] = user_names[c]
            _users['passwords'][c] = passwords[c]
            _users['designations'][c] = designations[c]
        return _users

    
    def get_products(self):
        products = self.products
        
        stats = self.ids.scrn_product_stats
        stats.clear_widgets()
        
        _stocks = {}
        _stocks['Ref'] = {}
        _stocks['designation'] = {}
        _stocks['prix'] = {}
        _stocks['prix_achat'] = {}
        _stocks['en_stock'] = {}
        _stocks['vendu'] = {}
        _stocks['commande'] = {}
        _stocks['fournisseur'] = {}
        _stocks['dernier_achat'] = {}
        _stocks['commentaire'] = {}

        Ref = []
        prix = []
        prix_achat = []
        marque = []
        modele = []
        cpu = []
        ram = []
        gpu = []
        stockage = []
        batterie = []
        en_stock = []
        vendu = []
        commande = []
        fournisseur = []
        dernier_achat = []
        commentaire = []

        for product in products.find():
            Ref.append(product['Ref'])
            prix.append(product['prix'])
            try:
                prix_achat.append(product['prix_achat'])
            except KeyError:
                prix_achat.append('')
            marque.append(product['marque'])
            modele.append(product['modele'])
            cpu.append(product['cpu'])
            ram.append(product['ram'])
            gpu.append(product['gpu'])
            stockage.append(product['stockage'])
            batterie.append(product['batterie'])
            try:    
                en_stock.append(product['en_stock'])
            except KeyError:
                en_stock.append('')
            
            try:    
                vendu.append(product['vendu'])
            except KeyError:
                vendu.append('')
            
            commande.append(product['commande'])
            
            try:    
                fournisseur.append(product['fournisseur'])
            except KeyError:
                fournisseur.append('')
            
            try:    
                dernier_achat.append(product['dernier_achat'])
            except KeyError:
                dernier_achat.append('')
                
            try:    
                commentaire.append(product['commentaire'])
            except KeyError:
                commentaire.append('****')
                
        sum_purchase_price = []
        sum_sold_list = []
        sold_items = []
        in_stock_items = []
        in_stock_items_price = []
                        
        for c, v in enumerate(Ref):
            _stocks['Ref'][c] = Ref[c]
            _stocks['designation'][c] = f"{marque[c]} {modele[c]} | {cpu[c]} | {ram[c]}GB\n{stockage[c]} | {gpu[c]} | {batterie[c]}"
            _stocks['prix'][c] = prix[c]
            _stocks['prix_achat'][c] = prix_achat[c]
            _stocks['en_stock'][c] = en_stock[c]
            _stocks['vendu'][c] = vendu[c]
            _stocks['commande'][c] = commande[c]
            _stocks['dernier_achat'][c] = dernier_achat[c]
            _stocks['commentaire'][c] = commentaire[c]
            _stocks['fournisseur'][c] = fournisseur[c]
            
            if vendu[c] == '':
                vendu[c] = 0
            if int(vendu[c]) >= 1:
                sum_sold_list.append(int(vendu[c])*float(prix[c]))
                sold_items.append(int(vendu[c]))
                sum_purchase_price.append(int(vendu[c])*float(prix_achat[c]))
            
            if int(en_stock[c]) >= 1:
                in_stock_items_price.append(int(en_stock[c])*float(prix_achat[c]))
                in_stock_items.append(int(en_stock[c]))
                sum_purchase_price.append(int(en_stock[c])*float(prix_achat[c]))

        # key numbers
        total_order_price = sum(sum_purchase_price)
        in_stock_items = sum(in_stock_items)
        in_stock_items_price = sum(in_stock_items_price)
        sold_items = sum(sold_items)
        sold_products_price = float(sum(sum_sold_list))
        profit = sold_products_price-total_order_price
        
        totalorderpricelabel = Label(text=f'Prix Totale:\n{total_order_price} DH', bold=True, color=(0,0,0,1))
        instockitemslabel = Label(text=f'Produits en stock:\n{in_stock_items}', bold=True, color=(0,0,0,1))
        instockitemspricelabel = Label(text=f'Prix des produits en stock:\n{in_stock_items_price} DH', bold=True, color=(0,0,0,1))
        solditemslabel = Label(text=f'Produits Vendu:\n{sold_items}', bold=True, color=(0,0,0,1))
        soldproductspricelabel = Label(text=f'Prix des produits Vendu:\n{sold_products_price} DH', bold=True, color=(0,0,0,1))
        profitlabel = Label(text=f'Profit:\n{profit} DH', bold=True, color=(0,0,0,1))
        
        stats.add_widget(totalorderpricelabel)
        stats.add_widget(instockitemslabel)
        stats.add_widget(instockitemspricelabel)
        stats.add_widget(solditemslabel)
        stats.add_widget(soldproductspricelabel)
        stats.add_widget(profitlabel)
        
        return _stocks
    
    
    def export_excel_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
        

        crud_export_instock =  Button(text='Exporter Les Produits En Stock', size_hint_x=1/8, width=100,
                                    on_release=lambda x: self.export_xlsx(True),background_color=(0.184, 0.216, 0.231), background_normal='')
        
        crud_export_all =  Button(text='Exporter Tous Les Produits', size_hint_x=1/8, width=100,
                                on_release=lambda x: self.export_xlsx(),background_color=(0.184, 0.216, 0.231), background_normal='')
        
        crud_close_p =  Button(text='Fermer', size_hint_x=1/8, width=100,
                            on_release=lambda x: self.ids.ops_fields_p.clear_widgets(),
                            background_color=(0.184, 0.216, 0.231), background_normal='')
        
        target.add_widget(crud_export_instock)
        target.add_widget(crud_export_all)
        target.add_widget(crud_close_p)
        
        return 0

    
    def add_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
        
        crud_marque = TextInput(hint_text='Marque', multiline=False)
        crud_modele = TextInput(hint_text='Modèle', multiline=False)
        crud_cpu = TextInput(hint_text='CPU', multiline=False)
        crud_ram = TextInput(hint_text='RAM', multiline=False)
        crud_gpu = TextInput(hint_text='GPU', multiline=False)
        crud_stockage = TextInput(hint_text='stockage', multiline=False)
        crud_batterie = TextInput(hint_text='Batterie', multiline=False)
        crud_price = TextInput(hint_text='Prix', multiline=False)
        crud_buy_price = TextInput(hint_text="Prix d'achat", multiline=False)
        exchange_rate = TextInput(hint_text="Taux de change", multiline=False)
        crud_stock = TextInput(hint_text='En stock', multiline=False)
        crud_sold = TextInput(hint_text='Vendu', multiline=False)
        crud_order = TextInput(hint_text='Commande', multiline=False)
        crud_fournisseur = TextInput(hint_text='Fournisseur', multiline=False)
        crud_last_purchase = TextInput(hint_text='Dernier Achat', multiline=False)
        crud_comment = TextInput(hint_text='Commentaire', multiline=False)

        crud_submit_p =  Button(text='Ajouter Produit', size_hint_x=1/8, width=100,
                                on_release=lambda x:self.add_product(self.gen_ref(crud_marque.text), crud_marque.text,
                                                                    crud_modele.text, crud_cpu.text, crud_ram.text, crud_gpu.text,
                                                                    crud_stockage.text, crud_batterie.text, crud_price.text,
                                                                    crud_buy_price.text, exchange_rate.text, crud_stock.text, crud_sold.text, crud_order.text, 
                                                                    crud_fournisseur.text, crud_last_purchase.text, crud_comment.text), background_color=(0.184, 0.216, 0.231), background_normal='')
        
        crud_close_p =  Button(text='Fermer', size_hint_x=1/8, width=100,
                            on_release=lambda x: self.ids.ops_fields_p.clear_widgets(),
                            background_color=(0.184, 0.216, 0.231), background_normal='')
        
        target.add_widget(crud_marque)
        target.add_widget(crud_modele)
        target.add_widget(crud_cpu)
        target.add_widget(crud_ram)
        target.add_widget(crud_gpu)
        target.add_widget(crud_stockage)
        target.add_widget(crud_batterie)
        target.add_widget(crud_price)
        target.add_widget(crud_buy_price)
        target.add_widget(exchange_rate)
        target.add_widget(crud_stock)
        target.add_widget(crud_sold)
        target.add_widget(crud_order)
        target.add_widget(crud_fournisseur)
        target.add_widget(crud_last_purchase)
        target.add_widget(crud_comment)
        target.add_widget(crud_submit_p)
        target.add_widget(crud_close_p)
        
        return 0


    def add_product(self, ref, marque, modele, cpu, ram, gpu, stockage, batterie, price, buy_price, exchange, stock, sold, order, supplier, last_purchase, comment):
        if ref == '':
            self.missing_field_popup(field='Réf')
            return 0
        if self.product_exist(ref):
            self.error_popup('La Référence existe déjà')
            return 0
        if marque == '':
            self.missing_field_popup(field='marque')
            return 0
        if modele == '':
            self.missing_field_popup(field='Modèle')
            return 0
        if cpu == '':
            self.missing_field_popup(field='CPU')
            return 0
        if ram == '':
            self.missing_field_popup(field='RAM')
            return 0
        if gpu == '':
            gpu == 'STANDARD'
        if stockage == '':
            self.missing_field_popup(field='Stockage')
            return 0
        if batterie == '':
            self.missing_field_popup(field='Batterie')
            return 0
        
        if stock == '':
            self.missing_field_popup(field='En Stock')
            return 0
        if order == '':
            self.missing_field_popup(field='Commande')
            return 0
        
        if price == '':
            price = '0'
        if exchange == '':
            exchange = 1
        else:
            exchange = float(exchange)
            buy_price = float(buy_price)*exchange
            buy_price = "{:.2f}".format(buy_price)
            
        if supplier == '':
            supplier = '?'
        
        order_scrn = self.ids.scrn_order_contents
        order_scrn.clear_widgets()
        
        content = self.ids.scrn_product_contents
        content.clear_widgets()
        
        self.products.insert_one({'Ref':ref, 'marque': marque,
                            'modele':modele, 'cpu': cpu, 'ram':ram, 'gpu':gpu, 'stockage': stockage, 'batterie':batterie, 'prix': price,
                            'prix_achat': buy_price, 'en_stock': stock, 'vendu': sold, 'commande': order, 'dernier_achat': last_purchase,
                            'commentaire': comment, 'fournisseur': supplier})
        
        products = self.get_products()
        usertable  = DataTable(table=products)
        content.add_widget(usertable)
        
        product_table2  = DataTable(table=products)
        order_scrn.add_widget(product_table2)
        
        self.success_popup("Produit Ajouté")
        
        return 0
    

    def update_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
        
        crud_code = TextInput(hint_text='Réf', multiline=False)
        crud_marque = TextInput(hint_text='Marque', multiline=False)
        crud_modele = TextInput(hint_text='Modèle', multiline=False)
        crud_cpu = TextInput(hint_text='CPU', multiline=False)
        crud_ram = TextInput(hint_text='RAM', multiline=False)
        crud_gpu = TextInput(hint_text='GPU', multiline=False)
        crud_stockage = TextInput(hint_text='stockage', multiline=False)
        crud_batterie = TextInput(hint_text='Batterie', multiline=False)
        crud_price = TextInput(hint_text='Prix', multiline=False)
        crud_buy_price = TextInput(hint_text="Prix d'achat", multiline=False)
        crud_exchange_rate = TextInput(hint_text="Taux de change", multiline=False)
        crud_stock = TextInput(hint_text='En stock', multiline=False)
        crud_sold = TextInput(hint_text='Vendu', multiline=False)
        crud_order = TextInput(hint_text='Commande', multiline=False)
        crud_fournisseur = TextInput(hint_text='Fournisseur', multiline=False)
        crud_last_purchase = TextInput(hint_text='Dernier Achat', multiline=False)
        crud_comment = TextInput(hint_text='Commentaire', multiline=False)
        crud_submit_p =  Button(text='Modifier Produit', size_hint_x=1/8, width=100,
                                on_release=lambda x:self.update_product(crud_code.text, crud_marque.text, crud_modele.text, crud_cpu.text,
                                                                        crud_ram.text, crud_gpu.text, crud_stockage.text, crud_batterie.text,
                                                                        crud_price.text, crud_buy_price.text, crud_exchange_rate.text, crud_stock.text, crud_sold.text,
                                                                        crud_order.text, crud_fournisseur.text, crud_last_purchase.text, crud_comment.text), 
                                background_color=(0.184, 0.216, 0.231), background_normal='')
            
        crud_close_p =  Button(text='Fermer', size_hint_x=1/8, width=100, on_release=lambda x: self.ids.ops_fields_p.clear_widgets(),
                            background_color=(0.184, 0.216, 0.231), background_normal='')
        
        target.add_widget(crud_code)
        target.add_widget(crud_marque)
        target.add_widget(crud_modele)
        target.add_widget(crud_cpu)
        target.add_widget(crud_ram)
        target.add_widget(crud_gpu)
        target.add_widget(crud_stockage)
        target.add_widget(crud_batterie)
        target.add_widget(crud_price)
        target.add_widget(crud_buy_price)
        target.add_widget(crud_exchange_rate)
        target.add_widget(crud_stock)
        target.add_widget(crud_sold)
        target.add_widget(crud_order)
        target.add_widget(crud_fournisseur)
        target.add_widget(crud_last_purchase)
        target.add_widget(crud_comment)
        target.add_widget(crud_submit_p)
        return 0

  
    def update_product(self, ref, marque, modele, cpu, ram, gpu, stockage, batterie, price, buy_price, exchange, stock, sold, order, supplier, last_purchase, comment):
        if ref == '':
            self.missing_field_popup(field="Réf")
            return 0
        
        if not self.product_exist(ref):
            self.error_popup("la référence n' existe pas")
            return 0
        
        content = self.ids.scrn_product_contents
        content.clear_widgets()
        
        order_scrn = self.ids.scrn_order_contents
        order_scrn.clear_widgets()
        
        if price == '':
            price = '0'
        
        if exchange == '':
            exchange = 1
        else:
            exchange = float(exchange)
            buy_price = float(buy_price)*exchange
            buy_price = "{:.2f}".format(buy_price)
        
        if supplier == '':
            supplier = '?'
        
        if comment == '':
            comment = ' '    
        
        self.products.update_one({'Ref':ref}, {'$set':{'marque': marque, 'modele':modele, 'cpu': cpu, 'ram':ram, 'gpu':gpu, 'stockage': stockage, 'batterie':batterie, 'prix': price,'prix_achat': buy_price, 'en_stock': stock, 'vendu': sold, 'commande': order, 'fournisseur': supplier, 'dernier_achat': last_purchase, 'commentaire':comment}})
        
        products = self.get_products()
        usertable  = DataTable(table=products)
        content.add_widget(usertable)
        
        product_table2  = DataTable(table=products)
        order_scrn.add_widget(product_table2)

        self.success_popup("Produit Modifié")
        
        return 0
    

    def remove_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
        crud_ref = TextInput(hint_text="Référence", multiline=False, width=100, height=10)
        crud_submit =  Button(text='Supprimer Produit', size_hint_x=None, width=150, background_color=(0.184, 0.216, 0.231), background_normal='',
                            on_release=lambda x: self.remove_product(crud_ref.text))
        crud_close =  Button(text='Fermer', size_hint_x=None, width=100, on_release=lambda x: self.ids.ops_fields_p.clear_widgets(),
                            background_color=(0.184, 0.216, 0.231), background_normal='')
        spacer = Label(text='', size_hint_x=.6)
        target.add_widget(crud_ref)
        target.add_widget(crud_submit)
        target.add_widget(crud_close)
        target.add_widget(spacer)
        
        return 0

    
    def remove_product(self, ref):
        if ref == '':
            self.missing_field_popup(field="Nom d'utilisateur")
            return 0
        if not self.product_exist(ref):
            self.error_popup("Le Produit n' existe pas")
            return 0
        
        content = self.ids.scrn_product_contents
        content.clear_widgets()
        
        order_scrn = self.ids.scrn_order_contents
        order_scrn.clear_widgets()
        
        self.products.delete_many({"Ref":ref})
        
        products = self.get_products()
        usertable  = DataTable(table=products)
        content.add_widget(usertable)
        
        product_table2  = DataTable(table=products)
        order_scrn.add_widget(product_table2)
            
        self.success_popup(f"le Produit {ref} a été Supprimé")
        return 0
    
    
    def add_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_first = TextInput(hint_text='Prénom', multiline=False)
        crud_last = TextInput(hint_text='Nom', multiline=False)
        crud_user = TextInput(hint_text="Nom d'utilisateur", size_hint_x=3/2, multiline=False)
        crud_pwd = TextInput(hint_text='Mot de passe', multiline=False, password=True)
        crud_des = Spinner(text='Operateur', values=['Operateur', 'Administrateur'],
                        background_color=(0.184, 0.216, 0.231), background_normal='')
        crud_submit =  Button(text='Ajouter', size_hint_x=None, width=100,
                            background_color=(0.184, 0.216, 0.231), background_normal='',
                            on_release=lambda x: self.add_user(crud_first.text, crud_last.text, crud_user.text, crud_pwd.text, crud_des.text))
        crud_close =  Button(text='Fermer', size_hint_x=None, width=100, background_color=(0.184, 0.216, 0.231), background_normal='',
                            on_release=lambda x: self.ids.ops_fields.clear_widgets())
        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_user)
        target.add_widget(crud_pwd)
        target.add_widget(crud_des)
        target.add_widget(crud_submit)
        target.add_widget(crud_close)
        return 0
    
    
    def add_user(self, first, last, user,  pwd, des):
        if user == '':
            self.missing_field_popup(field="Nom d'utilisateur")
            return 0
        if self.user_exist(user):
            self.error_popup('Utilisateur existe déjà')
            return 0
        if pwd == '':
            self.missing_field_popup(field="Mot de Passe")
            return 0
        content = self.ids.scrn_contents
        content.clear_widgets()
        pwd = hashlib.sha256(pwd.encode()).hexdigest()
        self.users.insert_one({'first_name':first, 'last_name': last,
                            'user_name':user, 'password': pwd, 'designation':des, 'date':datetime.now()})
        users = self.get_users()
        usertable  = DataTable(table=users)
        content.add_widget(usertable)
        
        self.success_popup(f"Utilisateur {user} Ajouté")
        
        return  0


    def update_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_first = TextInput(hint_text='Prénom', multiline=False)
        crud_last = TextInput(hint_text='Nom', multiline=False)
        crud_user = TextInput(hint_text="Nom d'utilisateur", size_hint_x=3/2, multiline=False)
        crud_pwd = TextInput(hint_text='Mot de passe', multiline=False, password=True)
        crud_des = Spinner(text='Operateur', values=['Operateur', 'Administrateur'], background_color=(0.184, 0.216, 0.231), background_normal='')
        crud_submit =  Button(text='Modifier', size_hint_x=None, width=100,
                            background_color=(0.184, 0.216, 0.231), background_normal='',
                            on_release=lambda x: self.update_user(crud_first.text, crud_last.text, crud_user.text, crud_pwd.text, crud_des.text))
        crud_close =  Button(text='Fermer', background_color=(0.184, 0.216, 0.231), background_normal='',
                            size_hint_x=None, width=100, on_release=lambda x: self.ids.ops_fields.clear_widgets())
        target.add_widget(crud_user)
        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_pwd)
        target.add_widget(crud_des)
        target.add_widget(crud_submit)
        target.add_widget(crud_close)

        return 0

    
    def update_user(self, first, last, user,  pwd, des):
        if user == '':
            self.missing_field_popup(field="Nom d'utilisateur")
            return 0
        if not self.user_exist(user):
            self.error_popup("Utilisateur n' existe pas")
            return 0
        content = self.ids.scrn_contents
        content.clear_widgets()
        pwd = hashlib.sha256(pwd.encode()).hexdigest()
        self.users.update_one({'user_name':user}, {'$set':{'first_name':first, 'last_name': last,
                            'user_name':user, 'password': pwd, 'designation':des, 'date':datetime.now()}})
        users = self.get_users()
        usertable  = DataTable(table=users)
        content.add_widget(usertable)
        
        self.success_popup(f"Utilisateur {user} Modifié")
        
        return  0
    
    
    def remove_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_user = TextInput(hint_text="Nom d'utilisateur", multiline=False)
        crud_submit =  Button(text='Supprimer', size_hint_x=None, width=100, background_color=(0.184, 0.216, 0.231), background_normal='',
                            on_release=lambda x: self.remove_user(crud_user.text))
        crud_close =  Button(text='Fermer', size_hint_x=None, width=100, background_color=(0.184, 0.216, 0.231), background_normal='',
                            on_release=lambda x: self.ids.ops_fields.clear_widgets())
        target.add_widget(crud_user)
        target.add_widget(crud_submit)
        target.add_widget(crud_close)
        
        return 0
    
    
    def remove_user(self, username):
        if username == '':
            self.missing_field_popup(field="Nom d'utilisateur")
            return 0
        if not self.user_exist(username):
            self.error_popup("L' utilisateur n' existe pas")
            return 0
        content = self.ids.scrn_contents
        content.clear_widgets()
        self.users.delete_many({"user_name":username})
        users = self.get_users()
        usertable  = DataTable(table=users)
        content.add_widget(usertable)
        
        self.success_popup(f"Utilisateur {username} Ajouté")
        return 0
    
    
    def change_screen(self, instance):
        if instance.text == 'Utilisateurs':
            self.ids.scrn_mngr.current = 'scrn_content'
        elif instance.text == 'Inventaire':
            self.ids.scrn_mngr.current = 'scrn_product_content'
        elif instance.text == 'Commandes':
            self.ids.scrn_mngr.current = 'scrn_order_content'
        elif instance.text == 'Calculateur':
            self.ids.scrn_mngr.current = 'scrn_calc_content'
        elif instance.text == 'Statistiques':
            self.ids.scrn_mngr.current = 'scrn_analysis_content' 
        elif instance.text == 'Recherche':
            self.ids.scrn_mngr.current = 'scrn_search_content'
        elif instance.text == 'Fournisseurs':
            self.ids.scrn_mngr.current = 'scrn_supplier_content'
        return 0


class AdminApp(App):
    def build(self):
        return AdminWindow()


if __name__=="__main__":
    aa = AdminApp()
    aa.run()
    