import json
import re
import os

def writeInFile(content: dict, output_file: str):
    """Écrit le contenu extrait dans un fichier JSON."""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4, ensure_ascii=False)  # Conversion en JSON

def extract_content_from_dict(d: dict):
    """Récupère la partie pertinente du JSON."""
    if "mdast" in d:
        return d["mdast"]
    elif "type" in d:
        return d
    else:
        raise KeyError("Erreur, le fichier ne respecte pas la prédisposition")

def extract_admonition_ast_from_file(file_path: str, file_counter: int):
    """Extrait le sous-arbre AST des éléments "admonition" à partir d'un fichier JSON."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = extract_content_from_dict(json.load(file))
    
    def traverse(node):
        nonlocal file_counter
        if isinstance(node, dict):
            if node.get("type") == "admonition" and node.get("children"):
                first_child = node["children"][0]
                if first_child.get("children") and "value" in first_child["children"][0]:
                    value = first_child["children"][0]["value"]
                    if "Définition" in value:
                        first_child["children"][0]["value"] = re.sub(r"^\s*Définition\s*[:：]\s*", "", value)
                        
                        # Génération d'un numéro unique pour chaque fichier
                        output_file = os.path.join("JSON", f"definition_{file_counter}.json")
                        file_counter += 1  # Incrémente le compteur
                        
                        print(f"Écriture : {output_file}")
                        writeInFile(node, output_file)  # Stocke tout le sous-arbre
            
            # Parcours récursif
            for key, value in node.items():
                traverse(value)
        elif isinstance(node, list):
            for item in node:
                traverse(item)
    
    traverse(data)
    return file_counter

# Création du dossier JSON si inexistant
os.makedirs("JSON", exist_ok=True)

file_counter = 1  # Initialisation du compteur global
dossier = os.listdir("content")
for fichier in dossier:
    if fichier.endswith(".json"):
        file_counter = extract_admonition_ast_from_file(os.path.join("content", fichier), file_counter)
        print(f"--- {fichier} traité ---\n")
