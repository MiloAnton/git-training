# Chapitre 4 - Fusionner

15 exercices. Chaque bloc terminal est la sortie d'une execution reelle de la
correction officielle avec Git 2.43, horloge et identite figees. Les hashs sont
masques par `...` et ne sont pas compares.


## Niveau Echauffement

### La gazette du lycée

Identifiant : `ch4-e1-gazette`

La correction d'une coquille a été faite sur la branche `fix/titre`, et `main`
n'a pas bougé depuis.

Bascule sur `main`, fusionne la branche, et lis bien la réponse de Git : il
annonce un fast-forward, c'est à dire qu'il a simplement avancé le pointeur
sans créer de commit de fusion. Termine par l'historique compact avec le
dessin : il doit rester une ligne droite.

**Exemple**

```
$ git switch main
Already on 'main'
$ git merge fix/titre
Updating ...
Fast-forward
 une.txt | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
$ git log --oneline --graph
* ... fix(une): correction du titre
* ... feat(une): premiere une
```

**Indices**

1. La fusion se lance depuis la branche qui reçoit, jamais depuis celle qui donne.
2. Lis la première ligne de la réponse : elle contient le mot qui désigne ce type de fusion.
3. Le dessin final ne doit comporter aucune barre oblique : l'historique est resté linéaire.

**Correction officielle**

```bash
git switch main
git merge fix/titre
git log --oneline --graph
```

### La salle de sport

Identifiant : `ch4-e2-salle-sport`

Pendant que le planning était retravaillé sur sa branche, quelqu'un a modifié
les tarifs sur `main`. Les deux lignes de temps ont donc divergé.

Fusionne `feature/planning` dans `main` et lis la réponse : cette fois Git crée
un commit de fusion. Termine par l'historique compact avec le dessin et toutes
les branches.

**Exemple**

```
$ git switch main
Already on 'main'
$ git merge feature/planning
Merge made by the 'ort' strategy.
 planning.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 planning.txt
$ git log --oneline --all
... Merge branch 'feature/planning'
... feat(tarifs): tarif etudiant
... feat(planning): creneau cardio
... feat(tarifs): tarif annuel
```

**Indices**

1. Même commande qu'au premier exercice, mais la situation de départ est différente.
2. `main` a avancé depuis la divergence, donc le fast-forward est impossible.
3. Dans le dessin, repère le commit de fusion : c'est celui qui a deux traits qui le rejoignent.

**Correction officielle**

```bash
git switch main
git merge feature/planning
git log --oneline --all
```

### L'atelier poterie

Identifiant : `ch4-e3-poterie`

Le travail sur la branche `feature/four` est terminé, et `main` n'a pas bougé.
Un fast-forward serait donc possible, mais l'atelier veut garder une trace
explicite de ce lot de travail.

Force la création d'un commit de fusion avec l'option adaptée, puis affiche
l'historique de toutes les branches.

**Exemple**

```
$ git switch main
Already on 'main'
$ git merge --no-ff feature/four
Merge made by the 'ort' strategy.
 four.txt | 2 ++
 1 file changed, 2 insertions(+)
 create mode 100644 four.txt
$ git log --oneline --all
... Merge branch 'feature/four'
... feat(four): procedure d'emaillage
... feat(four): fiche du four
... feat(atelier): presentation
```

**Indices**

1. L'option demande à Git de ne pas faire de fast-forward, même quand il le pourrait.
2. Elle s'écrit avec deux tirets et reprend le nom de la stratégie qu'on refuse.
3. Le dessin montre alors un commit de fusion, alors que sans l'option la ligne serait restée droite.

**Correction officielle**

```bash
git switch main
git merge --no-ff feature/four
git log --oneline --all
```

### Le marché de Noël

Identifiant : `ch4-e4-marche`

L'équipe du marché de Noël exige un historique parfaitement linéaire. Toute
fusion qui créerait un commit de fusion doit échouer plutôt que d'être faite.

Essaie de fusionner `feature/chalets` avec l'option qui garantit la linéarité.
Lis le refus. Fusionne ensuite `fix/affiche`, qui elle est bien dans l'axe,
avec la même option. Termine par l'historique avec le dessin.

