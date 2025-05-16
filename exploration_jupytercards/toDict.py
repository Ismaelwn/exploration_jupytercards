import json
from . import extract
import os
from . import file

'''
Code pour créer une liste de dictionnaires stockées format Json
'''

def extract_root_titles(title):
    rtrn = title.removeprefix("JSON/").removesuffix(".json")
    return rtrn.replace("_", " ").capitalize()
    

def lire_fichier(chemin_fichier):
    """
    Lit le contenu d’un fichier texte et le retourne sous forme de chaîne.
    
    :param chemin_fichier: Chemin vers le fichier à lire
    :return: Contenu du fichier (str)
    """
    try:
        with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
            contenu = fichier.read()
        return contenu
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{chemin_fichier}' n'existe pas.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")


def convToDict(file_path): #censé etre une definition uniquement
   return {"front": extract_root_titles(file_path), "back": lire_fichier("HTML/"+file_path.removeprefix("JSON/").removesuffix(".json")+".html") , "topic" : "computerscience"}





