import os
from exploration_jupytercards import toDict
from exploration_jupytercards import file
import sys

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
    #  Argument positionnel : chemin du répertoire « content »
    current_dir = os.getcwd()
    content_dir = sys.argv[1]
    #content_par = os.path.dirname(content_dir)
    if not os.path.isdir(content_dir):
        raise FileNotFoundError(f"Le répertoire '{content_dir}' est introuvable.")
    
    os.makedirs(current_dir+"/JSON", exist_ok=True)
    
    file_counter = 0
    for fichier in os.listdir(content_dir):
        if fichier.endswith(".json"):
            chemin = os.path.join(content_dir, fichier)
            extract.extract_admonition_ast_from_file(chemin, file_counter)
            file_counter+=1
            print(file_counter)
            print(f"— {fichier} traité —\n")