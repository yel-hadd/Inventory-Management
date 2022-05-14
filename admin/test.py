from pymongo import MongoClient
import tkinter.filedialog
import os
from PIL import ImageFont, Image, ImageDraw
import qrcode
# self, path, ref, marque, modele, cpu, ram, stockage, gpu, batterie, commande

client = MongoClient()
db = client.pos
products = db.stocks
order = 'C1'

def create_order_labels(self, order):
    comm = products.find({"commande": f"eeeregef"})
    try:
        comm = comm[0]
    except IndexError:
        return 0

    path = tkinter.filedialog.askdirectory()
    if path == '':
        return 0

    font = ImageFont.truetype("Montserrat-Regular.ttf", 35)
    font2 = ImageFont.truetype("Montserrat-Regular.ttf", 54)
    img = Image.open("./utils/Label.jpg")
    Logo_link = './utils/logo.jpg'
    images = []
    for product in self.products.find({"commande": f"{order}"}):
        products.find({"commande": f"{order}"})
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

        logo = Image.open(Logo_link)    
        basewidth = 100 
        wpercent = (basewidth/float(logo.size[0]))
        hsize = int((float(logo.size[1])*float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)
        QRcode = qrcode.QRCode( 
        error_correction=qrcode.constants.ERROR_CORRECT_H
        )   
        QRcode.add_data(ref)    
        QRcode.make()
        QRcolor = '#000000'
        QRimg = QRcode.make_image(
        	fill_color=QRcolor, back_color="white").convert('RGB')
        QRimg = QRimg.resize((420, 420), Image.Resampling.NEAREST)
        pos = ((QRimg.size[0] - logo.size[0]) // 2,
        	(QRimg.size[1] - logo.size[1]) // 2)
        QRimg.paste(logo, pos)        
        img.paste(QRimg, (390, 680))
        images.append(img)
        img = Image.open("./utils/Label.jpg")

    images[0].save(
        f"{path}/{order}.pdf", "PDF" ,resolution=300.0, save_all=True, append_images=images[1:]
    )
