# -*- coding: utf-8 -*-
"""

Genetic Algorithm from scratch

03/2022

"""

import math 
import numpy as np
import random
import time

f = open("position_sample.csv", 'r')

def tab_fichier():
    mesures = []
    for ligne in f:    
        ltemp = ligne.split(';')
        if ltemp[0]!='#t':
            ltempt = float(ltemp[0])
            ltempx = float(ltemp[1])
            ltempy=float(ltemp[2])
            mesures.append((ltempt,ltempx))
    return mesures



def mutation(pres,p01,p02,p03):
    
    if p01=='x':
        p1 = random.randint(-100,100)
    else :
        p1 = random.randint(p01-pres,p01+pres)
        
    if p02=='x':
        p2 = random.randint(-100,100)
    else:
        p2 = random.randint(p02-pres,p02+pres)
        
    if p03=='x':
        p3 = random.randint(-100,100)
    else:
        p3 = random.randint(p03-pres,p03+pres)

    
    if (p1 < -100):
        p1=-100
    if (p1>100):
        p1=100
    
    if (p2 < -100):
        p2=-100
    if (p2>100):
        p2=100

    if (p3 < -100):
        p3=-100
    if (p3>100):
        p3=100
    liste_pop = [p1,p2,p3]
    
    return liste_pop


def mutation_dec(pres,p01,p02,p03):

    p1 = round(random.uniform(p01-pres,p01+pres),3)
    if (p1 < -100):
        p1=-100
    if (p1>100):
        p1=100
    p2 = round(random.uniform(p02-pres,p02+pres),3)
    if (p2 < -100):
        p2=-100
    if (p2>100):
        p2=100
    p3 = round(random.uniform(p03-pres,p03+pres),3)
    if (p3 < -100):
        p3=-100
    if (p3>100):
        p3=100
    liste_pop = [p1,p2,p3]
    
    return liste_pop

def evaluation(liste_pop, liste_xt):
    moyennetemp = 0
    for j in liste_xt:
        result = liste_pop[0]*math.sin(liste_pop[1]*j[0] + liste_pop[2])
        moyennetemp+= abs(abs(result)-abs(j[1]))
    moyennef = moyennetemp/30
       
    return moyennef

    
def croisement(l1,l2):
    l3=[0,0,0]
    for i in range(3):
        r2 = random.randint(0,1)
        if r2==0:
            l3[i] = l1[i]
        if r2==1:
            l3[i] = l2[i]
    return l3


    
    
    
def loop():
    start = time.time()
    old_moy = 100
    lx=tab_fichier()
    lpop = mutation(0,'x','x','x')
    print(lpop)
    step=0
    pres=0
    iterations=0
       
    while(old_moy>0.5):
        iterations+=1
        while(old_moy>1.16):
            iterations+=1
            
            lpop = mutation(pres, lpop[0], lpop[1],lpop[2])
            
            pres = int(old_moy)*6
            new_moy = evaluation(lpop, lx)     
            if new_moy < old_moy:
                print(new_moy,":", lpop) 
                old_moy = new_moy
                step=0
            else:
                step+=1
 
            if (step > 100000):           
                print("reset de l'individu' : ", lpop)
                print('')
                lpop = mutation(0,'x','x','x')
                pres=0
                step=0
                old_moy=100
            if old_moy<1.75:
                lreel=lpop
               

        if old_moy >1:
            pres = old_moy*6
        else:
            pres = old_moy*6
        
        lpop = mutation_dec(pres, lpop[0], lpop[1],lpop[2])

        new_moy = evaluation(lpop, lx)     
        if new_moy <= old_moy:
            print(new_moy,":", lpop) 
            old_moy = new_moy
            step=0
        else:
            step+=1

        if (step > 1000000):
            end=time.time()
            print("reset de l'individu' : ", lpop)
            print("iterations :" ,iterations)
            print('duree :', int(end-start),'sec')
            lpop = lreel         
            pres=0
            step=0
            old_moy=100
    end=time.time()        
    print("------------FIN---------", iterations,"iterations")
    print(lpop) 
    print(int(end-start),'sec')
    


