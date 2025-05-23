import json
import re
import os
import sys
from . import file


def extract_content_from_dict(d: dict):
    """Récupère la partie pertinente du JSON."""
    if "mdast" in d:
        return d["mdast"]
    elif "type" in d:
        return d
    else:
        raise KeyError("Erreur, le fichier ne respecte pas la prédisposition")
        

def list_index_entries(data):
    """
    Liste les indexEntries avec leur nom dans un dictionnaire.
    
    Args:
        data (dict): Dictionnaire contenant les données à parcourir.
        
    Returns:
        list: Liste des indexEntries avec leur nom.
    """
    index_entries_list = []
    
    def traverse(node):
        # Si le nœud contient des indexEntries, on les extrait
        if 'indexEntries' in node:
            for entry in node['indexEntries']:
                index_entries_list.append(entry['entry'])
        
        # Parcours des enfants du nœud
        if 'children' in node:
            for child in node['children']:
                traverse(child)

    # Démarrer la traversée du dictionnaire
    traverse(data)
    
    return index_entries_list
    

def extract_admonition_ast_from_file(file_path: str, file_counter: int):
    """Extrait le sous-arbre AST des éléments 'admonition' à partir d'un fichier JSON."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = extract_content_from_dict(json.load(f))

    def traverse(node):
        #print("ez")
        nonlocal file_counter
        if isinstance(node, dict):
            #print("ez2")
            if node.get("type") == "admonition" and node.get("children"):
                first_child = node["children"][0]
                if first_child.get("children") and "value" in first_child["children"][0]:
                    #print("ez3")
                    value = first_child["children"][0]["value"]
                    if "Définition" in value:
                        #print("ez4")
                        index_e = list_index_entries(node) 
                        if len(index_e) != 0 :
                            for index in index_e :
                                titre_slug = re.sub(r"[^\w\-]+", "_", index.strip().lower())
                                output_file = os.path.join("build_/JSON", f"{titre_slug}.json")
                                print(f"Écriture : {output_file}")
                                file.writeInFile(node, output_file)
                        else :
                            print("pas de titre, actions par defaut")
                            titre = re.sub(r"^\s*Définition\s*[:：]\s*", "", value)
                            titre_slug = re.sub(r"[^\w\-]+", "_", titre.strip().lower())
                            if not titre_slug:
                                    titre_slug ="Définition "+str(file_counter)
                                    first_child["children"][0]["value"] = titre_slug
                            else :
                                    first_child["children"][0]["value"] = titre
                                    output_file = os.path.join("build_/JSON", f"{titre_slug}.json")
                                    file_counter += 1
                                    print(f"Écriture : {output_file}")
                                    file.writeInFile(node, output_file)

            for key, value in node.items():
                traverse(value)
        elif isinstance(node, list):
            for item in node:
                traverse(item)

    traverse(data)
    return file_counter