**Exemple**

```
$ git switch main
Already on 'main'
$ git merge --ff-only feature/chalets
hint: Diverging branches can't be fast-forwarded, you need to either:
hint: 
hint: 	git merge --no-ff
hint: 
hint: or:
hint: 
hint: 	git rebase
hint: 
hint: Disable this message with "git config advice.diverging false"
fatal: Not possible to fast-forward, aborting.
$ git merge --ff-only fix/affiche
Updating ...
Fast-forward
 affiche.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 affiche.txt
$ git log --oneline --all
... fix(affiche): format et couleur
... feat(presentation): ajout des dates
... feat(chalets): nombre de chalets
... feat(presentation): le marche
```

**Indices**

1. L'option s'écrit avec deux tirets et contient les deux lettres du fast-forward.
2. La première fusion échoue parce que `main` a avancé de son côté : c'est voulu.
3. La seconde réussit, parce que cette branche est partie du commit où `main` se trouve encore.

**Correction officielle**

```bash
git switch main
git merge --ff-only feature/chalets
git merge --ff-only fix/affiche
git log --oneline --all
```

### La jardinerie

Identifiant : `ch4-e5-jardinerie`

La branche `feature/arrosage` est fusionnée et ne sert plus. On fait le ménage
dans la foulée, comme le recommande le cours.

Bascule sur `main`, fusionne la branche, supprime-la avec l'option prudente,
puis affiche la liste des branches et l'historique avec le dessin.

**Exemple**

```
$ git switch main
Already on 'main'
$ git merge feature/arrosage
Updating ...
Fast-forward
 arrosage.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 arrosage.txt
$ git branch -d feature/arrosage
Deleted branch feature/arrosage (was ...).
$ git branch
* main
$ git log --oneline --graph
* ... feat(arrosage): horaires d'arrosage
* ... feat(presentation): la jardinerie
```

**Indices**

1. L'ordre compte : on ne supprime une branche qu'après l'avoir fusionnée.
2. L'option prudente de suppression n'accepte que les branches déjà fusionnées, ce qui tombe bien.
3. Supprimer la branche n'efface pas ses commits : ils sont désormais sur `main`.

**Correction officielle**

```bash
git switch main
git merge feature/arrosage
git branch -d feature/arrosage
git branch
git log --oneline --graph
```


## Niveau Intermediaire

### L'auto-école

Identifiant : `ch4-i1-auto-ecole`

Deux branches attendent d'être intégrées, et elles ne relèvent pas du même
traitement. `fix/horaires` est une correction d'une ligne. `feature/simulateur`
est une vraie fonctionnalité, qui mérite une trace explicite.

Fusionne la correction en laissant Git choisir, puis la fonctionnalité en
forçant le commit de fusion. Termine par l'historique avec le dessin et toutes
les branches, puis supprime les deux branches fusionnées.

**Exemple**

```
$ git switch main
Already on 'main'
$ git merge fix/horaires
Updating ...
Fast-forward
 infos.txt | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
$ git merge --no-ff feature/simulateur
Merge made by the 'ort' strategy.
 simulateur.txt | 2 ++
 1 file changed, 2 insertions(+)
 create mode 100644 simulateur.txt
$ git log --oneline --all
... Merge branch 'feature/simulateur'
... feat(simulateur): duree des seances
... feat(simulateur): deux postes
... fix(infos): correction des horaires
... feat(infos): informations generales
$ git branch -d fix/horaires
Deleted branch fix/horaires (was ...).
$ git branch -d feature/simulateur
Deleted branch feature/simulateur (was ...).
```

**Indices**

1. La règle du cours : si la fonctionnalité est importante, on préfère garder la trace.
2. La première fusion se fait sans option, la seconde avec celle qui refuse le fast-forward.
3. Les suppressions se font après les fusions, sinon l'option prudente refuserait.

**Correction officielle**

```bash
git switch main
git merge fix/horaires
git merge --no-ff feature/simulateur
git log --oneline --all
git branch -d fix/horaires
git branch -d feature/simulateur
```

