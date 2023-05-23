from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.pickers import MDDatePicker
from kivy.core.window import Window
from kivy.graphics import Line
from datetime import datetime
from kivy.properties import ObjectProperty

class Window_App(MDApp):
  def build(self):
    Builder.load_file('main.kv')

    self.theme_cls.theme_style = "Light"
    self.theme_cls.primary_palette = "Orange"
    Window.size = [720,1280]
    
    sm = MDScreenManager()
    sm.add_widget(Index_Screen())
    sm.add_widget(Form_Screen())

    sm.current = "Form"
    return sm

  def show_Calendar():
    Date_Picker().open()

  def on_date_save(self, instance, value, daterange):
    Window_App.get_running_app().root.get_screen('Form').ids.date_btn.text = str(value)
    fechamento['Data'] = str(value)
  
class Index_Screen(MDScreen):
  def __init__(self):
    super().__init__()
    self.name = "Index"


class Form_Screen(MDScreen):
  def __init__(self):
    super().__init__()
    self.name = "Form"
    responsavel = ObjectProperty(None)
  def on_pre_enter(self):
    self.responsavel.bind(text = self.on_text)
      
  def on_text(self,instance,value):
    fechamento['Responsavel'] = value

class Side_L(MDGridLayout):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    
    self.cols = 1
    self.rows = 2

class Txt_Input_Sc1(MDTextField):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.mode = 'rectangle'
    self.size_hint = 0.8,None



class Calendar_Button(MDRectangleFlatIconButton):
  def __init__(self,**kwargs):
    super().__init__(**kwargs)
    self.icon = "calendar"
    self.text = "Data"
    self.theme_text_color = "Custom"
    self.text_color = "black"
    self.line_color = "black"
    self.theme_icon_color = "Custom"
    self.icon_color = "black"
    self.on_press = Window_App.show_Calendar
    
class Checks_Turno(MDGridLayout):
  def __init__(self,**kwargs):
    super().__init__(**kwargs)
    self.rows = 1 
    self.cols  = 11


    
    self.add_widget(MDLabel(text = 'Turno: ', width = 5))
    
    for turno in ['A','B','C','D','ADM']:
      self.check = MDCheckbox()
      self.check.group = 'group2'
      self.check.size = [48,48]
      self.check.value = turno
      self.txt = MDLabel(text = turno)
      
      self.add_widget(self.check)
      self.add_widget(self.txt)
      dict_Turno[turno] = self.check

class Date_Picker(MDDatePicker):
  def __init__(self,**kwargs):
    super().__init__(**kwargs)

    self.bind(on_save=Window_App.get_running_app().on_date_save)
    
    self.title = 'Selecione a Data'
    self.year = datetime.now().year
    self.month = datetime.now().month
    self.day = datetime.now().day

    self.min_year = self.year - 1
    self.max_year = self.year + 1



class Side_R(MDGridLayout):
  def __init__(self,**kwargs):
    super().__init__(**kwargs)
    
    self.padding = 10
    self.spacing = 15
    self.cols = 1

    l_Registro = ['Entrada','Baia I', 'Baia II', 'Baia III', 'Baia IV']
    self.rows = len(l_Registro)+1

    for reg in l_Registro:
      self.txt = Txt_Input_Sc1(hint_text = reg)
      self.add_widget(self.txt)
      dict_Registro[reg] = self.txt

class Selection_Materiais(MDBoxLayout):
    def __init__(self, **kwargs):
      super().__init__(**kwargs)

      self.orientation = 'vertical'
      
      l_materiais = ['Buritirama Bruta',
                     'Finos de Briquete',
                     'Finos de Buritirama',
                     'Finos de Carepa',
                     'Finos de Escória',
                     'Finos de Minério Pobre',
                     'Finos de Minério Rico',
                     'Finos de Sucata',
                     'Outro'
                    ]
      

      for material in l_materiais:
        self.cb = MDCheckbox()
        self.cb.group = 'group'
        self.cb.size_hint = (None, None)
        self.cb.size = [48,48]
        self.cb.value = material
        
        self.box = MDBoxLayout()
        
        self.box.add_widget(self.cb)
        self.box.add_widget(MDLabel(text = material))

        self.add_widget(self.box)
        dict_Materiais[material] = self.cb
        
class Confirm_Button(MDRaisedButton):
  def __init__(self,**kwargs):
    super().__init__(**kwargs)

    self.on_press = confirm
    self.text = "Confirma"
    self.size = 100, 50
    self.line_color = "black"


def confirm():
  for i in dict_Materiais:
    if dict_Materiais[i].active == True:
      fechamento['Material'] = dict_Materiais[i].value
      break

  for i in dict_Turno:
    if dict_Turno[i].active == True:
      fechamento['Turno'] = dict_Turno[i].value
      break

  for i in dict_Registro:
    if dict_Registro[i].text != "":
      for compara in fechamento:
        if i == compara:
          fechamento[i] = dict_Registro[i].text

  print(fechamento)
      
    


dict_Materiais = {} 
dict_Turno = {}
dict_Registro = {}

fechamento ={'Data':None,
            'Responsavel':None,
            'Turno':None,
            'Material':None,
            'Entrada':None,
            'Baia I': None,
            'Baia II': None,
            'Baia III': None,
            'Baia IV': None
            }


Window_App().run()
  