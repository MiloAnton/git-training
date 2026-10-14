# Chapitre 6 - Les conflits

15 exercices. Chaque bloc terminal est la sortie d'une execution reelle de la
correction officielle avec Git 2.43, horloge et identite figees. Les hashs sont
masques par `...` et ne sont pas compares.


## Niveau Echauffement

### Le menu de la cantine

Identifiant : `ch6-e1-menu-cantine`

Deux personnes ont modifié la même ligne du menu, chacune sur sa branche. La
fusion va échouer, et c'est exactement ce qu'on veut observer.

Lance la fusion, lis le message, puis regarde l'état du dépôt. Affiche enfin le
fichier pour voir les marqueurs que Git a écrits dedans. Tu ne résous rien dans
cet exercice : tu constates.

**Exemple**

```
$ git merge feature/mardi
Auto-merging menu.txt
CONFLICT (content): Merge conflict in menu.txt
Automatic merge failed; fix conflicts and then commit the result.
$ git status
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   menu.txt

no changes added to commit (use "git add" and/or "git commit -a")
$ cat menu.txt
Lundi : gratin
<<<<<<< HEAD
Mardi : lasagnes
=======
Mardi : poisson pane
>>>>>>> feature/mardi
```

**Indices**

1. La fusion se lance depuis la branche qui reçoit, comme d'habitude.
2. Git ne choisit jamais à ta place quand deux versions touchent la même ligne.
3. Les marqueurs encadrent les deux versions : la tienne au-dessus, la leur en dessous.

**Correction officielle**

```bash
git merge feature/mardi
git status
cat menu.txt
```

### La fiche des horaires

Identifiant : `ch6-e2-fiche-horaires`

Un conflit est en cours sur le dépôt. Tu dois d'abord savoir quels fichiers sont
concernés avant de toucher à quoi que ce soit.

Affiche l'état, puis la liste des seuls fichiers en conflit, celle qui ne montre
que les noms. Affiche enfin le fichier concerné.

**Exemple**

```
$ git status
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   horaires.txt

no changes added to commit (use "git add" and/or "git commit -a")
$ git diff --name-only --diff-filter=U
horaires.txt
$ cat horaires.txt
Ouverture : 9h
<<<<<<< HEAD
Fermeture : 18h
=======
Fermeture : 20h
>>>>>>> feature/soir
```

**Indices**

1. La commande de comparaison accepte un filtre sur l'état des fichiers.
2. La lettre du filtre est l'initiale de « unmerged » en anglais.
3. Combine-la avec l'option qui ne montre que les noms, sans le détail des lignes.

**Correction officielle**

```bash
git status
git diff --name-only --diff-filter=U
cat horaires.txt
```

### La liste du matériel

Identifiant : `ch6-e3-liste-materiel`

Le conflit est là, et tu as décidé : c'est ta version qui doit l'emporter.

Affiche le fichier en conflit, garde ta version avec la commande prévue, affiche
le fichier à nouveau, puis marque le conflit comme résolu. Termine par l'état du
dépôt.

**Exemple**

```
$ cat materiel.txt
Projecteur
<<<<<<< HEAD
Sono : modele B
=======
Sono : modele A
>>>>>>> feature/sono
$ git restore --ours -- materiel.txt
$ cat materiel.txt
Projecteur
Sono : modele B
$ git add materiel.txt
$ git status
On branch main
All conflicts fixed but you are still merging.
  (use "git commit" to conclude merge)
```

**Indices**

1. Deux options opposées existent : l'une garde ta version, l'autre la leur.
2. « ours » désigne la branche sur laquelle tu te trouves, celle qui reçoit la fusion.
3. Choisir ne suffit pas : il faut ensuite marquer le conflit comme résolu, avec la commande habituelle.

**Correction officielle**

```bash
cat materiel.txt
git restore --ours -- materiel.txt
cat materiel.txt
git add materiel.txt
git status
```

### Faire machine arrière

Identifiant : `ch6-e4-annulation`

Un conflit est en cours et tu préfères y revenir plus tard, au calme. Tu veux
remettre le dépôt exactement dans l'état d'avant la fusion.