### Le food truck

Identifiant : `ch4-i2-food-truck`

Trois branches sont prêtes et doivent rentrer dans `main` l'une après l'autre.
Tu vas voir que la première passe en fast-forward, et que les suivantes ne le
peuvent plus.

Fusionne-les dans l'ordre : `feature/burger`, puis `feature/dessert`, puis
`feature/boissons`. Lis chaque réponse. Termine par l'historique avec le dessin
et toutes les branches.

**Exemple**

```
$ git switch main
Already on 'main'
$ git merge feature/burger
Updating ...
Fast-forward
 burger.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 burger.txt
$ git merge feature/dessert
Merge made by the 'ort' strategy.
 dessert.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 dessert.txt
$ git merge feature/boissons
Merge made by the 'ort' strategy.
 boissons.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 boissons.txt
$ git log --oneline --all
... Merge branch 'feature/boissons'
... Merge branch 'feature/dessert'
... feat(boissons): limonade
... feat(dessert): tarte citron
... feat(burger): burger du jour
... feat(carte): ouverture
```

**Indices**

1. Quatre fusions à la suite, sans aucune option.
2. La première avance simplement le pointeur, les deux autres créent un commit de fusion.
3. Demande-toi après chaque fusion si `main` a bougé : c'est ça qui décide.

**Correction officielle**

```bash
git switch main
git merge feature/burger
git merge feature/dessert
git merge feature/boissons
git log --oneline --all
```

### La ressourcerie

Identifiant : `ch4-i3-ressourcerie`

Avant de fusionner, la ressourcerie veut savoir ce qu'elle intègre.

Bascule sur `main`, compare `main` et `feature/collecte` pour voir l'écart,
puis le même écart sous forme de résumé chiffré. Fusionne ensuite en forçant le
commit de fusion, et affiche le détail de ce commit de fusion.

Termine par l'historique de toutes les branches.

**Exemple**

```
$ git switch main
Already on 'main'
$ git diff main feature/collecte
diff --git a/collecte.txt b/collecte.txt
new file mode 100644
index ...
--- /dev/null
+++ b/collecte.txt
@@ -0,0 +1 @@
+Collecte : mardi et samedi
diff --git a/presentation.txt b/presentation.txt
index ... 100644
--- a/presentation.txt
+++ b/presentation.txt
@@ -1,2 +1 @@
 Ressourcerie du Pont
-Ouverte a tous
$ git diff --stat main feature/collecte
 collecte.txt     | 1 +
 presentation.txt | 1 -
 2 files changed, 1 insertion(+), 1 deletion(-)
$ git merge --no-ff feature/collecte
Merge made by the 'ort' strategy.
 collecte.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 collecte.txt
$ git show HEAD --stat
commit ...
Merge: ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 10:52:00 2026 +0100

    Merge branch 'feature/collecte'

 collecte.txt | 1 +
 1 file changed, 1 insertion(+)
$ git log --oneline --all
... Merge branch 'feature/collecte'
... feat(presentation): precision
... feat(collecte): jours de collecte
... feat(presentation): la ressourcerie
```

**Indices**

1. Une comparaison accepte deux noms de branches, exactement comme deux commits.
2. L'ordre compte : la branche de départ en premier, sinon les plus et les moins sont inversés.
3. Après la fusion, le dernier commit est le commit de fusion : c'est lui que tu affiches.

**Correction officielle**

```bash
git switch main
git diff main feature/collecte
git diff --stat main feature/collecte
git merge --no-ff feature/collecte
git show HEAD --stat
git log --oneline --all
```

### Le club d'échecs

Identifiant : `ch4-i4-club-echecs`

Le club veut comprendre la différence entre les deux stratégies, sur une même
situation de départ.

`main` n'a pas bougé depuis la divergence. Fusionne d'abord `feature/tournoi`
normalement et regarde le dessin. Puis fusionne `feature/cours` en forçant le
commit de fusion, et regarde à nouveau le dessin.

Deux fusions, deux dessins, et la différence doit sauter aux yeux.

