# Chapitre 1 - Du fichier au commit

15 exercices. Chaque bloc terminal est la sortie d'une execution reelle de la
correction officielle avec Git 2.43, horloge et identite figees. Les hashs sont
masques par `...` et ne sont pas compares.


## Niveau Echauffement

### Le carnet de recettes

Identifiant : `ch1-e1-carnet-recettes`

Tu démarres un carnet de recettes. Crée le dépôt, ajoute une première recette,
puis enregistre-la dans l'historique.

Entre chaque étape, regarde où en est Git : c'est le réflexe à prendre dès
maintenant. Ton message de commit respecte le format `type(scope): description`.

**Exemple**

```
$ git init carnet-recettes
Initialized empty Git repository in /home/eleve/carnet-recettes/.git/
$ cd carnet-recettes
$ echo "Tarte aux pommes" > recettes.txt
$ git status
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	recettes.txt

nothing added to commit but untracked files present (use "git add" to track)
$ git add recettes.txt
$ git status
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   recettes.txt
$ git commit -m "feat(recettes): ajout de la tarte aux pommes"
[main (root-commit) ...] feat(recettes): ajout de la tarte aux pommes
 1 file changed, 1 insertion(+)
 create mode 100644 recettes.txt
$ git status
On branch main
nothing to commit, working tree clean
```

**Indices**

1. Trois zones, donc trois moments : tu modifies, tu sélectionnes, tu enregistres.
2. Lis `git status` avant et après chaque commande. Les deux affichages ne disent pas la même chose, et c'est tout l'intérêt.
3. Six commandes en tout. L'avant-dernière met le fichier au panier, la dernière valide avec `-m`.

**Correction officielle**

```bash
git init carnet-recettes
cd carnet-recettes
echo "Tarte aux pommes" > recettes.txt
git status
git add recettes.txt
git status
git commit -m "feat(recettes): ajout de la tarte aux pommes"
git status
```

### La playlist de la soirée

Identifiant : `ch1-e2-playlist`

Tu prépares la playlist de la soirée de promo. Tu as deux fichiers : la liste
des titres, que tu veux partager, et tes notes personnelles, que tu veux garder
pour toi pour l'instant.

Enregistre uniquement la liste des titres. Les notes doivent rester hors de
l'historique, sans être supprimées pour autant.

**Exemple**

```
$ git init playlist
Initialized empty Git repository in /home/eleve/playlist/.git/
$ cd playlist
$ echo "Daft Punk - Around the World" > titres.txt
$ echo "demander la sono au BDE" > notes.txt
$ git status
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	notes.txt
	titres.txt

nothing added to commit but untracked files present (use "git add" to track)
$ git add titres.txt
$ git status
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   titres.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	notes.txt
$ git commit -m "feat(titres): ajout du premier morceau"
[main (root-commit) ...] feat(titres): ajout du premier morceau
 1 file changed, 1 insertion(+)
 create mode 100644 titres.txt
$ git status
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	notes.txt

nothing added to commit but untracked files present (use "git add" to track)
$ ls
notes.txt
titres.txt
```

**Indices**

1. `git add` prend un nom de fichier. Rien ne t'oblige à tout ajouter d'un coup.
2. Après le commit, `git status` doit encore parler de `notes.txt`. C'est normal et c'est le but.
3. Finis par un `ls` : le fichier est toujours sur le disque, Git ne le suit simplement pas.

**Correction officielle**

```bash
git init playlist
cd playlist
echo "Daft Punk - Around the World" > titres.txt
echo "demander la sono au BDE" > notes.txt
git status
git add titres.txt
git status
git commit -m "feat(titres): ajout du premier morceau"
git status
ls
```

### La liste de courses

Identifiant : `ch1-e3-liste-courses`

Le dépôt existe déjà et contient une liste de courses avec une ligne.

Ajoute le pain, enregistre-le. Ajoute ensuite le lait et enregistre-le à ton
tour, mais cette fois en une seule commande : pour un fichier que Git suit
déjà, tu peux mettre au panier et valider d'un coup.

