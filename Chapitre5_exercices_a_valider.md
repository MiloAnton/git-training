# Chapitre 5 - Réparer sans casser

15 exercices. Chaque bloc terminal est la sortie d'une execution reelle de la
correction officielle avec Git 2.43, horloge et identite figees. Les hashs sont
masques par `...` et ne sont pas compares.


## Niveau Echauffement

### L'imprimerie

Identifiant : `ch5-e1-imprimerie`

Tu viens d'enregistrer un commit, et tu t'aperçois que le message est
incompréhensible. Rien n'a été publié, tu peux donc le réécrire.

Affiche l'historique compact pour voir le message fautif, corrige-le, puis
affiche à nouveau l'historique. Le nombre de commits ne doit pas changer, seul
le message.

**Exemple**

```
$ git log --oneline
... truc
... feat(tarifs): premiers tarifs
$ git commit --amend -m "feat(tarifs): ajout du tarif des affiches A2"
[main ...] feat(tarifs): ajout du tarif des affiches A2
 Date: Mon Jan 5 09:49:00 2026 +0100
 1 file changed, 1 insertion(+)
$ git log --oneline
... feat(tarifs): ajout du tarif des affiches A2
... feat(tarifs): premiers tarifs
```

**Indices**

1. L'option cherchée ne crée pas de commit, elle remplace le dernier.
2. Elle s'écrit avec deux tirets et veut dire « amender » en anglais.
3. Garde l'option du message : sans elle, Git ouvrirait un éditeur.

**Correction officielle**

```bash
git log --oneline
git commit --amend -m "feat(tarifs): ajout du tarif des affiches A2"
git log --oneline
```

### La cave à vin

Identifiant : `ch5-e2-cave-vin`

Le dernier commit a été poussé sur le dépôt partagé, et il contient une erreur.
Comme il est déjà public, il ne faut surtout pas réécrire l'historique : on
annule proprement en ajoutant un commit qui fait l'inverse.

Affiche l'historique compact, annule le dernier commit sans réécriture, puis
affiche l'historique et le contenu du fichier.

**Exemple**

```
$ git log --oneline
... feat(cave): erreur de saisie
... feat(cave): stock initial
$ git revert HEAD --no-edit
[main ...] Revert "feat(cave): erreur de saisie"
 Date: Mon Jan 5 10:03:00 2026 +0100
 1 file changed, 1 deletion(-)
$ git log --oneline
... Revert "feat(cave): erreur de saisie"
... feat(cave): erreur de saisie
... feat(cave): stock initial
$ cat cave.txt
Bordeaux 2018 : 24 bouteilles
```

**Indices**

1. La commande qui annule sans réécrire ajoute un commit, elle n'en supprime aucun.
2. L'option `--no-edit` évite que Git demande un message : il en propose un tout fait.
3. Après l'annulation, l'historique compte un commit de plus, pas un de moins.

**Correction officielle**

```bash
git log --oneline
git revert HEAD --no-edit
git log --oneline
cat cave.txt
```

### La salle d'escalade

Identifiant : `ch5-e3-escalade`

Tu as modifié un fichier et tu regrettes : tu veux revenir à la version du
dernier commit, sans toucher au reste.

Affiche le fichier abîmé, remets-le dans l'état du dernier commit avec la
commande prévue pour un seul fichier, affiche-le à nouveau, puis vérifie que le
dossier est propre.

**Exemple**

```
$ cat voies.txt
n importe quoi
$ git restore voies.txt
$ cat voies.txt
Voie bleue : 5a
Voie rouge : 6b
$ git status
On branch main
nothing to commit, working tree clean
```

**Indices**

1. La commande agit sur un fichier, pas sur l'historique : elle ne déplace rien.
2. Elle porte le nom anglais de la restauration.
3. Attention, ce que tu avais tapé est définitivement perdu : c'est le but, mais il faut le savoir.

**Correction officielle**

```bash
cat voies.txt
git restore voies.txt
cat voies.txt
git status
```

### L'école de musique

Identifiant : `ch5-e4-ecole-musique`

Tu as mis trois fichiers au panier d'un coup alors que tu voulais n'en enregistrer
qu'un. Tu veux vider le panier sans perdre une seule ligne de ton travail.

Affiche l'état, vide complètement le panier, affiche l'état à nouveau. Les trois
fichiers doivent toujours être là, simplement plus sélectionnés.

**Exemple**