Affiche l'état, annule complètement la fusion, affiche l'état à nouveau et le
contenu du fichier. Tout doit être revenu comme avant.

**Exemple**

```
$ git status
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   tarifs.txt

no changes added to commit (use "git add" and/or "git commit -a")
$ git merge --abort
$ git status
On branch main
nothing to commit, working tree clean
$ cat tarifs.txt
Entree : 6 euros
```

**Indices**

1. L'option cherchée s'écrit avec deux tirets et veut dire « abandonner ».
2. Elle remet le dossier et le panier exactement dans l'état d'avant la fusion.
3. Après elle, `git status` ne doit plus parler de fichiers en conflit du tout.

**Correction officielle**

```bash
git status
git merge --abort
git status
cat tarifs.txt
```

### Trancher et finir

Identifiant : `ch6-e5-resolution-simple`

Un conflit est en cours. Tu vas le résoudre en gardant leur version, puis
terminer la fusion.

Affiche le fichier, garde leur version, marque le conflit comme résolu, termine
la fusion avec un message clair, puis affiche l'historique compact de toutes les
branches.

**Exemple**

```
$ cat couleurs.txt
<<<<<<< HEAD
Couleur principale : bleu
=======
Couleur principale : vert
>>>>>>> feature/charte
$ git restore --theirs -- couleurs.txt
$ git add couleurs.txt
$ git commit -m "fix(couleurs): resolution du conflit, on garde le vert"
[main ...] fix(couleurs): resolution du conflit, on garde le vert
$ git log --oneline --all
... fix(couleurs): resolution du conflit, on garde le vert
... feat(couleurs): le bleu
... feat(couleurs): le vert
... feat(couleurs): charte a definir
```

**Indices**

1. « theirs » désigne la branche que tu es en train de faire entrer.
2. Après avoir choisi, il faut marquer la résolution avant de pouvoir terminer.
3. Le commit final est le commit de fusion : il ferme le conflit.

**Correction officielle**

```bash
cat couleurs.txt
git restore --theirs -- couleurs.txt
git add couleurs.txt
git commit -m "fix(couleurs): resolution du conflit, on garde le vert"
git log --oneline --all
```


## Niveau Intermediaire

### Le journal local

Identifiant : `ch6-i1-journal-local`

Tu vas provoquer le conflit toi-même, le diagnostiquer, puis le résoudre en
gardant ta version.

Lance la fusion et lis le refus. Diagnostique : état du dépôt, liste des seuls
fichiers en conflit, contenu du fichier. Résous en gardant ta version, marque la
résolution, termine la fusion.

Affiche l'historique compact de toutes les branches pour finir.

**Exemple**

```
$ git merge feature/edito
Auto-merging une.txt
CONFLICT (content): Merge conflict in une.txt
Automatic merge failed; fix conflicts and then commit the result.
$ git status
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   une.txt

no changes added to commit (use "git add" and/or "git commit -a")
$ git diff --name-only --diff-filter=U
une.txt
$ cat une.txt
<<<<<<< HEAD
Une : la piscine rouvre
=======
Une : le marche renait
>>>>>>> feature/edito
Pages : 12
$ git restore --ours -- une.txt
$ git add une.txt
$ git commit -m "fix(une): resolution du conflit sur le titre"
[main ...] fix(une): resolution du conflit sur le titre
$ git log --oneline --all
... fix(une): resolution du conflit sur le titre
... feat(une): titre sur la piscine
... feat(une): titre sur le marche
... feat(une): maquette
```

**Indices**

1. Le diagnostic vient toujours avant la décision : trois commandes pour voir, une pour trancher.
2. Le filtre sur l'état des fichiers est celui des fichiers non fusionnés.
3. Une fois le choix fait, la marque de résolution puis le commit ferment la fusion.

**Correction officielle**

```bash
git merge feature/edito
git status
git diff --name-only --diff-filter=U
cat une.txt
git restore --ours -- une.txt
git add une.txt
git commit -m "fix(une): resolution du conflit sur le titre"
git log --oneline --all
```

### La recette de famille