**Exemple**

```
$ echo "- pain" >> courses.txt
$ git status
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   courses.txt

no changes added to commit (use "git add" and/or "git commit -a")
$ git add courses.txt
$ git commit -m "feat(courses): ajout du pain"
[main ...] feat(courses): ajout du pain
 1 file changed, 1 insertion(+)
$ echo "- lait" >> courses.txt
$ git commit -am "feat(courses): ajout du lait"
[main ...] feat(courses): ajout du lait
 1 file changed, 1 insertion(+)
$ git status
On branch main
nothing to commit, working tree clean
$ cat courses.txt
- cafe
- pain
- lait
```

**Indices**

1. Deux chevrons ajoutent une ligne, un seul écrase tout le fichier. Vérifie avec `cat` si tu as un doute.
2. Pour le second ajout, cherche l'option de `git commit` qui fait le `git add` a ta place.
3. Cette option ne marche que sur les fichiers déjà suivis. Un fichier tout neuf serait ignore.

**Correction officielle**

```bash
echo "- pain" >> courses.txt
git status
git add courses.txt
git commit -m "feat(courses): ajout du pain"
echo "- lait" >> courses.txt
git commit -am "feat(courses): ajout du lait"
git status
cat courses.txt
```

### Le journal de bord

Identifiant : `ch1-e4-journal-bord`

Tu tiens le journal de bord d'une traversée. Tu viens d'écrire la première
entrée, mais tu as aussi note le code du coffre dans un fichier à côté.

Par réflexe, tu mets tout au panier d'un coup. Rattrape-toi : retire le fichier
sensible du panier sans perdre son contenu, puis enregistre le reste.

**Exemple**

```
$ echo "Jour 1 : départ du port de Brest" > journal.txt
$ echo "code du coffre : 4471" > prive.txt
$ git add .
$ git status
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   journal.txt
	new file:   prive.txt
$ git reset prive.txt
$ git status
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   journal.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	prive.txt
$ git commit -m "feat(journal): premiere entree de la traversee"
[main (root-commit) ...] feat(journal): premiere entree de la traversee
 1 file changed, 1 insertion(+)
 create mode 100644 journal.txt
$ git status
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	prive.txt

nothing added to commit but untracked files present (use "git add" to track)
$ cat prive.txt
code du coffre : 4471
```

**Indices**

1. `git add .` prend tout le dossier. Pratique, et c'est exactement là que naissent les accidents.
2. La commande qui retire du panier est au programme du cycle de base. Elle prend un nom de fichier.
3. Elle ne touche pas au contenu du fichier : le `cat` final doit afficher ton texte intact.

**Correction officielle**

```bash
echo "Jour 1 : départ du port de Brest" > journal.txt
echo "code du coffre : 4471" > prive.txt
git add .
git status
git reset prive.txt
git status
git commit -m "feat(journal): premiere entree de la traversee"
git status
cat prive.txt
```

### L'inventaire de l'atelier

Identifiant : `ch1-e5-inventaire-atelier`

L'atelier tient son inventaire dans un fichier texte. Le logiciel de saisie
génère à côté un fichier de sauvegarde automatique en `.bak` dont personne n'a
besoin dans l'historique.

Mets en place le réglage qui dit à Git d'ignorer tous les fichiers `.bak`, puis
enregistre l'inventaire et ce réglage.

**Exemple**

```
$ git init atelier
Initialized empty Git repository in /home/eleve/atelier/.git/
$ cd atelier
$ echo "perceuse à colonne" > inventaire.txt
$ echo "sauvegarde automatique" > inventaire.txt.bak
$ git status
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	inventaire.txt
	inventaire.txt.bak

nothing added to commit but untracked files present (use "git add" to track)
$ printf "*.bak\n" > .gitignore
$ git status
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.gitignore
	inventaire.txt

nothing added to commit but untracked files present (use "git add" to track)
$ git add .
$ git commit -m "config(depot): ajout du gitignore et de l'inventaire"
[main (root-commit) ...] config(depot): ajout du gitignore et de l'inventaire
 2 files changed, 2 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 inventaire.txt
$ git status
On branch main
nothing to commit, working tree clean
```

