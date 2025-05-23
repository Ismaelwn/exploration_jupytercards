import fs from 'fs';
import { parseMyst } from 'mystmd';

const fichierMarkdown = fs.readFileSync('01r.md', 'utf-8');

// Parse MyST en AST
const ast = parseMyst(fichierMarkdown);

// Sauvegarde au format JSON
fs.writeFileSync('monfichier.ast.json', JSON.stringify(ast, null, 2));

console.log('Conversion terminée !');
