# @title Ricorsivamente
from itertools import product
import re
class Nodo:
  def __init__(self,name,parent=None):
    self.name=name
    self.left=None
    self.right=None
    self.parent=parent

    self.vector=[]


  def stampa(self, livello=0): #funzione di stampa, suggerita dal prof
    spazio=" "*livello+self.name+"\n"
    if self.left:
      spazio+=self.left.stampa(livello+1)

    if self.right:
      spazio+=self.right.stampa(livello+1)
    return spazio

  def __repr__(self):
   return self.stampa()

  def values(self,dizionario):
    self.iter = [x for x in self.name]
    for x in range(len(self.iter)):
      if self.iter[x] in dizionario:
        self.iter[x] = str(dizionario[self.iter[x]])
    self.stringa=''.join(self.iter)
    #print(self.stringa, eval(self.stringa))
    return eval(self.stringa)

  def ld_values(self, relazione, conta_atomici):
    U=[x for x in range(1,100)]
     #contiamo quanti P[*x] ci sono nella preposizione

    prod=list(product(U, repeat=conta_atomici+1))

    #print(prod)
    risultati=[eval(relazione.replace('x', str(x))) for x in U[:4]] #calcolo i risultati della relazione
    counter=0
    filter_list=[]
    for num in range(len(risultati)):  # per ogni numero nei risultati scorro attraverso il prodotto cartesiano di U x U x ... U finche' non trovo le ennuple che soddisafano la relaizone

      for prod_row in prod:
        valid=[]
        for element in prod_row:
          if counter==0:
            if element==U[num]:  #il primo elemento della ennupla deve essere l'elemento del insieme universo
              valid.append(U[num])
              pass
            else: #se non parte gia' cosi', esco e vado alla prossima riga
              break
          else:
            if element == risultati[num]:  #se l'elemento e' uguale ai risultati indice num , appendo l'elemento, senno' esco dalla riga direttamente
              valid.append(element)
            else:
              break
          if counter==conta_atomici: #se il counter raggiunge il numero di predicati atomici, appendo a filter_list, valid, una lista dove appendo temporaneamente le variabili in fase di check
            filter_list.append(valid)
          counter+=1
        counter=0
    print('insieme Universo (Ristretto da 1 a 4): ',filter_list)
    return filter_list

  def Truthcheck(self, filter_list,variable, *argv):
    if len(argv) == 1:
      for row in argv:
        lst=row
    elif len(argv) >1:
      lst=[]
      for row in argv:
        lst.append(row)
    elif len(argv)==0:
      raise Exception('Nessun insieme da comparare')

    #print(self.name)
    match self.name[0]:
      case 'P':
        if variable in self.name:
          if lst in filter_list:
            self.vector.append(True)
          else:
            self.vector.append(False)
     

    if self.left:
      self.left.Truthcheck(filter_list,variable, lst)
    if self.right:
      self.right.Truthcheck(filter_list,variable, lst)

  def update_vector(self): #questa funzione scorre attraverso l'albero e non fa nulla, finche' non arriva in basso
    button=False

    if self.left:
      self.left.update_vector()
    if self.right:
      self.right.update_vector()

    if self.left is None and self.right is None: #appena arriva in basso, attiva un bottone che chiama una funzione
      button=True 

    if button==True:
      self.myfunc()

  def myfunc(self, change=False): 
      '''
      'questa funzione ha un parametro opzionale messo a false. di
      default, passa i valori di self.vector al suo parent, finche non raggiunge un quantificatore' 
      ''' 
      if change==False:


        if self.parent:
          for element in self.vector:
              self.parent.vector.append(element)
          if 'V' not in self.name and 'E' not in self.name:
            self.vector.clear()
          self.parent.myfunc()
      else:
        #print(self.name, self.vector)
        if self.parent:
          self.parent.vector.clear()
          for element in self.vector:
              self.parent.vector.append(element)
          if 'V' not in self.name and 'E' not in self.name:
            self.vector.clear()

          self.parent.myfunc(change=True)

      # print(self.name, self.vector)

  def opera(self):
    match self.name:
      case 'A':
        if self.left.vector !=[] and self.right.vector!=[]:
          self.vector=[eval(f'{x} and {y}') for (x, y) in zip(self.left.vector,self.right.vector)]
          self.myfunc(change=True)
      case 'O':
        if self.left.vector !=[] and self.right.vector!=[]:
          self.vector=[eval(f'{x} or {y}') for (x, y) in zip(self.left.vector,self.right.vector)]
          self.myfunc(change=True)
      case 'N':
        if self.vector !=[]:
          self.vector=[eval(f'not {x}') for x in self.vector]
          self.myfunc(change=True)


    if self.left:
      self.left.opera()
    if self.right:
      self.right.opera()

  def finalmente(self):
  
    match self.name[0]:
      case 'V':
        self.valore_V=all(self.vector)
        print(self.name,self.valore_V)
      case 'E':
        self.valore_E=any(self.vector)
        print(self.name, self.valore_E)

    if self.left:
      self.left.finalmente()
    if self.right:
      self.right.finalmente()
    