Identifiant : `ch6-i2-recette-famille`

Deux branches ont modifié la même ligne, mais aussi des lignes différentes.
Git va résoudre tout seul ce qu'il peut, et ne te laisser que le vrai conflit.

Lance la fusion, lis le message, affiche le fichier. Observe bien : une partie a
été fusionnée automatiquement, et seule une ligne porte les marqueurs. Résous en
gardant leur version, marque la résolution et termine.

Affiche le fichier une dernière fois.

**Exemple**

```
$ git merge feature/cuisson
Auto-merging tarte.txt
CONFLICT (content): Merge conflict in tarte.txt
Automatic merge failed; fix conflicts and then commit the result.
$ cat tarte.txt
Pate brisee
<<<<<<< HEAD
Pommes golden
Cuisson : 45 min a 170 degres
=======
Pommes
Cuisson : 35 min a 180 degres
>>>>>>> feature/cuisson
Servir tiede
$ git restore --theirs -- tarte.txt
$ git add tarte.txt
$ git commit -m "fix(tarte): resolution sur le temps de cuisson"
[main ...] fix(tarte): resolution sur le temps de cuisson
$ cat tarte.txt
Pate brisee
Pommes
Cuisson : 35 min a 180 degres
Servir tiede
```

**Indices**

1. Git ne signale un conflit que là où les deux versions touchent la même zone.
2. Les lignes modifiées d'un seul côté sont intégrées sans rien te demander.
3. Regarde bien le fichier avant de trancher : tout n'est pas en conflit.

**Correction officielle**

```bash
git merge feature/cuisson
cat tarte.txt
git restore --theirs -- tarte.txt
git add tarte.txt
git commit -m "fix(tarte): resolution sur le temps de cuisson"
cat tarte.txt
```

### Reprendre au calme

Identifiant : `ch6-i3-reprise-calme`

Tu vas abandonner une fusion, puis la refaire proprement.

Lance la fusion et constate le conflit. Annule-la complètement et vérifie que le
dépôt est propre. Relance la même fusion, et cette fois résous-la en gardant ta
version, marque la résolution et termine.

Affiche l'historique compact de toutes les branches.

**Exemple**

```
$ git merge feature/adresse
Auto-merging contact.txt
CONFLICT (content): Merge conflict in contact.txt
Automatic merge failed; fix conflicts and then commit the result.
$ git merge --abort
$ git status
On branch main
nothing to commit, working tree clean
$ git merge feature/adresse
Auto-merging contact.txt
CONFLICT (content): Merge conflict in contact.txt
Automatic merge failed; fix conflicts and then commit the result.
$ git restore --ours -- contact.txt
$ git add contact.txt
$ git commit -m "fix(contact): resolution du conflit d'adresse"
[main ...] fix(contact): resolution du conflit d'adresse
$ git log --oneline --all
... fix(contact): resolution du conflit d'adresse
... feat(contact): adresse place du Marche
... feat(contact): adresse rue des Lilas
... feat(contact): fiche de contact
```

**Indices**

1. L'annulation remet tout en place : tu peux relancer la fusion comme si de rien n'était.
2. Entre les deux, `git status` doit annoncer un dossier propre.
3. La seconde fusion échouera exactement de la même façon : c'est normal, le conflit n'a pas disparu.

**Correction officielle**

```bash
git merge feature/adresse
git merge --abort
git status
git merge feature/adresse
git restore --ours -- contact.txt
git add contact.txt
git commit -m "fix(contact): resolution du conflit d'adresse"
git log --oneline --all
```

### Un pull plus propre

Identifiant : `ch6-i4-pull-propre`

Le dépôt distant a avancé pendant que tu travaillais, et tes commits locaux ne
sont pas encore publiés. Un `pull` ordinaire créerait un commit de fusion inutile.

Affiche l'état, puis récupère le travail distant en rejouant tes commits
par-dessus, pour garder un historique en ligne droite. Affiche l'historique
compact, puis publie.

**Exemple**

