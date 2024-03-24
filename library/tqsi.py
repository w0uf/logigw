##gerer tq et si 
##laliste[] est une liste d instructions
##qui contient des tq et des fin_tq, des si et des fin_si
##on veut remplacer iterativement les blocs les plus imbriqués par des blocs


html = { '>': '&gt;',
         '<': '&lt;',
        "'" : '&apos;'}
 
def code_html(chaine):
    propre = ''
 
    for c in chaine:
        if c in html:
            propre += html[c]
        else:
            propre += c
 
    return propre


def est_bloc(ligne):
    """ligne est une chaine, la fonction renvoie
vraie si c'est une instruction en rapport avec si ou tq
fin ou debut
"""
    ligne_liste=[x.strip() for x in ligne.lower().strip().split(" ")]
    if len(ligne_liste)>1 and ligne.lower().strip().split(" ")[0].strip() in marqueur_fin:
        return ligne_liste[1] in marqueur_tq+marqueur_si
    
    marqueur=marqueur_tq+marqueur_fin_tq+marqueur_si+marqueur_fin_si
    return ligne_liste[0] in marqueur

def est_tq(ligne):
    return ligne.lower().strip().split(" ")[0].strip() in marqueur_tq

def est_si(ligne):
    return ligne.lower().strip().split(" ")[0].strip() in marqueur_si


def est_fin_tq(ligne):
    ligne_liste=[x.strip() for x in ligne.lower().strip().split(" ")]
    if len(ligne_liste)>1 and ligne.lower().strip().split(" ")[0].strip() in marqueur_fin:
        return ligne_liste[1] in marqueur_tq
    return ligne_liste[0] in marqueur_fin_tq

def est_fin_si(ligne):
    ligne_liste=[x.strip() for x in ligne.lower().strip().split(" ")]
    if len(ligne_liste)>1 and ligne.lower().strip().split(" ")[0].strip() in marqueur_fin:
        return ligne_liste[1] in marqueur_si
    return ligne_liste[0] in marqueur_fin_si


def est_fin(ligne):
    return est_fin_tq(ligne) or est_fin_si(ligne)

def est_debut(ligne):
    return est_tq(ligne) or est_si(ligne)

def est_sinon(ligne):
    return str(ligne).lower().strip() in marqueur_sinon




    

def lesblocs(options,*arg):
    global  marqueur_tq,marqueur_fin_tq,marqueur_si,marqueur_fin_si,marqueur_sinon,marqueur_fin
    marqueur_tq=options["TQ"]["prefixe"].split()
    marqueur_fin_tq=options["TQ"]["fin"].split()
    marqueur_si=options["SI"]["prefixe"].split()
    marqueur_fin_si=options["SI"]["fin"].split()
    marqueur_sinon=options["SINON"]["prefixe"].split()
    marqueur_fin=options["fin"]["prefixe"].split()
    
    laliste=[str(x) for x in arg]
    if len (laliste)==0:
        return [False,_("Pas de code à traiter...")]
    rang=[]
    tq,si=0,0
    pile=[]
    last=""
    for l in laliste:
        if not est_bloc(l):
            last="autre"
        elif est_tq(l):
            tq+=1
            pile.append("tq")
            last="tq"
        elif est_si(l):
            si+=1
            pile.append("si")
            last="si"
        elif est_fin_tq(l) and tq>0 and pile[-1]=="tq" and last!="tq" :
            tq-=1
            del pile[-1]
            last="fin_tq"
               
        elif est_fin_si(l) and si>0 and pile[-1]=="si" and last !="si":
            si-=1
            del pile[-1]
            last="fin_si"
        else:
            return [False,_("Erreur fatale dans le code ! ")]
            
            

        rang.append(tq+si)
            
    if tq!=0 or si!=0:
        return [False,_("Erreur fatale dans le code ! ")]
    else:
     #on ajoute 0.5 à tous les fin_ en enleve 0.5 aux debuts
        for k in range(len(laliste)):
            if est_fin(laliste[k]):
                rang[k]+=0.5
            if est_debut(laliste[k]):
                rang[k]-=0.5


        blocs=[]
        rang_bloc=0
        fini=False
        while not fini:         

            lemax=max(rang)

            if lemax==0 or lemax==min(rang):
                fini=True
            #on trouve le premier bloc à traiter
            k=0
            
            bloc=[]
            bloc2=[]
            nb_sinon=0
            while rang[k]!=lemax:
                k+=1
            l=k
            #texte=laliste[l-1].split(" ",1)[-1]
            texte=laliste[l-1]
            if est_si(laliste[l-1]):
                      b="si"
                                            
            else:
                      b="tq"

            #print("texte :",texte,b)      
            while l<len(laliste):
                
                if rang[l]==lemax:
                    if est_sinon(laliste[l]):
                        nb_sinon+=1
                        
                        if nb_sinon>1 or b=="tq" or len(bloc)==0:
                            return [False,_("Erreur fatale dans le code ! ")]
                        else:
                            bloc2=[x for x in bloc]
                            bloc=[]
                            #print ("bloc2",bloc2)
                    else:                          
                        bloc.append(laliste[l])
                else:
                    l=len(laliste)
                l+=1
            #print("bloc 1 et 2",bloc,bloc2)
            #On détruit ce bloc dans rang et laliste et on le reference
            if len(bloc2)==0:
                
              
                rang_bloc+=1
                del rang[k-1:k+1+len(bloc)]
               
                del laliste[k-1:k+1+len(bloc)]
                rang.insert(k-1,lemax-1)
                blocs.append(bloc)
                laliste.insert(k-1,"@bloc_"+b+"_"+str(rang_bloc)+":"+texte+"###"+str(blocs.index(bloc)))
                
             
            else:
               
                rang_bloc+=1
                del rang[k-1:k+1+len(bloc2)+len(bloc)+1]
               
                del laliste[k-1:k+1+len(bloc2)+len(bloc)+1]
              
                rang.insert(k-1,lemax-1)
                blocs.append(bloc2)
                blocs.append(bloc)
                laliste.insert(k-1,"@bloc_"+b+"2_"+str(rang_bloc)+":"+texte+"###"+str(blocs.index(bloc2))+"*"+str(blocs.index(bloc)))
                
               
  
        return [True,blocs]
            
                
        
