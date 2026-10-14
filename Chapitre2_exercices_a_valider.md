# Chapitre 2 - Lire l'historique

15 exercices. Chaque bloc terminal est la sortie d'une execution reelle de la
correction officielle avec Git 2.43, horloge et identite figees. Les hashs sont
masques par `...` et ne sont pas compares.


## Niveau Echauffement

### Le journal de la station météo

Identifiant : `ch2-e1-station-meteo`

La station météo du lycée enregistre ses relevés depuis trois jours, un commit
par jour. Tu reprends le projet et tu veux savoir ce qui s'est passé.

Affiche l'historique complet, celui qui donne pour chaque commit son empreinte,
son auteur, sa date et son message. Affiche ensuite la version compacte, une
ligne par commit.

**Exemple**

```
$ git log
commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 10:03:00 2026 +0100

    feat(releves): releve du mercredi

commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 09:49:00 2026 +0100

    feat(releves): releve du mardi

commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 09:35:00 2026 +0100

    feat(releves): releve du lundi
$ git log --oneline
... feat(releves): releve du mercredi
... feat(releves): releve du mardi
... feat(releves): releve du lundi
```

**Indices**

1. Deux commandes suffisent, la même avec et sans une option.
2. La version longue est celle par défaut, sans aucune option.
3. La version compacte tient sur une ligne par commit : cherche l'option qui porte ce nom en anglais.

**Correction officielle**

```bash
git log
git log --oneline
```

### Le carnet d'adresses du club

Identifiant : `ch2-e2-carnet-adresses`

Le carnet d'adresses du club compte déjà cinq commits. Tu veux t'y retrouver
sans être noyé.

Affiche d'abord l'historique compact en entier. Affiche ensuite les deux
derniers commits seulement. Termine par la vue compacte avec le dessin des
branches à gauche.

**Exemple**

```
$ git log --oneline
... feat(infos): ajout du local
... feat(infos): horaire des reunions
... feat(adresses): ajout d'Amel
... feat(adresses): ajout de Tom
... feat(adresses): ajout de Sarah
$ git log --oneline -n 2
... feat(infos): ajout du local
... feat(infos): horaire des reunions
$ git log --oneline --graph
* ... feat(infos): ajout du local
* ... feat(infos): horaire des reunions
* ... feat(adresses): ajout d'Amel
* ... feat(adresses): ajout de Tom
* ... feat(adresses): ajout de Sarah
```

**Indices**

1. Trois affichages de la même commande, avec des options qui s'ajoutent.
2. Pour limiter le nombre de commits, l'option prend un nombre juste après elle.
3. Le dessin à gauche s'obtient avec une option dont le nom veut dire « graphe ». Ici l'historique est une ligne droite, donc tu verras une colonne d'étoiles.

**Correction officielle**

```bash
git log --oneline
git log --oneline -n 2
git log --oneline --graph
```

### Le script de sauvegarde

Identifiant : `ch2-e3-script-sauvegarde`

Le dépôt contient la procédure de sauvegarde du serveur. Tu viens de corriger
l'heure de passage, qui était fausse.

Regarde ce que tu as changé avant de l'enregistrer. Mets la correction au
panier, puis regarde à nouveau, de deux façons : ce qui n'est pas encore au
panier, puis ce qui y est. Les deux réponses ne diront pas la même chose, et
c'est tout l'intérêt de l'exercice.

**Exemple**

```
$ printf "Sauvegarde du serveur\nPassage a 23h00\nDestination : disque externe\n" > procedure.txt
$ git status
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   procedure.txt

no changes added to commit (use "git add" and/or "git commit -a")
$ git diff
diff --git a/procedure.txt b/procedure.txt
index ... 100644
--- a/procedure.txt
+++ b/procedure.txt
@@ -1,3 +1,3 @@
 Sauvegarde du serveur
-Passage a 02h00
+Passage a 23h00
 Destination : disque externe
$ git add procedure.txt
$ git diff
$ git diff --staged
diff --git a/procedure.txt b/procedure.txt
index ... 100644
--- a/procedure.txt
+++ b/procedure.txt
@@ -1,3 +1,3 @@
 Sauvegarde du serveur
-Passage a 02h00
+Passage a 23h00
 Destination : disque externe
```

**Indices**

