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
        self.ids.scrn_admin.add_widget(self.admin_widget)
        self.ids.scrn_op.add_widget(self.operator_widget)
        
    def refresh_screens(self):
        self.admin_widget = AdminWindow()
        self.operator_widget = OperateurWindow()
        
        self.ids.scrn_admin.add_widget(self.admin_widget)
        self.ids.scrn_op.add_widget(self.operator_widget)

class MainApp(App):
    def build(self):
        return MainWindow()
    
if __name__=='__main__':
    MainApp().run()
