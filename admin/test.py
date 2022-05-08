from pymongo import MongoClient

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

def user_exist(self, ref):
    client = MongoClient()
    db = client.pos
    users = db.users
    i = 0
    for p in users.find():
        if p['Ref'] == f"{ref}":
            i += 1
    if i == 0:
        return False
    else:
        return True

    
print(product_exist('HP-000001'))