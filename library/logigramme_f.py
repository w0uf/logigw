#version 4.0.0

from library.Elements_c import *
from library.tqsi import *
from library.erreur_svg import *



def logigramme(fichier,options):
    #constantes
    symbole_commentaire="#"
    debug=0

    #mots clefs

    #print(options)
    debut=options["début"]["prefixe"].split()
    fin=options["fin"]["prefixe"].split()
    es=options["E/S"]["prefixe"].split()
        
    suffixes=["",":",".","?"]

    debut=[x+y for x in debut for y in suffixes]
    fin=[x+y for x in fin for y in suffixes]
    es=[x+y for x in es for y in suffixes]
    #les autres mots sont des instructions


        
    svg="""<?xml version="1.0" encoding="utf-8"?>
    <svg xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="{0}" height="{1}">
        <!-- Created with logigw - https://site2wouf.fr/logigw-->
        <style>
        {2}
        </style>
        <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5"
            markerWidth="6" markerHeight="6"
            orient="auto-start-reverse"
            stroke="black">
          <path d="M 0 0 L 10 5 L 0 10 z" />
        </marker>
        
    <defs>
    """

    style="""
.debut {{ {} }}""".format(options["début"]["style"])
    style+="""
.fin{{ {};}}""".format(options["fin"]["style"])
    style+="""
.es{{ {};}}""".format(options["E/S"]["style"])
    style+="""
.instructions{{ {};}}""".format(options["instructions"]["style"])
    style+="""
.TQ{{ {};}}""".format(options["TQ"]["style"])
    style+="""
.SI{{ {};}}""".format(options["SI"]["style"])
    style+="""
.texte-debut {{ {} }}""".format(options["texte"]["debut"])
    style+="""
.texte-fin{{ {};}}""".format(options["texte"]["fin"])
    style+="""
.texte-es{{ {};}}""".format(options["texte"]["es"])
    style+="""
.texte-instructions{{ {};}}""".format(options["texte"]["instructions"])
    style+="""
.texte-TQ{{ {};}}""".format(options["texte"]["tq"])
    style+="""
.texte-SI{{ {};}}""".format(options["texte"]["si"])



    

 
    objets=[]
    touslesblocs=[]
    a=(x for x in list(fichier.splitlines()) if x.strip()!="")
    
    lb=lesblocs(options,*a)
   
    if lb[0]:
        
        etapes=lb[1]
       
    else:
        return er(lb[1])
    if debug:
        
        print("Les étapes :")
        print(etapes)
    i,j=0,0
    for etape in etapes:
        j+=1
        if debug:
            print("Etape :",j)
        #creation bloc
        objets_etape=[]
        for e in etape:
            #print(e)
            #création objet
            i+=1
                #purge des commentaires
            l=e.split(symbole_commentaire)[0].strip()
            
            if l=="":
                #chaine vide, on ignore
                pass;
            elif l.split(" ")[0].strip().lower() in debut:
                #debut
                objets_etape.append(Debut(str(j)+"."+str(i),l))
                
            elif l.split(" ")[0].strip().lower() in fin:
                #fin
                objets_etape.append(Fin(str(j)+"."+str(i),l))
            elif l.split(" ")[0].strip().lower() in es:
                #es
                objets_etape.append(Es(str(j)+"."+str(i),l))
            elif l.split("_")[0].strip().lower()=="@bloc":
                typebloc=l.split("_")[1].strip().lower()
                part3=l.split("_")[-1].strip()
                ainserer="Bloc_"+str(part3.split(":")[0])
                letexte=part3.split(":")[1]
                suffixe=e.split("###")[-1]
                if debug:
                    print("bloc  à créer :",typebloc)
                    print("Informations :",l)
                    print(".......................")
                    
                #on retrouve l objet à inserer
               
                if typebloc=="tq":
    ##                print("debug-1------------------------------------------------------------> ")
    ##                print(e,etapes,etapes)
                    bool_un=etape.index(e)==len(etape)-1 
    ##                print(bool_un)
                    lobj=Tq(str(j)+"."+str(i),letexte,bool_un,touslesblocs[int(suffixe)])
                    objets_etape.append(lobj)
                    
                elif typebloc=="si":
    ##                print("debug-2-------------------------------------------------------------> ")
    ##                print(e,etapes,etapes)
                    bool_un=False 
    ##                print(bool_un)
                    lobj=Si(str(j)+"."+str(i),letexte,bool_un,touslesblocs[int(suffixe)])
                    objets_etape.append(lobj)

                elif typebloc=="si2":
                      
                    lobj=Si2(str(j)+"."+str(i),letexte,touslesblocs[int(suffixe.split("*")[1])],touslesblocs[int(suffixe.split("*")[0])],False)
                    objets_etape.append(lobj)
        
                        
            else:
                #instruction
                objets_etape.append(Instruction(str(j)+"."+str(i),l.strip()))
            objets.append(objets_etape[-1])
            if debug:
               
                print("objets {}.{} créé : -{}- {},largeur: {}, hauteur: {}, fromx: {}, versx: {}".format(j,i,objets[-1].type,objets[-1].texte,objets[-1].w,objets[-1].h,objets[-1].fromx,objets[-1].versx))
            svg+=objets[-1].svg
        i=0
        #print("création du bloc",j)
        objet_ci=Bloc("Bloc_"+str(j),"",*objets_etape)
        touslesblocs.append(objet_ci)
        objets.append(objet_ci)
        svg+=objets[-1].svg
    svg+="""
    </defs>

    """

    svg=svg.format(objets[-1].w+10,objets[-1].h+10,style) 
    svg+='\n<use xlink:href="#{0}" transform ="translate ({1})" />\n</svg>'.format(objets[-1].id,5)

        
    #print(svg)
    return(svg)
      
    