**Indices**

1. Le fichier de réglage se place à la racine du dépôt et son nom commence par un point.
2. Une ligne = un motif. L'étoile remplace n'importe quelle suite de caractères.
3. Fais un `git status` avant et après avoir crée le fichier : un nom doit disparaître de la liste, un autre apparaître.

**Correction officielle**

```bash
git init atelier
cd atelier
echo "perceuse à colonne" > inventaire.txt
echo "sauvegarde automatique" > inventaire.txt.bak
git status
printf "*.bak\n" > .gitignore
git status
git add .
git commit -m "config(depot): ajout du gitignore et de l'inventaire"
git status
```


## Niveau Intermediaire

### Le budget de la coloc

Identifiant : `ch1-i1-budget-coloc`

Tu ranges les comptes de la colocation. Deux sujets différents arrivent en
même temps : les charges fixes d'un côté, les courses partagées de l'autre.

Enregistre-les en deux commits distincts, un par sujet, pour qu'on puisse
annuler l'un sans toucher à l'autre. Les deux fichiers existent avant ton
premier commit : c'est à toi de choisir ce qui part dans quel commit.

**Exemple**

```
$ printf "loyer : 820\ninternet : 30\n" > charges.txt
$ printf "courses du 3 janvier : 54\n" > courses-communes.txt
$ git status
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	charges.txt
	courses-communes.txt

nothing added to commit but untracked files present (use "git add" to track)
$ git add charges.txt
$ git status
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   charges.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	courses-communes.txt
$ git commit -m "feat(charges): ajout des charges fixes"
[main (root-commit) ...] feat(charges): ajout des charges fixes
 1 file changed, 2 insertions(+)
 create mode 100644 charges.txt
$ git add courses-communes.txt
$ git commit -m "feat(courses): ajout des courses du 3 janvier"
[main ...] feat(courses): ajout des courses du 3 janvier
 1 file changed, 1 insertion(+)
 create mode 100644 courses-communes.txt
$ git status
On branch main
nothing to commit, working tree clean
```

**Indices**

1. Un commit = un sujet. Deux sujets, donc deux passages par le panier.
2. Tu peux parfaitement laisser un fichier non suivi pendant que tu valides l'autre.
3. Entre les deux commits, `git status` doit encore signaler le second fichier comme non suivi.

**Correction officielle**

```bash
printf "loyer : 820\ninternet : 30\n" > charges.txt
printf "courses du 3 janvier : 54\n" > courses-communes.txt
git status
git add charges.txt
git status
git commit -m "feat(charges): ajout des charges fixes"
git add courses-communes.txt
git commit -m "feat(courses): ajout des courses du 3 janvier"
git status
```

### Les fiches de révision

Identifiant : `ch1-i2-fiches-revision`

Ton dossier de fiches de révision est en désordre : des fiches définitives,
un dossier de brouillons, des fichiers temporaires, et un fichier système que
ton ordinateur dépose partout.

Écris le réglage qui ignore les fichiers temporaires, le dossier de brouillons
et le fichier système, mais qui garde quand même `rappel.tmp`, dont tu as
besoin. Enregistre ensuite ce qui reste.

**Exemple**

```
$ printf "*.tmp\nbrouillons/\n.DS_Store\n!rappel.tmp\n" > .gitignore
$ git status
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.gitignore
	fiche-git.txt
	fiche-reseau.txt
	rappel.tmp

nothing added to commit but untracked files present (use "git add" to track)
$ git add .
$ git commit -m "config(depot): reglage du gitignore et ajout des fiches"
[main (root-commit) ...] config(depot): reglage du gitignore et ajout des fiches
 4 files changed, 7 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 fiche-git.txt
 create mode 100644 fiche-reseau.txt
 create mode 100644 rappel.tmp
$ git status
On branch main
nothing to commit, working tree clean
$ cat .gitignore
*.tmp
brouillons/
.DS_Store
!rappel.tmp
```