```
$ git status
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
$ git pull --rebase
From https://github.com/leonis-formation/depot-asso.git
   ...  main       -> origin/main
Rebasing (1/1)

                                                                                
Successfully rebased and updated refs/heads/main.
$ git log --oneline
... feat(adhesion): montant de l'adhesion
... feat(reunion): date de la reunion
... feat(accueil): presentation
$ git push
To https://github.com/leonis-formation/depot-asso.git
   ...  main -> main
$ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

**Indices**

1. L'option cherchée change la façon dont `pull` intègre : au lieu de fusionner, il rejoue.
2. Le résultat est un historique sans commit de fusion, donc plus simple à relire.
3. À n'utiliser que sur des commits qui n'ont pas encore été publiés.

**Correction officielle**

```bash
git status
git pull --rebase
git log --oneline
git push
git status
```

### Le kit de diagnostic

Identifiant : `ch6-i5-kit-complet`

Un conflit est en cours et on te demande un diagnostic complet avant toute
décision.

Affiche l'état, la liste des seuls fichiers en conflit, le contenu du fichier, et
l'historique compact de toutes les branches pour comprendre d'où viennent les
deux versions.

Résous ensuite en gardant leur version, marque la résolution et termine la
fusion. Affiche l'historique compact pour finir.

**Exemple**

```
$ git status
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   regles.txt

no changes added to commit (use "git add" and/or "git commit -a")
$ git diff --name-only --diff-filter=U
regles.txt
$ cat regles.txt
<<<<<<< HEAD
Nombre de joueurs : 11
=======
Nombre de joueurs : 7
>>>>>>> feature/club
Duree : 90 min
$ git log --oneline --all
... feat(regles): onze joueurs
... feat(regles): sept joueurs
... feat(regles): premieres regles
$ git restore --theirs -- regles.txt
$ git add regles.txt
$ git commit -m "fix(regles): resolution, on garde la version du club"
[main ...] fix(regles): resolution, on garde la version du club
$ git log --oneline --all
... fix(regles): resolution, on garde la version du club
... feat(regles): onze joueurs
... feat(regles): sept joueurs
... feat(regles): premieres regles
```

**Indices**

1. Quatre commandes de diagnostic, puis trois de résolution.
2. L'historique de toutes les branches montre les deux commits à l'origine du conflit.
3. Compare les deux historiques compacts, avant et après : un commit de fusion est apparu.

**Correction officielle**

```bash
git status
git diff --name-only --diff-filter=U
cat regles.txt
git log --oneline --all
git restore --theirs -- regles.txt
git add regles.txt
git commit -m "fix(regles): resolution, on garde la version du club"
git log --oneline --all
```


## Niveau BOSS

### Le site de l'association

Identifiant : `ch6-b1-site-asso`

Scénario complet de conflit, du diagnostic à la publication.

Lance la fusion de `feature/refonte` et constate le conflit. Diagnostique
complètement : état, liste des fichiers en conflit, contenu du fichier,
historique compact de toutes les branches.

Résous en gardant ta version, marque la résolution, et termine la fusion avec un
message qui documente le choix.

Vérifie : état, historique compact de toutes les branches, détail du commit de
fusion en résumé chiffré.

**Exemple**

```
$ git merge feature/refonte
Auto-merging accueil.txt
CONFLICT (content): Merge conflict in accueil.txt
Automatic merge failed; fix conflicts and then commit the result.
$ git status
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   accueil.txt

no changes added to commit (use "git add" and/or "git commit -a")
$ git diff --name-only --diff-filter=U
accueil.txt
$ cat accueil.txt
<<<<<<< HEAD
Slogan : ensemble, plus forts depuis 1998
=======
Slogan : agir ensemble
>>>>>>> feature/refonte
Contact : contact@asso.fr
$ git log --oneline --all
... feat(accueil): slogan avec la date
... feat(accueil): nouveau slogan
... feat(accueil): page d'accueil
$ git restore --ours -- accueil.txt
$ git add accueil.txt
$ git commit -m "fix(accueil): resolution du conflit, on garde le slogan actuel"
[main ...] fix(accueil): resolution du conflit, on garde le slogan actuel
$ git status
On branch main
nothing to commit, working tree clean
$ git log --oneline --all
... fix(accueil): resolution du conflit, on garde le slogan actuel
... feat(accueil): slogan avec la date
... feat(accueil): nouveau slogan
... feat(accueil): page d'accueil
$ git show HEAD --stat
commit ...
Merge: ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 11:13:00 2026 +0100

    fix(accueil): resolution du conflit, on garde le slogan actuel
