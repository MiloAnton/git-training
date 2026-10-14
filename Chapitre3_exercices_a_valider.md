# Chapitre 3 - Les branches

15 exercices. Chaque bloc terminal est la sortie d'une execution reelle de la
correction officielle avec Git 2.43, horloge et identite figees. Les hashs sont
masques par `...` et ne sont pas compares.


## Niveau Echauffement

### La fanfare du village

Identifiant : `ch3-e1-fanfare`

La fanfare veut tester un nouveau morceau sans toucher au répertoire officiel.

Crée une branche `feature/nouveau-morceau` et bascule dessus en une seule
commande. Vérifie que tu es bien dessus, ajoute le morceau au répertoire et
enregistre. Reviens enfin sur `main` et regarde le fichier : il ne doit plus
contenir le nouveau morceau.

**Exemple**

```
$ git switch -c feature/nouveau-morceau
Switched to a new branch 'feature/nouveau-morceau'
$ git branch
* feature/nouveau-morceau
  main
$ printf "Marche de la Saint-Jean\nValse du 14 juillet\nSamba de la kermesse\n" > repertoire.txt
$ git commit -am "feat(repertoire): ajout de la samba"
[feature/nouveau-morceau ...] feat(repertoire): ajout de la samba
 1 file changed, 1 insertion(+)
$ git switch main
Switched to branch 'main'
$ cat repertoire.txt
Marche de la Saint-Jean
Valse du 14 juillet
```

**Indices**

1. Une seule commande crée la branche et bascule dessus : cherche l'option de `git switch`.
2. `git branch` sans argument liste les branches et marque la courante d'une étoile.
3. Le `cat` final est la preuve que les deux branches sont bien indépendantes.

**Correction officielle**

```bash
git switch -c feature/nouveau-morceau
git branch
printf "Marche de la Saint-Jean\nValse du 14 juillet\nSamba de la kermesse\n" > repertoire.txt
git commit -am "feat(repertoire): ajout de la samba"
git switch main
cat repertoire.txt
```

### Le potager partagé

Identifiant : `ch3-e2-potager`

Le potager partagé a déjà deux branches en cours. Tu arrives et tu dois
d'abord te repérer.

Liste les branches, puis liste-les à nouveau avec, pour chacune, l'empreinte et
le message de son dernier commit. Bascule ensuite sur la branche
`feature/serre` et affiche le contenu du dossier.

**Exemple**

```
$ git branch
  feature/serre
* main
$ git branch -v
  feature/serre ... feat(serre): plan de la serre
* main          ... feat(parcelles): ajout des haricots
$ git switch feature/serre
Switched to branch 'feature/serre'
$ ls
parcelles.txt
serre.txt
```

**Indices**

1. La liste détaillée s'obtient avec une option d'une seule lettre.
2. Pour basculer sur une branche qui existe déjà, pas besoin de l'option de création.
3. Le `ls` final doit montrer un fichier de plus que sur `main`.

**Correction officielle**

```bash
git branch
git branch -v
git switch feature/serre
ls
```

### L'escape game

Identifiant : `ch3-e3-escape-game`

La branche de travail s'appelle `enigmes`, mais l'équipe utilise une
convention : les nouvelles fonctionnalités commencent par `feature/`.

Bascule sur la branche, renomme-la en `feature/enigmes` sans perdre son
historique, puis vérifie la liste détaillée des branches. L'empreinte du
dernier commit doit être exactement la même qu'avant le renommage.

**Exemple**

```
$ git switch enigmes
Switched to branch 'enigmes'
$ git branch -v
* enigmes ... feat(enigmes): enigme du cadran
  main    ... feat(salles): premiere salle
$ git branch -m feature/enigmes
$ git branch -v
* feature/enigmes ... feat(enigmes): enigme du cadran
  main            ... feat(salles): premiere salle
```

**Indices**