**Exemple**

```
$ git switch main
Already on 'main'
$ git merge feature/tournoi
Updating ...
Fast-forward
 tournoi.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 tournoi.txt
$ git log --oneline --all
... feat(cours): cours debutants
... feat(tournoi): date du tournoi
... feat(presentation): le club
$ git merge --no-ff feature/cours
Merge made by the 'ort' strategy.
 cours.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 cours.txt
$ git log --oneline --all
... Merge branch 'feature/cours'
... feat(cours): cours debutants
... feat(tournoi): date du tournoi
... feat(presentation): le club
```

**Indices**

1. Les deux branches partent du même commit, donc les deux pourraient passer en fast-forward.
2. C'est l'option de la seconde fusion qui change tout.
3. Compare les deux dessins : le second fait apparaître une bifurcation qui n'existait pas.

**Correction officielle**

```bash
git switch main
git merge feature/tournoi
git log --oneline --all
git merge --no-ff feature/cours
git log --oneline --all
```

### La pépinière

Identifiant : `ch4-i5-pepiniere`

La pépinière applique une règle stricte : tout ce qui entre dans `main` doit
être tracé par un commit de fusion, et les branches doivent être supprimées
derrière.

Fusionne `feature/semis` et `feature/greffes` en forçant la trace à chaque
fois, supprime les deux branches, puis affiche la liste des branches
restantes et l'historique avec le dessin.

**Exemple**

```
$ git switch main
Already on 'main'
$ git merge --no-ff feature/semis
Merge made by the 'ort' strategy.
 semis.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 semis.txt
$ git merge --no-ff feature/greffes
Merge made by the 'ort' strategy.
 greffes.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 greffes.txt
$ git branch -d feature/semis
Deleted branch feature/semis (was ...).
$ git branch -d feature/greffes
Deleted branch feature/greffes (was ...).
$ git branch
* main
$ git log --oneline --all
... Merge branch 'feature/greffes'
... Merge branch 'feature/semis'
... feat(greffes): calendrier des greffes
... feat(semis): calendrier des semis
... feat(presentation): la pepiniere
```

**Indices**

1. Sept commandes, deux fusions et deux suppressions.
2. L'option qui force la trace s'applique à chaque fusion, il faut la répéter.
3. À la fin, `git branch` ne doit plus afficher qu'une seule ligne.

**Correction officielle**

```bash
git switch main
git merge --no-ff feature/semis
git merge --no-ff feature/greffes
git branch -d feature/semis
git branch -d feature/greffes
git branch
git log --oneline --all
```


## Niveau BOSS

### Le festival de musique

Identifiant : `ch4-b1-festival`

Veille de bouclage du festival. Quatre branches attendent, et chacune relève
d'un traitement différent.

Place-toi sur `main`. Fusionne `fix/typo`, une correction d'une ligne, sans
option. Fusionne `feature/scene` en forçant la trace, c'est un gros lot.
Essaie de fusionner `feature/buvette` avec l'option qui exige la linéarité,
constate le refus, puis fusionne-la normalement. Laisse `abandonnee` de côté.

Supprime les trois branches fusionnées avec l'option prudente, essaie de
supprimer `abandonnee` de la même façon et constate le second refus. Termine
par la liste des branches et l'historique complet de toutes les branches.

**Exemple**

```
$ git switch main
Already on 'main'
$ git merge fix/typo
Updating ...
Fast-forward
 presentation.txt | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
$ git merge --no-ff feature/scene
Merge made by the 'ort' strategy.
 scene.txt | 2 ++
 1 file changed, 2 insertions(+)
 create mode 100644 scene.txt
$ git merge --ff-only feature/buvette
hint: Diverging branches can't be fast-forwarded, you need to either:
hint: 
hint: 	git merge --no-ff
hint: 
hint: or:
hint: 
hint: 	git rebase
hint: 
hint: Disable this message with "git config advice.diverging false"
fatal: Not possible to fast-forward, aborting.
$ git merge feature/buvette
Merge made by the 'ort' strategy.
 buvette.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 buvette.txt
$ git branch -d fix/typo
Deleted branch fix/typo (was ...).
$ git branch -d feature/scene
Deleted branch feature/scene (was ...).
$ git branch -d feature/buvette
Deleted branch feature/buvette (was ...).
$ git branch -d abandonnee
error: the branch 'abandonnee' is not fully merged.
If you are sure you want to delete it, run 'git branch -D abandonnee'
$ git branch
  abandonnee
* main
$ git log --oneline --all
... Merge branch 'feature/buvette'
... Merge branch 'feature/scene'
... feat(idee): piste non retenue
... feat(buvette): points de vente
... feat(scene): seconde scene
... feat(scene): capacite
... fix(presentation): precision sur la duree
... feat(presentation): le festival
```

