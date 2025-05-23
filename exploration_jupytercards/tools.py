import os
from exploration_jupytercards import toDict
from exploration_jupytercards import file
from exploration_jupytercards import extract
import sys



def extract_tools(current_dir):
    # Argument positionnel : chemin du répertoire « content »
    content_dir = sys.argv[1]
    if not os.path.isdir(content_dir):
        raise FileNotFoundError(f"Le répertoire '{content_dir}' est introuvable.")
    chemin = os.path.join(current_dir, "build_")
    os.makedirs(chemin, exist_ok=True)
    chemin_json = os.path.join(chemin, "JSON")
    os.makedirs(chemin_json, exist_ok=True)
    print(chemin_json)
    
    file_counter = 0
    
    for fichier in os.listdir(content_dir):
        if fichier.endswith(".json"):
            print(fichier)
            chemin_fichier = os.path.join(content_dir, fichier)  # FICHIER SOURCE
            print(chemin_fichier)
            if not os.path.isfile(chemin_fichier):
                raise FileNotFoundError(f"Le fichier '{chemin_fichier}' est introuvable.")
            extract.extract_admonition_ast_from_file(chemin_fichier, file_counter)
            file_counter += 1
            print(f"— {fichier} traité —\n")

           
def toDict_tools(current_dir) :
    l = []
    dossier = os.listdir(current_dir+"/build_/JSON")
    #print(dossier +" 3")
    for fichier in dossier:
        if fichier.endswith(".json"):
            dict_ = toDict.convToDict("build_/JSON/"+fichier, current_dir)
            #print(dict_ +" 4")
            l.append(dict_)
            print(f"--- {fichier} traité ---\n")
    
    file.writeInFile(l, current_dir+"/build_/def_converted.json")

