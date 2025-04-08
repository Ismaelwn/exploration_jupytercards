import os
import extract
# Création du dossier JSON si inexistant
os.makedirs("JSON", exist_ok=True)

file_counter = 1
dossier = os.listdir("content")
for fichier in dossier:
    if fichier.endswith(".json"):
        file_counter = extract.extract_admonition_ast_from_file(os.path.join("content", fichier), file_counter)
        print(f"--- {fichier} traité ---\n")