```
$ git status
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	new file:   planning.txt
	new file:   professeurs.txt
	new file:   salles.txt
$ git reset
$ git status
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	planning.txt
	professeurs.txt
	salles.txt

nothing added to commit but untracked files present (use "git add" to track)
```

**Indices**

1. Sans aucun argument, cette commande remet le panier dans l'état du dernier commit.
2. Elle ne touche ni à l'historique ni au contenu de tes fichiers.
3. Git affiche ensuite la liste de ce qui est ressorti du panier.

**Correction officielle**

```bash
git status
git reset
git status
```

### Le garage

Identifiant : `ch5-e5-garage`

Tu as fait un `git reset --hard` un peu vite et tu as perdu ton dernier commit.
Rien n'est perdu : Git garde la trace de tous les déplacements de HEAD.

Affiche l'historique compact pour constater le dégât, affiche le journal des
déplacements de HEAD, puis affiche à nouveau l'historique. Tu n'as rien à
récupérer dans cet exercice, seulement à savoir où regarder.

**Exemple**

```
$ git log --oneline
... feat(prestations): revision
$ git reflog
... HEAD@{0}: reset: moving to HEAD~1
... HEAD@{1}: commit: feat(prestations): vidange
... HEAD@{2}: commit (initial): feat(prestations): revision
$ git log --oneline
... feat(prestations): revision
```

**Indices**

1. Le journal des déplacements porte un nom qui commence comme « référence ».
2. Il liste les positions successives de HEAD, la plus récente en premier.
3. Chaque ligne donne l'empreinte, la position `HEAD@{n}` et ce qui a provoqué le déplacement.

**Correction officielle**

```bash
git log --oneline
git reflog
git log --oneline
```


## Niveau Intermediaire

### La pharmacie de garde

Identifiant : `ch5-i1-pharmacie`

Les trois modes de `reset` ne font pas la même chose, et c'est tout l'objet de
cet exercice. Tu vas les comparer sur la même situation.

Recule d'un commit en gardant le panier et les fichiers intacts, et regarde
l'état. Recule à nouveau, cette fois en vidant le panier mais en gardant les
fichiers, et regarde l'état. Vérifie enfin que le contenu du fichier n'a jamais
bougé.

**Exemple**

```
$ git log --oneline
... feat(planning): garde du week-end
... feat(planning): garde du jeudi
... feat(planning): garde du lundi
$ git reset --soft HEAD~1
$ git status
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   planning.txt
$ git reset HEAD~1
Unstaged changes after reset:
M	planning.txt
$ git status
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   planning.txt

no changes added to commit (use "git add" and/or "git commit -a")
$ cat planning.txt
Garde : nuit du lundi
Garde : nuit du jeudi
Garde : week-end
```

**Indices**

1. Le premier mode conserve tout sauf la position de HEAD.
2. Le second, qui est celui par défaut, vide aussi le panier.
3. Aucun des deux ne touche à tes fichiers : le `cat` final doit montrer la version la plus récente.

**Correction officielle**

```bash
git log --oneline
git reset --soft HEAD~1
git status
git reset HEAD~1
git status
cat planning.txt
```

### L'hôtel du Lac

Identifiant : `ch5-i2-hotel`

Le dernier commit est bon sur le fond mais il lui manque un fichier que tu as
oublié d'ajouter. Comme rien n'est publié, tu peux le compléter.

Affiche l'historique compact. Ajoute le fichier oublié au panier, complète le
dernier commit sans changer son message, puis vérifie : le nombre de commits ne
doit pas avoir changé, mais le commit doit maintenant contenir deux fichiers.

**Exemple**

```
$ git log --oneline
... feat(services): navette et petit dejeuner
... feat(presentation): l'hotel
$ git status
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	petit-dejeuner.txt

nothing added to commit but untracked files present (use "git add" to track)
$ git add petit-dejeuner.txt
$ git commit --amend -m "feat(services): navette et petit dejeuner"
[main ...] feat(services): navette et petit dejeuner
 Date: Mon Jan 5 09:56:00 2026 +0100
 2 files changed, 2 insertions(+)
 create mode 100644 navette.txt
 create mode 100644 petit-dejeuner.txt
$ git log --oneline
... feat(services): navette et petit dejeuner
... feat(presentation): l'hotel
$ git show HEAD --stat
commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 09:56:00 2026 +0100

    feat(services): navette et petit dejeuner

 navette.txt        | 1 +
 petit-dejeuner.txt | 1 +
 2 files changed, 2 insertions(+)
```