**Indices**

1. Quatre lignes suffisent, une par motif. L'ordre compte : l'exception se place après la règle qu'elle annule.
2. Un nom suivi d'une barre oblique désigne un dossier entier.
3. Le point d'exclamation réintroduit un fichier qu'un motif précédent avait exclu.

**Correction officielle**

```bash
printf "*.tmp\nbrouillons/\n.DS_Store\n!rappel.tmp\n" > .gitignore
git status
git add .
git commit -m "config(depot): reglage du gitignore et ajout des fiches"
git status
cat .gitignore
```

### Le catalogue de plantes

Identifiant : `ch1-i3-catalogue-plantes`

La serre partage son catalogue sur un dépôt distant. Récupère-le sur ta
machine, ajoute la fougère au catalogue et enregistre ton travail en local.

Rien n'est encore envoyé au dépôt distant à ce stade : tu travailles sur ta
copie.

**Exemple**

```
$ git clone https://github.com/leonis-formation/depot-serre.git catalogue
Cloning into 'catalogue'...
done.
$ cd catalogue
$ ls
catalogue.txt
$ cat catalogue.txt
monstera
ficus
$ echo "fougère" >> catalogue.txt
$ git status
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   catalogue.txt

no changes added to commit (use "git add" and/or "git commit -a")
$ git add catalogue.txt
$ git commit -m "feat(catalogue): ajout de la fougere"
[main ...] feat(catalogue): ajout de la fougere
 1 file changed, 1 insertion(+)
$ git status
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
```

**Indices**

1. Une seule commande récupère les fichiers, l'historique et l'adresse du dépôt distant.
2. Après la récupération, tu dois entrer dans le dossier crée avant de travailler.
3. Le `git status` final signale que ta branche est en avance : ton commit est bien local, pas encore envoyé.

**Correction officielle**

```bash
git clone https://github.com/leonis-formation/depot-serre.git catalogue
cd catalogue
ls
cat catalogue.txt
echo "fougère" >> catalogue.txt
git status
git add catalogue.txt
git commit -m "feat(catalogue): ajout de la fougere"
git status
```

### Le menu du restaurant

Identifiant : `ch1-i4-menu-restaurant`

Le restaurant met son menu à jour. Tu as modifie trois fichiers d'un coup :
les entrées, les plats, et un fichier de test que tu avais laisse traîner.

Tu mets tout au panier par réflexe. Retire le fichier de test, vérifie que le
panier ne contient plus que ce qu'il faut, puis valide.

**Exemple**

```
$ echo "- velouté de potiron" >> entrees.txt
$ echo "- risotto aux champignons" >> plats.txt
$ echo "essai de mise en page" > test.txt
$ git add .
$ git status
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   entrees.txt
	modified:   plats.txt
	new file:   test.txt
$ git reset test.txt
$ git status
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   entrees.txt
	modified:   plats.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	test.txt
$ git commit -m "feat(menu): ajout du veloute et du risotto"
[main ...] feat(menu): ajout du veloute et du risotto
 2 files changed, 2 insertions(+)
$ git status
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	test.txt

nothing added to commit but untracked files present (use "git add" to track)
```

**Indices**

1. Le piège est à la ligne `git add .` : regarde ce qu'elle a vraiment ramasse.
2. Un seul fichier doit sortir du panier. Les deux autres y restent.
3. Après le commit, le fichier de test doit toujours apparaître comme non suivi : il n'a jamais été enregistre.

**Correction officielle**

```bash
echo "- velouté de potiron" >> entrees.txt
echo "- risotto aux champignons" >> plats.txt
echo "essai de mise en page" > test.txt
git add .
git status
git reset test.txt
git status
git commit -m "feat(menu): ajout du veloute et du risotto"
git status
```

### Le carnet de voyage

Identifiant : `ch1-i5-carnet-voyage`

Tu tiens un carnet de voyage partage avec deux amis sur un dépôt distant.
Tu as déjà récupère le dépôt.