def costruisci(albero, nodo):
  nodo_corrente=nodo
  x=0
  while x < len(albero):
    match albero[x]:

      case '(':
        nodo_sinistro=Nodo('',parent=nodo_corrente)
        nodo_corrente.left=nodo_sinistro
        nodo_corrente=nodo_sinistro
      case ')':
        nodo_corrente=nodo_corrente.parent
      case 'E' | 'V':
        nodo_corrente=nodo_corrente.parent
        nodo_corrente.left=None
        nodo_corrente.name=albero[x:x+2]
        nodo_destro=Nodo('', nodo_corrente)
        nodo_corrente.right=nodo_destro
        nodo_corrente=nodo_destro
        x+=1

      case 'P':
        for j in range(x,len(albero)):
          if albero[j]==']':
            break
        nodo_corrente.name=albero[x:j+1]
        nodo_corrente=nodo_corrente.parent
        x=j

      case 'A' | 'O':
        #print(albero[x])
        nodo_corrente.name=albero[x]
        nodo_destro=Nodo('', nodo_corrente)
        nodo_corrente.right=nodo_destro
        nodo_corrente=nodo_destro
      case 'N' :
        nodo_corrente=nodo_corrente.parent
        nodo_corrente.left=None
        nodo_corrente.name=albero[x]
        nodo_destro=Nodo('', nodo_corrente)
        nodo_corrente.right=nodo_destro
        nodo_corrente=nodo_destro
      case _:
        print(albero[x])
        nodo_corrente.name=albero[x]
        nodo_corrente=nodo_corrente.parent


    x+=1

def main():
  A='(EyP[xy])'.replace(' and ', 'A').replace('not ','N').replace(' or ', 'O')
  B='(Vx((EyP[xy]) or (EzP[xz]))'.replace(' and ', 'A').replace('not ','N').replace(' or ', 'O')
  C='(Vx(EyP[xy]))'.replace(' and ', 'A').replace('not ','N').replace(' or ', 'O')
  D='((Vx(EyP[xy])) and (Vy(EzP[xz])))'.replace(' and ', 'A').replace('not ','N').replace(' or ', 'O')


  p1=Nodo(A)
  p2=Nodo(B)
  p3=Nodo(C)
  p4=Nodo(D)

  def build(p2,B):
    relazione='x+1' #la relazione di partenza

    lista=p2.ld_values(relazione,1)
    costruisci(B,p2)
    Ins=[[1,1],[2,5],[3,9],[4,16]]  #preposizione -> Vx: Ey:P[xy] dove P= x^2 y=A
    Ins2=[[1,2],[2,3],[3,4],[4,5]]  #elementi che ho
    for x in range(len(Ins)):
        p2.Truthcheck(lista,'y',Ins[x])
        #p2.Truthcheck(lista,'z',Ins2[x])
    p2.update_vector()
    p2.opera()
    return p2.finalmente()    
  
  #build(p1,A) # commenta la seconda riga del ciclo
  build(p2,B)  # togli il commento dalla seconda riga del ciclo
  #build(p3,C) # commenta la seconda riga del ciclo
  build(p4,D)  # togli il commento dalla seconda riga del ciclo
  
  
main()