```

**Indices**

1. Onze commandes : une fusion, quatre de diagnostic, trois de résolution, trois de vérification.
2. Documente ton choix dans le message de commit : dans six mois, personne ne s'en souviendra.
3. Le détail final doit montrer le commit de fusion, avec ses deux parents.

**Correction officielle**

```bash
git merge feature/refonte
git status
git diff --name-only --diff-filter=U
cat accueil.txt
git log --oneline --all
git restore --ours -- accueil.txt
git add accueil.txt
git commit -m "fix(accueil): resolution du conflit, on garde le slogan actuel"
git status
git log --oneline --all
git show HEAD --stat
```

### Deux fichiers en conflit

Identifiant : `ch6-b2-double-conflit`

Cette fois deux fichiers sont en conflit en même temps, et tu ne vas pas les
traiter de la même façon.

Lance la fusion et diagnostique : état et liste des fichiers en conflit. Affiche
les deux fichiers.

Pour le premier, garde ta version. Pour le second, garde la leur. Marque les deux
résolutions, vérifie l'état, puis termine la fusion.

Affiche les deux fichiers et l'historique compact de toutes les branches.

**Exemple**

```
$ git merge feature/saison
Auto-merging horaires.txt
CONFLICT (content): Merge conflict in horaires.txt
Auto-merging tarifs.txt
CONFLICT (content): Merge conflict in tarifs.txt
Automatic merge failed; fix conflicts and then commit the result.
$ git status
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   horaires.txt
	both modified:   tarifs.txt

no changes added to commit (use "git add" and/or "git commit -a")
$ git diff --name-only --diff-filter=U
horaires.txt
tarifs.txt
$ cat tarifs.txt
<<<<<<< HEAD
Entree : 6 euros
=======
Entree : 7 euros
>>>>>>> feature/saison
$ cat horaires.txt
<<<<<<< HEAD
Ouverture : 11h
=======
Ouverture : 9h
>>>>>>> feature/saison
$ git restore --ours -- tarifs.txt
$ git restore --theirs -- horaires.txt
$ git add tarifs.txt
$ git add horaires.txt
$ git status
On branch main
All conflicts fixed but you are still merging.
  (use "git commit" to conclude merge)

Changes to be committed:
	modified:   horaires.txt
