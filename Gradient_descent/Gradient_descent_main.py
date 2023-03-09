# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 16:38:37 2022

Descente de gradient

"""
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt
#y = mx + b

""" Part 1 - Brute force """

#2) Ecrire une fonction permettant de calculer l'erreur d'un modele.
#Cette fonction doit prendre en parametre m, b et un ensemble d'exemples(X,Y)
#et retourner l'erreur MSE



f = open("IA_tp6_data.csv", 'r')

def tab_fichier():
    mesures = []
    #mesures = {}
    for ligne in f:    
        ltemp = ligne.split(',')
        ltempx = float(ltemp[0])
        ltempy = float(ltemp[1])
        mesures.append((ltempx,ltempy))
        #mesures[ligne] = (ltempx,ltempy)
    #print(mesures)
    return mesures


data=  tab_fichier()


def calcul_erreur(m,b, data):
    moyennetemp = 0
    for x,y in data:
        result = m*x +b
        moyennetemp+= abs(y - result)
    mse = moyennetemp/len(data)
    #print(m,b, ":", mse)
    return mse
    

def bruteforce():
    valmin=2500
    for m in np.around(np.arange(0,3,0.01),2):
        for b in np.around(np.arange(-10,10,0.01),2):
            moyenne = calcul_erreur(m, b, data)
            if moyenne <valmin:
                print(moyenne, "m :",m,"b :", b)
                valmin=moyenne
        
    return 0
    
""" Part 2 - Descente de gradient """


    
def descente_gradient(m,b):
    m_maj=0
    b_maj =0
    #vtemp1=0
    #vtemp2 =0
    pas = 0.0001
        
    #for x,y in data:
     #   vtemp1 += x*(y-(m*x +b))
     #   vtemp2 += y-(m*x + b)
    grad_m = (-2/len(data))*sum(data[i][0]*(data[i][1]-m*data[i][0] - b) for i in range(len(data)))
    grad_b = (-2/len(data))*sum(data[i][1]-m*data[i][0] - b for i in range(len(data)))
    #grad_m = -(2/len(data))*vtemp1
    #grad_b = -(2/len(data))*vtemp2
    
    m_maj = np.around(m-pas*grad_m, 2)
    b_maj = np.around(b-pas*grad_b,2)
    
    return m_maj, b_maj
    
def loop():
    m=-50
    b=-10
    valmin = 2500

    for i in range(100):
        erreur0 = calcul_erreur(m, b, data)
        #print(m,b )
        (m,b) = descente_gradient(m, b)
        
        
        if erreur0 < valmin:
            print(erreur0, m, b)
        
        
        
   
    print("MSE : ", erreur0)
    return m,b
    
"""
x = [data[i][0] for i in range(len(data))]
y = [data[i][0] for i in range(len(data))]
plt.plot(x,y,'ro')
   """ 
    
    
    
    
    
    
    
    
    
    
    

