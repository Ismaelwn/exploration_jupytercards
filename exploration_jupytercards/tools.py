import os
import sys
from exploration_jupytercards import toDict, file, extract

def extract_tools(current_dir):
    # Récupère l'argument positionnel (répertoire source « content »)
    if len(sys.argv) < 2:
        raise ValueError("Veuillez spécifier le répertoire 'content' en argument.")
    content_dir = sys.argv[1]

    if not os.path.isdir(content_dir):
        raise FileNotFoundError(f"Le répertoire '{content_dir}' est introuvable.")

    # Création des répertoires de sortie
    chemin = os.path.join(current_dir, "build_")
    chemin_json = os.path.join(chemin, "JSON")
    os.makedirs(chemin_json, exist_ok=True)

    print(f"[INFO] Fichiers JSON seront enregistrés dans : {chemin_json}")
    file_counter = 0

    for fichier in os.listdir(content_dir):
        chemin_fichier = os.path.join(content_dir, fichier)

        if fichier.endswith(".md"):
            # Appelle `myst build` en ligne de commande sur chaque fichier Markdown
            os.system(f"myst build --output {chemin_json} {chemin_fichier}")

        elif fichier.endswith(".json"):
            if not os.path.isfile(chemin_fichier):
                raise FileNotFoundError(f"Le fichier '{chemin_fichier}' est introuvable.")
            extract.extract_admonition_ast_from_file(chemin_fichier, file_counter)
            file_counter += 1
            print(f"— {fichier} traité —\n")


def toDict_tools(current_dir):
    liste_dicts = []
    dossier_json = os.path.join(current_dir, "build_/JSON")

    for fichier in os.listdir(dossier_json):
        if fichier.endswith(".json"):
            chemin = os.path.join("build_/JSON", fichier)
            dict_ = toDict.convToDict(chemin, current_dir)
            liste_dicts.append(dict_)
            print(f"--- {fichier} converti en dictionnaire ---\n")

    sortie = os.path.join(current_dir, "build_/def_converted.json")
    file.writeInFile(liste_dicts, sortie)
    print(f"[INFO] Fichier JSON global écrit dans : {sortie}")
