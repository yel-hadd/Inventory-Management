from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.uix.image import Image
from kivy.uix.label import Label


from pymongo import MongoClient
import hashlib


Builder.load_file('./POS/signin.kv')


class SigninWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        client = MongoClient()
        db = client.pos
        self.users = db.users
        
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
 
 

    def validate_user(self):
        user = self.ids.username_field
        pwd = self.ids.pwd_field
        info = self.ids.info
        
        username = user.text
        password = pwd.text
        
        if username == "" or password == "":
            self.error_popup("NOM D'UTILISATEUR ET / OU MOT DE PASSE REQUIS")
        else:
            user = self.users.find_one({'user_name': username})
            if user == None:
                self.error_popup("NOM D'UTILISATEUR ET / OU MOT DE PASSE INVALIDE")
            else:
                password = hashlib.sha256(password.encode()).hexdigest()
                if username == user['user_name'] and user['password'] == password:
                    self.success_popup("connecté")
                    if user['designation'] == 'Administrateur':
                        self.parent.parent.current = 'scrn_admin'
                        self.parent.parent.parent.ids.scrn_admin.children[0].ids.loggedin_user.text = user['user_name']
                    else:
                        self.parent.parent.current = 'scrn_op'
                        self.parent.parent.parent.ids.scrn_op.children[0].ids.loggedin_user.text = user['user_name']
                    self.ids.username_field.text = ''
                    self.ids.pwd_field.text = ''
                else:
                    self.error_popup("NOM D'UTILISATEUR ET / OU MOT DE PASSE INVALIDE")
                    

class SigninApp(App):
    def build(self):
        return SigninWindow()

if __name__=="__main__":
    sa = SigninApp()
    sa.run()