Ajoute l'étape de Lisbonne, enregistre-la, puis envoie-la pour que les autres
la voient. Vérifie l'état avant et après l'envoi : les deux affichages ne
disent pas la même chose.

**Exemple**

```
$ echo "Jour 3 : Lisbonne, tramway 28" >> etapes.txt
$ git add etapes.txt
$ git commit -m "feat(etapes): ajout de l'étape de Lisbonne"
[main ...] feat(etapes): ajout de l'étape de Lisbonne
 1 file changed, 1 insertion(+)
$ git status
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
$ git push
To https://github.com/leonis-formation/depot-voyage.git
   ...  main -> main
$ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

**Indices**

1. Enregistrer en local et publier sont deux gestes séparés. Git ne fait jamais le second tout seul.
2. Avant l'envoi, `git status` parle d'une branche en avance. Après, il parle d'une branche à jour.
3. Le dépôt distant est déjà connu de ta copie : la commande d'envoi n'a besoin d'aucun argument.

**Correction officielle**

```bash
echo "Jour 3 : Lisbonne, tramway 28" >> etapes.txt
git add etapes.txt
git commit -m "feat(etapes): ajout de l'étape de Lisbonne"
git status
git push
git status
```


## Niveau BOSS

### Le répertoire de contacts

Identifiant : `ch1-b1-repertoire-contacts`

Mauvaise nouvelle : le fichier `cles-api.txt` a été enregistré dans
l'historique au commit précédent, et le dépôt est public.

Ajouter le fichier au `.gitignore` ne suffira pas, le réglage n'est pas
rétroactif. Il faut d'abord retirer le fichier du suivi de Git tout en le
gardant sur ton disque, puis écrire le réglage pour que l'accident ne se
reproduise pas, et enregistrer le tout.

Termine en vérifiant que le fichier est bien toujours sur ton disque.

**Exemple**

```
$ git status
On branch main
nothing to commit, working tree clean
$ git rm --cached cles-api.txt
rm 'cles-api.txt'
$ git status
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	deleted:    cles-api.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	cles-api.txt
$ printf "cles-api.txt\n" > .gitignore
$ git status
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	deleted:    cles-api.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.gitignore
$ git add .gitignore
$ git commit -m "config(depot): retrait des clés du suivi et ajout du gitignore"
[main ...] config(depot): retrait des clés du suivi et ajout du gitignore
 2 files changed, 1 insertion(+), 1 deletion(-)
 create mode 100644 .gitignore
 delete mode 100644 cles-api.txt
$ git status
On branch main
nothing to commit, working tree clean
$ ls
cles-api.txt
contacts.txt
$ cat cles-api.txt
token-prod : abcd1234
```

**Indices**

1. Le réglage n'agit que sur les fichiers que Git ne suit pas encore. Celui-là, il le suit déjà.
2. Cherche la commande qui retire un fichier du dépôt sans le supprimer du disque. C'est une option de `git rm`.
3. Fais-le dans cet ordre : retirer du suivi, puis écrire le réglage, puis valider. Le `ls` final doit encore montrer le fichier.

**Correction officielle**

```bash
git status
git rm --cached cles-api.txt
git status
printf "cles-api.txt\n" > .gitignore
git status
git add .gitignore
git commit -m "config(depot): retrait des clés du suivi et ajout du gitignore"
git status
ls
cat cles-api.txt
```

### La bibliothèque du club

Identifiant : `ch1-b2-bibliotheque`

Le club de lecture partage sa liste d'ouvrages. Pendant que tu lisais,
quelqu'un a publié la fiche des avis sur le dépôt distant, et toi tu as ajoute
un titre à la liste en local, sans être à jour.

Constate d'abord que ton envoi est refusé, et lis ce que Git te répond. Mets-toi
a jour, vérifie ce que tu as récupère, puis renvoie ton travail.

Les deux modifications portent sur des fichiers différents : Git sait les
combiner tout seul.

**Exemple**

```
$ git status
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
$ git push
To https://github.com/leonis-formation/depot-club.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'https://github.com/leonis-formation/depot-club.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. This is usually caused by another repository pushing to
hint: the same ref. If you want to integrate the remote changes, use
hint: 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
$ git pull --no-edit
From https://github.com/leonis-formation/depot-club.git
   ...  main       -> origin/main