$ git commit -m "fix(saison): resolution, nos tarifs et leurs horaires"
[main ...] fix(saison): resolution, nos tarifs et leurs horaires
$ cat tarifs.txt
Entree : 6 euros
$ cat horaires.txt
Ouverture : 9h
$ git log --oneline --all
... fix(saison): resolution, nos tarifs et leurs horaires
... feat(saison): ajustement de la saison
... feat(saison): nouvelle saison
... feat(saison): tarifs et horaires
```

**Indices**

1. La liste des fichiers en conflit doit en afficher deux : c'est le point de départ.
2. Les deux options opposées s'utilisent fichier par fichier, dans la même fusion.
3. Le `git status` avant le commit doit ne plus signaler aucun fichier non fusionné.

**Correction officielle**

```bash
git merge feature/saison
git status
git diff --name-only --diff-filter=U
cat tarifs.txt
cat horaires.txt
git restore --ours -- tarifs.txt
git restore --theirs -- horaires.txt
git add tarifs.txt
git add horaires.txt
git status
git commit -m "fix(saison): resolution, nos tarifs et leurs horaires"
cat tarifs.txt
cat horaires.txt
git log --oneline --all
```

### Essayer, annuler, recommencer

Identifiant : `ch6-b3-essai-erreur`

Tu vas traiter le même conflit de deux façons, pour voir la différence.

Première tentative. Lance la fusion, résous en gardant ta version, marque la
résolution, puis change d'avis : annule complètement la fusion avant de la
terminer. Vérifie que le dépôt est propre.

Seconde tentative. Relance la fusion, résous cette fois en gardant leur version,
marque la résolution et termine.

Affiche le fichier et l'historique compact de toutes les branches.

**Exemple**

```
$ git merge feature/affiche
Auto-merging affiche.txt
CONFLICT (content): Merge conflict in affiche.txt
Automatic merge failed; fix conflicts and then commit the result.
$ git restore --ours -- affiche.txt
$ git add affiche.txt
$ git merge --abort
$ git status
On branch main
nothing to commit, working tree clean
$ git merge feature/affiche
Auto-merging affiche.txt
CONFLICT (content): Merge conflict in affiche.txt
Automatic merge failed; fix conflicts and then commit the result.
$ git restore --theirs -- affiche.txt
$ git add affiche.txt
$ git commit -m "fix(affiche): resolution, on garde leur visuel"
[main ...] fix(affiche): resolution, on garde leur visuel
$ cat affiche.txt
Visuel : photo noir et blanc
Format : A2
$ git log --oneline --all
... fix(affiche): resolution, on garde leur visuel
... feat(affiche): illustration coloree
... feat(affiche): photo noir et blanc
... feat(affiche): cahier des charges
```

**Indices**

1. L'annulation fonctionne même après avoir marqué une résolution, tant que le commit n'est pas fait.
2. C'est précisément ce qui rend la commande sûre : rien n'est définitif avant le commit.
3. La seconde tentative repart du même conflit, puisque rien n'a été enregistré.

**Correction officielle**

```bash
git merge feature/affiche
git restore --ours -- affiche.txt
git add affiche.txt
git merge --abort
git status
git merge feature/affiche
git restore --theirs -- affiche.txt
git add affiche.txt
git commit -m "fix(affiche): resolution, on garde leur visuel"
cat affiche.txt
git log --oneline --all
```

### Le dépôt partagé

Identifiant : `ch6-b4-depot-partage`

Le dépôt distant a avancé et tu as des commits locaux. Tu vas comparer les deux
façons d'intégrer.

Affiche l'état et constate que ton envoi serait refusé : essaie de publier. Puis
récupère le travail distant en rejouant tes commits par-dessus, pour garder une
ligne droite.

Affiche l'historique compact, publie, et vérifie l'état. Termine par le détail du
dernier commit en résumé chiffré.

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
$ git pull --rebase
From https://github.com/leonis-formation/depot-club.git
   ...  main       -> origin/main
Rebasing (1/1)

                                                                                
Successfully rebased and updated refs/heads/main.
$ git log --oneline
... feat(cotisation): montant annuel
... feat(sorties): sortie du dimanche
... feat(presentation): le club
$ git push
To https://github.com/leonis-formation/depot-club.git
   ...  main -> main
$ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
$ git show HEAD --stat
commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 11:20:00 2026 +0100

    feat(cotisation): montant annuel

 cotisation.txt | 1 +
 1 file changed, 1 insertion(+)
```

**Indices**

1. Le refus du premier envoi fait partie de l'exercice : lis bien ce que Git te répond.
2. L'option de rejeu évite le commit de fusion que produirait un `pull` ordinaire.
3. Après le rejeu, l'historique est en ligne droite : aucun commit n'a deux parents.

**Correction officielle**

```bash
git status
git push
git pull --rebase
git log --oneline
git push
git status
git show HEAD --stat
```

### Le grand final

Identifiant : `ch6-b5-grand-final`

Dernier exercice de la plateforme. Tu mobilises tout ce que tu sais.

Première partie. Crée la branche `feature/programme` depuis `main`, fais-y un
commit sur le fichier `programme.txt`. Reviens sur `main` et modifie la même
ligne du même fichier, puis enregistre.

Deuxième partie. Lance la fusion et diagnostique complètement : état, liste des
fichiers en conflit, contenu du fichier, historique compact de toutes les
branches.

Troisième partie. Résous en gardant leur version, marque la résolution, vérifie
l'état, puis termine la fusion avec un message clair.

