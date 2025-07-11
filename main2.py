from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.toast import toast
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList,OneLineIconListItem,IconLeftWidget
from kivymd.uix.datatables import MDDataTable
from kivy.uix.screenmanager import NoTransition
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivy.uix.image import Image
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
import os
from time import strftime
import datetime
#Window.size = [360,610]

from kivy.metrics import dp
from reportlab.lib.pagesizes import letter 
from reportlab.pdfgen import canvas
import sqlite3 as sp
from pythonforandroid.recipe import PythonRecipe

class ReportlabRecipe(PythonRecipe):
    version = '3.6.12'
    url = 'https://files.pythonhosted.org/packages/source/r/reportlab/reportlab-{version}.tar.gz'
    site_packages_name = 'reportlab'
    depends = ['python3', 'pillow']

recipe = ReportlabRecipe()

#main
class ImageButton(MDCard, RectangularRippleBehavior):
    """Bouton personnalisé avec image et texte"""
    
    def __init__(self, image_source, text, callback=None,List = None, **kwargs):
        super().__init__(**kwargs)
        
        # Propriétés de la carte
        self.elevation = 2
        self.radius = [15]
        self.md_bg_color = (1, 1, 1, 1)  # Blanc
        self.size_hint_y = None
        self.height = dp(120)
        self.ripple_behavior = True
        
        # Layout principal
        main_layout = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            spacing=dp(8),
            padding=[dp(10), dp(15), dp(10), dp(10)]
        )
        
        # Image
        img = Image(
            source=image_source,
            size_hint=(None, None),
            size=(dp(150), dp(65)),
            pos_hint={'center_x': 0.5}
        )
        
        # Label
        label = MDLabel(
            text=text,
            theme_text_color="Custom",
            text_color = self.theme_cls.primary_color,
            halign="center",
            bold = True,
            size_hint_y=None,
            height=dp(30),
            markup = "True",
            font_style="Caption"
        )
        
        main_layout.add_widget(img)
        main_layout.add_widget(label)
        self.add_widget(main_layout)
        
        # Callback
        if callback:
            if not List:
                self.bind(on_release=lambda x: callback(text))
            else:
                self.bind(on_release = lambda x:callback(text,*List))