1. L'option de renommage est une seule lettre, celle de « move » en anglais.
2. Donne-lui simplement le nouveau nom : la branche courante est renommée.
3. Compare les deux `git branch -v` : seul le nom change, pas l'empreinte.

**Correction officielle**

```bash
git switch enigmes
git branch -v
git branch -m feature/enigmes
git branch -v
```

### La radio associative

Identifiant : `ch3-e4-radio`

Tu es en train de modifier la grille des programmes quand on te demande en
urgence de regarder un détail sur `main`. Ton travail n'est pas fini, il ne
mérite pas un commit.

Mets-le de côté, vérifie que le dossier est propre, bascule sur `main`, reviens
sur ta branche et récupère ton travail. Termine en affichant le fichier pour
prouver que rien n'a été perdu.

**Exemple**

```
$ printf "6h Reveil\n9h Chronique\n12h Journal\n" > grille.txt
$ git stash
Saved working directory and index state WIP on feature/grille: ... feat(grille): premiere grille
$ git status
On branch feature/grille
nothing to commit, working tree clean
$ git switch main
Switched to branch 'main'
$ git switch feature/grille
Switched to branch 'feature/grille'
$ git stash pop
On branch feature/grille
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   grille.txt

no changes added to commit (use "git add" and/or "git commit -a")
Dropped refs/stash@{0} (...)
$ cat grille.txt
6h Reveil
9h Chronique
12h Journal
```

**Indices**

1. La commande qui met de côté porte le nom anglais d'une cachette.
2. Après l'avoir utilisée, `git status` doit annoncer un dossier propre.
3. Pour récupérer, une sous-commande réapplique et retire de la pile.

**Correction officielle**

```bash
printf "6h Reveil\n9h Chronique\n12h Journal\n" > grille.txt
git stash
git status
git switch main
git switch feature/grille
git stash pop
cat grille.txt
```

### Le refuge de montagne

Identifiant : `ch3-e5-refuge`

La branche `fix/tarifs` a été fusionnée la semaine dernière, elle ne sert plus
à rien et encombre la liste.

Liste les branches, supprime `fix/tarifs` avec l'option prudente, celle qui
refuse d'effacer une branche non fusionnée, puis vérifie qu'elle a bien
disparu.

**Exemple**

```
$ git branch
  fix/tarifs
* main
$ git branch -d fix/tarifs
Deleted branch fix/tarifs (was ...).
$ git branch
* main
```

**Indices**

1. L'option prudente est une seule lettre, en minuscule.
2. Sa grande sœur en majuscule force la suppression : on ne l'utilise qu'en dernier recours.
3. Le message de confirmation rappelle l'empreinte du dernier commit supprimé, au cas où.

**Correction officielle**

```bash
git branch
git branch -d fix/tarifs
git branch
```


## Niveau Intermediaire

### La boulangerie

Identifiant : `ch3-i1-boulangerie`

Deux chantiers démarrent le même jour dans la boulangerie : la carte des pains
spéciaux et la fiche des allergènes. Ils ne doivent pas se mélanger.

Crée une branche par chantier, en partant de `main` à jour à chaque fois, et
fais un commit sur chacune. Reviens sur `main` et affiche la liste détaillée
des branches : les trois doivent pointer sur des commits différents.

**Exemple**

```
$ git switch -c feature/pains-speciaux
Switched to a new branch 'feature/pains-speciaux'
$ printf "Pain aux noix\nPain de seigle\n" > pains.txt
$ git add pains.txt
$ git commit -m "feat(pains): carte des pains speciaux"
[feature/pains-speciaux ...] feat(pains): carte des pains speciaux
 1 file changed, 2 insertions(+)
 create mode 100644 pains.txt
$ git switch main
Switched to branch 'main'
$ git switch -c feature/allergenes
Switched to a new branch 'feature/allergenes'
$ printf "Gluten, fruits a coque\n" > allergenes.txt
$ git add allergenes.txt
$ git commit -m "feat(allergenes): premiere fiche"
[feature/allergenes ...] feat(allergenes): premiere fiche
 1 file changed, 1 insertion(+)
 create mode 100644 allergenes.txt
$ git switch main
Switched to branch 'main'
$ git branch -v
  feature/allergenes     ... feat(allergenes): premiere fiche
  feature/pains-speciaux ... feat(pains): carte des pains speciaux
* main                   ... feat(produits): produits de base
```

