from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from admin.admin import AdminWindow
from POS.signin import SigninWindow
from OPERATOR.operateur import OperateurWindow 

class MainWindow(BoxLayout):
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.admin_widget = AdminWindow()
        self.signin_widget = SigninWindow()
        self.operator_widget = OperateurWindow()
        
        self.ids.scrn_si.add_widget(self.signin_widget)

class MainApp(App):
    def build(self):
        return MainWindow()
    
if __name__=='__main__':
    MainApp().run()
