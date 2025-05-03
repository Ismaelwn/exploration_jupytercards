import json
import os
import toDict
import extract

l = []
dossier = os.listdir("JSON")
for fichier in dossier:
    if fichier.endswith(".json"):
        dict_ = toDict.convToDict("JSON/"+fichier)
        l.append(dict_)
        print(f"--- {fichier} traité ---\n")

extract.writeInFile(l, "../def_converted.json")