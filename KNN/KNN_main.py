# -*- coding: utf-8 -*-
"""
Created on Thu May  5 22:42:22 2022

Projet knn DIA - classification challenge
"""

import collections
from collections import OrderedDict
import random as r
import time
import numpy as np

#Crée 2 bases de données : une d'apprentissage et une de test
#contant chacune aléatoirements 50% des données du fichier 
def Creation_bases_Alea(ldata, lpredata):

    all_data = ldata+lpredata   
    
        
    #Mélange aléatoire des valeurs de la liste
    #et création des 2 listes 
    r.shuffle(all_data)
        
    data_test = all_data[800:]
    data_train = all_data[:200]
               
    return (data_train,data_test)


def Creation_base_preTest():
    f = open("preTest.txt", "r" )
    all_data = []    
    lignes = f.readlines()    
    
    for i in range(0, len(lignes)):
        ldonnee = lignes[i].split(';')
        ltemp=[]
        for j in range(0,10):
            ltemp.append(float(ldonnee[j]))
        
        ltemp.append(int(ldonnee[10][0]))   
        all_data.append(ltemp)
        
    all_data = Centrer_reduire(all_data)
    #print("base PreTest créée.")                    
    return all_data

def Creation_base_data():
    f = open("data.txt", "r" )
    all_data = []    
    lignes = f.readlines()    
    
    for i in range(0, len(lignes)):
        ldonnee = lignes[i].split(';')
        ltemp=[]
        for j in range(0,10):
            ltemp.append(float(ldonnee[j]))
        
        ltemp.append(int(ldonnee[10][0]))   
        all_data.append(ltemp)
        
    all_data = Centrer_reduire(all_data)
    #print("base data créée.")
                         
    return all_data


def Centrer_reduire(liste_valeurs):
    
    liste_moyennes = [0,0,0,0,0,0,0,0,0,0]
    liste_ecarts_types = [0,0,0,0,0,0,0,0,0,0]
    liste_sortie =[]
    #calcul moyenne
    for i in range(0,10):
        for indiv in liste_valeurs:     
            liste_moyennes[i] += indiv[i]
            
        liste_moyennes[i] = liste_moyennes[i]/len(liste_valeurs)
    
    #calcul ecart-type
    for i in range(0,10):
        for indiv in liste_valeurs:
            liste_ecarts_types[i]+=pow(liste_moyennes[i]-indiv[i],2)
        liste_ecarts_types[i] = pow(liste_ecarts_types[i]/len(liste_valeurs), 0.5)
   
    #print(liste_moyennes)
    #print(liste_ecarts_types)
    #calcul données centrées réduites
    for indiv in liste_valeurs:
        ltemp=[]
        for i in range(0,10):
            ltemp.append((indiv[i]-liste_moyennes[i])/liste_ecarts_types[i])
        ltemp.append(indiv[10])
        liste_sortie.append(ltemp)
        
    return liste_sortie

def Centrer_reduire2(liste_valeurs):
    
    liste_moyennes = [0,0,0,0,0,0,0,0,0,0]
    liste_ecarts_types = [0,0,0,0,0,0,0,0,0,0]
    liste_sortie =[]
    
    #calcul moyenne
    for i in range(0,10):
        for indiv in liste_valeurs:     
            liste_moyennes[i] += indiv[i]
            
        liste_moyennes[i] = liste_moyennes[i]/len(liste_valeurs)
    
    #calcul ecart-type
    for i in range(0,10):
        for indiv in liste_valeurs:
            liste_ecarts_types[i]+=pow(liste_moyennes[i]-indiv[i],2)
        liste_ecarts_types[i] = pow(liste_ecarts_types[i]/len(liste_valeurs), 0.5)
   

    #calcul données centrées réduites
    for indiv in liste_valeurs:
        ltemp=[]
        for i in range(0,10):
            ltemp.append((indiv[i]-liste_moyennes[i])/liste_ecarts_types[i])

        liste_sortie.append(ltemp)
        
    return liste_sortie


def calcul_moyenne(l_reference, l_inconnu, k):
   
    dico_moyennes = OrderedDict()
    for val in l_reference:
        somme=0
        for index in range(0,10):
            somme+= abs(val[index] - l_inconnu[index])
        moyenne = round((somme/10),4)
        dico_moyennes[str(val)] = moyenne
        

    dico_trie = OrderedDict(sorted(dico_moyennes.items(), key=lambda t: t[1]))
    k_voisins = {}
    valeurs = list(dico_trie.values())
    cles = list(dico_trie.keys())
    for i in range(0,k):
        k_voisins[cles[i]] = valeurs[i]
    
    return k_voisins


        
def reponse(dico_knn):
    dstats = {}
    for i in dico_knn:
        ltemp = eval(i)
        categorie = ltemp[10]
        if categorie  not in dstats:
            dstats[categorie] = 1
        else:
            dstats[categorie]+=1
    dtri = OrderedDict(sorted(dstats.items(), key=lambda t: t[1]))
    cles = list(dtri.keys())
    nom_element = cles[-1]

    
    return nom_element
            
        
def Recherche_type(k,l_base,l_test):

    f_rep = open("reponses.txt", "w")
   
    for l_indiv in l_test:
           
        dknn = calcul_moyenne(l_base, l_indiv,k)
       
        result = reponse(dknn)
        f_rep.write(str(result))
        f_rep.write('\n')
        
    print('Fichier rempi.' )


def Calcul_Succes(k,l_base,l_test):

    succes = 0
    echecs = 0
   
    for l_indiv in l_test:
           
        dknn = calcul_moyenne(l_base, l_indiv,k)      
        result = reponse(dknn)
        
        if result == l_indiv[10]:
            succes+=1
        else:
            echecs+=1
        taux_succes = round(((succes)/(succes+echecs)*100),5)

    print('taux :',taux_succes,'% | k=',k )
    return (taux_succes)
        
    


#Effectue le knn sur 100 bases différentes pour chaque K 
#et renvoie la liste triée des K dont la moyenne est la plus élevée
def TestDesK():
    
    listeKs = []
    
    for k in range(10,35):
        ltaux = []
        for i in range(15):
            l_b1 = Creation_base_data()
            l_t1 = Creation_base_preTest()
                
            (l_base, l_test) =Creation_bases_Alea(l_b1, l_t1)
            taux = Recherche_type(k, l_base, l_test)
            ltaux.append(taux)
        
        score_moyen = np.mean(ltaux)
        kscore = (k, score_moyen)
        listeKs.append(kscore)
        print(listeKs)
        
    k_tries = sorted(listeKs, key=lambda x: x[1], reverse=True)
    print("-----------  FIN  --------------")
    for i in liste_k:
        print(i)
        
    return k_tries


def Creation_base_finalTest():
    f = open("predictions.txt", "r" )
    all_data = []    
    lignes = f.readlines()    
    
    for i in range(0, len(lignes)):
        ldonnee = lignes[i].split(';')
        ltemp=[]
        for j in range(0,10):
            ltemp.append(float(ldonnee[j]))
          
        all_data.append(ltemp)
        
    all_data = Centrer_reduire2(all_data)
                
    return all_data



def AppliKnn(k):
    
    #création base de test 
    l_b1 = Creation_base_data()
    l_t1 = Creation_base_preTest()                
    l_base = l_b1 + l_t1
    
    #Création base à prédire
    l_final_test = Creation_base_finalTest()
    Recherche_type(k, l_base, l_final_test)
    


#AppliKnn(13)






