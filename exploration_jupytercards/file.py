import json
import re
import os
import sys

def writeInFile(content: dict, output_file: str):
    """Écrit le contenu extrait dans un fichier JSON."""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4, ensure_ascii=False)