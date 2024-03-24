from library.tqsi import *
debug=0

def purge_html(x):
   
    html = { '>': '&gt;',
     '<': '&lt;',
    "'" : '&apos;'}
    
    for old,new in html.items():
        x=x.replace(old,new)
    return x

def formate_texte(x,classe=""):
    #constantes locales

    """Renvoie une liste des lignes construites et purgées
des caractère html illicite, suivi du nombre de lignes et
de la longueur maximum"""
    texte_svg="""<text font-size="12" font-family="Monospace" text-anchor="start" xml:space="preserve" fill="black">\n"""
    
    nb_lettres_max= 22
    mots=x.split()
    lignes=[]
    laligne=""
    plus_grande_ligne=0
    for m in mots:
        if len(laligne)+len(m)+1<nb_lettres_max:
            laligne+=" "+m
           
        else:
            if laligne.strip()!="":
                lignes.append(laligne.strip())
                plus_grande_ligne=max(len(laligne.strip()),plus_grande_ligne)
            laligne=m
    if laligne!="":
        lignes.append(laligne.strip())
        plus_grande_ligne=max(len(laligne.strip()),plus_grande_ligne)

    nl=1
    for l in lignes:
        texte_svg+="""<tspan  class="{2}" x="12" y="{0}" >{1}</tspan>\n""".format(nl*20+2,purge_html(l),classe)
        nl+=1
        
    texte_svg+="</text>"
    
    return texte_svg,len(lignes)*20+20,plus_grande_ligne*8+24



general_svg="""

    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5"
        markerWidth="6" markerHeight="6"
        orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" />
    </marker>\n

"""

connecteur_vertical_svg="""
<line x1="{0}" y1="{1}" x2="{0}" y2="{2}" style="stroke:black;stroke-width:2" marker-end="url(#arrow)"/>\n
"""
def connecteur(x,y):
    return connecteur_vertical_svg.format(x,y,y+30)

def debut_svg(x,c,l,texte):
    
    return """<g id="{0}" ><rect class="debut" width="{1}" height="{2}" rx="20"  stroke="black"   />{3}</g>\n\n""".format(x,c,l,texte)

def fin_svg(x,c,l,texte):
    
    return """<g id="{0}" ><rect class="fin" width="{1}" height="{2}" rx="20"  stroke="black"   />{3}</g>\n\n""".format(x,c,l,texte)

def instruction_svg(x,c,l,texte):
    return """<g id="{0}"><rect width="{1}" height="{2}"  class="instructions" stroke="black"   />{3}</g>\n""".format(x,c,l,texte)

def es_svg(x,c,l,texte):
    return """<g id="{0}" transform="skewX(-20) translate({4})"><rect  width="{1}" height="{2}"  class="es" stroke="black"   />{3}</g>\n\n""".format(x,c,l,texte,round(l*0.364))

def tq_incomplet(x,c,l,texte,bloc):
    #abscisse sommmet gauche: 0
    decal=min(c-bloc.fromx,0)-30
    chaine= """<g id="{}" transform="translate({})">\n<polygon points="{},{} {},{} {},{} {},{}"  class="TQ" stroke="black"/>\\n
    <g transform="translate({} {})">{}</g>\n""".format(x,-decal,c,0,2*c,l,c,2*l,0,l,c/2,l/2,texte)
    chaine+="""<line x1="{0}" y1="{1}" x2="{0}" y2="{2}" style="stroke:black;stroke-width:2" marker-end="url(#arrow)"/>\n""".format(c,2*l,2*l+31)
    chaine+="""<use x="{}" y="{}" xlink:href="#{}" ></use>""".format(c-bloc.fromx,2*l+37,bloc.id)
    chaine+="""<line x1="{0}" y1="{1}" x2="{0}" y2="{2}" style="stroke:black;stroke-width:2" />\n""".format(c-bloc.fromx+bloc.versx,bloc.h+2*l+37,bloc.h+2*l+67)
    chaine+="""<line x1="{0}" y1="{1}" x2="{2}" y2="{1}" style="stroke:black;stroke-width:2" />\n""".format(c-bloc.fromx+bloc.versx,bloc.h+2*l+67,decal)
    chaine+="""<line x1="{0}" y1="{1}" x2="{0}" y2="{2}" style="stroke:black;stroke-width:2" />\n""".format(decal,bloc.h+2*l+67,l)
    chaine+="""<line x1="{0}" y1="{1}" x2="{2}" y2="{1}" style="stroke:black;stroke-width:2" marker-end="url(#arrow)" />\n""".format(decal,l,-5)
    
    return chaine