**Indices**

1. Onze commandes. Deux d'entre elles doivent échouer, et c'est l'énoncé qui le demande.
2. Après la première fusion forcée, `main` a avancé : la linéarité devient impossible.
3. La suppression d'une branche jamais fusionnée est refusée par l'option prudente. On ne force pas.

**Correction officielle**

```bash
git switch main
git merge fix/typo
git merge --no-ff feature/scene
git merge --ff-only feature/buvette
git merge feature/buvette
git branch -d fix/typo
git branch -d feature/scene
git branch -d feature/buvette
git branch -d abandonnee
git branch
git log --oneline --all
```

### L'espace de coworking

Identifiant : `ch4-b2-coworking`

L'espace de coworking veut comprendre ce qu'il intègre avant de l'intégrer.
Tu vas donc inspecter, puis fusionner, puis vérifier.

Place-toi sur `main`. Affiche l'écart entre `main` et `feature/salles`, puis son
résumé chiffré. Fusionne en forçant la trace. Affiche le commit de fusion avec
son résumé chiffré, puis l'historique compact de toutes les branches.

Recommence le même cycle complet avec `feature/tarifs`, puis supprime les deux
branches.

**Exemple**

```
$ git switch main
Already on 'main'
$ git diff --stat main feature/salles
 presentation.txt | 1 -
 salles.txt       | 2 ++
 2 files changed, 2 insertions(+), 1 deletion(-)
$ git merge --no-ff feature/salles
Merge made by the 'ort' strategy.
 salles.txt | 2 ++
 1 file changed, 2 insertions(+)
 create mode 100644 salles.txt
$ git show HEAD --stat
commit ...
Merge: ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 11:20:00 2026 +0100

    Merge branch 'feature/salles'

 salles.txt | 2 ++
 1 file changed, 2 insertions(+)
$ git log --oneline --all
... Merge branch 'feature/salles'
... feat(presentation): ouverture 7j/7
... feat(tarifs): grille tarifaire
... feat(salles): deux salles
... feat(presentation): l'espace
$ git diff --stat main feature/tarifs
 presentation.txt | 1 -
 salles.txt       | 2 --
 tarifs.txt       | 2 ++
 3 files changed, 2 insertions(+), 3 deletions(-)
$ git merge --no-ff feature/tarifs
Merge made by the 'ort' strategy.
 tarifs.txt | 2 ++
 1 file changed, 2 insertions(+)
 create mode 100644 tarifs.txt
$ git show HEAD --stat
commit ...
Merge: ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 11:48:00 2026 +0100

    Merge branch 'feature/tarifs'

 tarifs.txt | 2 ++
 1 file changed, 2 insertions(+)
$ git branch -d feature/salles
Deleted branch feature/salles (was ...).
$ git branch -d feature/tarifs
Deleted branch feature/tarifs (was ...).
$ git log --oneline --all
... Merge branch 'feature/tarifs'
... Merge branch 'feature/salles'
... feat(presentation): ouverture 7j/7
... feat(tarifs): grille tarifaire
... feat(salles): deux salles
... feat(presentation): l'espace
```

**Indices**

1. Onze commandes : deux cycles identiques, puis le ménage et la vue finale.
2. Le commit de fusion est toujours le dernier : `HEAD` le désigne juste après la fusion.
3. Les deux fusions forcent la trace, donc l'historique final compte deux bifurcations.