Quatrième partie. Vérifie tout : historique compact de toutes les branches,
détail du commit de fusion en résumé chiffré, contenu du fichier, et liste des
branches. Supprime enfin la branche fusionnée.

**Exemple**

```
$ git switch -c feature/programme
Switched to a new branch 'feature/programme'
$ printf "Samedi : concert\nDimanche : a definir\n" > programme.txt
$ git add programme.txt
$ git commit -m "feat(programme): concert du samedi"
[feature/programme ...] feat(programme): concert du samedi
 1 file changed, 2 insertions(+)
 create mode 100644 programme.txt
$ printf "Samedi : concert\nDimanche : brocante\n" > programme.txt
$ git commit -am "feat(programme): brocante le dimanche"
[feature/programme ...] feat(programme): brocante le dimanche
 1 file changed, 1 insertion(+), 1 deletion(-)
$ git switch main
Switched to branch 'main'
$ printf "Samedi : a definir\nDimanche : vide-grenier\n" > programme.txt
$ git add programme.txt
$ git commit -m "feat(programme): vide-grenier le dimanche"
[main ...] feat(programme): vide-grenier le dimanche
 1 file changed, 2 insertions(+)
 create mode 100644 programme.txt
$ git merge feature/programme
Auto-merging programme.txt
CONFLICT (add/add): Merge conflict in programme.txt
Automatic merge failed; fix conflicts and then commit the result.
$ git status
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both added:      programme.txt

no changes added to commit (use "git add" and/or "git commit -a")
$ git diff --name-only --diff-filter=U
programme.txt
$ cat programme.txt
<<<<<<< HEAD
Samedi : a definir
Dimanche : vide-grenier
=======
Samedi : concert
Dimanche : brocante
>>>>>>> feature/programme
$ git log --oneline --all
... feat(programme): vide-grenier le dimanche
... feat(programme): brocante le dimanche
... feat(programme): concert du samedi
... feat(presentation): la fete
$ git restore --theirs -- programme.txt
$ git add programme.txt
$ git status
On branch main
All conflicts fixed but you are still merging.
  (use "git commit" to conclude merge)

Changes to be committed:
	modified:   programme.txt
$ git commit -m "fix(programme): resolution, on garde le programme de la branche"
[main ...] fix(programme): resolution, on garde le programme de la branche
$ git log --oneline --all
... fix(programme): resolution, on garde le programme de la branche
... feat(programme): vide-grenier le dimanche
... feat(programme): brocante le dimanche
... feat(programme): concert du samedi
... feat(presentation): la fete
$ git show HEAD --stat
commit ...
Merge: ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 11:48:00 2026 +0100

    fix(programme): resolution, on garde le programme de la branche

 programme.txt | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
$ cat programme.txt
Samedi : concert
Dimanche : brocante
$ git branch
  feature/programme
* main
$ git branch -d feature/programme
Deleted branch feature/programme (was ...).
```

**Indices**

1. Vingt commandes, quatre parties. Traite-les une par une, en relisant l'énoncé à chaque fois.
2. La branche et `main` touchent la même ligne du même fichier : le conflit est garanti.
3. La suppression de la branche n'est possible qu'après la fusion, sinon l'option prudente refuse.

**Correction officielle**

```bash
git switch -c feature/programme
printf "Samedi : concert\nDimanche : a definir\n" > programme.txt
git add programme.txt
git commit -m "feat(programme): concert du samedi"
printf "Samedi : concert\nDimanche : brocante\n" > programme.txt
git commit -am "feat(programme): brocante le dimanche"
git switch main
printf "Samedi : a definir\nDimanche : vide-grenier\n" > programme.txt
git add programme.txt
git commit -m "feat(programme): vide-grenier le dimanche"
git merge feature/programme
git status
git diff --name-only --diff-filter=U
cat programme.txt
git log --oneline --all
git restore --theirs -- programme.txt
git add programme.txt
git status
git commit -m "fix(programme): resolution, on garde le programme de la branche"
git log --oneline --all
git show HEAD --stat
cat programme.txt
git branch
git branch -d feature/programme
```