1. Trois zones, donc trois comparaisons possibles. Celle par défaut compare le disque au panier.
2. Après le `git add`, la comparaison par défaut n'affiche plus rien : c'est normal, le disque et le panier sont redevenus identiques.
3. Pour voir ce qui est dans le panier, il faut l'option qui veut dire « mis en scène » en anglais.

**Correction officielle**

```bash
printf "Sauvegarde du serveur\nPassage a 23h00\nDestination : disque externe\n" > procedure.txt
git status
git diff
git add procedure.txt
git diff
git diff --staged
```

### La fiche produit

Identifiant : `ch2-e4-fiche-produit`

La fiche d'un produit vient d'être retouchée à deux endroits : le prix a
changé, et une ligne de description a été ajoutée dans un autre fichier.

Mets uniquement le prix au panier. Affiche ensuite les trois comparaisons
possibles, dans cet ordre : ce qui reste hors du panier, ce qui est dans le
panier, puis tout ce qui te sépare du dernier commit.

**Exemple**

```
$ printf "Cafetiere italienne\nPrix : 29 euros\n" > fiche.txt
$ printf "Capacite : 6 tasses\nMatiere : aluminium\n" > description.txt
$ git add fiche.txt
$ git diff
diff --git a/description.txt b/description.txt
index ... 100644
--- a/description.txt
+++ b/description.txt
@@ -1 +1,2 @@
 Capacite : 6 tasses
+Matiere : aluminium
$ git diff --staged
diff --git a/fiche.txt b/fiche.txt
index ... 100644
--- a/fiche.txt
+++ b/fiche.txt
@@ -1,2 +1,2 @@
 Cafetiere italienne
-Prix : 24 euros
+Prix : 29 euros
$ git diff HEAD
diff --git a/description.txt b/description.txt
index ... 100644
--- a/description.txt
+++ b/description.txt
@@ -1 +1,2 @@
 Capacite : 6 tasses
+Matiere : aluminium
diff --git a/fiche.txt b/fiche.txt
index ... 100644
--- a/fiche.txt
+++ b/fiche.txt
@@ -1,2 +1,2 @@
 Cafetiere italienne
-Prix : 24 euros
+Prix : 29 euros
```

**Indices**

1. Les trois comparaisons sont les trois cas vus en cours. Chacune a sa commande.
2. La troisième compare le disque au dernier commit : elle doit donc montrer les deux fichiers d'un coup.
3. Si une des trois n'affiche rien, relis ce qu'elle compare avant de conclure à une erreur.

**Correction officielle**

```bash
printf "Cafetiere italienne\nPrix : 29 euros\n" > fiche.txt
printf "Capacite : 6 tasses\nMatiere : aluminium\n" > description.txt
git add fiche.txt
git diff
git diff --staged
git diff HEAD
```

### Le relevé du compteur

Identifiant : `ch2-e5-releve-compteur`

Le relevé du compteur d'eau de l'immeuble a été corrigé au dernier commit, mais
tu ne sais plus ce qui a bougé exactement.

Affiche le dernier commit en entier : son en-tête et le détail des lignes
ajoutées et supprimées. Affiche ensuite le même commit sous forme de résumé
chiffré, sans le détail ligne par ligne.

**Exemple**

```
$ git show HEAD
commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 09:49:00 2026 +0100

    fix(compteurs): correction du compteur B et ajout du D

diff --git a/compteurs.txt b/compteurs.txt
index ... 100644
--- a/compteurs.txt
+++ b/compteurs.txt
@@ -1,3 +1,4 @@
 Compteur A : 1240
-Compteur B : 980
+Compteur B : 1080
 Compteur C : 1105
+Compteur D : 640
$ git show HEAD --stat
commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 09:49:00 2026 +0100

    fix(compteurs): correction du compteur B et ajout du D

 compteurs.txt | 3 ++-
 1 file changed, 2 insertions(+), 1 deletion(-)
```

**Indices**

1. Une seule commande, avec et sans option. Elle sert à regarder un commit précis.
2. Le commit précis que tu veux voir est le dernier : il porte un nom court en Git.
3. Pour le résumé chiffré, l'option est la même que celle qui donne les statistiques dans `git log`.

**Correction officielle**

```bash
git show HEAD
git show HEAD --stat
```


## Niveau Intermediaire

### Le registre des interventions

Identifiant : `ch2-i1-registre-interventions`

Le registre des interventions du service technique compte quatre commits. On te
demande de remonter dans le temps sans toucher à quoi que ce soit.

