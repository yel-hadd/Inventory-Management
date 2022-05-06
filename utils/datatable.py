from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from kivy.lang import Builder

from collections import OrderedDict
from pymongo import MongoClient


Builder.load_string('''
<DataTable>:
    id: main_win
    RecycleView:
        viewclass: 'CustLabel'
        id: table_floor
        RecycleGridLayout:
            id: table_floor_layout
            cols: 8
            default_size: (None, 250)
            default_size_hint: (1, None)
            size_hint_y: None
            height: self.minimum_height
            spacing: 5
<CustLabel@Label>:
    bcolor: (1, 1, 1, 1)
    canvas.before:
        Color:
            rgba: root.bcolor
        Rectangle:
            size: self.size
            pos: self.pos
            
''')

class DataTable(BoxLayout):
    def __init__(self,  table, **kwargs):
        super().__init__(**kwargs)


        products = table
        col_titles = [k for k in products.keys()]
        row_len = len(products[col_titles[0]])
        self.columns = len(col_titles)
        table_data = []
        for t in col_titles:
            table_data.append({'text':str(t), 'size_hint_y':None, 'height':50, 'bcolor':(.06,.45, .45, 1)})
        
        for r in range(row_len):
            for t in col_titles:
                table_data.append({'text':str(products[t][r]),
                                   'size_hint_y':None, 'height':40, 'bcolor':(.06,  .25, .25, 1)})
                
        
        self.ids.table_floor.data = table_data
        self.ids.table_floor_layout.cols  = self.columns
    
    def get_users(self):
        client = MongoClient()
        db = client.pos
        users = db.users
        _users = OrderedDict(
            first_names = {},
            last_names = {},
            user_names = {},
            passwords = {},
            designations = {}
        )

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
            passwords.append(user['password'])
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
    



#class DataTableApp(App):
#    def build(self):
#
#        return DataTable()
#
#if __name__=='__main__':
#    DataTableApp().run()