**Correction officielle**

```bash
git switch main
git diff --stat main feature/salles
git merge --no-ff feature/salles
git show HEAD --stat
git log --oneline --all
git diff --stat main feature/tarifs
git merge --no-ff feature/tarifs
git show HEAD --stat
git branch -d feature/salles
git branch -d feature/tarifs
git log --oneline --all
```

### L'épicerie coopérative

Identifiant : `ch4-b3-epicerie`

L'épicerie travaille en parallèle sur trois sujets, et tu dois tout intégrer
en respectant une consigne précise sur chaque.

Crée d'abord `feature/vrac` depuis `main` et fais-y deux commits. Reviens sur
`main` et fais-y un commit sur les horaires. Crée `fix/etiquette` depuis `main`
et fais-y un commit.

Intègre ensuite : `fix/etiquette` sans option, puis `feature/vrac` en forçant
la trace. Supprime les deux branches. Termine par l'historique avec le dessin
et toutes les branches, puis par le détail du dernier commit de fusion.

**Exemple**

```
$ git switch -c feature/vrac
Switched to a new branch 'feature/vrac'
$ printf "Vrac : legumineuses\n" > vrac.txt
$ git add vrac.txt
$ git commit -m "feat(vrac): legumineuses"
[feature/vrac ...] feat(vrac): legumineuses
 1 file changed, 1 insertion(+)
 create mode 100644 vrac.txt
$ printf "Vrac : legumineuses\nVrac : cereales\n" > vrac.txt
$ git commit -am "feat(vrac): cereales"
[feature/vrac ...] feat(vrac): cereales
 1 file changed, 1 insertion(+)
$ git switch main
Switched to branch 'main'
$ printf "Ouvert du mardi au samedi\n" > horaires.txt
$ git add horaires.txt
$ git commit -m "feat(horaires): jours d'ouverture"
[main ...] feat(horaires): jours d'ouverture
 1 file changed, 1 insertion(+)
 create mode 100644 horaires.txt
$ git switch -c fix/etiquette
Switched to a new branch 'fix/etiquette'
$ printf "Etiquettes : prix au kilo\n" > etiquettes.txt
$ git add etiquettes.txt
$ git commit -m "fix(etiquettes): prix au kilo"
[fix/etiquette ...] fix(etiquettes): prix au kilo
 1 file changed, 1 insertion(+)
 create mode 100644 etiquettes.txt
$ git switch main
Switched to branch 'main'
$ git merge fix/etiquette
Updating ...
Fast-forward
 etiquettes.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 etiquettes.txt
$ git merge --no-ff feature/vrac
Merge made by the 'ort' strategy.
 vrac.txt | 2 ++
 1 file changed, 2 insertions(+)
 create mode 100644 vrac.txt
$ git branch -d fix/etiquette
Deleted branch fix/etiquette (was ...).
$ git branch -d feature/vrac
Deleted branch feature/vrac (was ...).
$ git log --oneline --all
... Merge branch 'feature/vrac'
... fix(etiquettes): prix au kilo
... feat(horaires): jours d'ouverture
... feat(vrac): cereales
... feat(vrac): legumineuses
... feat(presentation): l'epicerie
$ git show HEAD --stat
commit ...
Merge: ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 11:34:00 2026 +0100

    Merge branch 'feature/vrac'

 vrac.txt | 2 ++
 1 file changed, 2 insertions(+)
```

**Indices**

1. Attention au point de départ de `fix/etiquette` : elle part de `main` après le commit des horaires.
2. La première fusion passe en fast-forward, la seconde ne le peut pas et on force en plus la trace.
3. Dix-sept commandes. Traite l'énoncé paragraphe par paragraphe.

**Correction officielle**

