import sys
import json
from myst_parser.main import to_docutils
from docutils import nodes

def serialize_node(node):
    """Convertit un nœud docutils en dictionnaire JSON-serializable."""
    serialized = {
        "type": node.tagname,
        "attributes": dict(node.attributes),
        "children": []
    }

    # Si c'est un nœud texte, on ajoute son contenu directement
    if isinstance(node, nodes.Text):
        serialized["value"] = str(node)
    else:
        for child in node.children:
            serialized["children"].append(serialize_node(child))

    return serialized

def md_to_ast_json(md_content):
    """Transforme du texte Markdown (MyST) en AST JSON."""
    doc = to_docutils(md_content)
    return serialize_node(doc)

def main(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    ast = md_to_ast_json(md_content)
    print(json.dumps(ast, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python md_to_ast_json.py fichier.md")
        sys.exit(1)

    main(sys.argv[1])