**Indices**

1. Le commit complété reprend tout ce qui est dans le panier au moment où tu l'utilises.
2. Il faut donc d'abord mettre le fichier oublié au panier.
3. Le résumé chiffré final doit montrer deux fichiers créés.

**Correction officielle**

```bash
git log --oneline
git status
git add petit-dejeuner.txt
git commit --amend -m "feat(services): navette et petit dejeuner"
git log --oneline
git show HEAD --stat
```

### Le fablab

Identifiant : `ch5-i3-fablab`

Deux erreurs se sont glissées dans l'historique, et elles n'appellent pas le
même traitement.

Le commit d'il y a deux crans est déjà public : annule-le proprement, sans
réécriture. Le dernier commit, lui, n'a jamais été publié et son message est
mauvais : réécris-le.

Affiche l'historique compact avant et après, et termine par le contenu du
fichier.

**Exemple**

```
$ git log --oneline
... feat(fraiseuse): nouvelle fraiseuse
... feat(machines): decoupe laser
... feat(machines): imprimante 3D
$ git revert HEAD~1 --no-edit
[main ...] Revert "feat(machines): decoupe laser"
 Date: Mon Jan 5 10:24:00 2026 +0100
 1 file changed, 1 deletion(-)
$ git commit --amend -m "fix(machines): annulation de la ligne du laser"
[main ...] fix(machines): annulation de la ligne du laser
 Date: Mon Jan 5 10:24:00 2026 +0100
 1 file changed, 1 deletion(-)
$ git log --oneline
... fix(machines): annulation de la ligne du laser
... feat(fraiseuse): nouvelle fraiseuse
... feat(machines): decoupe laser
... feat(machines): imprimante 3D
$ cat machines.txt
Imprimante 3D : 1
```

**Indices**

1. La règle d'or du cours : si c'est poussé, on annule par un nouveau commit ; si c'est local, on réécrit.
2. L'annulation crée un commit, que tu réécris ensuite avec l'autre commande.
3. À la fin, l'historique compte un commit de plus qu'au départ, et non deux.

**Correction officielle**

```bash
git log --oneline
git revert HEAD~1 --no-edit
git commit --amend -m "fix(machines): annulation de la ligne du laser"
git log --oneline
cat machines.txt
```

### La savonnerie

Identifiant : `ch5-i4-savonnerie`

La branche `feature/parfums` contient quatre petits commits brouillons. Tu veux
les faire entrer dans `main` sous la forme d'un seul commit propre.

Place-toi sur `main`, prépare l'intégration groupée, regarde l'état pour
constater que tout est au panier mais que rien n'est encore enregistré, puis
fais le commit unique. Termine par l'historique compact de toutes les branches.

**Exemple**

```
$ git switch main
Already on 'main'
$ git merge --squash feature/parfums
Updating ...
Fast-forward
Squash commit -- not updating HEAD
 parfums.txt | 4 ++++
 1 file changed, 4 insertions(+)
 create mode 100644 parfums.txt
$ git status
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	new file:   parfums.txt
$ git commit -m "feat(parfums): gamme complete des parfums"
[main ...] feat(parfums): gamme complete des parfums
 1 file changed, 4 insertions(+)
 create mode 100644 parfums.txt
$ git log --oneline --all
... feat(parfums): gamme complete des parfums
... wip parfum 4
... wip parfum 3
... wip parfum 2
... wip parfum 1
... feat(presentation): la savonnerie
```

**Indices**

1. L'option cherchée prépare le résultat dans le panier sans créer de commit de fusion.
2. Après elle, c'est à toi de faire le commit, avec le message que tu veux.
3. L'historique final ne garde aucune trace des quatre brouillons sur `main`.

**Correction officielle**

```bash
git switch main
git merge --squash feature/parfums
git status
git commit -m "feat(parfums): gamme complete des parfums"
git log --oneline --all
```

### La scierie

Identifiant : `ch5-i5-scierie`

Tu as mis un fichier au panier par erreur, et tu en as abîmé un autre dans ton
dossier de travail. Deux problèmes, deux remèdes, et il ne faut pas les
confondre.

Affiche l'état. Retire du panier le fichier qui n'a rien à y faire, sans perdre
son contenu. Remets ensuite dans l'état du dernier commit le fichier que tu as
abîmé. Affiche l'état et les deux fichiers pour vérifier.

**Exemple**