Merge made by the 'ort' strategy.
 avis.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 avis.txt
$ ls
avis.txt
ouvrages.txt
$ cat ouvrages.txt
L'Etranger
Le Mythe de Sisyphe
$ git status
On branch main
Your branch is ahead of 'origin/main' by 2 commits.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
$ git push
To https://github.com/leonis-formation/depot-club.git
   ...  main -> main
$ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

**Indices**

1. Commence par tenter l'envoi sans rien faire d'autre. Le message de refus fait partie de l'exercice.
2. Git te dit quoi faire dans son message : il faut d'abord rapatrier ce que tu n'as pas.
3. L'option `--no-edit` évite que Git ouvre un éditeur pour le message de fusion. Le `ls` te montrera le fichier arrive du dépôt distant.

**Correction officielle**

```bash
git status
git push
git pull --no-edit
ls
cat ouvrages.txt
git status
git push
git status
```

### Le planning d'entraînement

Identifiant : `ch1-b3-planning-entrainement`

Le club d'athlétisme réorganise sa saison. Trois sujets arrivent en vrac dans
ton dossier : le planning des séances, la liste du matériel, et un brouillon
personnel qui ne doit jamais être publie.

Produis un historique propre : un commit par sujet, dans cet ordre, le planning
puis le matériel. Le brouillon ne doit apparaître dans aucun commit, et tu dois
mettre en place le réglage qui garantit qu'il n'y arrivera jamais, même si
quelqu'un fait un `git add .` plus tard.

Le réglage part dans son propre commit, en dernier.

**Exemple**

```
$ printf "mardi : fractionne\njeudi : endurance\n" > planning.txt
$ printf "12 plots\n4 chronos\n" > materiel.txt
$ printf "demander une augmentation au président\n" > brouillon-perso.txt
$ git status
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	brouillon-perso.txt
	materiel.txt
	planning.txt

nothing added to commit but untracked files present (use "git add" to track)
$ git add planning.txt
$ git commit -m "feat(planning): ajout des séances de la semaine"
[main (root-commit) ...] feat(planning): ajout des séances de la semaine
 1 file changed, 2 insertions(+)
 create mode 100644 planning.txt
$ git add materiel.txt
$ git commit -m "feat(materiel): ajout du matériel du club"
[main ...] feat(materiel): ajout du matériel du club
 1 file changed, 2 insertions(+)
 create mode 100644 materiel.txt
$ printf "brouillon-perso.txt\n" > .gitignore
$ git status
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.gitignore

nothing added to commit but untracked files present (use "git add" to track)
$ git add .gitignore
$ git commit -m "config(depot): exclusion du brouillon personnel"
[main ...] config(depot): exclusion du brouillon personnel
 1 file changed, 1 insertion(+)
 create mode 100644 .gitignore
$ git status
On branch main
nothing to commit, working tree clean
```

**Indices**

1. Trois commits, donc trois passages par le panier. Ne mets jamais `git add .` tant que le réglage n'existe pas.
2. L'ordre imposé : planning, matériel, puis réglage. Chaque commit ne contient qu'un seul fichier.
3. À la fin, `git status` ne doit plus rien signaler du tout : ni fichier modifie, ni fichier non suivi.

**Correction officielle**

```bash
printf "mardi : fractionne\njeudi : endurance\n" > planning.txt
printf "12 plots\n4 chronos\n" > materiel.txt
printf "demander une augmentation au président\n" > brouillon-perso.txt
git status
git add planning.txt
git commit -m "feat(planning): ajout des séances de la semaine"
git add materiel.txt
git commit -m "feat(materiel): ajout du matériel du club"
printf "brouillon-perso.txt\n" > .gitignore
git status
git add .gitignore
git commit -m "config(depot): exclusion du brouillon personnel"
git status
```