def si_incomplet(x,c,l,texte,bloc):
    decal=min(c-bloc.fromx,0)
    chaine= """<g id="{}" transform="translate({})">\n<polygon points="{},{} {},{} {},{} {},{}"  class="SI" stroke="black"/>\\n
    <g transform="translate({} {})">{}</g>\n""".format(x,-decal,c,0,2*c,l,c,2*l,0,l,c/2,l/2,texte)
    chaine+="""<line x1="{0}" y1="{1}" x2="{0}" y2="{2}" style="stroke:black;stroke-width:2" marker-end="url(#arrow)"/>\n""".format(c,2*l,2*l+31)
    chaine+="""<use x="{}" y="{}" xlink:href="#{}" ></use>""".format(c-bloc.fromx,2*l+37,bloc.id)
    return chaine
    

si_incomplet_svg="""

<g id="{0}">
<g transform="translate ({3})">
<polygon points="45,0 90,45 45,90 0,45"  style=" fill:white; stroke:black"/>
<text font-size="10" font-family="arial"  fill="black">
<tspan x="20" y="33" font-weight="bold">
SI
</tspan>
<tspan x="8" y="45" font-weight="bold">
{1}
</tspan>
</text>
<line x1="45" y1="90" x2="45" y2="121" style="stroke:black;stroke-width:2" marker-end="url(#arrow)"/>
</g>
<g>
<use x="{4}" y="127" xlink:href="#{2}" ></use>
</g>

"""

si_complet_svg="""

<g id="{0}">

<g transform="translate ({3})">
<polygon points="45,0 90,45 45,90 0,45"  style=" fill:white; stroke:black"/>
<text font-size="10" font-family="arial"  fill="black">
<tspan x="20" y="33" font-weight="bold">
SI
</tspan>
<tspan x="8" y="45" font-weight="bold">
{1}
</tspan>
</text>
<line x1="45" y1="90" x2="45" y2="121" style="stroke:black;stroke-width:2" marker-end="url(#arrow)"/>
<circle cx="90" cy="45" r="4" fill="black"/>
<line x1="90" y1="45" x2="{5}" y2="45" style="stroke:black;stroke-width:2" />
<line x1="{5}" y1="45" x2="{5}" y2="{9}" style="stroke:black;stroke-width:2" />
<line x1="{5}" y1="{9}" x2="{7}" y2="{9}" style="stroke:black;stroke-width:2" />
<line x1="{7}" y1="{8}" x2="{7}" y2="{9}" style="stroke:black;stroke-width:2" />
</g>
<g>
<use x="{4}" y="127" xlink:href="#{2}"></use>



</g>
"""

si2_svg="""<g id="{0}"><g transform="translate ({8})">

<polygon points="45,0 90,45 45,90  0,45"  style=" fill:white; stroke:black"/>
<text font-size="10" font-family="arial"  fill="black">
<tspan x="38" y="18" font-weight="bold">
SI
</tspan>
<tspan x="4" y="45" font-weight="bold">
{1}
</tspan>
</text>
<line x1="45" y1="90" x2="45" y2="121" style="stroke:black;stroke-width:2" marker-end="url(#arrow)"/>
<use x="{3}" y="127" xlink:href="#{2}" ></use>


<circle cx="90" cy="45" r="4" fill="black"/>
<line x1="90" y1="45" x2="{4}" y2="45" style="stroke:black;stroke-width:2" marker-end="url(#arrow)"/>
<line x1="{4}" y1="45" x2="{5}" y2="45" style="stroke:black;stroke-width:2" />
<line x1="{5}" y1="45" x2="{5}" y2="121" style="stroke:black;stroke-width:2" marker-end="url(#arrow)" />
<use x="{6}" y="127" xlink:href="#{7}" ></use>

"""
retour_si_svg="""
<g transform="translate ({5})">
<line x1="{0}" y1="{1}" x2="{0}" y2="{4}" style="stroke:black;stroke-width:2" />
<line x1="{2}" y1="{3}" x2="{2}" y2="{4}" style="stroke:black;stroke-width:2" />
<line x1="{0}" y1="{4}" x2="{2}" y2="{4}" style="stroke:black;stroke-width:2" />
</g></g>
"""

