import os
from exploration_jupytercards import toDict
from exploration_jupytercards import file
from exploration_jupytercards import extract




def extract_tools(current_dir):
    chemin = os.path.join(current_dir, "_build")
    content_dir = os.path.join(chemin, "content")
    chemin_json = os.path.join(chemin, "JSON")
    os.makedirs(chemin_json, exist_ok=True)
    print(f"Sortie JSON dans : {chemin_json}")
    
    file_counter = 0
    
    for fichier in os.listdir(os.path.join(current_dir, "_build", "content")):
        chemin_fichier = os.path.join(content_dir, fichier)
        extract.extract_admonition_ast_from_file(chemin_fichier, file_counter)
        file_counter += 1
        
        

           
def toDict_tools(current_dir) :
    l = []
    dossier = os.listdir(current_dir+"/_build/JSON")
    for fichier in dossier:
        if fichier.endswith(".json"):
            dict_ = toDict.convToDict("_build/JSON/"+fichier, current_dir)
            l.append(dict_)
            print(f"--- {fichier} traité ---\n")
    
    file.writeInFile(l, current_dir+"/_build/def_converted.json")