Affiche l'historique compact pour te repérer. Montre ensuite le commit qui se
trouve deux crans avant le dernier, puis celui qui se trouve juste avant le
dernier. Les deux se désignent à partir du dernier, sans jamais recopier une
empreinte.

**Exemple**

```
$ git log --oneline
... feat(registre): intervention du 22 janvier
... feat(registre): intervention du 15 janvier
... feat(registre): intervention du 8 janvier
... feat(registre): intervention du 1er janvier
$ git show HEAD~2
commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 09:49:00 2026 +0100

    feat(registre): intervention du 8 janvier

diff --git a/registre.txt b/registre.txt
index ... 100644
--- a/registre.txt
+++ b/registre.txt
@@ -1 +1,2 @@
 01/01 : remplacement du filtre
+08/01 : purge des radiateurs
$ git show HEAD~1
commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 10:03:00 2026 +0100

    feat(registre): intervention du 15 janvier

diff --git a/registre.txt b/registre.txt
index ... 100644
--- a/registre.txt
+++ b/registre.txt
@@ -1,2 +1,3 @@
 01/01 : remplacement du filtre
 08/01 : purge des radiateurs
+15/01 : controle electrique
```

**Indices**

1. Le dernier commit s'appelle HEAD. Les précédents se nomment à partir de lui.
2. Le signe qui recule d'un cran s'écrit avec un petit chiffre collé derrière.
3. Recopier une empreinte marcherait aussi, mais ce n'est pas ce qui est demandé : la notation relative est plus sûre, elle ne dépend pas du dépôt.

**Correction officielle**

```bash
git log --oneline
git show HEAD~2
git show HEAD~1
```

### Le cahier de laboratoire

Identifiant : `ch2-i2-cahier-laboratoire`

Le cahier de laboratoire suit trois expériences dans trois fichiers. Avant la
réunion, on te demande un état des lieux chiffré.

Affiche l'historique avec, sous chaque commit, le résumé des fichiers touchés et
du nombre de lignes modifiées. Affiche ensuite le même historique limité aux
deux derniers commits.

**Exemple**

```
$ git log --stat
commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 10:24:00 2026 +0100

    feat(exp-c): protocole dose forte et mise a jour du temoin

 exp-a.txt | 2 +-
 exp-c.txt | 2 ++
 2 files changed, 3 insertions(+), 1 deletion(-)

commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 09:56:00 2026 +0100

    feat(exp-b): protocole dose faible

 exp-b.txt | 2 ++
 1 file changed, 2 insertions(+)

commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 09:35:00 2026 +0100

    feat(exp-a): protocole temoin

 exp-a.txt | 2 ++
 1 file changed, 2 insertions(+)
$ git log --stat -n 2
commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 10:24:00 2026 +0100

    feat(exp-c): protocole dose forte et mise a jour du temoin

 exp-a.txt | 2 +-
 exp-c.txt | 2 ++
 2 files changed, 3 insertions(+), 1 deletion(-)

commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 09:56:00 2026 +0100

    feat(exp-b): protocole dose faible

 exp-b.txt | 2 ++
 1 file changed, 2 insertions(+)
```

**Indices**

1. L'option cherchée ajoute sous chaque commit un petit tableau des fichiers touchés.
2. Son nom est l'abréviation anglaise de « statistiques ».
3. Pour la seconde commande, ajoute simplement l'option de limitation vue à l'exercice précédent.

**Correction officielle**

```bash
git log --stat
git log --stat -n 2
```

### La check-list avant vol

Identifiant : `ch2-i3-checklist-vol`

L'aéroclub a modifié sa check-list deux fois depuis la version validée en
janvier. Le responsable sécurité veut savoir ce qui a changé entre la version de
janvier et celle d'aujourd'hui, en un seul affichage.

Repère d'abord les commits, puis compare directement le commit d'il y a deux
crans avec le dernier. Termine par le même écart sous forme de résumé chiffré.

**Exemple**

```
$ git log --oneline
... fix(checklist): precision sur les gouvernes
... feat(checklist): ajout du controle carburant
... feat(checklist): version de janvier
$ git diff HEAD~2 HEAD
diff --git a/checklist.txt b/checklist.txt
index ... 100644
--- a/checklist.txt
+++ b/checklist.txt
@@ -1,3 +1,4 @@
 1. Verifier le niveau d'huile
-2. Controler les gouvernes
+2. Controler les gouvernes et les volets
 3. Tester la radio
+4. Verifier le carburant
$ git diff --stat HEAD~2 HEAD
 checklist.txt | 3 ++-
 1 file changed, 2 insertions(+), 1 deletion(-)
```

