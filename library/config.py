import configparser
from library.erreur_svg import *
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




def parametres():
    repertoire=os.path.expanduser('~')+"\\logigw"
    config_txt=os.path.expanduser('~')+"\\logigw\\config.txt"
    try:
        la_config = configparser.ConfigParser(delimiters="°")
        
        if  len(la_config.read(config_txt,encoding="utf-8"))==0:
            os.makedirs(repertoire, exist_ok=True)
            f = open(config_txt,"w",encoding="utf-8")
            f.write(config_de_base)
            f.close()
            la_config.read(config_txt,encoding="utf-8")
        x=la_config._sections
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
       

