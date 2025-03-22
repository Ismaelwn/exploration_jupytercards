import json

def writeInFile(content: str, output_file: str):
    """Écrit le contenu extrait dans un fichier."""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)


def extract_character_with_style(d):
    """Extrait les caractères avec style (ex: texte en gras)."""
    results = []
    if "children" in d:
        for child in d["children"]:
            results.extend(extract_character_with_style(child))
    elif "value" in d:
        results.append(d["value"])

    return "".join(results)


def extract_content_from_dict(d: dict):
    """Récupère la partie pertinente du JSON."""
    if "mdast" in d:
        return d["mdast"]
    elif "type" in d:
        return d
    else:
        raise KeyError("Erreur, le fichier ne respecte pas la prédisposition")


def extract_admonition_content_from_file(file_path: str):
    """Extrait le contenu des éléments "admonition" à partir d'un fichier JSON."""
    
    with open(file_path, 'r', encoding='utf-8') as file:
        data = extract_content_from_dict(json.load(file))
    
    result = []

    def traverse(node, parent_title=""):
        if isinstance(node, dict):
            if node.get("type") == "admonition":
                title = ""
                content = []
                code = []

                for child in node.get("children", []):
                    if child.get("type") == "admonitionTitle":  # Récupérer le titre
                        title = "".join(
                            grandchild["value"]
                            for grandchild in child.get("children", [])
                            if "value" in grandchild
                        )
                    elif child.get("type") == "paragraph":  # Récupérer un paragraphe de texte
                        paragraph_content = []
                        for grandchild in child.get("children", []):
                            if "value" in grandchild:
                                paragraph_content.append(grandchild["value"])
                            elif grandchild["type"] == "strong":
                                paragraph_content.append(extract_character_with_style(grandchild))
                        content.append("".join(paragraph_content))
                    elif child.get("type") == "code":
                        code.append(child.get("value"))
                    elif child.get("type") == "list":
                        for item in child.get("children", []):
                            if item.get("type") == "listItem":
                                for subitem in item.get("children", []):
                                    if "value" in subitem:
                                        content.append(subitem["value"])

                # Concaténer le titre et gérer l'imbrication
                full_title = f"{parent_title} > {title}" if parent_title else title
                full_content = "\n".join(content + code)

                if title:
                    result.append({"front": full_title, "back": full_content})

                # Gestion récursive des admonitions imbriquées
                for child in node.get("children", []):
                    if child.get("type") == "admonition":
                        traverse(child, full_title)

            for key, value in node.items():
                traverse(value, parent_title)

        elif isinstance(node, list):
            for item in node:
                traverse(item, parent_title)

    traverse(data)
    return result


# Test avec le fichier fourni
fichier1 = "content/sources.conditions.conditions.json"
fichier2 = "content/test.json"
fichier3 = "content/test2.json"
fichier4 = "content/test3.json"
fichier5 = "content/test4.json"
# Affichage des résultats
admonitions = extract_admonition_content_from_file(fichier1)

'''
for admonition in admonitions:
    if "Définition" in admonition['title'] :
        print(f"Title: {admonition['title']}")
        print(f"Content: {admonition['content']}\n")
'''
