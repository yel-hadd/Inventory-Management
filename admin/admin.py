from turtle import bgcolor, title
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from pymongo import MongoClient
from utils.datatable import DataTable
from datetime import datetime
import hashlib

class AdminWindow(BoxLayout):
    # Add screen size to get_products(self)
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
        users = self.get_products()
        prod_table  = DataTable(table=products)
        product_scrn.add_widget(prod_table)
        
     
    def missing_field_popup(self, field):
        box = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)        
        error_img = Image(source='./utils/1.png', size=(150, 150))
        error_msg = Label(text=f'champ obligatoire ({field}) manquant', bold=True)
        
        
        popup = ModalView(size_hint=(None, None), size=(400, 200))
        box.add_widget(error_img)
        box.add_widget(error_msg)
        
        popup.add_widget(box)
        
        popup.open()
        
        return 0
    
    
    def error_popup(self, message):
        box = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)        
        error_img = Image(source='./utils/1.png', size=(150, 150))
        error_msg = Label(text=f'{message}', bold=True)
        
        popup = ModalView(size_hint=(None, None), size=(400, 200))
        box.add_widget(error_img)
        box.add_widget(error_msg)
        
        popup.add_widget(box)
        
        popup.open()
        
        return 0
    
    
    def success_popup(self, operation):
        box = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)        
        error_img = Image(source='./utils/2.png', size=(150, 150))
        error_msg = Label(text=f'{operation} avec succès', bold=True)
        
        
        popup = ModalView(size_hint=(None, None), size=(300, 200))
        box.add_widget(error_img)
        box.add_widget(error_msg)
        
        popup.add_widget(box)
        
        popup.open()
        
        return 0


    def product_exist(self, ref):
        client = MongoClient()
        db = client.pos
        products = db.stocks
        i = 0
        for p in products.find():
            if p['Ref'] == f"{ref}":
                i += 1
        if i == 0:
            return False
        else:
            return True


    def user_exist(self, username):
        client = MongoClient()
        db = client.pos
        users = db.users
        i = 0
        for p in users.find():
            if p['user_name'] == f"{username}":
                i += 1
        if i == 0:
            return False
        else:
            return True
    
    
    def get_users(self):
        client = MongoClient()
        db = client.pos
        users = db.users
        
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
        client = MongoClient()
        db = client.pos
        products = db.stocks
        _stocks = {}
        _stocks['Ref'] = {}
        _stocks['designation'] = {}
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
                dernier_achat.append(product['dernier_achat'])
            except KeyError:
                dernier_achat.append('')
                        
        for c, v in enumerate(Ref):
            _stocks['Ref'][c] = Ref[c]
            _stocks['designation'][c] = f"{marque[c]} {modele[c]} | {cpu[c]} | {ram[c]}GB\n{stockage[c]} | {gpu[c]} | {batterie[c]}"
            _stocks['prix'][c] = prix[c]
            _stocks['prix_achat'][c] = prix_achat[c]
            _stocks['en_stock'][c] = en_stock[c]
            _stocks['vendu'][c] = vendu[c]
            _stocks['commande'][c] = commande[c]
            _stocks['dernier_achat'][c] = dernier_achat[c]

        return _stocks
    
    
    def add_product_fields(self):
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
        crud_stock = TextInput(hint_text='En stock', multiline=False)
        crud_sold = TextInput(hint_text='Vendu', multiline=False)
        crud_order = TextInput(hint_text='Commande', multiline=False)
        crud_last_purchase = TextInput(hint_text='Dernier Achat', multiline=False)
        crud_submit_p =  Button(text='Ajouter Produit', size_hint_x=1/8, width=100,
                                on_release=lambda x:self.add_product(crud_code.text, crud_marque.text, crud_modele.text, crud_cpu.text, crud_ram.text, crud_gpu.text, crud_stockage.text, crud_batterie.text, crud_price.text, crud_buy_price.text, crud_stock.text, crud_sold.text, crud_order.text, crud_last_purchase.text))
        
        crud_close_p =  Button(text='Fermer', size_hint_x=1/8, width=100, on_release=lambda x: self.ids.ops_fields_p.clear_widgets())
        #
        
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
        target.add_widget(crud_stock)
        target.add_widget(crud_sold)
        target.add_widget(crud_order)
        target.add_widget(crud_last_purchase)
        target.add_widget(crud_submit_p)
        target.add_widget(crud_close_p)
        
        return 0


    def add_product(self, ref, marque, modele, cpu, ram, gpu, stockage, batterie, price, buy_price, stock, sold, order, last_purchase):
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
        if price == '':
            self.missing_field_popup(field='Prix')
            return 0
        if stock == '':
            self.missing_field_popup(field='En Stock')
            return 0
        if order == '':
            self.missing_field_popup(field='Commande')
            return 0
        
        
        content = self.ids.scrn_product_contents
        content.clear_widgets()
        
        self.products.insert_one({'Ref':ref, 'marque': marque,
                               'modele':modele, 'cpu': cpu, 'ram':ram, 'gpu':gpu, 'stockage': stockage, 'batterie':batterie, 'prix': price,
                               'prix_achat': buy_price, 'en_stock': stock, 'vendu': sold, 'commande': order, 'dernier_achat': last_purchase})
        
        products = self.get_products()
        usertable  = DataTable(table=products)
        content.add_widget(usertable)
        
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
        crud_stock = TextInput(hint_text='En stock', multiline=False)
        crud_sold = TextInput(hint_text='Vendu', multiline=False)
        crud_order = TextInput(hint_text='Commande', multiline=False)
        crud_last_purchase = TextInput(hint_text='Dernier Achat', multiline=False)
        crud_submit_p =  Button(text='Modifier Produit', size_hint_x=1/8, width=100,
                                on_release=lambda x:self.update_product(crud_code.text, crud_marque.text, crud_modele.text, crud_cpu.text, crud_ram.text, crud_gpu.text, crud_stockage.text, crud_batterie.text, crud_price.text, crud_buy_price.text, crud_stock.text, crud_sold.text, crud_order.text, crud_last_purchase.text))
        
        crud_close_p =  Button(text='Fermer', size_hint_x=1/8, width=100, on_release=lambda x: self.ids.ops_fields_p.clear_widgets())
        
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
        target.add_widget(crud_stock)
        target.add_widget(crud_sold)
        target.add_widget(crud_order)
        target.add_widget(crud_last_purchase)
        target.add_widget(crud_submit_p)
        target.add_widget(crud_close_p)
        
        return 0

    
    def update_product(self, ref, marque, modele, cpu, ram, gpu, stockage, batterie, price, buy_price, stock, sold, order, last_purchase):
        if ref == '':
            self.missing_field_popup(field="Réf")
            return 0
        
        if not self.product_exist(ref):
            self.error_popup("la référence n' existe pas")
            return 0
        content = self.ids.scrn_product_contents
        content.clear_widgets()
        
        self.products.update_one({'Ref':ref}, {'$set':{'marque': marque, 'modele':modele, 'cpu': cpu, 'ram':ram, 'gpu':gpu, 'stockage': stockage, 'batterie':batterie, 'prix': price, 'prix_achat': buy_price, 'en_stock': stock, 'vendu': sold, 'commande': order, 'dernier_achat': last_purchase}})
                
        
        products = self.get_products()
        usertable  = DataTable(table=products)
        content.add_widget(usertable)
        
        self.success_popup("Produit Modifié")
        
        return 0
    
  
    def remove_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
        crud_ref = TextInput(hint_text="Référence", multiline=False, width=100, height=10)
        crud_submit =  Button(text='Supprimer Produit', size_hint_x=None, width=150, on_release=lambda x: self.remove_product(crud_ref.text))
        crud_close =  Button(text='Fermer', size_hint_x=None, width=100, on_release=lambda x: self.ids.ops_fields_p.clear_widgets())
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
        content = self.ids.scrn_contents
        content.clear_widgets()
        self.products.delete_many({"Ref":ref})
        products = self.get_products()
        usertable  = DataTable(table=products)
        content.add_widget(usertable)
        
        self.success_popup(f"le Produit {ref} a été Supprimé")
        return 0
    
    
    def add_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_first = TextInput(hint_text='Prénom', multiline=False)
        crud_last = TextInput(hint_text='Nom', multiline=False)
        crud_user = TextInput(hint_text="Nom d'utilisateur", size_hint_x=3/2, multiline=False)
        crud_pwd = TextInput(hint_text='Mot de passe', multiline=False, password=True)
        crud_des = Spinner(text='Operateur', values=['Operateur', 'Administrateur'])
        crud_submit =  Button(text='Ajouter', size_hint_x=None, width=100, on_release=lambda x:
            self.add_user(crud_first.text, crud_last.text, crud_user.text, crud_pwd.text, crud_des.text))
        crud_close =  Button(text='Fermer', size_hint_x=None, width=100, on_release=lambda x: self.ids.ops_fields.clear_widgets())
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
        crud_des = Spinner(text='Operateur', values=['Operateur', 'Administrateur'])
        crud_submit =  Button(text='Modifier', size_hint_x=None, width=100, on_release=lambda x:
            self.update_user(crud_first.text, crud_last.text, crud_user.text, crud_pwd.text, crud_des.text))
        crud_close =  Button(text='Fermer', size_hint_x=None, width=100, on_release=lambda x: self.ids.ops_fields.clear_widgets())
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
        crud_submit =  Button(text='Supprimer', size_hint_x=None, width=100, on_release=lambda x: self.remove_user(crud_user.text))
        crud_close =  Button(text='Fermer', size_hint_x=None, width=100, on_release=lambda x: self.ids.ops_fields.clear_widgets())
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
        return 0


class AdminApp(App):
    def build(self):
        return AdminWindow()


if __name__=="__main__":
    aa = AdminApp()
    aa.run()