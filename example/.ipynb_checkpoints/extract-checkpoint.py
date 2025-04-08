import json
import re
import os

def writeInFile(content: dict, output_file: str):
    """Écrit le contenu extrait dans un fichier JSON."""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4, ensure_ascii=False)

def extract_content_from_dict(d: dict):
    """Récupère la partie pertinente du JSON."""
    if "mdast" in d:
        return d["mdast"]
    elif "type" in d:
        return d
    else:
        raise KeyError("Erreur, le fichier ne respecte pas la prédisposition")

def extract_admonition_ast_from_file(file_path: str, file_counter: int):
    """Extrait le sous-arbre AST des éléments 'admonition' à partir d'un fichier JSON."""
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
                        # Nettoyage du titre
                        titre = re.sub(r"^\s*Définition\s*[:：]\s*", "", value)
                        titre_slug = re.sub(r"[^\w\-]+", "_", titre.strip().lower())
                        if not titre_slug:
                            titre_slug ="Définition "+str(file_counter)
                            first_child["children"][0]["value"] = titre_slug
                        else :
                            first_child["children"][0]["value"] = titre
                        output_file = os.path.join("JSON", f"{titre_slug}.json")
                        file_counter += 1

                        print(f"Écriture : {output_file}")
                        writeInFile(node, output_file)

            for key, value in node.items():
                traverse(value)
        elif isinstance(node, list):
            for item in node:
                traverse(item)

    traverse(data)
    return file_counter

# Création du dossier JSON si inexistant
os.makedirs("JSON", exist_ok=True)

file_counter = 1
dossier = os.listdir("content")
for fichier in dossier:
    if fichier.endswith(".json"):
        file_counter = extract_admonition_ast_from_file(os.path.join("content", fichier), file_counter)
        print(f"--- {fichier} traité ---\n")