**Indices**

1. La comparaison accepte deux points de l'historique, séparés par une espace.
2. Le plus ancien se met en premier, sinon les plus et les moins seront inversés.
3. Le résumé chiffré utilise la même option que dans `git log`.

**Correction officielle**

```bash
git log --oneline
git diff HEAD~2 HEAD
git diff --stat HEAD~2 HEAD
```

### La configuration du serveur

Identifiant : `ch2-i4-config-serveur`

Quelqu'un a modifié le fichier de configuration et le service ne démarre plus.
Tu veux relire l'ancienne version sans rien restaurer ni rien casser.

Affiche l'historique compact. Affiche ensuite le contenu du fichier
`config.txt` tel qu'il était au commit précédent, puis son contenu actuel, pour
comparer de visu. Termine en affichant proprement l'écart entre les deux.

**Exemple**

```
$ git log --oneline
... fix(config): passage en debug
... feat(config): configuration initiale
$ git show HEAD~1:config.txt
port = 8080
mode = production
timeout = 30
$ cat config.txt
port = 8080
mode = debug
timeout = 3000
$ git diff HEAD~1 HEAD
diff --git a/config.txt b/config.txt
index ... 100644
--- a/config.txt
+++ b/config.txt
@@ -1,3 +1,3 @@
 port = 8080
-mode = production
-timeout = 30
+mode = debug
+timeout = 3000
```

**Indices**

1. Pour lire un fichier tel qu'il était à un commit, on donne au même outil le commit, puis le chemin du fichier.
2. Les deux se séparent par un caractère de ponctuation, celui des rapports de deux-points.
3. Attention à ne pas confondre : cette commande affiche le fichier, elle ne le remet pas en place.

**Correction officielle**

```bash
git log --oneline
git show HEAD~1:config.txt
cat config.txt
git diff HEAD~1 HEAD
```

### Le planning des salles

Identifiant : `ch2-i5-planning-salles`

Le planning des salles et la liste du matériel vivent dans le même dépôt, et
l'historique mélange les deux sujets.

Affiche l'historique compact complet. Affiche ensuite l'historique compact
limité au seul fichier `planning.txt`, pour ne voir que les commits qui l'ont
touché. Termine par la vue compacte avec le dessin à gauche et toutes les
références.

**Exemple**

```
$ git log --oneline
... feat(materiel): ajout des rallonges
... feat(planning): creneau du mardi
... feat(materiel): inventaire initial
... feat(planning): creneau du lundi
$ git log --oneline -- planning.txt
... feat(planning): creneau du mardi
... feat(planning): creneau du lundi
$ git log --oneline --graph --all
* ... feat(materiel): ajout des rallonges
* ... feat(planning): creneau du mardi
* ... feat(materiel): inventaire initial
* ... feat(planning): creneau du lundi
```

**Indices**

1. Pour ne garder que les commits touchant un fichier, on donne son nom à la fin de la commande.
2. Deux tirets seuls séparent les options du nom de fichier : ils évitent toute ambiguïté si un fichier porte le nom d'une branche.
3. Compare bien les deux premières sorties : il doit manquer des commits dans la seconde.

**Correction officielle**

```bash
git log --oneline
git log --oneline -- planning.txt
git log --oneline --graph --all
```


## Niveau BOSS

### L'enquête sur la panne

Identifiant : `ch2-b1-enquete-panne`

Le site affiche une erreur depuis ce matin. Quatre commits ont été poussés
hier soir, et personne ne sait lequel a cassé quoi.

Mène l'enquête sans rien modifier. Affiche l'historique compact pour avoir la
liste. Affiche ensuite l'historique avec le détail des lignes de chaque commit,
ce qui te montre d'un coup tout ce qui a été touché. Puis isole le commit
suspect, celui d'il y a deux crans, et affiche-le seul.

Termine en comparant l'avant-dernier commit au dernier, pour vérifier que la
correction attendue n'a jamais été faite.

**Exemple**

