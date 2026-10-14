# Plateforme d'entraînement Git, guide de l'intervenant

Ce paquet contient tout ce qui sert à fabriquer le site : les exercices, le moteur,
le générateur et les tests. Le dossier `public/` est la seule chose à mettre en ligne.

## 1. Ce qu'il faut sur la machine

- Python 3.9 ou plus, avec la bibliothèque `cryptography` (`pip install cryptography`)
- Node.js 18 ou plus
- Git 2.30 ou plus, c'est lui qui produit les exemples
- Pour le test navigateur seulement : `npm install playwright && npx playwright install chromium`

## 2. Fabriquer le site, en une commande

```
./construire.sh
```

Elle enchaîne quatre étapes et s'arrête à la première qui échoue.

1. **Les exemples.** Chaque correction officielle est rejouée avec le vrai Git, horloge
   et identité figées, dans un dossier temporaire jeté ensuite. La transcription obtenue
   devient `exemple.txt`. Une seconde version, `affichage.txt`, remplace chaque commande
   tapée par `$ ...` : c'est elle qui est montrée à l'étudiant, sinon l'exemple donnerait
   la solution.
2. **La conformité.** Le moteur du site rejoue les mêmes corrections et sa sortie est
   comparée à celle du vrai Git, ligne par ligne. Un exercice que le moteur ne reproduit
   pas fait échouer la construction : il ne partira jamais en ligne.
3. **Le site.** Les indices et les corrections sont chiffrés en AES-GCM, puis les données
   du chapitre sont écrites dans `public/data/`.
4. **Le navigateur.** Un Chromium ouvre le site et vérifie une vingtaine de points :
   les quinze corrections officielles passent la vérification, les codes de séance
   ouvrent bien les coffres, rien n'est lisible en clair dans la page, la sauvegarde
   automatique fonctionne, une boucle trop longue est coupée.

Pour relancer une étape seule : `python3 build.py exercices`, `node conformance.js -v`,
`node graphes.js`, `python3 site.py`, `node test_navigateur.js`.

Pour voir où un exercice précis diffère du vrai Git : `node dbg2.js ch4-b1-festival`.

## 3. Mettre en ligne sur GitHub Pages

1. Créer un dépôt, par exemple `entrainement-git`.
2. Copier **le contenu** de `public/` à la racine du dépôt, pas le dossier lui-même.
3. Pousser, puis dans **Settings**, **Pages**, choisir la branche `main` et le dossier `/ (root)`.
4. L'adresse sera `https://<votre-compte>.github.io/entrainement-git/`.

Ce qui part en ligne ne contient aucune correction ni aucun indice en clair : ils sont
chiffrés dans `public/data/chapitre-1.json` et ne s'ouvrent qu'avec les codes de séance.
Le reste du paquet, lui, ne doit jamais être poussé sur un dépôt public.

## 4. Changer les codes de séance

Les codes sont dans `codes.json`, un par chapitre, un pour les indices et un pour les
corrections.

```json
{
  "1": { "indices": "LEONIS-GIT-IND-7421", "corrections": "LEONIS-GIT-COR-5839" }
}
```

Changez les valeurs, relancez `./construire.sh`, renvoyez `public/` en ligne. Les anciens
codes cessent aussitôt de fonctionner. Un sel et un vecteur d'initialisation sont tirés
au hasard à chaque génération, donc deux générations avec le même code produisent des
fichiers différents : c'est normal.

Les codes sont à ressaisir à chaque visite. Rien n'est conservé dans le navigateur, ni le
code ni la clé. Seul le travail de l'étudiant est sauvegardé en local.

## 5. Ajouter un exercice

Un exercice est un dossier sous `exercices/`, nommé `ch<N>-<niveau><rang>-<sujet>`.
Par exemple `ch1-e3-liste-courses`. Il contient cinq fichiers, dont un facultatif.

```
exercices/ch1-e3-liste-courses/
  meta.json      identite de l'exercice
  enonce.md      le titre en # puis le texte
  seed.sh        facultatif : l'etat de depart, joue sans etre affiche
  solution.sh    la correction officielle, une commande par ligne, sans commentaire
  indices.md     2 ou 3 indices numerotes
```

`meta.json` ressemble à ceci :

```json
{
  "ident": "ch1-e3-liste-courses",
  "chapitre": 1,
  "niveau": "Echauffement",
  "titre": "La liste de courses"
}
```

Les niveaux possibles sont `Echauffement`, `Intermediaire` et `BOSS`, sans accent dans
le fichier : l'affichage les accentue tout seul.

Ajoutez `"montrer_commandes": true` si, pour cet exercice précis, vous voulez que
l'exemple affiche les commandes au lieu de les masquer par `$ ...`.

`seed.sh` prépare le terrain : créer un dépôt déjà rempli, poser un dépôt distant,
laisser des fichiers en désordre. Il n'apparaît jamais à l'écran, et le dossier dans
lequel il se termine devient le dossier de départ de l'étudiant.