```
$ git status
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	new file:   brouillon.txt

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   stock.txt
$ git restore --staged brouillon.txt
$ git restore stock.txt
$ git status
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	brouillon.txt

nothing added to commit but untracked files present (use "git add" to track)
$ cat stock.txt
Chene : 12 m3
Hetre : 8 m3
$ cat brouillon.txt
idees en vrac pour la scierie
```

**Indices**

1. Le premier remède agit sur le panier, le second sur le dossier de travail.
2. C'est la même commande, avec une option qui change tout : elle désigne la zone visée.
3. Le `cat` final prouve que le premier fichier a gardé son contenu, et que le second est revenu à la version enregistrée.

**Correction officielle**

```bash
git status
git restore --staged brouillon.txt
git restore stock.txt
git status
cat stock.txt
cat brouillon.txt
```


## Niveau BOSS

### La chocolaterie

Identifiant : `ch5-b1-chocolaterie`

Trois réparations à mener dans l'ordre, chacune avec le bon outil.

Le dernier commit n'est pas publié et son message ne respecte pas le format :
réécris-le. Le commit d'il y a deux crans est publié et contient des horaires
faux : annule-le proprement. Un fichier de ton dossier a été abîmé : remets-le
dans l'état du dernier commit.

Affiche l'historique compact au début et à la fin, et termine par le journal des
déplacements de HEAD.

**Exemple**

```
$ git log --oneline
... ganache
... feat(conditionnement): boites de 12
... feat(horaires): horaires errones
... feat(recettes): la praline
... feat(presentation): la chocolaterie
$ git commit --amend -m "feat(recettes): ajout de la ganache"
[main ...] feat(recettes): ajout de la ganache
 Date: Mon Jan 5 10:52:00 2026 +0100
 1 file changed, 1 insertion(+)
$ git revert HEAD~2 --no-edit
[main ...] Revert "feat(horaires): horaires errones"
 Date: Mon Jan 5 11:20:00 2026 +0100
 1 file changed, 1 deletion(-)
 delete mode 100644 horaires.txt
$ git restore conditionnement.txt
$ git status
On branch main
nothing to commit, working tree clean
$ git log --oneline
... Revert "feat(horaires): horaires errones"
... feat(recettes): ajout de la ganache
... feat(conditionnement): boites de 12
... feat(horaires): horaires errones
... feat(recettes): la praline
... feat(presentation): la chocolaterie
$ git reflog
... HEAD@{0}: revert: Revert "feat(horaires): horaires errones"
... HEAD@{1}: commit (amend): feat(recettes): ajout de la ganache
... HEAD@{2}: commit: ganache
... HEAD@{3}: commit: feat(conditionnement): boites de 12
... HEAD@{4}: commit: feat(horaires): horaires errones
... HEAD@{5}: commit: feat(recettes): la praline
... HEAD@{6}: commit (initial): feat(presentation): la chocolaterie
```

**Indices**

1. Trois outils différents : un pour réécrire, un pour annuler sans réécrire, un pour un fichier.
2. L'ordre de l'énoncé est le bon : la réécriture d'abord, sinon les crans changeraient de place.
3. Le journal final doit montrer la trace des deux déplacements que tu viens de provoquer.

**Correction officielle**

```bash
git log --oneline
git commit --amend -m "feat(recettes): ajout de la ganache"
git revert HEAD~2 --no-edit
git restore conditionnement.txt
git status
git log --oneline
git reflog
```

### La conserverie

Identifiant : `ch5-b2-conserverie`

Tu vas parcourir les trois modes de `reset` sur un même dépôt, et constater
précisément ce que chacun conserve.

Affiche l'historique compact. Recule d'un commit en gardant tout, puis affiche
l'état et le fichier. Reviens au commit le plus récent grâce au journal des
déplacements : repère-le d'abord avec le journal, puis reviens-y.

Recule enfin d'un commit en jetant tout, et constate que cette fois le fichier a
changé. Affiche l'état et le fichier une dernière fois.

**Exemple**

```
$ git log --oneline
... feat(bocaux): stock de 1 litre
... feat(bocaux): stock de 500 ml
$ git reset --soft HEAD~1
$ git status
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   bocaux.txt
$ cat bocaux.txt
Bocaux 500 ml : 200
Bocaux 1 l : 120
$ git reflog
... HEAD@{0}: reset: moving to HEAD~1
... HEAD@{1}: commit: feat(bocaux): stock de 1 litre
... HEAD@{2}: commit (initial): feat(bocaux): stock de 500 ml
$ git reset --hard HEAD@{1}
HEAD is now at ... feat(bocaux): stock de 1 litre
$ git log --oneline
... feat(bocaux): stock de 1 litre
... feat(bocaux): stock de 500 ml
$ git reset --hard HEAD~1
HEAD is now at ... feat(bocaux): stock de 500 ml
$ git status
On branch main
nothing to commit, working tree clean
$ cat bocaux.txt
Bocaux 500 ml : 200
```