```
$ git log --oneline
... feat(page): ajout du pied de page
... style(page): nouvelle couleur
... feat(page): ajout du menu
... feat(page): page d'accueil
$ git log -p
commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 10:17:00 2026 +0100

    feat(page): ajout du pied de page

diff --git a/page.txt b/page.txt
index ... 100644
--- a/page.txt
+++ b/page.txt
@@ -1,3 +1,4 @@
 titre = Accueil
 couleur = 
 menu = visible
+pied = visible

commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 10:03:00 2026 +0100

    style(page): nouvelle couleur

diff --git a/page.txt b/page.txt
index ... 100644
--- a/page.txt
+++ b/page.txt
@@ -1,3 +1,3 @@
 titre = Accueil
-couleur = bleu
+couleur = 
 menu = visible

commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 09:49:00 2026 +0100

    feat(page): ajout du menu

diff --git a/page.txt b/page.txt
index ... 100644
--- a/page.txt
+++ b/page.txt
@@ -1,2 +1,3 @@
 titre = Accueil
 couleur = bleu
+menu = visible

commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 09:35:00 2026 +0100

    feat(page): page d'accueil

diff --git a/page.txt b/page.txt
new file mode 100644
index ...
--- /dev/null
+++ b/page.txt
@@ -0,0 +1,2 @@
+titre = Accueil
+couleur = bleu
$ git show HEAD~2
commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 09:49:00 2026 +0100

    feat(page): ajout du menu

diff --git a/page.txt b/page.txt
index ... 100644
--- a/page.txt
+++ b/page.txt
@@ -1,2 +1,3 @@
 titre = Accueil
 couleur = bleu
+menu = visible
$ git diff HEAD~1 HEAD
diff --git a/page.txt b/page.txt
index ... 100644
--- a/page.txt
+++ b/page.txt
@@ -1,3 +1,4 @@
 titre = Accueil
 couleur = 
 menu = visible
+pied = visible
```

**Indices**

1. Quatre commandes, dans l'ordre de l'énoncé, et aucune ne modifie le dépôt.
2. Pour voir le détail des lignes sous chaque commit de l'historique, l'option est la même lettre que « patch ».
3. Le commit d'il y a deux crans se désigne à partir du dernier, pas par son empreinte.

**Correction officielle**

```bash
git log --oneline
git log -p
git show HEAD~2
git diff HEAD~1 HEAD
```

### Le fichier de traduction

Identifiant : `ch2-b2-fichier-traduction`

Le fichier de traduction a été retouché trois fois. La relectrice veut savoir
ce qui a changé entre la toute première version et l'avant-dernière, uniquement
pour ce fichier, et pas pour le reste du dépôt.

Repère les commits. Compare ensuite ces deux versions en limitant la
comparaison au seul fichier `fr.txt`. Affiche aussi le contenu complet du
fichier à la première version, pour la citer dans son rapport.

Termine par le résumé chiffré de l'écart entre ces deux mêmes versions.

**Exemple**

```
$ git log --oneline
... style(fr): precision sur l'aide
... feat(fr): relecture et ajout de l'aide
... feat(en): fichier anglais
... feat(fr): premieres chaines
$ git diff HEAD~3 HEAD~1 -- fr.txt
diff --git a/fr.txt b/fr.txt
index ... 100644
--- a/fr.txt
+++ b/fr.txt
@@ -1,2 +1,3 @@
-accueil = Bienvenue
-quitter = Sortir
+accueil = Bienvenue chez vous
+quitter = Quitter
+aide = Aide
$ git show HEAD~3:fr.txt
accueil = Bienvenue
quitter = Sortir
$ git diff --stat HEAD~3 HEAD~1 -- fr.txt
 fr.txt | 5 +++--
 1 file changed, 3 insertions(+), 2 deletions(-)
```

**Indices**

1. Deux points de l'historique, puis deux tirets, puis le fichier à surveiller.
2. La première version est trois crans avant le dernier commit, l'avant-dernière est un cran avant.
3. Pour afficher un fichier à un commit donné, c'est la commande d'affichage de commit, avec deux-points entre le commit et le chemin.

**Correction officielle**

```bash
git log --oneline
git diff HEAD~3 HEAD~1 -- fr.txt
git show HEAD~3:fr.txt
git diff --stat HEAD~3 HEAD~1 -- fr.txt
```

### L'audit avant livraison

Identifiant : `ch2-b3-audit-depot`

Veille de livraison, et le dépôt est en désordre : un fichier modifié mais pas
au panier, un autre déjà au panier, et un troisième que Git ne suit pas encore.