```bash
git switch -c feature/vrac
printf "Vrac : legumineuses\n" > vrac.txt
git add vrac.txt
git commit -m "feat(vrac): legumineuses"
printf "Vrac : legumineuses\nVrac : cereales\n" > vrac.txt
git commit -am "feat(vrac): cereales"
git switch main
printf "Ouvert du mardi au samedi\n" > horaires.txt
git add horaires.txt
git commit -m "feat(horaires): jours d'ouverture"
git switch -c fix/etiquette
printf "Etiquettes : prix au kilo\n" > etiquettes.txt
git add etiquettes.txt
git commit -m "fix(etiquettes): prix au kilo"
git switch main
git merge fix/etiquette
git merge --no-ff feature/vrac
git branch -d fix/etiquette
git branch -d feature/vrac
git log --oneline --all
git show HEAD --stat
```

### Le studio d'enregistrement

Identifiant : `ch4-b4-studio`

Le studio veut deux historiques différents pour comparer, et c'est à toi de
les produire.

Première partie. Fusionne `feature/micros` normalement, puis affiche
l'historique avec le dessin. Note qu'il est resté linéaire.

Deuxième partie. Fusionne `feature/cabine` en forçant la trace, puis affiche à
nouveau l'historique de toutes les branches.

Troisième partie. Affiche le détail du commit de fusion, puis compare le
commit d'il y a deux crans au dernier, et termine par le résumé chiffré de cet
écart.

**Exemple**

```
$ git switch main
Already on 'main'
$ git merge feature/micros
Updating ...
Fast-forward
 micros.txt | 2 ++
 1 file changed, 2 insertions(+)
 create mode 100644 micros.txt
$ git log --oneline --graph
* ... feat(micros): parc de micros
* ... feat(presentation): le studio
$ git merge --no-ff feature/cabine
Merge made by the 'ort' strategy.
 cabine.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 cabine.txt
$ git log --oneline --all
... Merge branch 'feature/cabine'
... feat(cabine): dimensions
... feat(micros): parc de micros
... feat(presentation): le studio
$ git show HEAD --stat
commit ...
Merge: ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 11:13:00 2026 +0100

    Merge branch 'feature/cabine'

 cabine.txt | 1 +
 1 file changed, 1 insertion(+)
$ git diff HEAD~2 HEAD
diff --git a/cabine.txt b/cabine.txt
new file mode 100644
index ...
--- /dev/null
+++ b/cabine.txt
@@ -0,0 +1 @@
+Cabine : 12 m2, traitement acoustique
diff --git a/micros.txt b/micros.txt
new file mode 100644
index ...
--- /dev/null
+++ b/micros.txt
@@ -0,0 +1,2 @@
+Micro statique : 2
+Micro dynamique : 4
$ git diff --stat HEAD~2 HEAD
 cabine.txt | 1 +
 micros.txt | 2 ++
 2 files changed, 3 insertions(+)
```

**Indices**

1. Huit commandes, trois parties, et la bascule se joue sur une seule option.
2. `HEAD~2` depuis un commit de fusion suit le premier parent : c'est la ligne de `main`.
3. Les deux dessins doivent être visiblement différents, c'est tout l'objet de l'exercice.

**Correction officielle**

```bash
git switch main
git merge feature/micros
git log --oneline --graph
git merge --no-ff feature/cabine
git log --oneline --all
git show HEAD --stat
git diff HEAD~2 HEAD
git diff --stat HEAD~2 HEAD
```

### La médiathèque

Identifiant : `ch4-b5-mediatheque`

Dernier exercice du chapitre : tu produis seul un historique précis.

Depuis `main`, crée `feature/numerique` et fais-y deux commits. Reviens sur
`main` et fais-y un commit sur les horaires. Crée ensuite `fix/affichage`
depuis `main` et fais-y un commit.

Intègre `fix/affichage` avec l'option qui exige la linéarité, puis
`feature/numerique` en forçant la trace. Supprime les deux branches.

Vérifie enfin ton travail : liste des branches, historique avec le dessin et
toutes les branches, détail du commit de fusion, et écart entre le commit
d'il y a trois crans et le dernier.

**Exemple**

