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


def convToDict(file_path, direct):
    """
    file_path : chemin du fichier .json (peut inclure 'build_/JSON/' ou non)
    direct : dossier racine courant (ex: dossier du projet)
    """
    # On récupère le nom de base sans extension
    base_name = os.path.basename(file_path).removesuffix('.json')
    html_file_path = os.path.join(direct, "_build", "HTML", base_name + ".html")
    print(base_name.replace("_"," ")),
    return {
        "front": base_name.replace("_"," "),
        "back": lire_fichier(html_file_path),
        "topic": "computerscience"
    }