debug_text="""
<text font-size="10" font-family="arial"  fill="{0}">
<tspan x="{2}" y="{3}" font-weight="bold">
{1}
</tspan>
</text>"""

class Elements:
    """ elements """
    def __init__(self,id,texte):
        self.id=id
        self.texte=code_html(texte)
         

    def taille(self):
        return len(self.texte)

class Debut(Elements):
    def __init__(self,id,texte):
        Elements.__init__(self,id,texte)
        a,self.h,self.w=formate_texte(self.texte,"texte-debut")
        self.versx= self.w//2
        self.fromx=self.versx
        self.svg = debut_svg(self.id,self.w,self.h,a)
        self.type="debut"
        self.fromy=self.h
        
class Fin(Elements):
    def __init__(self,id,texte):
        Elements.__init__(self,id,texte)
        a,self.h,self.w=formate_texte(self.texte,"texte-fin")
        self.versx= self.w//2
        self.fromx=self.versx
        self.svg = fin_svg(self.id,self.w,self.h,a)
        self.type="fin"
        self.fromy=self.h
        
class Instruction(Elements):
    def __init__(self,id,texte):
        Elements.__init__(self,id,texte)
        a,self.h,self.w=formate_texte(self.texte,"texte-instructions")
        self.versx= self.w//2
        self.fromx=self.versx
        self.svg = instruction_svg(self.id,self.w,self.h,a)
        self.type="instruction"
        self.fromy=self.h
        
class Es(Elements):
      def __init__(self,id,texte):
        Elements.__init__(self,id,texte)
        a,self.h,self.w=formate_texte(self.texte,"texte-es")
        self.svg = es_svg(self.id,self.w,self.h,a)
        self.w+=round(self.h*0.364) #tan(20)
        self.versx= self.w//2
        self.fromx=self.w//2
        
        self.type="Entree / Sortie"
        self.fromy=self.h

class Bloc():
    def __init__(self,id,texte,*el):
        self.id=id
        self.texte=texte
        self.el=el
        if debug:
            print("Création du bloc {} : {}".format(id,texte))
            print("--------------")
            for x in el:
                print(x.id)
          
            print("--------------")
        vx=0
        translationx=0
        maxtranslationx=0

        
        #premier element
        translationx=0
        chaine='\n<use xlink:href="#{0}" transform="translate({1} {2})"  />'.format(el[0].id,translationx,0)
        svg=chaine
        y=el[0].h
        i=1
        mingauche=0
        maxdroite=el[0].w
        while i<len(el):
            #connecteur
            t1=translationx
            w1=el[i-1].w
            v1=el[i-1].versx
            w2=el[i].w
            f2=el[i].fromx
            translationx+=(-el[i].fromx+el[i-1].versx)
            svg+=connecteur(translationx+el[i].fromx,y)
            y+=36
            chaine='\n<use xlink:href="#{0}" transform="translate({1} {2})"  />'.format(el[i].id,translationx,y)
            mingauche=min(mingauche,translationx)
            maxdroite=max(maxdroite,translationx+el[i].w)
            svg+=chaine
            y+=el[i].h
            
            #element d'indice i
            if debug:
                print("{} < contenant {} < {} - hauteur :{}".format(mingauche,i,maxdroite,y))
                
                
                
            i+=1
        self.w=maxdroite-mingauche
        introsvg='\n <g id="{0}" transform="translate({1})"  >\n'.format(self.id,-mingauche)
        svg=introsvg+svg
       
        self.versx=el[-1].versx+translationx+max(0,-mingauche)
        self.h=y
        
        self.type="Bloc"
        self.fromx=el[0].fromx-mingauche
        
        
       
        
        
        if debug:
            print("Bilan> largeur: {}, hauteur: {}, fromx: {}, versx: {}".format(self.w,self.h,self.fromx,self.versx))
            print()
            svg+='<rect width="{0}" height="{1}" x="{2}" y="{3}" rx="0" fill="black" stroke="black" fill-opacity="0.25"   />'.format(self.w,self.h,0+mingauche,0)
            svg+=debug_text.format("black",self.id,-maxtranslationx,0)
            svg+='<circle cx="{0}" cy="{1}" r="10" fill="black"/>'.format(self.fromx+mingauche,0) #debug
            svg+='<circle cx="{0}" cy="{1}" r="10" fill="black" fill-opacity="0.3"/>'.format(self.versx+mingauche,self.h) #debug
        self.svg=svg+"</g>"

