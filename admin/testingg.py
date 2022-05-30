"""    def get_order(self):
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
            if vendu[c] == '':
                vendu[c] = 0
            
            if en_stock[c] == '':
                en_stock[c] = 0
                
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
"""