from pathlib import Path
import sys
import configparser
from library2.erreur_svg import *
import os

config_de_base="""[options]
lang ° en
[TQ]
prefixe° tq while répéter repeat pour for
fin° fin_tq end_while endwhile jusqu jusqu'à
style ° fill:rgb(255, 220, 220); stroke:red
[SI]
prefixe° si if
fin° fin_si end_if endif finsi
style ° fill:rgb(255, 220, 220); stroke:red
[SINON]
prefixe° sinon else
[début]
prefixe° début debut begin programme program fonction
style ° fill:rgb(246, 246, 221); stroke:black
[fin]
prefixe° fin end
style ° fill:rgb(195, 195, 171); stroke:black
[E/S]
prefixe ° lire écrire ecrire afficher demander dire print input retourner
style ° fill:rgb(254, 245, 108 ); stroke:black
[instructions]
style ° fill:rgb(156, 255, 146 ); stroke:black
[texte]
debut ° fill: navy; font-style : italic 
fin ° fill: navy; font-style : italic 
es ° fill: blue
instructions° fill:black; font-style: bolder
tq ° fill: red
si ° fill: grey
"""


def lecture_config():


    current = Path(".")
    # print(current.absolute())
    temp = current / "temp"
    while not temp.is_dir():
        try:
            temp.mkdir()
        except:
            print("Le repertoire ", current.absolute(), "est protégé en écriture")

    conf = (temp / "config.txt")
    # print (conf.exists())
    while not conf.exists():
        with conf.open("w") as f:
            try:
                f.write(config_de_base)
            except OSError:
                print('cannot open', arg)
    try:
        with conf.open("r") as f:

            retour = f.read()
    except:
        a = input("erreur de lecture sur config.txt")
        sys.exit()

    return retour



def parametres():
    current = Path(".")
    temp = current / "temp"

    conf = (temp / "config.txt")
    temp = current / "temp"
    la_config = configparser.ConfigParser(delimiters="°")
    la_config.read(conf)
    try:
        la_config = configparser.ConfigParser(delimiters="°")
        la_config.read(conf)
        #print("debug ------ ",la_config.sections())
        x=la_config._sections
        #print(x)
        #les prefixes doivent être disjoints et tous différents!
        chaine=_("""Pas de prefixe pour les "{} " dans le fichier config.txt !""") 
        try:
            prefixes =x["TQ"]["prefixe"].split()
        except:
            return False,chaine.format("TQ")
        if len(prefixes)==0:
            return False,chaine.format("TQ")
        for p in ("SI","SINON","début","fin","E/S"):
            try:
                prefixes +=x[p]["prefixe"].split()
            except:
                return False,er(chaine.format(p))
            if len(x[p]["prefixe"].split())==0:
                return False,er(chaine.format(p))
            
        if len(prefixes)!=len(set(prefixes)):
            return False,er(_("Doublons dans les préfixes dans config.txt!"))
                              
        try:
            fins=x["TQ"]["fin"].split()
        except:
            return False,er(_(""" Pas de définition pour "fin" de "TQ" !"""))

        if len(x["TQ"]["fin"].split())==0:
            return False,er(_(""" Pas de définition pour "fin" de "TQ" !"""))
        try:
         
            fins +=x["SI"]["fin"].split()
        except:
            return False,er(_(""" Pas de définition pour "fin" de "SI" !"""))
        if len(x["SI"]["fin"].split())==0:
            return False,er(_(""" Pas de définition pour "fin" de "SI" !"""))

        if len(fins)!=len(set(fins)):
            return False,er(_("""Doublons dans les définitions de "fin" (TQ-SI) dans config.txt!"""))
    
        return True,x
    except:
        return False, er(_("Erreur fatale dans config.txt"))
       

