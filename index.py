import os
import sys
import extract

# Argument positionnel : chemin du répertoire « content »
content_dir = sys.argv[1]

if not os.path.isdir(content_dir):
    raise FileNotFoundError(f"Le répertoire '{content_dir}' est introuvable.")

os.makedirs("JSON", exist_ok=True)

file_counter = 1
for fichier in os.listdir(content_dir):
    if fichier.endswith(".json"):
        chemin = os.path.join(content_dir, fichier)
        file_counter = extract.extract_admonition_ast_from_file(chemin, file_counter)
        print(f"— {fichier} traité —\n")
