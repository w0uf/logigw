from tkinter import *
from tkinter import messagebox
import base64
from tkinter import ttk
from tkinter import filedialog
from library2.logigramme_f import *
from svglib.svglib import svg2rlg
import io, textwrap
from reportlab.graphics import renderPDF, renderPM
from PIL import ImageTk as itk
from PIL import Image
from library2.config import*
import webbrowser
import os
from pylunasvg import Document
import numpy as np
from urllib import request
import fitz
from svglib import svglib
from reportlab.graphics import renderPDF

class Win:
    def __init__(self,master,content,langue):
        self.master = master
        self.content=content
        
        self.langue=langue.upper()
        self.les_options=parametres()
        self.file=""
        
    def create(self):
        self.master = Tk()
        self.master.title ("LOGIGW :   " + _("Pseudo-code vers SVG"))
        self.master.geometry("600x300")
        #img = PhotoImage(file="flowchart.ico")
        #self.master.iconbitmap(img)
        
     
    def add_text(self):
        self.content = Text(self.master)
        self.content.pack(expand=1,fill='both')
        
    def generate(self):
        self.master.mainloop()
        

    def nouveau(self):
        self.file=""
        self.content.delete("1.0", END)
        
    def fopen(self):
        self.file =  filedialog.askopenfilename(initialdir = "/",title = _("Selectionner un fichier"),filetypes = (("Text Files","*.txt"),(_("Tous les fichiers"),"*.*")))
        if self.file:
            fp = open(self.file,"r",encoding="utf-8")
            r = fp.read()
            self.content.delete("1.0", END)
            self.content.insert("1.0",r)         
            fp.close()
        
    def saveAs(self):
        # create save dialog
        self.file =  filedialog.asksaveasfilename(initialdir = "/",title = _("Enregistrer Sous..."),filetypes = (("Fichier Texte","*.txt"),(_("Tous les fichiers"),"*.*")))
        if self.file:
            if self.file[-4:]!=".txt":
                self.file+=".txt"
            
            f = open(self.file,"w",encoding="utf-8")
            s = self.content.get("1.0",END)
            f.write(s) 
            f.close()
       
        
    def save(self):
        if(self.file ==""):
            self.saveAs()            
        else:
            f = open(self.file,"w",encoding="utf-8")
            s = self.content.get("1.0",END)
            f.write(s) 
            f.close()
    def compile3(self):

        self.les_options=parametres()
        try:
             self.ecran_svg.destroy()
        except:
             pass
        vd=parametres()
        if vd[0]:
             
             self.les_options=vd[1]
             try:
                 self.ecran_svg.destroy()
             except:
                pass
             s = self.content.get("1.0",END)
             self.svg=logigramme(s,self.les_options)

        else:
            
             self.svg=vd[1]
             

              
        f = open("file.svg","w",encoding="utf-8")
        f.write(self.svg)
        f.flush()
        webbrowser.open("file.svg")
        
        
         

    def compile(self):
         global img
         vd=parametres()
         if vd[0]:
             
             self.les_options=vd[1]
             try:
                 self.ecran_svg.destroy()
             except:
                pass
             s = self.content.get("1.0",END)
             self.svg=logigramme(s,self.les_options)

         else:
            
             self.svg=vd[1]



         output=(io.BytesIO(self.svg.encode()))
         drawing=svg2rlg(output)
         mem_image = io.BytesIO()
         renderPM.drawToFile(drawing, mem_image, fmt="png")
         im = Image.open(mem_image)
         self.ecran_svg = Toplevel(self.master) 
         #ecran_svg= Tk()
         self.ecran_svg.title(_("Prévisualiser (png)"))
         #self.ecran_svg.iconbitmap("flowchart.ico")
         menuBar2 = Menu(self.ecran_svg)
         menuFichier2 = Menu(menuBar2,tearoff=0)
         menuBar2.add_command(label = _("Enregistrer SVG"), command=self.SVGsaveAs)
         menuBar2.add_command(label = _("Aide  en ligne"), command=self.aide)
         self.ecran_svg.config(menu = menuBar2)

         img =  itk.PhotoImage(master=self.ecran_svg,image=im)
        
         w_max,h_max=round(self.ecran_svg.winfo_screenwidth()*0.9),round(self.ecran_svg.winfo_screenheight()*0.8)
         w_i,h_i=img.width()+5,img.height()+5
         rapport_w,rapport_h=w_i/w_max,h_i/h_max
         rapport=max(rapport_w,rapport_h)

         if rapport>1:

             im=im.resize((round(w_i/rapport),round(h_i/rapport)))
             img =  itk.PhotoImage(master=self.ecran_svg,image=im)






         canevas=Canvas(self.ecran_svg,bg="white",height=img.height()+10, width=max(img.width(),240)+10)

         canevas.create_image(10, 10, image=img, anchor = NW)

         canevas.pack()

         self.ecran_svg.mainloop()



    def aide(self):
        webbrowser.open('https://site2wouf.fr/logigw_aide.php')

    def sources(self):
        webbrowser.open('https://site2wouf.fr/logigw.php')

    def sponsoring(self):
        webbrowser.open('https://site2wouf.fr/sponsoring.php')    

    def SVGsaveAs(self):

        fichier=filedialog.asksaveasfilename(initialdir = "/",title = "Enregistrer Sous\
        ",filetypes = ((_("Fichier SVG"),"*.svg"),(_("Tous les fichiers"),"*.*")))
        fichier = fichier + ".svg"
        
      
        f = open(fichier,"w",encoding="utf-8")
        
        f.write(self.svg) 
        f.close()

    def param(self):
        message=_("""Pour modifier les paramètres il suffit d'éditer le fichier
config.txt dans le répertoire de l'application.""")
        
        messagebox.showinfo(title="Paramètres", message=message)


    def infolangue(self):
        message=_("""Vous pouvez choisir une autre langue (si disponible) dans le fichier config.txt.
Par defaut, ou en cas d'erreur, logigw est en français !""")
        
        messagebox.showinfo(title=_("Langue"), message=message)
       
    
    def add_menu(self):
        #  barre des menus
        menuBar = Menu(self.master)
        
        #  menu Fichier
        menuFichier = Menu(menuBar,tearoff=0)
        menuBar.add_cascade(label = _("Fichier"), menu=menuFichier)
        menuFichier.add_command(label=_("Nouveau"), command=self.nouveau)
        menuFichier.add_command(label=_("Ouvrir"), command=self.fopen)
        menuFichier.add_command(label=_("Enregistrer"), command=self.save)
        menuFichier.add_command(label=_("Enregistrer sous..."), command=self.saveAs)
        self.master.config(menu = menuBar)
        

        # menu Outils
        menuOutils = Menu(menuBar,tearoff=0)
        menuBar.add_cascade(label = "Logigw", menu = menuOutils)
        menuOutils.add_command(label=_("Previsualiser LQ (png)"),command=self.compile)
        menuOutils.add_command(label=_("Ouvrir dans un navigateur HQ (svg)"),command=self.compile3)
        menuOutils.add_command(label=_("Options"),command=self.param)

        
        # menu Aide
        menuAide = Menu(menuBar,tearoff=0)
        menuBar.add_cascade(label = _("A propos"), menu=menuAide)
        menuAide.add_command(label=_("Aide en ligne"),command=self.aide)
        menuAide.add_command(label=_("Sources et téléchargement"),command=self.sources)
        menuAide.add_command(label=_("Faire un don"),command=self.sponsoring)

        menuBar.add_command(label=self.langue, command=self.infolangue)

        