**Indices**

1. Attention au point de départ : la seconde branche doit partir de `main`, pas de la première.
2. Il faut donc revenir sur `main` entre les deux créations.
3. À la fin, les trois lignes de `git branch -v` doivent afficher trois empreintes différentes.

**Correction officielle**

```bash
git switch -c feature/pains-speciaux
printf "Pain aux noix\nPain de seigle\n" > pains.txt
git add pains.txt
git commit -m "feat(pains): carte des pains speciaux"
git switch main
git switch -c feature/allergenes
printf "Gluten, fruits a coque\n" > allergenes.txt
git add allergenes.txt
git commit -m "feat(allergenes): premiere fiche"
git switch main
git branch -v
```

### La troupe de théâtre

Identifiant : `ch3-i2-theatre`

Tu as commencé à retravailler la distribution, et tu as aussi créé un fichier
de notes personnelles que Git ne suit pas encore. On te demande de basculer sur
`main` tout de suite.

Mets de côté ton travail, **y compris le fichier non suivi**, vérifie que le
dossier est complètement propre, puis récupère tout. Affiche la liste de la
pile avant de récupérer.

**Exemple**

```
$ printf "Hamlet : Lea\nOphelie : Sarah\n" > distribution.txt
$ printf "demander un rappel de texte a Lea\n" > notes-perso.txt
$ git stash -u
Saved working directory and index state WIP on main: ... feat(distribution): premiere distribution
$ git status
On branch main
nothing to commit, working tree clean
$ ls
distribution.txt
$ git stash list
stash@{0}: WIP on main: ... feat(distribution): premiere distribution
$ git stash pop
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   distribution.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	notes-perso.txt

no changes added to commit (use "git add" and/or "git commit -a")
Dropped refs/stash@{0} (...)
$ ls
distribution.txt
notes-perso.txt
```

**Indices**

1. Par défaut, la mise de côté ignore les fichiers non suivis. Une option les embarque aussi.
2. C'est la même lettre que dans « untracked ».
3. Le `ls` juste après doit montrer un fichier de moins que le `ls` final.

**Correction officielle**

```bash
printf "Hamlet : Lea\nOphelie : Sarah\n" > distribution.txt
printf "demander un rappel de texte a Lea\n" > notes-perso.txt
git stash -u
git status
ls
git stash list
git stash pop
ls
```

### Le ciné-club

Identifiant : `ch3-i3-cinema`

Tu travailles sur la programmation du ciné-club, tu as modifié le fichier mais
tu n'as rien enregistré. Tu essaies de basculer sur `main`.

Tente la bascule et lis le refus de Git. Mets alors ton travail de côté,
bascule, reviens, et récupère-le. Le refus fait partie de l'exercice : ne
cherche pas à l'éviter.

**Exemple**

```
$ printf "Lundi : Les Temps modernes\nMardi : Le Cuirasse Potemkine\n" > programme.txt
$ git switch main
error: Your local changes to the following files would be overwritten by checkout:
	programme.txt
Please commit your changes or stash them before you switch branches.
Aborting
$ git stash
Saved working directory and index state WIP on feature/programme: ... feat(programme): cycle Chaplin
$ git switch main
Switched to branch 'main'
$ git switch feature/programme
Switched to branch 'feature/programme'
$ git stash pop
On branch feature/programme
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   programme.txt

no changes added to commit (use "git add" and/or "git commit -a")
Dropped refs/stash@{0} (...)
$ cat programme.txt
Lundi : Les Temps modernes
Mardi : Le Cuirasse Potemkine
```

