# -*- coding: utf-8 -*-
# Importation des bibliothèques nécessaires
from tkinter import *
from tkinter import filedialog
from library2.library import*
import gettext
gettext.install("main")
options=parametres()

#print(options[0],options[1]["options"]["lang"])

if options[0]:
    try: 
        gettext.find("langues")
        traduction = gettext.translation("langue",localedir='locales', languages=[options[1]["options"]["lang"]])
        traduction.install()
        lalangue=str(options[1]["options"]["lang"])
    except:
        
        lalangue="fr"
else:
    gettext.install("")
    lalangue="fr"



root = Win("root","",lalangue)

root.create()
root.add_text() 
root.add_menu() 
root.generate()
