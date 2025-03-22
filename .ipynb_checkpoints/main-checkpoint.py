import os
import extract

dossier = os.listdir("content")

def main() :
    for fichier in dossier :
        test = extract.extract_def("content\\"+fichier)
        print("---"+ fichier + "\n")
        for admonition in test:
                print(f"Title: {admonition['front']}")
                print(f"Content: {admonition['back']}\n")

main()