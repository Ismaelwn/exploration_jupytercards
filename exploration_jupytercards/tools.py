import os
from exploration_jupytercards import toDict
from exploration_jupytercards import file


def toDict_tools() :
    l = []
    chemin_courant = os.getcwd()
    dossier = os.listdir("build_/JSON")
    for fichier in dossier:
        if fichier.endswith(".json"):
            dict_ = toDict.convToDict("build_/JSON/"+fichier)
            l.append(dict_)
            print(f"--- {fichier} traité ---\n")
    
    file.writeInFile(l, chemin_courant+"build_/def_converted.json")

def extract_tools() :
    l = []
    chemin_courant = os.getcwd()
    dossier = os.listdir("build_/JSON")
    for fichier in dossier:
        if fichier.endswith(".json"):
            dict_ = toDict.convToDict("build_/JSON/"+fichier)
            l.append(dict_)
            print(f"--- {fichier} traité ---\n")
    
    file.writeInFile(l, chemin_courant+"build_/def_converted.json")