class Tq():
    def __init__(self,id,texte,flag,objetbloc):
        self.id=id
        self.texte=code_html(texte)
        self.flag=flag  #si True c'est un Tq incomplet
        
        
        self.type="Tant que"
        a,hh,ww=formate_texte(self.texte,"texte-TQ")
        self.h=hh+127+objetbloc.h
        decal=min(ww-objetbloc.fromx,0)-30
        self.fromx=ww-decal
        self.versx=max(2*ww,objetbloc.w-objetbloc.fromx+ww)+30
        self.svg=tq_incomplet(self.id,ww,hh,a,objetbloc)
        if not flag:

            self.svg+="""<circle cx="{}" cy="{}" r="4" fill="black"/>\n""".format(2*ww,hh)
            self.svg+="""<line x1="{0}" y1="{1}" x2="{2}" y2="{1}" style="stroke:black;stroke-width:2" />\n""".format(2*ww,hh,self.versx)
            self.svg+="""<line x1="{0}" y1="{1}" x2="{0}" y2="{2}" style="stroke:black;stroke-width:2" />\n""".format(self.versx,hh,self.h)

        self.w=self.versx-decal
        self.versx-=decal
      
        if debug:
            self.svg+='<rect width="{0}" height="{1}" x="{2}" y="{3}" rx="0" fill="red" fill-opacity=" .25" stroke="red"    />'.format(self.w,self.h,decal,0)
            self.svg+=debug_text.format("red",self.id,0,0)
            self.svg+='<circle cx="{0}" cy="{1}" r="10" fill="red"/>'.format(self.fromx+decal,0) #debug
            self.svg+='<circle cx="{0}" cy="{1}" r="10" fill="red" fill-opacity="0.3"/>'.format(self.versx+decal,self.h) #debug
        self.svg+="</g>"
        
        
        
class Si():
    def __init__(self,id,texte,flag,ob):
        self.id=id
        
        self.texte=code_html(texte)
        self.flag=flag  #si True c'est un si incomplet
        
        a,hh,ww=formate_texte(self.texte,"texte-SI")
        decal=min(ww-ob.fromx,0)
        self.svg=si_incomplet(self.id,ww,hh,a,ob)

        self.w=max(2*ww,ww-ob.fromx+ob.w)-min(0,ww-ob.fromx)
        self.h=2*hh+67+ob.h
        self.fromx=ww-decal
        self.versx=ww-ob.fromx+ob.versx
        self.type="Si"
        if not flag: #si complet
            self.versx=max(2*ww,ob.w-ob.fromx+ww)+30
            self.w=self.versx-decal
            self.svg+="""<circle cx="{}" cy="{}" r="4" fill="black"/>""".format(2*ww,hh)
            self.svg+="""<line x1="{0}" y1="{1}" x2="{2}" y2="{1}" style="stroke:black;stroke-width:2" />\n""".format(2*ww,hh,self.versx)
            self.svg+="""<line x1="{0}" y1="{1}" x2="{0}" y2="{2}" style="stroke:black;stroke-width:2" />\n""".format(self.versx,hh,self.h)
            self.svg+="""<line x1="{0}" y1="{1}" x2="{0}" y2="{2}" style="stroke:black;stroke-width:2" />\n""".format(ww-ob.fromx+ob.versx,2*hh+37+ob.h,self.h)
            m=(self.versx+ww-ob.fromx+ob.versx)/2
            self.svg+="""<line x1="{0}" y1="{1}" x2="{2}" y2="{1}" style="stroke:black;stroke-width:2" marker-end="url(#arrow)"/>\n""".format(ww-ob.fromx+ob.versx,self.h,m)
            self.svg+="""<line x1="{0}" y1="{1}" x2="{2}" y2="{1}" style="stroke:black;stroke-width:2" />\n""".format(m,self.h,self.versx)
        if debug:
            self.svg+='<rect width="{0}" height="{1}" x="{2}" y="{3}" rx="0" fill="green" fill-opacity=" .25" stroke="green"    />'.format(self.w,self.h,decal,0)
            self.svg+=debug_text.format("red",self.id,0,0)
            self.svg+='<circle cx="{0}" cy="{1}" r="10" fill="green"/>'.format(self.fromx+decal,0) #debug
            self.svg+='<circle cx="{0}" cy="{1}" r="10" fill="green" fill-opacity="0.7"/>'.format(self.versx,self.h) #debug
        self.versx-=decal

        self.svg+="</g>"
        