### L'inventaire de la ludothèque

Identifiant : `ch1-b4-inventaire-jeux`

La ludothèque fait son inventaire. Tu as travaille vite : tu as fait un
`git add .` alors que le dossier contient aussi un export temporaire et un
dossier de photos trop lourd.

Rattrape le coup sans rien perdre. Sors du panier ce qui n'a rien à y faire,
mets en place le réglage pour que ces deux éléments soient ignorés à l'avenir,
puis enregistre l'inventaire et le réglage ensemble.

**Exemple**

```
$ git add .
$ git status
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   export.tmp
	new file:   inventaire.txt
	new file:   photos/catan.jpg
$ git reset export.tmp
$ git reset photos
$ git status
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   inventaire.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	export.tmp
	photos/
$ printf "*.tmp\nphotos/\n" > .gitignore
$ git status
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   inventaire.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.gitignore
$ git add .
$ git commit -m "config(depot): inventaire et exclusion des fichiers temporaires"
[main (root-commit) ...] config(depot): inventaire et exclusion des fichiers temporaires
 2 files changed, 4 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 inventaire.txt
$ git status
On branch main
nothing to commit, working tree clean
$ ls
export.tmp
inventaire.txt
photos
```

**Indices**

1. Deux éléments à sortir du panier : un fichier et un dossier. La commande accepte les deux.
2. Écris le réglage après avoir vide le panier, sinon `git status` continuera de te montrer ce que tu viens de retirer.
3. Une fois le réglage en place, un second `git add .` devient sans danger : c'est tout l'intérêt.

**Correction officielle**

```bash
git add .
git status
git reset export.tmp
git reset photos
git status
printf "*.tmp\nphotos/\n" > .gitignore
git status
git add .
git commit -m "config(depot): inventaire et exclusion des fichiers temporaires"
git status
ls
```

### La reprise du site de l'asso

Identifiant : `ch1-b5-atelier-complet`

Scénario complet. L'association partage le contenu de son site sur un dépôt
distant. Tu récupères le projet, tu ajoutes la page des horaires, tu mets en
place le réglage qui ignore les journaux d'erreur produits par l'hébergeur,
puis tu publies ton travail.

Attention : un fichier de journal existe déjà dans ton dossier de travail des
la récupération. Il ne doit jamais partir sur le dépôt distant.

Termine par un `git status` qui prouve que tout est enregistré et publie.

**Exemple**

```
$ git clone https://github.com/leonis-formation/depot-asso.git site
Cloning into 'site'...
done.
$ cd site
$ ls
accueil.txt
$ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
$ printf "*.log\n" > .gitignore
$ git status
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.gitignore

nothing added to commit but untracked files present (use "git add" to track)
$ printf "Permanence : mardi 18h-20h\n" > horaires.txt
$ git add .gitignore horaires.txt
$ git status
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	new file:   .gitignore
	new file:   horaires.txt
$ git commit -m "feat(horaires): ajout des horaires et exclusion des journaux"
[main ...] feat(horaires): ajout des horaires et exclusion des journaux
 2 files changed, 2 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 horaires.txt
$ git push
To https://github.com/leonis-formation/depot-asso.git
   ...  main -> main
$ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

**Indices**

1. Fais le réglage avant d'ajouter quoi que ce soit : tu évites d'avoir à te rattraper ensuite.
2. Tu peux donner plusieurs fichiers à `git add` en une seule commande.
3. Le `git status` final doit indiquer une branche à jour et un dossier propre, sans mentionner le journal.

**Correction officielle**

```bash
git clone https://github.com/leonis-formation/depot-asso.git site
cd site
ls
git status
printf "*.log\n" > .gitignore
git status
printf "Permanence : mardi 18h-20h\n" > horaires.txt
git add .gitignore horaires.txt
git status
git commit -m "feat(horaires): ajout des horaires et exclusion des journaux"
git push
git status
```