**Indices**

1. Git refuse de basculer quand un fichier suivi et modifié serait écrasé. C'est une protection.
2. Le message te propose deux solutions : enregistrer, ou mettre de côté.
3. Ici on choisit la seconde, puisque le travail n'est pas fini.

**Correction officielle**

```bash
printf "Lundi : Les Temps modernes\nMardi : Le Cuirasse Potemkine\n" > programme.txt
git switch main
git stash
git switch main
git switch feature/programme
git stash pop
cat programme.txt
```

### La chorale

Identifiant : `ch3-i4-chorale`

La chorale a trois branches en cours et personne ne sait plus où en est
chacune.

Produis l'état des lieux : la liste détaillée des branches, puis l'historique
compact avec le dessin à gauche et toutes les branches. Bascule ensuite sur
`feature/concert` et affiche à nouveau la liste détaillée, pour montrer que
l'étoile a changé de ligne.

**Exemple**

```
$ git branch -v
  feature/concert  ... feat(concert): lieu et horaire
  feature/costumes ... feat(costumes): choix des tuniques
* main             ... feat(repertoire): ajout du cantique
$ git log --oneline --all
... feat(repertoire): ajout du cantique
... feat(costumes): choix des tuniques
... feat(concert): lieu et horaire
... feat(repertoire): premier chant
$ git switch feature/concert
Switched to branch 'feature/concert'
$ git branch -v
* feature/concert  ... feat(concert): lieu et horaire
  feature/costumes ... feat(costumes): choix des tuniques
  main             ... feat(repertoire): ajout du cantique
```

**Indices**

1. Trois commandes de lecture, aucune ne modifie quoi que ce soit.
2. Le dessin à gauche montre les branches qui ont divergé : les barres verticales sont des lignes de temps parallèles.
3. Compare les deux `git branch -v` : seule la position de l'étoile change.

**Correction officielle**

```bash
git branch -v
git log --oneline --all
git switch feature/concert
git branch -v
```

### L'atelier vélo

Identifiant : `ch3-i5-atelier-velo`

L'atelier vélo a une branche `brouillon` qui contient du vrai travail, et une
branche `essai` qui n'a jamais rien donné.

Renomme `brouillon` en `feature/reparations` sans perdre son historique.
Essaie ensuite de supprimer `essai` avec l'option prudente et lis le refus de
Git. Supprime-la pour de bon avec l'option qui force, puisque ce travail est
réellement abandonné. Vérifie la liste à la fin.

**Exemple**

```
$ git branch -m brouillon feature/reparations
$ git branch
  essai
  feature/reparations
* main
$ git branch -d essai
error: the branch 'essai' is not fully merged.
If you are sure you want to delete it, run 'git branch -D essai'
$ git branch -D essai
Deleted branch essai (was ...).
$ git branch
  feature/reparations
* main
```

**Indices**

1. Le renommage accepte deux noms : l'ancien puis le nouveau, même si tu n'es pas dessus.
2. L'option prudente refuse parce que le travail de `essai` n'a jamais été fusionné.
3. L'option qui force est la même lettre, en majuscule. Lis bien le message avant de l'utiliser.

**Correction officielle**

```bash
git branch -m brouillon feature/reparations
git branch
git branch -d essai
git branch -D essai
git branch
```


## Niveau BOSS

### La librairie de quartier

Identifiant : `ch3-b1-librairie`

Journée complète à la librairie. Tu dois mener deux chantiers en parallèle et
gérer une urgence au milieu.

Commence le chantier des rayons sur une branche dédiée, avec un commit. Reviens
sur `main`, commence le chantier du site sur une autre branche, fais un commit,
puis **modifie encore le fichier sans enregistrer**. L'urgence arrive : mets ton
travail en cours de côté, bascule sur `main`, et reviens aussitôt le récupérer.