```
$ git switch -c feature/numerique
Switched to a new branch 'feature/numerique'
$ printf "Postes informatiques : 8\n" > numerique.txt
$ git add numerique.txt
$ git commit -m "feat(numerique): postes informatiques"
[feature/numerique ...] feat(numerique): postes informatiques
 1 file changed, 1 insertion(+)
 create mode 100644 numerique.txt
$ printf "Postes informatiques : 8\nPret de liseuses : 20\n" > numerique.txt
$ git commit -am "feat(numerique): pret de liseuses"
[feature/numerique ...] feat(numerique): pret de liseuses
 1 file changed, 1 insertion(+)
$ git switch main
Switched to branch 'main'
$ printf "Ouvert mardi, jeudi, samedi\n" > horaires.txt
$ git add horaires.txt
$ git commit -m "feat(horaires): jours d'ouverture"
[main ...] feat(horaires): jours d'ouverture
 1 file changed, 1 insertion(+)
 create mode 100644 horaires.txt
$ git switch -c fix/affichage
Switched to a new branch 'fix/affichage'
$ printf "Affichage : panneau a l'entree\n" > affichage.txt
$ git add affichage.txt
$ git commit -m "fix(affichage): panneau d'entree"
[fix/affichage ...] fix(affichage): panneau d'entree
 1 file changed, 1 insertion(+)
 create mode 100644 affichage.txt
$ git switch main
Switched to branch 'main'
$ git merge --ff-only fix/affichage
Updating ...
Fast-forward
 affichage.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 affichage.txt
$ git merge --no-ff feature/numerique
Merge made by the 'ort' strategy.
 numerique.txt | 2 ++
 1 file changed, 2 insertions(+)
 create mode 100644 numerique.txt
$ git branch -d fix/affichage
Deleted branch fix/affichage (was ...).
$ git branch -d feature/numerique
Deleted branch feature/numerique (was ...).
$ git branch
* main
$ git log --oneline --all
... Merge branch 'feature/numerique'
... fix(affichage): panneau d'entree
... feat(horaires): jours d'ouverture
... feat(numerique): pret de liseuses
... feat(numerique): postes informatiques
... feat(presentation): la mediatheque
$ git show HEAD --stat
commit ...
Merge: ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 11:34:00 2026 +0100

    Merge branch 'feature/numerique'

 numerique.txt | 2 ++
 1 file changed, 2 insertions(+)
$ git diff HEAD~3 HEAD
diff --git a/affichage.txt b/affichage.txt
new file mode 100644
index ...
--- /dev/null
+++ b/affichage.txt
@@ -0,0 +1 @@
+Affichage : panneau a l'entree
diff --git a/horaires.txt b/horaires.txt
new file mode 100644
index ...
--- /dev/null
+++ b/horaires.txt
@@ -0,0 +1 @@
+Ouvert mardi, jeudi, samedi
diff --git a/numerique.txt b/numerique.txt
new file mode 100644
index ...
--- /dev/null
+++ b/numerique.txt
@@ -0,0 +1,2 @@
+Postes informatiques : 8
+Pret de liseuses : 20
```

**Indices**

1. Vingt commandes. Les sept premières construisent la situation, les autres l'intègrent et la vérifient.
2. `fix/affichage` part de `main` après le commit des horaires : la fusion linéaire est donc possible.
3. `HEAD~3` depuis le commit de fusion remonte la ligne de `main`, pas celle de la branche.

**Correction officielle**

```bash
git switch -c feature/numerique
printf "Postes informatiques : 8\n" > numerique.txt
git add numerique.txt
git commit -m "feat(numerique): postes informatiques"
printf "Postes informatiques : 8\nPret de liseuses : 20\n" > numerique.txt
git commit -am "feat(numerique): pret de liseuses"
git switch main
printf "Ouvert mardi, jeudi, samedi\n" > horaires.txt
git add horaires.txt
git commit -m "feat(horaires): jours d'ouverture"
git switch -c fix/affichage
printf "Affichage : panneau a l'entree\n" > affichage.txt
git add affichage.txt
git commit -m "fix(affichage): panneau d'entree"
git switch main
git merge --ff-only fix/affichage
git merge --no-ff feature/numerique
git branch -d fix/affichage
git branch -d feature/numerique
git branch
git log --oneline --all
git show HEAD --stat
git diff HEAD~3 HEAD
```