Produis l'audit dans cet ordre précis. L'état général d'abord. Puis les trois
comparaisons, hors panier, dans le panier, et l'écart total avec le dernier
commit. Enfin, la liste des seuls noms de fichiers qui séparent le disque du
dernier commit, sans le détail des lignes.

Tu ne dois rien enregistrer : à la fin, l'état doit être exactement celui du
début.

**Exemple**

```
$ git status
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   guide.txt
$ printf "Version 2.1\nDate : 5 janvier\n" > version.txt
$ printf "correction du calcul de TVA\n" > notes-internes.txt
$ git add version.txt
$ git status
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   guide.txt
	modified:   version.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	notes-internes.txt
$ git diff
$ git diff --staged
diff --git a/guide.txt b/guide.txt
index ... 100644
--- a/guide.txt
+++ b/guide.txt
@@ -1 +1,2 @@
 Guide d'installation
+Etape 1 : telecharger
diff --git a/version.txt b/version.txt
index ... 100644
--- a/version.txt
+++ b/version.txt
@@ -1,2 +1,2 @@
-Version 2.0
-Date : 1 janvier
+Version 2.1
+Date : 5 janvier
$ git diff HEAD
diff --git a/guide.txt b/guide.txt
index ... 100644
--- a/guide.txt
+++ b/guide.txt
@@ -1 +1,2 @@
 Guide d'installation
+Etape 1 : telecharger
diff --git a/version.txt b/version.txt
index ... 100644
--- a/version.txt
+++ b/version.txt
@@ -1,2 +1,2 @@
-Version 2.0
-Date : 1 janvier
+Version 2.1
+Date : 5 janvier
$ git diff HEAD --name-only
guide.txt
version.txt
```

**Indices**

1. Les trois comparaisons sont celles du cours, dans l'ordre : sans option, puis l'option du panier, puis le dernier commit.
2. La dernière commande demande les noms seuls : l'option contient le mot « name ».
3. Le fichier que Git ne suit pas n'apparaîtra dans aucune comparaison. C'est normal, et c'est une bonne question à se poser.

**Correction officielle**

```bash
git status
printf "Version 2.1\nDate : 5 janvier\n" > version.txt
printf "correction du calcul de TVA\n" > notes-internes.txt
git add version.txt
git status
git diff
git diff --staged
git diff HEAD
git diff HEAD --name-only
```

### Le rapport d'incident

Identifiant : `ch2-b4-rapport-incident`

Un incident a eu lieu et tu dois écrire le rapport. Tout ce dont tu as besoin
est dans l'historique, il suffit d'aller le chercher dans le bon ordre.

Commence par la vue d'ensemble : l'historique compact, avec le dessin à gauche
et toutes les références. Donne ensuite le volume de chaque commit avec le
résumé chiffré sous chacun. Isole le commit de bascule, deux crans avant le
dernier, et montre-le en entier.

Pour finir, cite l'état du fichier `seuils.txt` juste avant l'incident, c'est
à dire au commit qui précède celui de bascule, et montre l'écart entre cet état
et le dernier.

**Exemple**

```
$ git log --oneline --graph --all
* ... feat(seuils): ajout du seuil disque
* ... fix(seuils): seuils remontes en urgence
* ... feat(alertes): canal courriel
* ... feat(seuils): seuils d'alerte initiaux
$ git log --stat
commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 10:24:00 2026 +0100

    feat(seuils): ajout du seuil disque

 seuils.txt | 1 +
 1 file changed, 1 insertion(+)

commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 10:10:00 2026 +0100

    fix(seuils): seuils remontes en urgence

 seuils.txt | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)

commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 09:56:00 2026 +0100

    feat(alertes): canal courriel

 alertes.txt | 1 +
 1 file changed, 1 insertion(+)

commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 09:35:00 2026 +0100

    feat(seuils): seuils d'alerte initiaux

 seuils.txt | 2 ++
 1 file changed, 2 insertions(+)
$ git show HEAD~2
commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 09:56:00 2026 +0100

    feat(alertes): canal courriel

diff --git a/alertes.txt b/alertes.txt
new file mode 100644
index ...
--- /dev/null
+++ b/alertes.txt
@@ -0,0 +1 @@
+Alerte par courriel
$ git show HEAD~3:seuils.txt
cpu = 80
memoire = 75
$ git diff HEAD~3 HEAD -- seuils.txt
diff --git a/seuils.txt b/seuils.txt
index ... 100644
--- a/seuils.txt
+++ b/seuils.txt
@@ -1,2 +1,3 @@
-cpu = 80
-memoire = 75
+cpu = 99
+memoire = 98
+disque = 95
```