Pour un dépôt distant, utilisez une adresse en `https://github.com/leonis-formation/<nom>.git` :
le générateur la fait pointer vers un dépôt local, et l'affichage montre bien l'adresse
GitHub. Le nom doit commencer par `depot-`.

Une fois le dossier écrit, lancez `./construire.sh`. Si le moteur du site ne sait pas
reproduire une commande que vous avez utilisée, la construction s'arrête à l'étape 2 et
vous dit quelle ligne diffère.

## 6. Les schémas de graphe

Chaque exercice affiche deux schémas : le **schéma attendu**, sous l'exemple, et
**ton schéma**, sous le résultat, redessiné à chaque exécution. Le temps va de la
gauche vers la droite, chaque branche a sa ligne, un commit de fusion est un cercle
creux et le lien vers son second parent est en pointillés. L'étiquette jaune marque
HEAD.

Les schémas sont produits par `node graphes.js`, qui rejoue la correction officielle
dans le moteur du site et écrit `graphe.json` dans chaque dossier d'exercice. Comme
l'étape de conformité garantit déjà que le moteur se comporte exactement comme le vrai
Git, ce graphe est fidèle. Le rendu est dans `public/assets/schema.js` : il ne dépend
d'aucune bibliothèque et produit du SVG.

Pour changer l'allure des schémas, les constantes utiles sont en haut de ce fichier :
`PAS_X` et `PAS_Y` pour l'espacement, `RAYON` pour la taille des commits, `LANES` pour
les couleurs de branches.

## 7. Ce que le moteur sait faire

Le moteur couvre l'intégralité des six chapitres.

- Chapitre 1 : `init` (et `--bare`), `status`, `add` (`-A`), `commit` (`-m`, `-am`),
  `reset <fichier>`, `rm --cached`, `clone`, `push`, `pull`, le `.gitignore` avec
  motifs, dossiers et exceptions `!`.
- Chapitre 2 : `log` (`--oneline`, `--graph`, `--decorate`, `--all`, `-n`, `--stat`,
  `-p`, filtrage par fichier), `show` (y compris `show <ref>:<fichier>`), `diff` dans
  ses six formes, les références `HEAD~n` et `HEAD^`. Le diff est un vrai diff unifié,
  avec les blocs `@@`, trois lignes de contexte et le rappel de section.
- Chapitre 3 : `branch` (`-v`, `-d`, `-D`, `-m`), `switch` (`-c`), `checkout` (`-b`),
  `stash` (`push`, `-u`, `list`, `pop`, `apply`, `drop`), et le refus de bascule quand
  un fichier modifié serait écrasé.
- Chapitre 4 : `merge` avec le fast-forward, le commit de fusion, `--no-ff`, `--ff-only`
  et son message de refus complet.
- Chapitre 5 : `commit --amend`, `revert` (avec `-m` pour les fusions), `reset` dans ses
  trois modes, `reflog` et les références `HEAD@{n}`, `restore` (`--staged`, `--source`),
  `merge --squash`.
- Chapitre 6 : la fusion à trois points avec marqueurs de conflit, l'état `Unmerged
  paths`, `add` qui résout, `merge --abort` et `--continue`, `restore --ours/--theirs`,
  `diff --diff-filter=U`, `rebase` et `pull --rebase`.

Côté shell : `echo`, `printf`, `cat`, `ls`, `cd`, `mkdir`, `rm`, `pwd`, avec les
redirections `>` et `>>`.

Deux limites assumées, annoncées dans le bandeau des chapitres concernés. Le dessin
ASCII de `git log --graph` n'est rendu que pour un historique en ligne droite :
reproduire l'algorithme de mise en page de Git pour les branches est un chantier à
part, et le schéma SVG rend le même service en mieux. Et `git rebase -i` est absent,
puisqu'il ouvre un éditeur de texte ; le regroupement de commits se travaille avec
`git merge --squash`.

Chaque commande est une fonction dans l'objet `GIT` de `public/assets/gitleo.js`.

## 8. Organisation des fichiers

```
construire.sh          la commande unique
codes.json             les codes de seance, a ne jamais publier
build.py               rejoue les corrections avec le vrai Git
conformance.js         compare le moteur du site au vrai Git
site.py                chiffre et genere les donnees du site
test_navigateur.js     test de bout en bout dans Chromium
revue.py               produit un document de relecture de tous les exercices
make_ch1.py            scripts d'amorcage ayant cree les dossiers d'exercices
make_ch2.py
make_ch34.py
make_ch56.py
patch_accents.py       outil ayant pose les accents sur les textes du chapitre 1
graphes.js             extrait graphe.json pour chaque exercice
dbg.js, dbg2.js        aides au debogage d'un exercice precis
exercices/             un dossier par exercice, la source de verite
public/                le site, seul dossier a mettre en ligne
```