class Si2():
    def __init__(self,id,texte,ob1,ob2,flag):
        self.id=id
        self.texte=code_html(texte)
        self.objetbloc1=ob1
        self.objetbloc2=ob2
        self.flag=flag
        a,hh,ww=formate_texte(self.texte,"texte-SI")
        decal=min(ww-ob2.fromx,0)
        self.svg=si_incomplet(self.id,ww,hh,a,ob2)
        self.fromx=ww-decal
        
        droite=max(2*ww,ww-ob2.fromx+ob2.w)+30
        self.svg+="""<circle cx="{}" cy="{}" r="4" fill="black"/>""".format(2*ww,hh)
        self.svg+="""<line x1="{0}" y1="{1}" x2="{2}" y2="{1}" style="stroke:black;stroke-width:2" />\n""".format(2*ww,hh,droite)
        self.svg+="""<line x1="{0}" y1="{1}" x2="{0}" y2="{2}" style="stroke:black;stroke-width:2" marker-end="url(#arrow)"/>\n""".format(droite,hh,2*hh+31)
        self.svg+="""<use x="{}" y="{}" xlink:href="#{}" ></use>""".format(droite-ob1.fromx,2*hh+37,ob1.id)
##        t=max(ob2.fromx-30,0)
##        droite =max(ob2.w+30,90)+30
##        milieu=(droite)/2+45
##        self.h=max(ob1.h,ob2.h)+150
        self.h=2*hh+37 + max(ob1.h,ob2.h)
        self.verx=0
        if not flag:
            self.svg+="""<line x1="{0}" y1="{1}" x2="{0}" y2="{2}" style="stroke:black;stroke-width:2" />\n""".format(ww-ob2.fromx+ob2.versx,2*hh+37+ob2.h,self.h+37)
            self.svg+="""<line x1="{0}" y1="{1}" x2="{0}" y2="{2}" style="stroke:black;stroke-width:2" />\n""".format(droite-ob1.fromx+ob1.versx,2*hh+37+ob1.h,self.h+37)
            self.svg+="""<line x1="{0}" y1="{1}" x2="{2}" y2="{1}" style="stroke:black;stroke-width:2" />\n""".format(ww-ob2.fromx+ob2.versx,self.h+37,droite-ob1.fromx+ob1.versx)
           
           
            self.h+=37
            self.versx=(ww-ob2.fromx+ob2.versx+droite-ob1.fromx+ob1.versx)/2
##            
##        g=45-ob2.fromx +ob2.versx-t
##        d=droite+ob1.versx-ob1.fromx
##        
##        self.svg=si2_svg.format(id,texte,ob2.id,45-ob2.fromx,milieu,droite,droite-ob1.fromx,ob1.id,t)
##        if not flag:
##            #retour des deux blocs!
##            
##            
##            self.svg+=retour_si_svg.format(g,ob2.h+127,d-t,ob1.h+127,h,t)
##            
##            self.h=h
##            
##        else:
##            
##            self.h=0
##           

        
        self.w=droite-ob1.fromx+ob1.w-decal
        
        
        if debug:
            self.svg+='<rect width="{0}" height="{1}" rx="0" fill="white" stroke="green" fill-opacity="0.3"   />'.format(self.w,self.h)
            self.svg+=debug_text.format("green",self.id,0,0)
            self.svg+='<circle cx="{0}" cy="{1}" r="4" fill="green"/>'.format(self.fromx,0) #debug
            self.svg+='<circle cx="{0}" cy="{1}" r="4" fill="green"/>'.format(self.versx,self.h) #debug
        self.svg+="</g>"
        self.type ="Si avec sinon"
        
