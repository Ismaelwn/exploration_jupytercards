import os
import extract

dossier = os.listdir("content")

def main() :
    for fichier in dossier :
        if fichier.endswith(".json" ) :
            test = extract.extract_def("content\\"+fichier)
            print("---"+ fichier + "\n")
        

main()