Termine par la liste détaillée des branches et l'historique compact avec le
dessin et toutes les branches.

**Exemple**

```
$ git switch -c feature/rayons
Switched to a new branch 'feature/rayons'
$ printf "Rayon poche\nRayon jeunesse\n" > rayons.txt
$ git add rayons.txt
$ git commit -m "feat(rayons): plan des rayons"
[feature/rayons ...] feat(rayons): plan des rayons
 1 file changed, 2 insertions(+)
 create mode 100644 rayons.txt
$ git switch main
Switched to branch 'main'
$ git switch -c feature/site
Switched to a new branch 'feature/site'
$ printf "Page accueil\n" > site.txt
$ git add site.txt
$ git commit -m "feat(site): page d'accueil"
[feature/site ...] feat(site): page d'accueil
 1 file changed, 1 insertion(+)
 create mode 100644 site.txt
$ printf "Page accueil\nPage contact\n" > site.txt
$ git stash
Saved working directory and index state WIP on feature/site: ... feat(site): page d'accueil
$ git switch main
Switched to branch 'main'
$ git switch feature/site
Switched to branch 'feature/site'
$ git stash pop
On branch feature/site
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   site.txt

no changes added to commit (use "git add" and/or "git commit -a")
Dropped refs/stash@{0} (...)
$ git branch -v
  feature/rayons ... feat(rayons): plan des rayons
* feature/site   ... feat(site): page d'accueil
  main           ... feat(accueil): presentation
$ git log --oneline --all
... feat(site): page d'accueil
... feat(rayons): plan des rayons
... feat(accueil): presentation
```

**Indices**

1. Treize commandes, et deux retours sur `main` : un entre les chantiers, un pour l'urgence.
2. La seconde branche doit partir de `main`, donc il faut y revenir avant de la créer.
3. La mise de côté ne concerne que la modification non enregistrée, pas le commit déjà fait.

**Correction officielle**

```bash
git switch -c feature/rayons
printf "Rayon poche\nRayon jeunesse\n" > rayons.txt
git add rayons.txt
git commit -m "feat(rayons): plan des rayons"
git switch main
git switch -c feature/site
printf "Page accueil\n" > site.txt
git add site.txt
git commit -m "feat(site): page d'accueil"
printf "Page accueil\nPage contact\n" > site.txt
git stash
git switch main
git switch feature/site
git stash pop
git branch -v
git log --oneline --all
```

### Le musée municipal

Identifiant : `ch3-b2-musee`

Le musée te confie le ménage de ses branches. Il y en a quatre, dans des états
différents, et tu dois les remettre d'équerre.

Fais d'abord l'inventaire : liste détaillée, puis historique compact avec le
dessin et toutes les branches. Renomme ensuite `truc` en `feature/audioguide`,
qui décrit enfin ce qu'elle contient. Supprime `vieux-test` avec l'option
prudente, elle a déjà été fusionnée. Essaie de supprimer `jamais-fini` de la
même façon, constate le refus, et laisse-la en place : ce travail mérite peut
être d'être repris.

Termine par la liste détaillée.

**Exemple**

```
$ git branch -v
  jamais-fini ... feat(suspens): piste non terminee
* main        ... feat(salles): salle moderne
  truc        ... feat(audioguide): version francaise
  vieux-test  ... feat(salles): salle moderne
$ git log --oneline --all
... feat(suspens): piste non terminee
... feat(salles): salle moderne
... feat(audioguide): version francaise
... feat(salles): salle antique
$ git branch -m truc feature/audioguide
$ git branch -d vieux-test
Deleted branch vieux-test (was ...).
$ git branch -d jamais-fini
error: the branch 'jamais-fini' is not fully merged.
If you are sure you want to delete it, run 'git branch -D jamais-fini'
$ git branch -v
  feature/audioguide ... feat(audioguide): version francaise
  jamais-fini        ... feat(suspens): piste non terminee
* main               ... feat(salles): salle moderne
```

