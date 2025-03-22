import fs from 'node:fs/promises'
import { toHtml } from 'hast-util-to-html'

async function convertMySTAstToHTML(jsonFile) {
  try {
    // Lire le fichier JSON
    const jsonData = await fs.readFile(jsonFile, 'utf8')
    const ast = JSON.parse(jsonData) // AST en objet JS

    // Convertir l'AST MyST en HTML
    const html = toHtml(ast)

    console.log(html)
  } catch (error) {
    console.error("Erreur lors de la conversion :", error)
  }
}

// Exécuter la conversion avec ton fichier JSON
convertMySTAstToHTML('example.json')