class Cotise(MDApp):
    Screen_Manager = ObjectProperty(None)
    def build(self):
        #self.theme_cls.theme_style = "Dark"
        main = Builder.load_file("main2.kv")
        #main.ids.cr.current = "Page1"
        return main

    def on_start(self):
        self.con = sp.connect("base.db")
    
    def Recharge_Page2(self):
        Pge = self.root.ids.Page2_cont
        Img = ImageButton(
                    image_source = "New.png",
                    text = "[b]New Cotisation[/b]",
                    pos_hint = {"center_x":0.25,"center_y":0.45},
                    size_hint = (0.4,0.2),
                    callback = self.New_Cot)
        Pge.add_widget(Img)

        Img = ImageButton(
                    image_source = "Cot.png",
                    text = "[b]Cotisation[/b]",
                    pos_hint = {"center_x":0.75,"center_y":0.45},
                    size_hint = (0.4,0.2),
                    callback = self.Cotiser)
        Pge.add_widget(Img)

    def do(self,instance):
        Name = self.root.ids.Ident.text
        Pass = self.root.ids.Pass.text
        if "" in [Name,Pass]:
            toast("Tous les champs sont Oblig. !")
        else:
            if (Name,Pass) in [("Deg","Deg"),("Zelipro","Dieuestgrand")]:
            #if Name in ["Zelipro","Deg"] and Pass in ["Deg","Dieuestgr@nd"]:
                self.show_info(title = "Message",text = "Bienvenue M.Elisée",fonct = self.Next)
            else:
                toast("Vous n'est pas le Bienvenue !")
    
    def show_info(self,title,text,fonct = None):
        self.MD = MDDialog(
            title = title,
            text = text,
            buttons = [
                MDFlatButton(
                    text = "Ok",
                    on_release=lambda x : self.Ok(x,fonct)
                )
            ]
        )
        self.MD.open()
    
    def Ok(self,instance,fonct):
        self.MD.dismiss()
        if fonct:
            fonct()
    
    def Next(self):
        Pge = self.root.ids.cr.current
        self.root.ids.cr.current = f"{Pge[:-1]}{str(int(Pge[-1])+1)}"
        if self.root.ids.cr.current == "Page2":
            self.root.ids.Page2_cont.clear_widgets()
            self.Recharge_Page2()
    
    def Back(self,instance):
        self.Back_s()
    
    def Back_s(self):
        Pge = self.root.ids.cr.current
        if Pge[-1] == "1":
            self.stop()
        else:
            self.root.ids.cr.current = f"{Pge[:-1]}{str(int(Pge[-1])-1)}"
    
    def New_Cot(self,instance):
        Cont = MDBoxLayout(orientation =  'vertical',size_hint =(0.3,0.3))
        self.input = MDTextField (hint_text = "Motif",helper_text = "Exple : Marriage de Zeli",helper_text_mode = "on_focus",halign = "center")
        But =MDFlatButton(text = "[b]Valider[/b]",on_release= self.Valider2,pos_hint= {'center_x': 0.5,'center_y': 0.4})
        Cont.add_widget(self.input)
        Cont.add_widget(But)
        
        
        self.pop = Popup(
            title = "Information",
            content = Cont,
            size_hint = (0.8,0.3)
        )
        
        self.pop.open()
    
    def Valider2(self,instance):
         text = self.input.text

         if text == "":
             toast("Ce champs est Obligatoire !")
         else:
            fil = self.exist_in_base(text)
            if fil:
                toast("Ce motif exist déjà !")
            else:
                self.Create_base(text)
                toast(f"{text} est enregistré avec succes !")
                self.pop.dismiss()
                #self.Back_s()

    def exist_in_base(self,text):
        cur = self.con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        tables = cur.fetchall()
        return text in [table[0] for table in tables]

    def Create_base(self,text):
        cur = self.con.cursor()
        cur.execute(f"CREATE TABLE {text} (value TEXT)")
    
    def on_stop(self):
        self.con.close()

    def Ok2(self,instance):
        self.pop.dismiss()
    
    def FICHIER_DOC(self,rep):
        return [fic for fic in os.listdir(rep) if os.path.isdir(os.path.join(rep,fic))]
    
    def FICHIER_BASE(self):
        cur = self.con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cur.fetchall()
        return [table[0] for table in tables]
    
    def Cotiser(self,instance):
        self.root.ids.cr.transition = NoTransition()
        self.root.ids.cr.current = "Page3"
        Pge = self.root.ids.List
        Pge.clear_widgets()
        for elmt in self.FICHIER_BASE():
            Lis = OneLineIconListItem(
                text = elmt,
                on_release= lambda x : self.appui(x),
            )
            Icon = IconLeftWidget(icon = "folder")
            Lis.add_widget(Icon)
            Pge.add_widget(Lis)
    
    def appui(self,instance):
        self.Motif = instance.text
        self.Instance = instance.text
        self.root.ids.cr.current = "Page4"
        self.Page4()
    
    def Page4(self):
        Pge = self.root.ids.List2
        Pge.clear_widgets()
        for elmt in ["Ajouter","Voir la liste","Total","Version Pdf"]:
            Lis = OneLineIconListItem(
                text = elmt,
                on_release=lambda x :self.appui2(x)
            )
            Icon = IconLeftWidget(icon = "list-box")
            Lis.add_widget(Icon)
            Pge.add_widget(Lis)
    
    def appui2(self,instance):
        dic = {"Ajouter" : self.add,"Voir la liste" : self.list,"Total": self.total,"Version Pdf" : self.pdf}
        do = dic.get(instance.text)
        do(self.Motif)
    
    def Liste_base(self,motif):
        curs = self.con.cursor()
        Liste = curs.execute(f"select * from {motif}")

        return [lis[0] for lis in Liste]
    
    def list(self,motif):
        try:
            self.root.ids.cr.current = "Page5"
            self.root.ids.TopBar.title = self.Instance
            Pge = self.root.ids.Data   
            Pge.clear_widgets()
            row_data2 = []
            tous = self.Liste_base(motif)
            i = 1
            Tous = []
            for emt in tous:
                if len(emt)>6:
                    emt = emt.split("!!!")
                    Tous = [str(i)] + emt
                    i += 1
                    row_data2.append(tuple(Tous))
            
            Data = MDDataTable(
            pos_hint = {"center_x":0.5,"center_y":0.5},
            use_pagination = True,
            size_hint=(0.9,0.5),
            column_data =  [
                ("ID",dp(12)),("Date",dp(25)),("Name",dp(35)),("Prix",dp(25))
                ],
            row_data = row_data2)
            Pge.add_widget(Data)
        except:
            toast("La fichier est vide")

    def add(self,motif):
        Cont = MDBoxLayout(orientation = 'vertical',spacing = 5)
        self.Name = MDTextField(hint_text = "Name",helper_text = "Maybe first name + second name",helper_text_mode = "on_focus",halign = "center")
        self.prix = MDTextField(input_filter = "int",hint_text = "Prix",helper_text = "300 , 500 ,....",helper_text_mode = "on_focus",halign = "center")
        self.But = MDFlatButton(text = "[b]Valider[/b]",on_release=lambda x : self.Valider3(x,motif),pos_hint = {"center_x":.5})
        
        Cont.add_widget(self.Name)
        Cont.add_widget(self.prix)
        Cont.add_widget(self.But)
        
        self.pop2 = Popup(
            title = "Information",
            content = Cont,
            size_hint = (0.9,0.4)
        )
        self.pop2.open()
    
    def Valider3(self,instance,motif):
        if "" in [self.Name.text ,self.prix.text]:
            toast("Tous les champs sont obligatoire !")
        elif self.exist(self.Name.text): #Verifi si ce nom existe
            toast("Ce nom existe  déjà")
        else:
            add = f"{strftime("%D")}!!!{self.Name.text}!!!{self.prix.text}"
            self.ADD_table(add,motif)#Cette fonction permet d'ajouter a la table
            self.pop2.dismiss()
            #self.oui()
            toast("Ajout effectué !!!")
    
    def ADD_table(self,add,motif):
        cur = self.con.cursor()
        cur.execute(f"Insert into {motif} (value) values (?)",(add,))
        self.con.commit()

    def contenu(self,motif):
            retur = []
            tous = self.Liste_base(motif)
            Date = ""
            Som = 0
            for elmt in tous:
                if len(elmt)>6:
                    elmt = elmt.split("!!!")
                    if Date != elmt[0]:
                        Date = elmt[0]
                        retur.append(Date)
                    retur.append(f"{elmt[1]} : {elmt[2]}")
                    Som += int(elmt[2])
            retur.append(f"Total = {Som}")
            return retur
        
    def PDF(self, rep, Messagess): #Ici
        file = canvas.Canvas(f"{rep}/Liste.pdf", pagesize=letter)
        file.setTitle("Liste PDF")
        
        # Configuration initiale
        line = 750  # Position verticale initiale
        page_number = 1
        
        def draw_header():
            """Dessine l'en-tête sur chaque page"""
            nonlocal file, line
            header = f"REPPORT DE COTISATION POUR {self.Instance}"
            file.setFont("Helvetica-Bold", 18)
            file.drawString(150, line, f"{header}")
            file.setLineWidth(1.5)
            file.line(150, line - 3, 200 + file.stringWidth(f"{header}", "Helvetica-Bold", 17), line - 3)
            file.setFont("Helvetica", 16)
            line -= 40
        
        # Dessiner l'en-tête de la première page
        draw_header()
        
        for elmt in Messagess:
            # Vérifier si on a besoin d'une nouvelle page
            if line < 50:  # Marge basse
                file.showPage()
                page_number += 1
                line = 750
                draw_header()
            
            # Dessiner l'élément avec son formatage approprié
            if "Total" in elmt or len(elmt.split("/")) == 3:
                file.drawString(250, line, elmt)
                #file.line(250, line - 2, 250 + file.stringWidth(elmt, "Helvetica", 12), line - 2)
            else:
                file.drawString(200, line, elmt)
                #file.line(200, line - 2, 200 + file.stringWidth(elmt, "Helvetica", 12), line - 2)
            
            line -= 25  # Espacement entre les lignes
        
        # Pied de page sur la dernière page
        file.setFont("Helvetica", 10)
        file.drawString(500, 30, f"Fin du document - {datetime.datetime.now().strftime('%d/%m/%Y')}")
        
        file.save()
        
    def exist(self,name):
        try:
            tous = self.Liste_base(self.Motif)
            for elmt in tous:
                if len(elmt) > 6:
                    elmt = elmt.split("!!!")
                    if elmt[1] == name:
                        return True
            return False
        except:
            return False
  
    def Change(self,instance):
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
    
    def Option_List(self,instance):
        dic = {"Leave":self.stopp , "Help":self.help , "About as":self.info}
        dic.get(instance.text)()
    
    def info(self):
        self.show_info(title = "info" , text = "Name : Gestion des cotisation \nAuthor : Elisée ATIKPO")
    
    def help(self):
        self.show_info(title = "Help" ,text="Here is for a cotisation so , follow the instrction.\nThanks")
    
    def stopp(self):
        self.show_info(title = "Info",text = "Bye !!!",fonct=self.stop)
            
    def total(self,motif): #Pge 7
        try:
            self.show_info(title = "Total",text = f"Le total des prix est {self.Somme_prix(motif)} FCFA.")
        except:
            self.show_info(title = "Total",text = f"Le total des prix est 0 FCFA.")
        
    def Somme_prix(self,motif):
        tous = self.Liste_base(motif=motif)
        Som = 0
        for emt in tous:
            if emt!="":
                emt = emt.split("!!!")
                Som += int(emt[-1])
        return Som
    
    def pdf(self,motif): #Pge 8
        self.root.ids.cr.current = "Page6"
    
    def this(self,instance):
        selct = self.root.ids.selct.selection
        try:
            file_select = selct[0]
            self.PDF(file_select,self.contenu(self.Motif))
            toast(f"Fichier enregisté à\n {file_select}")
            self.Back_s()
        except:
            toast("Impossible")

Cotise().run()