**Indices**

1. Six commandes, dans l'ordre de l'énoncé.
2. Une seule des deux suppressions aboutit : l'autre est refusée, et c'est voulu.
3. Ne force rien : le message de refus est la bonne réponse de l'exercice.

**Correction officielle**

```bash
git branch -v
git log --oneline --all
git branch -m truc feature/audioguide
git branch -d vieux-test
git branch -d jamais-fini
git branch -v
```

### Le camping des Pins

Identifiant : `ch3-b3-camping`

Au camping, tu jongles entre deux chantiers et tu as en plus des notes
personnelles qui ne doivent jamais partir dans un commit.

Sur la branche `feature/emplacements`, modifie la carte sans enregistrer, et
crée un fichier `notes-perso.txt`. Mets tout de côté, fichier non suivi
compris. Bascule sur `main`, fais-y un commit sur le règlement, puis reviens et
récupère ton travail.

Enregistre alors uniquement la carte, pas les notes. Termine par un `git status`
qui doit encore signaler le fichier non suivi.

**Exemple**

```
$ printf "Emplacement 1 : ombrage\nEmplacement 2 : plein soleil\n" > carte.txt
$ printf "penser a racheter des piquets\n" > notes-perso.txt
$ git stash -u
Saved working directory and index state WIP on feature/emplacements: ... feat(carte): premier emplacement
$ git switch main
Switched to branch 'main'
$ printf "Silence a partir de 22h\n" > reglement.txt
$ git add reglement.txt
$ git commit -m "feat(reglement): horaires de silence"
[main ...] feat(reglement): horaires de silence
 1 file changed, 1 insertion(+)
 create mode 100644 reglement.txt
$ git switch feature/emplacements
Switched to branch 'feature/emplacements'
$ git stash pop
On branch feature/emplacements
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   carte.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	notes-perso.txt

no changes added to commit (use "git add" and/or "git commit -a")
Dropped refs/stash@{0} (...)
$ git add carte.txt
$ git commit -m "feat(carte): ajout du second emplacement"
[feature/emplacements ...] feat(carte): ajout du second emplacement
 1 file changed, 1 insertion(+)
$ git status
On branch feature/emplacements
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	notes-perso.txt

nothing added to commit but untracked files present (use "git add" to track)
```

**Indices**

1. L'option qui embarque les fichiers non suivis est indispensable ici, sinon les notes resteraient.
2. Après la récupération, c'est à toi de choisir ce qui part au panier.
3. Le `git status` final doit montrer `notes-perso.txt` comme non suivi : c'est la preuve qu'il n'est pas dans l'historique.

**Correction officielle**

```bash
printf "Emplacement 1 : ombrage\nEmplacement 2 : plein soleil\n" > carte.txt
printf "penser a racheter des piquets\n" > notes-perso.txt
git stash -u
git switch main
printf "Silence a partir de 22h\n" > reglement.txt
git add reglement.txt
git commit -m "feat(reglement): horaires de silence"
git switch feature/emplacements
git stash pop
git add carte.txt
git commit -m "feat(carte): ajout du second emplacement"
git status
```

### La brasserie artisanale

Identifiant : `ch3-b4-brasserie`

La brasserie veut trois recettes travaillées en parallèle, chacune sur sa
branche, toutes parties de `main`.

Crée les trois branches `feature/blonde`, `feature/ambree` et `feature/brune`,
avec un commit sur chacune, en revenant bien sur `main` entre chaque. Reviens
sur `main` et fais-y un commit sur le fichier commun des étiquettes.

Termine par la liste détaillée des branches et par l'historique compact avec le
dessin et toutes les branches. Le dessin doit montrer quatre lignes de temps
parallèles.

**Exemple**

