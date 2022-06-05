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
        bold: True
        RecycleGridLayout:
            id: table_floor_layout
            cols: 8
            default_size: (None, 250)
            default_size_hint: (1, None)
            size_hint_y: None
            height: self.minimum_height
            spacing: 5
<CustLabel@Label>:
    bcolor: (0, 0, 0, 1)
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
            if  t == 'designation':
                table_data.append({'text':str(t), 'size_hint_y':None, 'size_hint_x':5, 'height':50, 'bcolor':(0.145, 0.376, 0.541, 1), 'color': (1, 1, 1, 1)})
            else:
                table_data.append({'text':str(t), 'size_hint_y':None, 'height':50, 'bcolor':(0.145, 0.376, 0.541, 1), 'color': (1, 1, 1, 1)})

        for r in range(row_len):
            if r % 2 == 0:
                colr = (0.722, 0.835, 0.918, 1)
            else:
                colr = (0.173, 0.51, 0.757, 1)
            
            for t in col_titles:
                table_data.append({'text':str(products[t][r]), 'color': (0, 0, 0, 1),
                                   'size_hint_y':None, 'height':40, 'bcolor':colr})

                    
        
        self.ids.table_floor.data = table_data
        self.ids.table_floor_layout.cols  = self.columns


#class DataTableApp(App):
#    def build(self):
#
#        return DataTable()
#
#if __name__=='__main__':
#    DataTableApp().run()