**Indices**

1. Cinq commandes, et aucune ne modifie quoi que ce soit : un rapport se lit, il ne se construit pas.
2. Le commit de bascule est deux crans avant le dernier ; celui d'avant est donc trois crans avant.
3. Pour citer un fichier à un commit, pense aux deux-points entre le commit et le chemin.

**Correction officielle**

```bash
git log --oneline --graph --all
git log --stat
git show HEAD~2
git show HEAD~3:seuils.txt
git diff HEAD~3 HEAD -- seuils.txt
```

### La revue de la semaine

Identifiant : `ch2-b5-revue-semaine`

Chaque vendredi, l'équipe fait le point. C'est ton tour de préparer la revue,
et tu dois la faire en partant d'un dépôt dans lequel tu as encore du travail
en cours.

Première partie, l'état de ton travail. Modifie le fichier `avancement.txt`
pour y ajouter la ligne `vendredi : revue de la semaine`. Mets-le au panier,
puis montre successivement ce qui reste hors du panier et ce qui s'y trouve.

Deuxième partie, l'historique. Enregistre ton travail avec un message au bon
format, affiche l'historique compact avec le dessin à gauche, puis l'historique
avec le résumé chiffré limité aux trois derniers commits.

Troisième partie, la comparaison. Montre l'écart entre le commit d'il y a trois
crans et le dernier, puis la liste des seuls noms de fichiers concernés par cet
écart.

**Exemple**

```
$ printf "lundi : mise en route\nmercredi : premiers essais\nvendredi : revue de la semaine\n" > avancement.txt
$ git add avancement.txt
$ git diff
$ git diff --staged
diff --git a/avancement.txt b/avancement.txt
index ... 100644
--- a/avancement.txt
+++ b/avancement.txt
@@ -1,2 +1,3 @@
 lundi : mise en route
 mercredi : premiers essais
+vendredi : revue de la semaine
$ git commit -m "feat(avancement): point du vendredi"
[main ...] feat(avancement): point du vendredi
 1 file changed, 1 insertion(+)
$ git log --oneline --graph
* ... feat(avancement): point du vendredi
* ... feat(avancement): point du mercredi
* ... feat(objectifs): objectif du trimestre
* ... feat(avancement): point du lundi
$ git log --stat -n 3
commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 10:45:00 2026 +0100

    feat(avancement): point du vendredi

 avancement.txt | 1 +
 1 file changed, 1 insertion(+)

commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 10:10:00 2026 +0100

    feat(avancement): point du mercredi

 avancement.txt | 1 +
 1 file changed, 1 insertion(+)

commit ...
Author: Eleve Leonis <eleve@leonis.fr>
Date:   Mon Jan 5 09:56:00 2026 +0100

    feat(objectifs): objectif du trimestre

 objectifs.txt | 1 +
 1 file changed, 1 insertion(+)
$ git diff HEAD~3 HEAD
diff --git a/avancement.txt b/avancement.txt
index ... 100644
--- a/avancement.txt
+++ b/avancement.txt
@@ -1 +1,3 @@
 lundi : mise en route
+mercredi : premiers essais
+vendredi : revue de la semaine
diff --git a/objectifs.txt b/objectifs.txt
new file mode 100644
index ...
--- /dev/null
+++ b/objectifs.txt
@@ -0,0 +1 @@
+Objectif : livrer la version 1
$ git diff HEAD~3 HEAD --name-only
avancement.txt
objectifs.txt
```

**Indices**

1. Neuf commandes en tout, dans l'ordre des trois parties de l'énoncé.
2. Après le `git add`, la comparaison sans option n'affiche rien : c'est le résultat attendu, ne cherche pas d'erreur.
3. Pour la dernière, l'option des noms seuls se place après les deux points de l'historique.

**Correction officielle**

```bash
printf "lundi : mise en route\nmercredi : premiers essais\nvendredi : revue de la semaine\n" > avancement.txt
git add avancement.txt
git diff
git diff --staged
git commit -m "feat(avancement): point du vendredi"
git log --oneline --graph
git log --stat -n 3
git diff HEAD~3 HEAD
git diff HEAD~3 HEAD --name-only
```