```
$ git switch -c feature/blonde
Switched to a new branch 'feature/blonde'
$ printf "Blonde : malt pale, houblon Saaz\n" > blonde.txt
$ git add blonde.txt
$ git commit -m "feat(blonde): recette de la blonde"
[feature/blonde ...] feat(blonde): recette de la blonde
 1 file changed, 1 insertion(+)
 create mode 100644 blonde.txt
$ git switch main
Switched to branch 'main'
$ git switch -c feature/ambree
Switched to a new branch 'feature/ambree'
$ printf "Ambree : malt caramel\n" > ambree.txt
$ git add ambree.txt
$ git commit -m "feat(ambree): recette de l'ambree"
[feature/ambree ...] feat(ambree): recette de l'ambree
 1 file changed, 1 insertion(+)
 create mode 100644 ambree.txt
$ git switch main
Switched to branch 'main'
$ git switch -c feature/brune
Switched to a new branch 'feature/brune'
$ printf "Brune : malt torrefie\n" > brune.txt
$ git add brune.txt
$ git commit -m "feat(brune): recette de la brune"
[feature/brune ...] feat(brune): recette de la brune
 1 file changed, 1 insertion(+)
 create mode 100644 brune.txt
$ git switch main
Switched to branch 'main'
$ printf "Etiquettes rondes, papier kraft\n" > etiquettes.txt
$ git add etiquettes.txt
$ git commit -m "feat(etiquettes): choix du support"
[main ...] feat(etiquettes): choix du support
 1 file changed, 1 insertion(+)
 create mode 100644 etiquettes.txt
$ git branch -v
  feature/ambree ... feat(ambree): recette de l'ambree
  feature/blonde ... feat(blonde): recette de la blonde
  feature/brune  ... feat(brune): recette de la brune
* main           ... feat(etiquettes): choix du support
$ git log --oneline --all
... feat(etiquettes): choix du support
... feat(brune): recette de la brune
... feat(ambree): recette de l'ambree
... feat(blonde): recette de la blonde
... feat(presentation): la brasserie
```

**Indices**

1. Le piège est de créer la deuxième branche depuis la première. Reviens sur `main` à chaque fois.
2. Seize commandes en tout : trois blocs identiques, puis le commit sur `main`, puis les deux lectures.
3. Dans le dessin final, les étoiles doivent apparaître sur des colonnes différentes.

**Correction officielle**

```bash
git switch -c feature/blonde
printf "Blonde : malt pale, houblon Saaz\n" > blonde.txt
git add blonde.txt
git commit -m "feat(blonde): recette de la blonde"
git switch main
git switch -c feature/ambree
printf "Ambree : malt caramel\n" > ambree.txt
git add ambree.txt
git commit -m "feat(ambree): recette de l'ambree"
git switch main
git switch -c feature/brune
printf "Brune : malt torrefie\n" > brune.txt
git add brune.txt
git commit -m "feat(brune): recette de la brune"
git switch main
printf "Etiquettes rondes, papier kraft\n" > etiquettes.txt
git add etiquettes.txt
git commit -m "feat(etiquettes): choix du support"
git branch -v
git log --oneline --all
```

### La ferme pédagogique

Identifiant : `ch3-b5-ferme`

Scénario complet à la ferme. Tu vas enchaîner tout ce que tu sais sur les
branches.

Crée `feature/visites` et fais-y deux commits. Reviens sur `main`, crée
`brouillon-ateliers` et fais-y un commit. Renomme cette seconde branche en
`feature/ateliers`. Reviens sur `main` et fais-y un commit.

Bascule sur `feature/visites`, modifie le fichier sans enregistrer, mets de
côté, reviens sur `main`, puis retourne sur `feature/visites` et récupère.
Enregistre cette dernière modification.

Termine par la liste détaillée et l'historique complet de toutes les branches.

**Exemple**