**Indices**

1. Le premier mode garde le panier et les fichiers : seul HEAD recule.
2. Le journal des déplacements se désigne par `HEAD@{n}`, et on peut l'utiliser comme une référence.
3. Le dernier mode est le seul destructif : c'est pour ça qu'on ne l'utilise jamais sur du travail publié.

**Correction officielle**

```bash
git log --oneline
git reset --soft HEAD~1
git status
cat bocaux.txt
git reflog
git reset --hard HEAD@{1}
git log --oneline
git reset --hard HEAD~1
git status
cat bocaux.txt
```

### La serre municipale

Identifiant : `ch5-b3-serre`

La branche `feature/semis` contient cinq commits de travail en cours, aux
messages inutilisables. L'équipe veut un seul commit propre sur `main`, et elle
veut aussi vérifier ce qu'elle intègre avant de le faire.

Place-toi sur `main`. Compare d'abord `main` à la branche, en résumé chiffré.
Prépare ensuite l'intégration groupée, affiche l'état, puis fais le commit
unique avec un message au bon format.

Vérifie enfin : historique compact de toutes les branches, détail du dernier
commit en résumé chiffré, et liste des branches.

**Exemple**

```
$ git switch main
Already on 'main'
$ git diff --stat main feature/semis
 semis.txt | 5 +++++
 1 file changed, 5 insertions(+)
$ git merge --squash feature/semis
Updating ...
Fast-forward
Squash commit -- not updating HEAD
 semis.txt | 5 +++++
 1 file changed, 5 insertions(+)
 create mode 100644 semis.txt
$ git status
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	new file:   semis.txt
$ git commit -m "feat(semis): calendrier complet des semis"
[main ...] feat(semis): calendrier complet des semis
 1 file changed, 5 insertions(+)
 create mode 100644 semis.txt
$ git log --oneline --all
... feat(semis): calendrier complet des semis
... wip 5
... wip 4
... wip 3
... wip 2
... wip 1
... feat(presentation): la serre
$ git show HEAD --stat
commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 11:41:00 2026 +0100

    feat(semis): calendrier complet des semis

 semis.txt | 5 +++++
 1 file changed, 5 insertions(+)
$ git branch
  feature/semis
* main
```

**Indices**

1. La comparaison se fait avant l'intégration, elle ne modifie rien.
2. L'option d'intégration groupée ne crée pas de commit : elle remplit le panier.
3. Sur `main`, l'historique ne gagne qu'un seul commit, alors que la branche en comptait cinq.

**Correction officielle**

```bash
git switch main
git diff --stat main feature/semis
git merge --squash feature/semis
git status
git commit -m "feat(semis): calendrier complet des semis"
git log --oneline --all
git show HEAD --stat
git branch
```

### L'atelier de reliure

Identifiant : `ch5-b4-atelier-reliure`

Tu vas provoquer volontairement une perte, puis la réparer. C'est l'exercice de
sauvetage du chapitre.

Affiche l'historique compact. Recule brutalement de deux commits en jetant tout,
et constate la perte dans l'historique et dans le fichier. Ouvre le journal des
déplacements de HEAD, repère la position d'avant la catastrophe, et reviens-y.

Vérifie que l'historique et le fichier sont revenus, puis affiche le journal une
dernière fois : il doit contenir la trace des deux allers-retours.

**Exemple**

