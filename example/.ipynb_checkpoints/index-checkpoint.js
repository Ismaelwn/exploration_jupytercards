import fs from 'node:fs/promises'
import { readdir } from 'fs/promises';
import { join } from 'path';

/**
 * Convertit un AST MyST en HTML en prenant en compte le style et la hiérarchie.
 * @param {Object} node - Un nœud de l'AST.
 * @param {number} depth - Niveau de profondeur pour structurer l'affichage.
 * @returns {string} - HTML généré.
 */
function convertNodeToHtml(node, depth = 0) {
    if (!node) return ""

    const indent = " ".repeat(depth * 4) // Indentation pour la hiérarchie
    const position = node.position ? ` data-line="${node.position.start.line}" data-column="${node.position.start.column}"` : ""

    switch (node.type) {
        case "admonition": {
            const type = node.kind || "note" // Type par défaut "note"
            return `${indent}<div class="admonition" data-type="${type}"${position}>\n${node.children.map(child => convertNodeToHtml(child, depth + 1)).join("\n")}\n${indent}</div>`
        }

        case "admonitionTitle":
            return `${indent}<p class="admonition-title"${position}>${node.children.map(child => convertNodeToHtml(child, depth + 1)).join("")}</p>`

        case "text":
            return `${indent}${node.value}`

        case "grid":
            return `${indent}<div class="grid"${position}>\n${node.children.map(child => convertNodeToHtml(child, depth + 1)).join("\n")}\n${indent}</div>`

        case "card":
            return `${indent}<div class="card"${position}>\n${node.children.map(child => convertNodeToHtml(child, depth + 1)).join("\n")}\n${indent}</div>`

        case "code":
            return `${indent}<pre><code${position}>${node.value}</code></pre>`

        case "image":
            return `${indent}<img src="${node.url}" alt="Image"${position} style="height:${node.height}; text-align:${node.align};">`

        default:
            return node.children ? node.children.map(child => convertNodeToHtml(child, depth)).join("\n") : ""
    }
}

function isList(obj) {
    return Array.isArray(obj);
}

async function convertMySTAstToHTML(jsonFile, outputFile) {
    try {
            // Lire le fichier JSON
            const jsonData = await fs.readFile(jsonFile, 'utf8')
            const ast = JSON.parse(jsonData) // Parser l'AST
    
            // Convertir l'AST MyST en HTML avec hiérarchie et styles
            const htmlContent = convertNodeToHtml(ast)
    
            // Ajouter une structure HTML de base
            const fullHtml = `<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MyST AST to HTML</title>
    <style>
    /* === CSS pour les admonitions (version allégée) === */
    .admonition {
        border-left: 3px solid #4a90e2;
        padding: 6px 10px;
        
        border-radius: 6px;
        background: #f3f6fa;
        position: relative;
        box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.05);
    }

    .admonition-title {
        font-weight: 600;
        font-size: 1em;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        color: black !important;
        }

    .admonition-title::before {
        content: "ℹ️";
        font-size: 1em;
        margin-right: 6px;
    }

    .admonition[data-type="warning"] {
        border-left-color: #e67e22;
        background: #fdf6e3;
    }

    .admonition[data-type="warning"] .admonition-title::before {
        content: "⚠️";
    }

    .admonition[data-type="tip"] {
        border-left-color: #27ae60;
        background: #e8f5e9;
    }

    .admonition[data-type="tip"] .admonition-title::before {
        content: "💡";
    }

    .admonition[data-type="error"] {
        border-left-color: #c0392b;
        background: #fdecea;
    }

    .admonition[data-type="error"] .admonition-title::before {
        content: "❌";
    }

    /* === Grille et cartes === */
    .grid {
        display: flex;
        gap: 6px;
    }

    .card {
        border: 1px solid #ccc;
        padding: 8px;
        flex: 1;
        border-radius: 6px;
        background: #fff;
    }

    pre {
        background: #f5f5f5;
        padding: 8px;
        border-radius: 4px;
        font-size: 0.9em;
    }
</style>

</head>
<body>
    ${htmlContent}
</body>
</html>`

        // Écrire le HTML dans le fichier de sortie
        await fs.writeFile(outputFile, fullHtml, 'utf8')
        console.log(`✅ Conversion terminée ! Fichier généré : ${outputFile}`)
    } catch (error) {
        console.error("❌ Erreur lors de la conversion :", error)
    }
}




// Chemin du dossier à lister
const dossierCible = join(process.cwd(), 'JSON');
const dossierSortie = join(process.cwd(), 'HTML');

try {
    // Lire les fichiers du dossier
    const fichiers = await readdir(dossierCible);
    
    console.log("Fichiers récupérés :", fichiers);

    
    
    for (let i = 0; i < fichiers.length; i++) {
        if (fichiers[i].endsWith('.json')) {
            console.log(`- ${fichiers[i]}`);
            const cheminJson = join(dossierCible, fichiers[i]);
            const cheminHtml = join(dossierSortie, `${fichiers[i].replace(/\.json$/, '')}.html`
);

            // Lancer la conversion
            convertMySTAstToHTML(cheminJson, cheminHtml); 
        }
    }

} catch (err) {
    console.error("Erreur :", err);
}