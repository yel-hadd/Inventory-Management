from http import client
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
import re
from collections import OrderedDict
from pymongo import MongoClient
from utils.datatable import DataTable
from datetime import datetime
import hashlib

class AdminWindow(BoxLayout):
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
        product_scrn = self.ids.scrn_product_content
        products = self.get_products()
        users = self.get_products()
        prod_table  = DataTable(table=products)
        product_scrn.add_widget(prod_table)

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
                pwd  = pwd[:10]
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
            prix_achat.append(product['prix_achat'])
            marque.append(product['marque'])
            modele.append(product['modele'])
            cpu.append(product['cpu'])
            ram.append(product['ram'])
            gpu.append(product['gpu'])
            stockage.append(product['stockage'])
            batterie.append(product['batterie'])
            en_stock.append(product['en_stock'])
            vendu.append(product['vendu'])
            commande.append(product['commande'])
            dernier_achat.append(product['dernier_achat'])
            
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
        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_user)
        target.add_widget(crud_pwd)
        target.add_widget(crud_des)
        target.add_widget(crud_submit)

        return 0
    
    
    def add_user(self, first, last, user,  pwd, des):
        content = self.ids.scrn_contents
        content.clear_widgets()
        pwd = hashlib.sha256(pwd.encode()).hexdigest()
        self.users.insert_one({'first_name':first, 'last_name': last,
                               'user_name':user, 'password': pwd, 'designation':des, 'date':datetime.now()})
        
        users = self.get_users()
        usertable  = DataTable(table=users)
        content.add_widget(usertable)
        
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
        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_user)
        target.add_widget(crud_pwd)
        target.add_widget(crud_des)
        target.add_widget(crud_submit)

        return 0
 
   
    def update_user(self, first, last, user,  pwd, des):
        content = self.ids.scrn_contents
        content.clear_widgets()
        pwd = hashlib.sha256(pwd.encode()).hexdigest()
        self.users.update_one({'user_name':user}, {'$set':{'first_name':first, 'last_name': last,
                               'user_name':user, 'password': pwd, 'designation':des, 'date':datetime.now()}})
        
        users = self.get_users()
        usertable  = DataTable(table=users)
        content.add_widget(usertable)
        
        return  0
       
    def remove_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_user = TextInput(hint_text="Nom d'utilisateur", multiline=False)
        crud_submit =  Button(text='Supprimer', size_hint_x=None, width=100, on_release=lambda x: self.remove_user(crud_user.text))
        target.add_widget(crud_user)
        target.add_widget(crud_submit)
        return 0
    
    def remove_user(self, username):
        content = self.ids.scrn_contents
        content.clear_widgets()
        print('*****************')
        print(username)
        self.users.delete_many({"user_name":username})
        users = self.get_users()
        usertable  = DataTable(table=users)
        content.add_widget(usertable)
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