```
$ git log --oneline
... feat(techniques): reliure copte
... feat(techniques): dos carre colle
... feat(techniques): couture japonaise
$ git reset --hard HEAD~2
HEAD is now at ... feat(techniques): couture japonaise
$ git log --oneline
... feat(techniques): couture japonaise
$ cat techniques.txt
Couture a la japonaise
$ git reflog
... HEAD@{0}: reset: moving to HEAD~2
... HEAD@{1}: commit: feat(techniques): reliure copte
... HEAD@{2}: commit: feat(techniques): dos carre colle
... HEAD@{3}: commit (initial): feat(techniques): couture japonaise
$ git reset --hard HEAD@{1}
HEAD is now at ... feat(techniques): reliure copte
$ git log --oneline
... feat(techniques): reliure copte
... feat(techniques): dos carre colle
... feat(techniques): couture japonaise
$ cat techniques.txt
Couture a la japonaise
Dos carre colle
Reliure copte
$ git reflog
... HEAD@{0}: reset: moving to HEAD@{1}
... HEAD@{1}: reset: moving to HEAD~2
... HEAD@{2}: commit: feat(techniques): reliure copte
... HEAD@{3}: commit: feat(techniques): dos carre colle
... HEAD@{4}: commit (initial): feat(techniques): couture japonaise
```

**Indices**

1. Le journal des déplacements est la seule chose qui survit à un reset destructif.
2. `HEAD@{1}` désigne la position précédente de HEAD, celle d'avant le reset.
3. On peut passer cette notation à `reset` comme n'importe quelle référence.

**Correction officielle**

```bash
git log --oneline
git reset --hard HEAD~2
git log --oneline
cat techniques.txt
git reflog
git reset --hard HEAD@{1}
git log --oneline
cat techniques.txt
git reflog
```

### La brocante

Identifiant : `ch5-b5-brocante`

Dernier exercice du chapitre : un dépôt en désordre, et tous les outils de
réparation à mobiliser.

Première partie. Le dernier commit n'est pas publié et son message est mauvais :
réécris-le. Affiche l'historique compact.

Deuxième partie. Un fichier a été abîmé dans le dossier, et un autre a été mis
au panier par erreur. Répare les deux, chacun avec le bon outil, puis affiche
l'état. Fais-le avant de toucher à l'historique : Git refuse d'annuler un commit
quand un fichier concerné est modifié dans ton dossier.

Troisième partie. Le commit d'il y a deux crans est publié et contient une
erreur : annule-le proprement, puis affiche son effet avec le détail du dernier
commit.

Termine par l'historique compact et le journal des déplacements.

**Exemple**

```
$ git commit --amend -m "feat(stands): ajout du stand des livres"
[main ...] feat(stands): ajout du stand des livres
 Date: Mon Jan 5 10:45:00 2026 +0100
 2 files changed, 2 insertions(+)
 create mode 100644 brouillon.txt
$ git log --oneline
... feat(stands): ajout du stand des livres
... feat(stands): stand buvette
... feat(tarifs): emplacement couvert
... feat(tarifs): prix de l'emplacement
... feat(presentation): la brocante
$ git restore tarifs.txt
$ git restore --staged brouillon.txt
$ git status
On branch main
nothing to commit, working tree clean
$ git revert HEAD~2 --no-edit
[main ...] Revert "feat(tarifs): emplacement couvert"
 Date: Mon Jan 5 11:48:00 2026 +0100
 1 file changed, 1 deletion(-)
$ git show HEAD --stat
commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 11:48:00 2026 +0100

    Revert "feat(tarifs): emplacement couvert"
    
    This reverts commit ....

 tarifs.txt | 1 -
 1 file changed, 1 deletion(-)
$ git log --oneline
... Revert "feat(tarifs): emplacement couvert"
... feat(stands): ajout du stand des livres
... feat(stands): stand buvette
... feat(tarifs): emplacement couvert
... feat(tarifs): prix de l'emplacement
... feat(presentation): la brocante
$ git reflog
... HEAD@{0}: revert: Revert "feat(tarifs): emplacement couvert"
... HEAD@{1}: commit (amend): feat(stands): ajout du stand des livres
... HEAD@{2}: commit: stands
... HEAD@{3}: commit: feat(stands): stand buvette
... HEAD@{4}: commit: feat(tarifs): emplacement couvert
... HEAD@{5}: commit: feat(tarifs): prix de l'emplacement
... HEAD@{6}: commit (initial): feat(presentation): la brocante
```

**Indices**

1. Neuf commandes, et quatre outils différents : amend, revert, restore, et restore sur le panier.
2. Compte les crans après la réécriture, pas avant : elle ne change pas le nombre de commits.
3. Les deux réparations de la deuxième partie utilisent la même commande, avec et sans l'option du panier.

**Correction officielle**

```bash
git commit --amend -m "feat(stands): ajout du stand des livres"
git log --oneline
git restore tarifs.txt
git restore --staged brouillon.txt
git status
git revert HEAD~2 --no-edit
git show HEAD --stat
git log --oneline
git reflog
```

