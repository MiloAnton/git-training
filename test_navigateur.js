/* Test du site dans un vrai navigateur (Chromium) :
   chargement, editeur, execution, verification, codes de seance, sauvegarde. */
const { chromium } = require('playwright');
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8731;
const RACINE = path.join(__dirname, 'public');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css',
                '.json': 'application/json', '.png': 'image/png' };

const serveur = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]);
  if (p === '/') p = '/index.html';
  const f = path.join(RACINE, p);
  if (!f.startsWith(RACINE) || !fs.existsSync(f)) { res.writeHead(404); res.end('404'); return; }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream' });
  res.end(fs.readFileSync(f));
});

const TOUS_CODES = JSON.parse(fs.readFileSync(path.join(__dirname, 'codes.json'), 'utf8'));
const CHAPITRES = [1, 2, 3, 4, 5, 6];

let echecs = 0;
function verifie(nom, ok, detail) {
  console.log((ok ? 'OK    ' : 'ECHEC ') + nom + (ok || !detail ? '' : '  -> ' + detail));
  if (!ok) echecs++;
}

(async () => {
  await new Promise(r => serveur.listen(PORT, r));
  const navigateur = await chromium.launch();
  const page = await navigateur.newPage();
  const erreurs = [];
  page.on('pageerror', e => erreurs.push(e.message));
  page.on('console', m => { if (m.type() === 'error') erreurs.push('console: ' + m.text()); });

  // --- accueil
  await page.goto(`http://localhost:${PORT}/index.html`);
  const titreAccueil = await page.locator('h1').innerText();
  verifie('accueil : titre present', titreAccueil === 'Entra\u00eene-toi \u00e0 Git', JSON.stringify(titreAccueil));
  verifie('accueil : liens vers les chapitres ouverts',
          await page.locator('a.carte-ch').count() === CHAPITRES.length);

  // --- chaque chapitre
  for (const CH of CHAPITRES) {
  const CODES = TOUS_CODES[String(CH)];
  const EX = JSON.parse(fs.readFileSync(path.join(RACINE, `data/chapitre-${CH}.json`), 'utf8'));
  const P = 'ch' + CH + ' : ';
  await page.goto(`http://localhost:${PORT}/chapitre-${CH}.html`);
  await page.waitForSelector('.exo');
  verifie(P + '15 exercices rendus', await page.locator('.exo').count() === 15,
          await page.locator('.exo').count() + ' trouves');
  verifie(P + '3 niveaux', await page.locator('h2.niveau').count() === 3);
  verifie(P + 'editeurs CodeMirror montes', await page.locator('.CodeMirror').count() === 15);
  verifie(P + 'bandeau des limites rempli', await page.locator('#limites li').count() === EX.limites.length);

  // --- aucun secret en clair dans la page
  const htmlRendu = await page.content();
  // aucune commande de la correction ne doit apparaitre comme ligne tapee
  const fuites = [];
  for (const ex of EX.exercices) {
    const sol = fs.readFileSync(path.join(__dirname, 'exercices', ex.ident, 'solution.sh'), 'utf8');
    for (const l of sol.split('\n').map(x => x.trim()).filter(Boolean)) {
      if (htmlRendu.includes('$ ' + l)) fuites.push(ex.ident + ' : ' + l);
    }
  }
  verifie(P + 'aucune commande de correction en clair dans le DOM', fuites.length === 0,
          fuites.slice(0, 3).join(' | '));

  verifie(P + 'aucun indice en clair dans le DOM',
          !htmlRendu.includes('Trois zones, donc trois moments'));

  // --- execution d'une correction correcte dans l'editeur
  async function ecrisEtClique(i, texte, bouton) {
    await page.evaluate(([idx, t]) => {
      const cm = document.querySelectorAll('.CodeMirror')[idx].CodeMirror;
      cm.setValue(t);
    }, [i, texte]);
    await page.locator('.exo').nth(i).locator('button', { hasText: bouton }).first().click();
  }

  const sol1 = fs.readFileSync(path.join(__dirname, 'exercices', EX.exercices[0].ident, 'solution.sh'), 'utf8').trim();
  await ecrisEtClique(0, sol1, 'Lancer');
  const sortie1 = await page.locator('.exo').nth(0).locator('pre.sortie').innerText();
  verifie(P + 'exercice 1 : Lancer produit la sortie Git',
          sortie1.length > 20);

  await ecrisEtClique(0, sol1, 'V\u00e9rifier');
  await page.waitForTimeout(150);
  const v1 = await page.locator('.exo').nth(0).locator('.verdict').innerText();
  verifie(P + 'exercice 1 : la correction officielle est validee',
          v1.includes('exactement la sortie attendue'), v1);

  // --- un programme faux doit etre refuse, avec la ligne d'ecart
  await ecrisEtClique(0, sol1 + '\ngit status', 'V\u00e9rifier');
  await page.waitForTimeout(150);
  const v2 = await page.locator('.exo').nth(0).locator('.verdict').innerText();
  verifie(P + 'un programme different est refuse', v2.includes('Premi\u00e8re diff\u00e9rence'), v2);

  // --- les 15 corrections officielles passent la verification dans le navigateur
  let valides = 0;
  for (let i = 0; i < EX.exercices.length; i++) {
    const sol = fs.readFileSync(
      path.join(__dirname, 'exercices', EX.exercices[i].ident, 'solution.sh'), 'utf8').trim();
    await ecrisEtClique(i, sol, 'V\u00e9rifier');
    await page.waitForTimeout(60);
    const v = await page.locator('.exo').nth(i).locator('.verdict').innerText();
    if (v.includes('exactement la sortie attendue')) valides++;
    else console.log('   ! ' + EX.exercices[i].ident + ' : ' + v.split('\n')[0]);
  }
  verifie(P + 'les 15 corrections officielles sont validees par le site', valides === 15,
          valides + '/15');

  // --- schemas
  verifie(P + 'un schema attendu est dessine sous chaque exemple',
          await page.locator('.exo .schema svg').count() >= EX.exercices.length,
          await page.locator('.exo .schema svg').count() + ' svg');
  const schemaVivant = await page.locator('.exo').nth(0).locator('.schema').count();
  verifie(P + 'le schema de l\u2019etudiant apparait apres execution', schemaVivant === 2,
          schemaVivant + ' schemas dans la carte');

  // --- terminal libre
  await page.locator('.exo').nth(0).locator('.ligne-saisie input').fill('git status');
  await page.locator('.exo').nth(0).locator('.ligne-saisie input').press('Enter');
  await page.waitForTimeout(100);
  const s3 = await page.locator('.exo').nth(0).locator('pre.sortie').innerText();
  verifie(P + 'terminal libre : git status repond', s3.includes('On branch main'), s3.split('\n').slice(-3).join(' / '));

  // --- indices verrouilles puis ouverts
  const bInd = page.locator('.exo').nth(0).locator('button', { hasText: 'indice' }).first();
  verifie(P + 'indices verrouilles au depart', await bInd.isDisabled());
  await page.locator('#code-indices').fill('MAUVAIS-CODE');
  await page.locator('#code-indices').press('Enter');
  await page.waitForTimeout(600);
  verifie(P + 'un mauvais code est refuse',
          (await page.locator('#etat-indices').innerText()) === 'code refus\u00e9');
  await page.locator('#code-indices').fill(CODES.indices);
  await page.locator('#code-indices').press('Enter');
  await page.waitForTimeout(900);
  verifie(P + 'le bon code ouvre les indices',
          (await page.locator('#etat-indices').innerText()) === 'ouvert');
  await bInd.click();
  const i1 = await page.locator('.exo').nth(0).locator('.indice').first().innerText();
  verifie(P + 'un indice se revele un par un', i1.startsWith('Indice 1.'), i1);
  verifie(P + 'un seul indice affiche', await page.locator('.exo').nth(0).locator('.indice').count() === 1);

  // --- corrections
  await page.locator('#code-corrections').fill(CODES.corrections);
  await page.locator('#code-corrections').press('Enter');
  await page.waitForTimeout(900);
  verifie(P + 'le bon code ouvre les corrections',
          (await page.locator('#etat-corrections').innerText()) === 'ouvert');
  await page.locator('.exo').nth(0).locator('details.correction summary').click();
  await page.waitForTimeout(100);
  const cor = await page.locator('.exo').nth(0).locator('details.correction pre').innerText();
  verifie(P + 'la correction dechiffree est la bonne', cor.trim().length > 5 && cor.includes('git'), cor.slice(0, 40));

  // --- sauvegarde automatique
  await page.evaluate(() => {
    document.querySelectorAll('.CodeMirror')[0].CodeMirror.setValue('git status\n# mon brouillon');
  });
  await page.waitForTimeout(200);
  await page.reload();
  await page.waitForSelector('.exo');
  const repris = await page.evaluate(() =>
    document.querySelectorAll('.CodeMirror')[0].CodeMirror.getValue());
  verifie(P + 'le travail est repris apres rechargement', repris.includes('mon brouillon'), repris);
  verifie(P + 'les codes sont a ressaisir apres rechargement',
          (await page.locator('#etat-indices').innerText()) === 'indices verrouill\u00e9s');

  // --- boucle longue coupee
  await page.evaluate(() => {
    const cm = document.querySelectorAll('.CodeMirror')[0].CodeMirror;
    cm.setValue(Array(9000).fill('git status').join('\n'));
  });
  const t0 = Date.now();
  await page.locator('.exo').nth(0).locator('button', { hasText: 'Lancer' }).first().click();
  const duree = Date.now() - t0;
  const sLong = await page.locator('.exo').nth(0).locator('pre.sortie').innerText();
  verifie(P + 'une execution trop longue est coupee',
          sLong.includes('execution interrompue'), 'duree ' + duree + ' ms');

  // --- responsive
  await page.setViewportSize({ width: 390, height: 840 });
  await page.waitForTimeout(150);
  const debord = await page.evaluate(() =>
    document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
  verifie(P + 'pas de debordement horizontal sur mobile', !debord);

  await page.setViewportSize({ width: 1180, height: 1000 });
  }

  verifie('aucune erreur JavaScript', erreurs.length === 0, erreurs.slice(0, 3).join(' | '));

  await navigateur.close();
  serveur.close();
  console.log('\n' + (echecs === 0 ? 'Tous les tests navigateur passent.' : echecs + ' test(s) en echec.'));
  process.exit(echecs === 0 ? 0 : 1);
})();
