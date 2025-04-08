import json

def extract_root_titles(node):
    with open(node, 'r', encoding='utf-8') as file:
        data = json.load(file)
    def _(node):
        titles = []
        if isinstance(node, dict) and node.get("type") == "admonition":
            for child in node.get("children", []):
                if child.get("type") == "admonitionTitle":
                    title = "".join(
                        grandchild["value"]
                        for grandchild in child.get("children", [])
                        if "value" in grandchild
                    )
                    if title:
                        titles.append(title)
    
        elif isinstance(node, list):
            for item in node:
                titles.extend(extract_root_titles(item))
    
        return titles
    return " ".join(_(data))

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
    return {"front": extract_root_titles(file_path), "back": lire_fichier("HTML/"+file_path.removeprefix("JSON/")+".html") , "topic" : "computerscience"}




print(convToDict("JSON/definition_10.json"))