```
$ git switch -c feature/visites
Switched to a new branch 'feature/visites'
$ printf "Visite 1 : la basse-cour\n" > visites.txt
$ git add visites.txt
$ git commit -m "feat(visites): visite de la basse-cour"
[feature/visites ...] feat(visites): visite de la basse-cour
 1 file changed, 1 insertion(+)
 create mode 100644 visites.txt
$ printf "Visite 1 : la basse-cour\nVisite 2 : la bergerie\n" > visites.txt
$ git commit -am "feat(visites): visite de la bergerie"
[feature/visites ...] feat(visites): visite de la bergerie
 1 file changed, 1 insertion(+)
$ git switch main
Switched to branch 'main'
$ git switch -c brouillon-ateliers
Switched to a new branch 'brouillon-ateliers'
$ printf "Atelier pain\n" > ateliers.txt
$ git add ateliers.txt
$ git commit -m "feat(ateliers): atelier pain"
[brouillon-ateliers ...] feat(ateliers): atelier pain
 1 file changed, 1 insertion(+)
 create mode 100644 ateliers.txt
$ git branch -m feature/ateliers
$ git switch main
Switched to branch 'main'
$ printf "Ferme ouverte du mardi au dimanche\n" > horaires.txt
$ git add horaires.txt
$ git commit -m "feat(horaires): jours d'ouverture"
[main ...] feat(horaires): jours d'ouverture
 1 file changed, 1 insertion(+)
 create mode 100644 horaires.txt
$ git switch feature/visites
Switched to branch 'feature/visites'
$ printf "Visite 1 : la basse-cour\nVisite 2 : la bergerie\nVisite 3 : le potager\n" > visites.txt
$ git stash
Saved working directory and index state WIP on feature/visites: ... feat(visites): visite de la bergerie
$ git switch main
Switched to branch 'main'
$ git switch feature/visites
Switched to branch 'feature/visites'
$ git stash pop
On branch feature/visites
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   visites.txt

no changes added to commit (use "git add" and/or "git commit -a")
Dropped refs/stash@{0} (...)
$ git commit -am "feat(visites): visite du potager"
[feature/visites ...] feat(visites): visite du potager
 1 file changed, 1 insertion(+)
$ git branch -v
  feature/ateliers ... feat(ateliers): atelier pain
* feature/visites  ... feat(visites): visite du potager
  main             ... feat(horaires): jours d'ouverture
$ git log --oneline --all
... feat(visites): visite du potager
... feat(horaires): jours d'ouverture
... feat(ateliers): atelier pain
... feat(visites): visite de la bergerie
... feat(visites): visite de la basse-cour
... feat(presentation): la ferme
```

**Indices**

1. Le renommage se fait depuis la branche elle-même : un seul nom suffit alors.
2. Vingt commandes. Relis l'énoncé paragraphe par paragraphe, chacun est un bloc.
3. La récupération ramène une modification non enregistrée : il reste donc un commit à faire après.

**Correction officielle**

```bash
git switch -c feature/visites
printf "Visite 1 : la basse-cour\n" > visites.txt
git add visites.txt
git commit -m "feat(visites): visite de la basse-cour"
printf "Visite 1 : la basse-cour\nVisite 2 : la bergerie\n" > visites.txt
git commit -am "feat(visites): visite de la bergerie"
git switch main
git switch -c brouillon-ateliers
printf "Atelier pain\n" > ateliers.txt
git add ateliers.txt
git commit -m "feat(ateliers): atelier pain"
git branch -m feature/ateliers
git switch main
printf "Ferme ouverte du mardi au dimanche\n" > horaires.txt
git add horaires.txt
git commit -m "feat(horaires): jours d'ouverture"
git switch feature/visites
printf "Visite 1 : la basse-cour\nVisite 2 : la bergerie\nVisite 3 : le potager\n" > visites.txt
git stash
git switch main
git switch feature/visites
git stash pop
git commit -am "feat(visites): visite du potager"
git branch -v
git log --oneline --all
```

