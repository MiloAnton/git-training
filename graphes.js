/* Produit graphe.json pour chaque exercice : l'etat du graphe une fois la
   correction officielle jouee. La conformite garantit qu'il correspond au vrai Git. */
const fs = require('fs');
const path = require('path');
const Gitleo = require('./public/assets/gitleo.js');
const BASE = process.env.BASE || 'exercices';
let n = 0;
for (const d of fs.readdirSync(BASE).sort()) {
  const p = path.join(BASE, d);
  if (!fs.existsSync(path.join(p, 'meta.json'))) continue;
  const lis = f => fs.existsSync(path.join(p, f)) ? fs.readFileSync(path.join(p, f), 'utf8') : '';
  const vm = Gitleo.creerSession(lis('seed.sh'));
  Gitleo.jouer(vm, lis('solution.sh'));
  const g = Gitleo.graphe(vm);
  fs.writeFileSync(path.join(p, 'graphe.json'), JSON.stringify(g));
  n++;
}
console.log(n + ' graphes extraits');
