from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class SigninWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate_user(self):
        user = self.ids.username_field
        pwd = self.ids.pwd_field
        info = self.ids.info
        
        username = user.text
        password = pwd.text

        if username == "" or password == "":
            info.text = "[color=#FF0000]NOM D'UTILISATEUR ET / OU MOT DE PASSE REQUIS[/color]"
        elif username == 'admin' and password == 'admin':
            info.text = "[color=#006400]CONNECTÉ AVEC SUCCÈS[/color]"
        else:
            info.text = "[color=#FF0000]NOM D'UTILISATEUR ET / OU MOT DE PASSE INVALIDE[/color]"

class SigninApp(App):
    def build(self):
        return SigninWindow()

if __name__=="__main__":
    sa = SigninApp()
    sa.run()
