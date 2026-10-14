#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chapitres 5 (reparer sans casser) et 6 (les conflits)."""
import os, json

BASE = "exercices"
EX = []


def ajoute(ident, chapitre, niveau, titre, enonce, solution, indices, seed=None):
    EX.append(dict(ident=ident, chapitre=chapitre, niveau=niveau, titre=titre,
                   enonce=enonce, solution=solution, indices=indices, seed=seed))


D = """git init %s
cd %s
"""

# =========================================================== CHAPITRE 5

ajoute("ch5-e1-imprimerie", 5, "Echauffement", "L'imprimerie",
"""Tu viens d'enregistrer un commit, et tu t'aperçois que le message est
incompréhensible. Rien n'a été publié, tu peux donc le réécrire.

Affiche l'historique compact pour voir le message fautif, corrige-le, puis
affiche à nouveau l'historique. Le nombre de commits ne doit pas changer, seul
le message.""",
"""git log --oneline
git commit --amend -m "feat(tarifs): ajout du tarif des affiches A2"
git log --oneline""",
["L'option cherchée ne crée pas de commit, elle remplace le dernier.",
 "Elle s'écrit avec deux tirets et veut dire « amender » en anglais.",
 "Garde l'option du message : sans elle, Git ouvrirait un éditeur."],
seed=D % ("imprimerie", "imprimerie") + """printf "Affiche A3 : 12 euros\\n" > tarifs.txt
git add tarifs.txt
git commit -m "feat(tarifs): premiers tarifs"
printf "Affiche A3 : 12 euros\\nAffiche A2 : 18 euros\\n" > tarifs.txt
git commit -am "truc\"""")

ajoute("ch5-e2-cave-vin", 5, "Echauffement", "La cave à vin",
"""Le dernier commit a été poussé sur le dépôt partagé, et il contient une erreur.
Comme il est déjà public, il ne faut surtout pas réécrire l'historique : on
annule proprement en ajoutant un commit qui fait l'inverse.

Affiche l'historique compact, annule le dernier commit sans réécriture, puis
affiche l'historique et le contenu du fichier.""",
"""git log --oneline
git revert HEAD --no-edit
git log --oneline
cat cave.txt""",
["La commande qui annule sans réécrire ajoute un commit, elle n'en supprime aucun.",
 "L'option `--no-edit` évite que Git demande un message : il en propose un tout fait.",
 "Après l'annulation, l'historique compte un commit de plus, pas un de moins."],
seed=D % ("cave", "cave") + """printf "Bordeaux 2018 : 24 bouteilles\\n" > cave.txt
git add cave.txt
git commit -m "feat(cave): stock initial"
printf "Bordeaux 2018 : 24 bouteilles\\nBordeaux 2018 : 2400 bouteilles\\n" > cave.txt
git commit -am "feat(cave): erreur de saisie\"""")

ajoute("ch5-e3-escalade", 5, "Echauffement", "La salle d'escalade",
"""Tu as modifié un fichier et tu regrettes : tu veux revenir à la version du
dernier commit, sans toucher au reste.

Affiche le fichier abîmé, remets-le dans l'état du dernier commit avec la
commande prévue pour un seul fichier, affiche-le à nouveau, puis vérifie que le
dossier est propre.""",
"""cat voies.txt
git restore voies.txt
cat voies.txt
git status""",
["La commande agit sur un fichier, pas sur l'historique : elle ne déplace rien.",
 "Elle porte le nom anglais de la restauration.",
 "Attention, ce que tu avais tapé est définitivement perdu : c'est le but, mais il faut le savoir."],
seed=D % ("escalade", "escalade") + """printf "Voie bleue : 5a\\nVoie rouge : 6b\\n" > voies.txt
git add voies.txt
git commit -m "feat(voies): cotations des voies"
printf "n importe quoi\\n" > voies.txt""")

ajoute("ch5-e4-ecole-musique", 5, "Echauffement", "L'école de musique",
"""Tu as mis trois fichiers au panier d'un coup alors que tu voulais n'en enregistrer
qu'un. Tu veux vider le panier sans perdre une seule ligne de ton travail.

Affiche l'état, vide complètement le panier, affiche l'état à nouveau. Les trois
fichiers doivent toujours être là, simplement plus sélectionnés.""",
"""git status
git reset
git status""",
["Sans aucun argument, cette commande remet le panier dans l'état du dernier commit.",
 "Elle ne touche ni à l'historique ni au contenu de tes fichiers.",
 "Git affiche ensuite la liste de ce qui est ressorti du panier."],
seed=D % ("musique", "musique") + """printf "Ecole de musique du Parc\\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): l'ecole"
printf "Piano : salle 1\\n" > salles.txt
printf "Lundi 17h : solfege\\n" > planning.txt
printf "Guitare : 3 professeurs\\n" > professeurs.txt
git add .""")

ajoute("ch5-e5-garage", 5, "Echauffement", "Le garage",
"""Tu as fait un `git reset --hard` un peu vite et tu as perdu ton dernier commit.
Rien n'est perdu : Git garde la trace de tous les déplacements de HEAD.

Affiche l'historique compact pour constater le dégât, affiche le journal des
déplacements de HEAD, puis affiche à nouveau l'historique. Tu n'as rien à
récupérer dans cet exercice, seulement à savoir où regarder.""",
"""git log --oneline
git reflog
git log --oneline""",
["Le journal des déplacements porte un nom qui commence comme « référence ».",
 "Il liste les positions successives de HEAD, la plus récente en premier.",
 "Chaque ligne donne l'empreinte, la position `HEAD@{n}` et ce qui a provoqué le déplacement."],
seed=D % ("garage", "garage") + """printf "Revision : 90 euros\\n" > prestations.txt
git add prestations.txt
git commit -m "feat(prestations): revision"
printf "Revision : 90 euros\\nVidange : 60 euros\\n" > prestations.txt
git commit -am "feat(prestations): vidange"
git reset --hard HEAD~1""")

ajoute("ch5-i1-pharmacie", 5, "Intermediaire", "La pharmacie de garde",
"""Les trois modes de `reset` ne font pas la même chose, et c'est tout l'objet de
cet exercice. Tu vas les comparer sur la même situation.

Recule d'un commit en gardant le panier et les fichiers intacts, et regarde
l'état. Recule à nouveau, cette fois en vidant le panier mais en gardant les
fichiers, et regarde l'état. Vérifie enfin que le contenu du fichier n'a jamais
bougé.""",
"""git log --oneline
git reset --soft HEAD~1
git status
git reset HEAD~1
git status
cat planning.txt""",
["Le premier mode conserve tout sauf la position de HEAD.",
 "Le second, qui est celui par défaut, vide aussi le panier.",
 "Aucun des deux ne touche à tes fichiers : le `cat` final doit montrer la version la plus récente."],
seed=D % ("pharmacie", "pharmacie") + """printf "Garde : nuit du lundi\\n" > planning.txt
git add planning.txt
git commit -m "feat(planning): garde du lundi"
printf "Garde : nuit du lundi\\nGarde : nuit du jeudi\\n" > planning.txt
git commit -am "feat(planning): garde du jeudi"
printf "Garde : nuit du lundi\\nGarde : nuit du jeudi\\nGarde : week-end\\n" > planning.txt
git commit -am "feat(planning): garde du week-end\"""")

ajoute("ch5-i2-hotel", 5, "Intermediaire", "L'hôtel du Lac",
"""Le dernier commit est bon sur le fond mais il lui manque un fichier que tu as
oublié d'ajouter. Comme rien n'est publié, tu peux le compléter.

Affiche l'historique compact. Ajoute le fichier oublié au panier, complète le
dernier commit sans changer son message, puis vérifie : le nombre de commits ne
doit pas avoir changé, mais le commit doit maintenant contenir deux fichiers.""",
"""git log --oneline
git status
git add petit-dejeuner.txt
git commit --amend -m "feat(services): navette et petit dejeuner"
git log --oneline
git show HEAD --stat""",
["Le commit complété reprend tout ce qui est dans le panier au moment où tu l'utilises.",
 "Il faut donc d'abord mettre le fichier oublié au panier.",
 "Le résumé chiffré final doit montrer deux fichiers créés."],
seed=D % ("hotel", "hotel") + """printf "Hotel du Lac\\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): l'hotel"
printf "Navette gare : 8h et 18h\\n" > navette.txt
git add navette.txt
git commit -m "feat(services): navette et petit dejeuner"
printf "Petit dejeuner : 7h-10h\\n" > petit-dejeuner.txt""")

ajoute("ch5-i3-fablab", 5, "Intermediaire", "Le fablab",
"""Deux erreurs se sont glissées dans l'historique, et elles n'appellent pas le
même traitement.

Le commit d'il y a deux crans est déjà public : annule-le proprement, sans
réécriture. Le dernier commit, lui, n'a jamais été publié et son message est
mauvais : réécris-le.

Affiche l'historique compact avant et après, et termine par le contenu du
fichier.""",
"""git log --oneline
git revert HEAD~1 --no-edit
git commit --amend -m "fix(machines): annulation de la ligne du laser"
git log --oneline
cat machines.txt""",
["La règle d'or du cours : si c'est poussé, on annule par un nouveau commit ; si c'est local, on réécrit.",
 "L'annulation crée un commit, que tu réécris ensuite avec l'autre commande.",
 "À la fin, l'historique compte un commit de plus qu'au départ, et non deux."],
seed=D % ("fablab", "fablab") + """printf "Imprimante 3D : 1\\n" > machines.txt
git add machines.txt
git commit -m "feat(machines): imprimante 3D"
printf "Imprimante 3D : 1\\nDecoupe laser : 900 W\\n" > machines.txt
git commit -am "feat(machines): decoupe laser"
printf "Fraiseuse : 1\\n" > fraiseuse.txt
git add fraiseuse.txt
git commit -m "feat(fraiseuse): nouvelle fraiseuse\"""")

ajoute("ch5-i4-savonnerie", 5, "Intermediaire", "La savonnerie",
"""La branche `feature/parfums` contient quatre petits commits brouillons. Tu veux
les faire entrer dans `main` sous la forme d'un seul commit propre.

Place-toi sur `main`, prépare l'intégration groupée, regarde l'état pour
constater que tout est au panier mais que rien n'est encore enregistré, puis
fais le commit unique. Termine par l'historique compact de toutes les branches.""",
"""git switch main
git merge --squash feature/parfums
git status
git commit -m "feat(parfums): gamme complete des parfums"
git log --oneline --all""",
["L'option cherchée prépare le résultat dans le panier sans créer de commit de fusion.",
 "Après elle, c'est à toi de faire le commit, avec le message que tu veux.",
 "L'historique final ne garde aucune trace des quatre brouillons sur `main`."],
seed=D % ("savonnerie", "savonnerie") + """printf "Savonnerie du Moulin\\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): la savonnerie"
git switch -c feature/parfums
printf "Lavande\\n" > parfums.txt
git add parfums.txt
git commit -m "wip parfum 1"
printf "Lavande\\nVerveine\\n" > parfums.txt
git commit -am "wip parfum 2"
printf "Lavande\\nVerveine\\nMiel\\n" > parfums.txt
git commit -am "wip parfum 3"
printf "Lavande\\nVerveine\\nMiel\\nRomarin\\n" > parfums.txt
git commit -am "wip parfum 4"
git switch main""")

ajoute("ch5-i5-scierie", 5, "Intermediaire", "La scierie",
"""Tu as mis un fichier au panier par erreur, et tu en as abîmé un autre dans ton
dossier de travail. Deux problèmes, deux remèdes, et il ne faut pas les
confondre.

Affiche l'état. Retire du panier le fichier qui n'a rien à y faire, sans perdre
son contenu. Remets ensuite dans l'état du dernier commit le fichier que tu as
abîmé. Affiche l'état et les deux fichiers pour vérifier.""",
"""git status
git restore --staged brouillon.txt
git restore stock.txt
git status
cat stock.txt
cat brouillon.txt""",
["Le premier remède agit sur le panier, le second sur le dossier de travail.",
 "C'est la même commande, avec une option qui change tout : elle désigne la zone visée.",
 "Le `cat` final prouve que le premier fichier a gardé son contenu, et que le second est revenu à la version enregistrée."],
seed=D % ("scierie", "scierie") + """printf "Chene : 12 m3\\nHetre : 8 m3\\n" > stock.txt
git add stock.txt
git commit -m "feat(stock): inventaire du bois"
printf "idees en vrac pour la scierie\\n" > brouillon.txt
git add brouillon.txt
printf "tout casse\\n" > stock.txt""")

ajoute("ch5-b1-chocolaterie", 5, "BOSS", "La chocolaterie",
"""Trois réparations à mener dans l'ordre, chacune avec le bon outil.

Le dernier commit n'est pas publié et son message ne respecte pas le format :
réécris-le. Le commit d'il y a deux crans est publié et contient des horaires
faux : annule-le proprement. Un fichier de ton dossier a été abîmé : remets-le
dans l'état du dernier commit.

Affiche l'historique compact au début et à la fin, et termine par le journal des
déplacements de HEAD.""",
"""git log --oneline
git commit --amend -m "feat(recettes): ajout de la ganache"
git revert HEAD~2 --no-edit
git restore conditionnement.txt
git status
git log --oneline
git reflog""",
["Trois outils différents : un pour réécrire, un pour annuler sans réécrire, un pour un fichier.",
 "L'ordre de l'énoncé est le bon : la réécriture d'abord, sinon les crans changeraient de place.",
 "Le journal final doit montrer la trace des deux déplacements que tu viens de provoquer."],
seed=D % ("chocolaterie", "chocolaterie") + """printf "Chocolaterie Les Trois Feves\\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): la chocolaterie"
printf "Praline : 40 pourcent cacao\\n" > recettes.txt
git add recettes.txt
git commit -m "feat(recettes): la praline"
printf "Horaires : 7h-23h\\n" > horaires.txt
git add horaires.txt
git commit -m "feat(horaires): horaires errones"
printf "Boites de 12\\n" > conditionnement.txt
git add conditionnement.txt
git commit -m "feat(conditionnement): boites de 12"
printf "Praline : 40 pourcent cacao\\nGanache : creme et chocolat\\n" > recettes.txt
git commit -am "ganache"
printf "n importe quoi\\n" > conditionnement.txt""")

ajoute("ch5-b2-conserverie", 5, "BOSS", "La conserverie",
"""Tu vas parcourir les trois modes de `reset` sur un même dépôt, et constater
précisément ce que chacun conserve.

Affiche l'historique compact. Recule d'un commit en gardant tout, puis affiche
l'état et le fichier. Reviens au commit le plus récent grâce au journal des
déplacements : repère-le d'abord avec le journal, puis reviens-y.

Recule enfin d'un commit en jetant tout, et constate que cette fois le fichier a
changé. Affiche l'état et le fichier une dernière fois.""",
"""git log --oneline
git reset --soft HEAD~1
git status
cat bocaux.txt
git reflog
git reset --hard HEAD@{1}
git log --oneline
git reset --hard HEAD~1
git status
cat bocaux.txt""",
["Le premier mode garde le panier et les fichiers : seul HEAD recule.",
 "Le journal des déplacements se désigne par `HEAD@{n}`, et on peut l'utiliser comme une référence.",
 "Le dernier mode est le seul destructif : c'est pour ça qu'on ne l'utilise jamais sur du travail publié."],
seed=D % ("conserverie", "conserverie") + """printf "Bocaux 500 ml : 200\\n" > bocaux.txt
git add bocaux.txt
git commit -m "feat(bocaux): stock de 500 ml"
printf "Bocaux 500 ml : 200\\nBocaux 1 l : 120\\n" > bocaux.txt
git commit -am "feat(bocaux): stock de 1 litre\"""")

ajoute("ch5-b3-serre", 5, "BOSS", "La serre municipale",
"""La branche `feature/semis` contient cinq commits de travail en cours, aux
messages inutilisables. L'équipe veut un seul commit propre sur `main`, et elle
veut aussi vérifier ce qu'elle intègre avant de le faire.

Place-toi sur `main`. Compare d'abord `main` à la branche, en résumé chiffré.
Prépare ensuite l'intégration groupée, affiche l'état, puis fais le commit
unique avec un message au bon format.

Vérifie enfin : historique compact de toutes les branches, détail du dernier
commit en résumé chiffré, et liste des branches.""",
"""git switch main
git diff --stat main feature/semis
git merge --squash feature/semis
git status
git commit -m "feat(semis): calendrier complet des semis"
git log --oneline --all
git show HEAD --stat
git branch""",
["La comparaison se fait avant l'intégration, elle ne modifie rien.",
 "L'option d'intégration groupée ne crée pas de commit : elle remplit le panier.",
 "Sur `main`, l'historique ne gagne qu'un seul commit, alors que la branche en comptait cinq."],
seed=D % ("serre", "serre") + """printf "Serre municipale\\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): la serre"
git switch -c feature/semis
printf "Janvier : poireaux\\n" > semis.txt
git add semis.txt
git commit -m "wip 1"
printf "Janvier : poireaux\\nFevrier : tomates\\n" > semis.txt
git commit -am "wip 2"
printf "Janvier : poireaux\\nFevrier : tomates\\nMars : courges\\n" > semis.txt
git commit -am "wip 3"
printf "Janvier : poireaux\\nFevrier : tomates\\nMars : courges\\nAvril : haricots\\n" > semis.txt
git commit -am "wip 4"
printf "Janvier : poireaux\\nFevrier : tomates\\nMars : courges\\nAvril : haricots\\nMai : courgettes\\n" > semis.txt
git commit -am "wip 5"
git switch main""")

ajoute("ch5-b4-atelier-reliure", 5, "BOSS", "L'atelier de reliure",
"""Tu vas provoquer volontairement une perte, puis la réparer. C'est l'exercice de
sauvetage du chapitre.

Affiche l'historique compact. Recule brutalement de deux commits en jetant tout,
et constate la perte dans l'historique et dans le fichier. Ouvre le journal des
déplacements de HEAD, repère la position d'avant la catastrophe, et reviens-y.

Vérifie que l'historique et le fichier sont revenus, puis affiche le journal une
dernière fois : il doit contenir la trace des deux allers-retours.""",
"""git log --oneline
git reset --hard HEAD~2
git log --oneline
cat techniques.txt
git reflog
git reset --hard HEAD@{1}
git log --oneline
cat techniques.txt
git reflog""",
["Le journal des déplacements est la seule chose qui survit à un reset destructif.",
 "`HEAD@{1}` désigne la position précédente de HEAD, celle d'avant le reset.",
 "On peut passer cette notation à `reset` comme n'importe quelle référence."],
seed=D % ("reliure", "reliure") + """printf "Couture a la japonaise\\n" > techniques.txt
git add techniques.txt
git commit -m "feat(techniques): couture japonaise"
printf "Couture a la japonaise\\nDos carre colle\\n" > techniques.txt
git commit -am "feat(techniques): dos carre colle"
printf "Couture a la japonaise\\nDos carre colle\\nReliure copte\\n" > techniques.txt
git commit -am "feat(techniques): reliure copte\"""")

ajoute("ch5-b5-brocante", 5, "BOSS", "La brocante",
"""Dernier exercice du chapitre : un dépôt en désordre, et tous les outils de
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

Termine par l'historique compact et le journal des déplacements.""",
"""git commit --amend -m "feat(stands): ajout du stand des livres"
git log --oneline
git restore tarifs.txt
git restore --staged brouillon.txt
git status
git revert HEAD~2 --no-edit
git show HEAD --stat
git log --oneline
git reflog""",
["Neuf commandes, et quatre outils différents : amend, revert, restore, et restore sur le panier.",
 "Compte les crans après la réécriture, pas avant : elle ne change pas le nombre de commits.",
 "Les deux réparations de la deuxième partie utilisent la même commande, avec et sans l'option du panier."],
seed=D % ("brocante", "brocante") + """printf "Brocante du dimanche\\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): la brocante"
printf "Emplacement : 8 euros\\n" > tarifs.txt
git add tarifs.txt
git commit -m "feat(tarifs): prix de l'emplacement"
printf "Emplacement : 8 euros\\nEmplacement couvert : 800 euros\\n" > tarifs.txt
git commit -am "feat(tarifs): emplacement couvert"
printf "Stand buvette\\n" > stands.txt
git add stands.txt
git commit -m "feat(stands): stand buvette"
printf "Stand buvette\\nStand livres\\n" > stands.txt
git commit -am "stands"
printf "efface par erreur\\n" > tarifs.txt
printf "notes en vrac\\n" > brouillon.txt
git add brouillon.txt""")

# =========================================================== CHAPITRE 6

ajoute("ch6-e1-menu-cantine", 6, "Echauffement", "Le menu de la cantine",
"""Deux personnes ont modifié la même ligne du menu, chacune sur sa branche. La
fusion va échouer, et c'est exactement ce qu'on veut observer.

Lance la fusion, lis le message, puis regarde l'état du dépôt. Affiche enfin le
fichier pour voir les marqueurs que Git a écrits dedans. Tu ne résous rien dans
cet exercice : tu constates.""",
"""git merge feature/mardi
git status
cat menu.txt""",
["La fusion se lance depuis la branche qui reçoit, comme d'habitude.",
 "Git ne choisit jamais à ta place quand deux versions touchent la même ligne.",
 "Les marqueurs encadrent les deux versions : la tienne au-dessus, la leur en dessous."],
seed=D % ("cantine", "cantine") + """printf "Lundi : gratin\\nMardi : a definir\\n" > menu.txt
git add menu.txt
git commit -m "feat(menu): debut de semaine"
git switch -c feature/mardi
printf "Lundi : gratin\\nMardi : poisson pane\\n" > menu.txt
git commit -am "feat(menu): poisson le mardi"
git switch main
printf "Lundi : gratin\\nMardi : lasagnes\\n" > menu.txt
git commit -am "feat(menu): lasagnes le mardi\"""")

ajoute("ch6-e2-fiche-horaires", 6, "Echauffement", "La fiche des horaires",
"""Un conflit est en cours sur le dépôt. Tu dois d'abord savoir quels fichiers sont
concernés avant de toucher à quoi que ce soit.

Affiche l'état, puis la liste des seuls fichiers en conflit, celle qui ne montre
que les noms. Affiche enfin le fichier concerné.""",
"""git status
git diff --name-only --diff-filter=U
cat horaires.txt""",
["La commande de comparaison accepte un filtre sur l'état des fichiers.",
 "La lettre du filtre est l'initiale de « unmerged » en anglais.",
 "Combine-la avec l'option qui ne montre que les noms, sans le détail des lignes."],
seed=D % ("horaires", "horaires") + """printf "Ouverture : 9h\\nFermeture : a definir\\n" > horaires.txt
git add horaires.txt
git commit -m "feat(horaires): ouverture"
git switch -c feature/soir
printf "Ouverture : 9h\\nFermeture : 20h\\n" > horaires.txt
git commit -am "feat(horaires): fermeture a 20h"
git switch main
printf "Ouverture : 9h\\nFermeture : 18h\\n" > horaires.txt
git commit -am "feat(horaires): fermeture a 18h"
git merge feature/soir""")

ajoute("ch6-e3-liste-materiel", 6, "Echauffement", "La liste du matériel",
"""Le conflit est là, et tu as décidé : c'est ta version qui doit l'emporter.

Affiche le fichier en conflit, garde ta version avec la commande prévue, affiche
le fichier à nouveau, puis marque le conflit comme résolu. Termine par l'état du
dépôt.""",
"""cat materiel.txt
git restore --ours -- materiel.txt
cat materiel.txt
git add materiel.txt
git status""",
["Deux options opposées existent : l'une garde ta version, l'autre la leur.",
 "« ours » désigne la branche sur laquelle tu te trouves, celle qui reçoit la fusion.",
 "Choisir ne suffit pas : il faut ensuite marquer le conflit comme résolu, avec la commande habituelle."],
seed=D % ("materiel", "materiel") + """printf "Projecteur\\nSono : a choisir\\n" > materiel.txt
git add materiel.txt
git commit -m "feat(materiel): projecteur"
git switch -c feature/sono
printf "Projecteur\\nSono : modele A\\n" > materiel.txt
git commit -am "feat(materiel): sono modele A"
git switch main
printf "Projecteur\\nSono : modele B\\n" > materiel.txt
git commit -am "feat(materiel): sono modele B"
git merge feature/sono""")

ajoute("ch6-e4-annulation", 6, "Echauffement", "Faire machine arrière",
"""Un conflit est en cours et tu préfères y revenir plus tard, au calme. Tu veux
remettre le dépôt exactement dans l'état d'avant la fusion.

Affiche l'état, annule complètement la fusion, affiche l'état à nouveau et le
contenu du fichier. Tout doit être revenu comme avant.""",
"""git status
git merge --abort
git status
cat tarifs.txt""",
["L'option cherchée s'écrit avec deux tirets et veut dire « abandonner ».",
 "Elle remet le dossier et le panier exactement dans l'état d'avant la fusion.",
 "Après elle, `git status` ne doit plus parler de fichiers en conflit du tout."],
seed=D % ("annulation", "annulation") + """printf "Entree : 5 euros\\n" > tarifs.txt
git add tarifs.txt
git commit -m "feat(tarifs): tarif d'entree"
git switch -c feature/reduction
printf "Entree : 3 euros\\n" > tarifs.txt
git commit -am "feat(tarifs): tarif reduit"
git switch main
printf "Entree : 6 euros\\n" > tarifs.txt
git commit -am "feat(tarifs): hausse du tarif"
git merge feature/reduction""")

ajoute("ch6-e5-resolution-simple", 6, "Echauffement", "Trancher et finir",
"""Un conflit est en cours. Tu vas le résoudre en gardant leur version, puis
terminer la fusion.

Affiche le fichier, garde leur version, marque le conflit comme résolu, termine
la fusion avec un message clair, puis affiche l'historique compact de toutes les
branches.""",
"""cat couleurs.txt
git restore --theirs -- couleurs.txt
git add couleurs.txt
git commit -m "fix(couleurs): resolution du conflit, on garde le vert"
git log --oneline --all""",
["« theirs » désigne la branche que tu es en train de faire entrer.",
 "Après avoir choisi, il faut marquer la résolution avant de pouvoir terminer.",
 "Le commit final est le commit de fusion : il ferme le conflit."],
seed=D % ("couleurs", "couleurs") + """printf "Couleur principale : a definir\\n" > couleurs.txt
git add couleurs.txt
git commit -m "feat(couleurs): charte a definir"
git switch -c feature/charte
printf "Couleur principale : vert\\n" > couleurs.txt
git commit -am "feat(couleurs): le vert"
git switch main
printf "Couleur principale : bleu\\n" > couleurs.txt
git commit -am "feat(couleurs): le bleu"
git merge feature/charte""")

ajoute("ch6-i1-journal-local", 6, "Intermediaire", "Le journal local",
"""Tu vas provoquer le conflit toi-même, le diagnostiquer, puis le résoudre en
gardant ta version.

Lance la fusion et lis le refus. Diagnostique : état du dépôt, liste des seuls
fichiers en conflit, contenu du fichier. Résous en gardant ta version, marque la
résolution, termine la fusion.

Affiche l'historique compact de toutes les branches pour finir.""",
"""git merge feature/edito
git status
git diff --name-only --diff-filter=U
cat une.txt
git restore --ours -- une.txt
git add une.txt
git commit -m "fix(une): resolution du conflit sur le titre"
git log --oneline --all""",
["Le diagnostic vient toujours avant la décision : trois commandes pour voir, une pour trancher.",
 "Le filtre sur l'état des fichiers est celui des fichiers non fusionnés.",
 "Une fois le choix fait, la marque de résolution puis le commit ferment la fusion."],
seed=D % ("journal", "journal") + """printf "Une : a definir\\nPages : 12\\n" > une.txt
git add une.txt
git commit -m "feat(une): maquette"
git switch -c feature/edito
printf "Une : le marche renait\\nPages : 12\\n" > une.txt
git commit -am "feat(une): titre sur le marche"
git switch main
printf "Une : la piscine rouvre\\nPages : 12\\n" > une.txt
git commit -am "feat(une): titre sur la piscine\"""")

ajoute("ch6-i2-recette-famille", 6, "Intermediaire", "La recette de famille",
"""Deux branches ont modifié la même ligne, mais aussi des lignes différentes.
Git va résoudre tout seul ce qu'il peut, et ne te laisser que le vrai conflit.

Lance la fusion, lis le message, affiche le fichier. Observe bien : une partie a
été fusionnée automatiquement, et seule une ligne porte les marqueurs. Résous en
gardant leur version, marque la résolution et termine.

Affiche le fichier une dernière fois.""",
"""git merge feature/cuisson
cat tarte.txt
git restore --theirs -- tarte.txt
git add tarte.txt
git commit -m "fix(tarte): resolution sur le temps de cuisson"
cat tarte.txt""",
["Git ne signale un conflit que là où les deux versions touchent la même zone.",
 "Les lignes modifiées d'un seul côté sont intégrées sans rien te demander.",
 "Regarde bien le fichier avant de trancher : tout n'est pas en conflit."],
seed=D % ("tarte", "tarte") + """printf "Pate brisee\\nPommes\\nCuisson : a definir\\nServir tiede\\n" > tarte.txt
git add tarte.txt
git commit -m "feat(tarte): recette de base"
git switch -c feature/cuisson
printf "Pate brisee\\nPommes\\nCuisson : 35 min a 180 degres\\nServir tiede\\n" > tarte.txt
git commit -am "feat(tarte): cuisson 35 min"
git switch main
printf "Pate brisee\\nPommes golden\\nCuisson : 45 min a 170 degres\\nServir tiede\\n" > tarte.txt
git commit -am "feat(tarte): pommes golden et cuisson 45 min\"""")

ajoute("ch6-i3-reprise-calme", 6, "Intermediaire", "Reprendre au calme",
"""Tu vas abandonner une fusion, puis la refaire proprement.

Lance la fusion et constate le conflit. Annule-la complètement et vérifie que le
dépôt est propre. Relance la même fusion, et cette fois résous-la en gardant ta
version, marque la résolution et termine.

Affiche l'historique compact de toutes les branches.""",
"""git merge feature/adresse
git merge --abort
git status
git merge feature/adresse
git restore --ours -- contact.txt
git add contact.txt
git commit -m "fix(contact): resolution du conflit d'adresse"
git log --oneline --all""",
["L'annulation remet tout en place : tu peux relancer la fusion comme si de rien n'était.",
 "Entre les deux, `git status` doit annoncer un dossier propre.",
 "La seconde fusion échouera exactement de la même façon : c'est normal, le conflit n'a pas disparu."],
seed=D % ("contact", "contact") + """printf "Adresse : a completer\\nTelephone : 01 02 03 04 05\\n" > contact.txt
git add contact.txt
git commit -m "feat(contact): fiche de contact"
git switch -c feature/adresse
printf "Adresse : 4 rue des Lilas\\nTelephone : 01 02 03 04 05\\n" > contact.txt
git commit -am "feat(contact): adresse rue des Lilas"
git switch main
printf "Adresse : 12 place du Marche\\nTelephone : 01 02 03 04 05\\n" > contact.txt
git commit -am "feat(contact): adresse place du Marche\"""")

ajoute("ch6-i4-pull-propre", 6, "Intermediaire", "Un pull plus propre",
"""Le dépôt distant a avancé pendant que tu travaillais, et tes commits locaux ne
sont pas encore publiés. Un `pull` ordinaire créerait un commit de fusion inutile.

Affiche l'état, puis récupère le travail distant en rejouant tes commits
par-dessus, pour garder un historique en ligne droite. Affiche l'historique
compact, puis publie.""",
"""git status
git pull --rebase
git log --oneline
git push
git status""",
["L'option cherchée change la façon dont `pull` intègre : au lieu de fusionner, il rejoue.",
 "Le résultat est un historique sans commit de fusion, donc plus simple à relire.",
 "À n'utiliser que sur des commits qui n'ont pas encore été publiés."],
seed="""git init --bare depot-asso.git
git clone https://github.com/leonis-formation/depot-asso.git amorce
cd amorce
printf "Association du quartier\\n" > accueil.txt
git add accueil.txt
git commit -m "feat(accueil): presentation"
git push origin main
cd ..
git clone https://github.com/leonis-formation/depot-asso.git travail
cd amorce
printf "Reunion le 12 mars\\n" > reunion.txt
git add reunion.txt
git commit -m "feat(reunion): date de la reunion"
git push origin main
cd ..
rm -rf amorce
cd travail
printf "Adhesion : 15 euros\\n" > adhesion.txt
git add adhesion.txt
git commit -m "feat(adhesion): montant de l'adhesion\"""")

ajoute("ch6-i5-kit-complet", 6, "Intermediaire", "Le kit de diagnostic",
"""Un conflit est en cours et on te demande un diagnostic complet avant toute
décision.

Affiche l'état, la liste des seuls fichiers en conflit, le contenu du fichier, et
l'historique compact de toutes les branches pour comprendre d'où viennent les
deux versions.

Résous ensuite en gardant leur version, marque la résolution et termine la
fusion. Affiche l'historique compact pour finir.""",
"""git status
git diff --name-only --diff-filter=U
cat regles.txt
git log --oneline --all
git restore --theirs -- regles.txt
git add regles.txt
git commit -m "fix(regles): resolution, on garde la version du club"
git log --oneline --all""",
["Quatre commandes de diagnostic, puis trois de résolution.",
 "L'historique de toutes les branches montre les deux commits à l'origine du conflit.",
 "Compare les deux historiques compacts, avant et après : un commit de fusion est apparu."],
seed=D % ("regles", "regles") + """printf "Nombre de joueurs : a definir\\nDuree : 90 min\\n" > regles.txt
git add regles.txt
git commit -m "feat(regles): premieres regles"
git switch -c feature/club
printf "Nombre de joueurs : 7\\nDuree : 90 min\\n" > regles.txt
git commit -am "feat(regles): sept joueurs"
git switch main
printf "Nombre de joueurs : 11\\nDuree : 90 min\\n" > regles.txt
git commit -am "feat(regles): onze joueurs"
git merge feature/club""")

ajoute("ch6-b1-site-asso", 6, "BOSS", "Le site de l'association",
"""Scénario complet de conflit, du diagnostic à la publication.

Lance la fusion de `feature/refonte` et constate le conflit. Diagnostique
complètement : état, liste des fichiers en conflit, contenu du fichier,
historique compact de toutes les branches.

Résous en gardant ta version, marque la résolution, et termine la fusion avec un
message qui documente le choix.

Vérifie : état, historique compact de toutes les branches, détail du commit de
fusion en résumé chiffré.""",
"""git merge feature/refonte
git status
git diff --name-only --diff-filter=U
cat accueil.txt
git log --oneline --all
git restore --ours -- accueil.txt
git add accueil.txt
git commit -m "fix(accueil): resolution du conflit, on garde le slogan actuel"
git status
git log --oneline --all
git show HEAD --stat""",
["Onze commandes : une fusion, quatre de diagnostic, trois de résolution, trois de vérification.",
 "Documente ton choix dans le message de commit : dans six mois, personne ne s'en souviendra.",
 "Le détail final doit montrer le commit de fusion, avec ses deux parents."],
seed=D % ("asso", "asso") + """printf "Slogan : ensemble, plus forts\\nContact : contact@asso.fr\\n" > accueil.txt
git add accueil.txt
git commit -m "feat(accueil): page d'accueil"
git switch -c feature/refonte
printf "Slogan : agir ensemble\\nContact : contact@asso.fr\\n" > accueil.txt
git commit -am "feat(accueil): nouveau slogan"
git switch main
printf "Slogan : ensemble, plus forts depuis 1998\\nContact : contact@asso.fr\\n" > accueil.txt
git commit -am "feat(accueil): slogan avec la date\"""")

ajoute("ch6-b2-double-conflit", 6, "BOSS", "Deux fichiers en conflit",
"""Cette fois deux fichiers sont en conflit en même temps, et tu ne vas pas les
traiter de la même façon.

Lance la fusion et diagnostique : état et liste des fichiers en conflit. Affiche
les deux fichiers.

Pour le premier, garde ta version. Pour le second, garde la leur. Marque les deux
résolutions, vérifie l'état, puis termine la fusion.

Affiche les deux fichiers et l'historique compact de toutes les branches.""",
"""git merge feature/saison
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
git log --oneline --all""",
["La liste des fichiers en conflit doit en afficher deux : c'est le point de départ.",
 "Les deux options opposées s'utilisent fichier par fichier, dans la même fusion.",
 "Le `git status` avant le commit doit ne plus signaler aucun fichier non fusionné."],
seed=D % ("saison", "saison") + """printf "Entree : 5 euros\\n" > tarifs.txt
printf "Ouverture : 10h\\n" > horaires.txt
git add .
git commit -m "feat(saison): tarifs et horaires"
git switch -c feature/saison
printf "Entree : 7 euros\\n" > tarifs.txt
printf "Ouverture : 9h\\n" > horaires.txt
git commit -am "feat(saison): nouvelle saison"
git switch main
printf "Entree : 6 euros\\n" > tarifs.txt
printf "Ouverture : 11h\\n" > horaires.txt
git commit -am "feat(saison): ajustement de la saison\"""")

ajoute("ch6-b3-essai-erreur", 6, "BOSS", "Essayer, annuler, recommencer",
"""Tu vas traiter le même conflit de deux façons, pour voir la différence.

Première tentative. Lance la fusion, résous en gardant ta version, marque la
résolution, puis change d'avis : annule complètement la fusion avant de la
terminer. Vérifie que le dépôt est propre.

Seconde tentative. Relance la fusion, résous cette fois en gardant leur version,
marque la résolution et termine.

Affiche le fichier et l'historique compact de toutes les branches.""",
"""git merge feature/affiche
git restore --ours -- affiche.txt
git add affiche.txt
git merge --abort
git status
git merge feature/affiche
git restore --theirs -- affiche.txt
git add affiche.txt
git commit -m "fix(affiche): resolution, on garde leur visuel"
cat affiche.txt
git log --oneline --all""",
["L'annulation fonctionne même après avoir marqué une résolution, tant que le commit n'est pas fait.",
 "C'est précisément ce qui rend la commande sûre : rien n'est définitif avant le commit.",
 "La seconde tentative repart du même conflit, puisque rien n'a été enregistré."],
seed=D % ("affiche", "affiche") + """printf "Visuel : a choisir\\nFormat : A2\\n" > affiche.txt
git add affiche.txt
git commit -m "feat(affiche): cahier des charges"
git switch -c feature/affiche
printf "Visuel : photo noir et blanc\\nFormat : A2\\n" > affiche.txt
git commit -am "feat(affiche): photo noir et blanc"
git switch main
printf "Visuel : illustration coloree\\nFormat : A2\\n" > affiche.txt
git commit -am "feat(affiche): illustration coloree\"""")

ajoute("ch6-b4-depot-partage", 6, "BOSS", "Le dépôt partagé",
"""Le dépôt distant a avancé et tu as des commits locaux. Tu vas comparer les deux
façons d'intégrer.

Affiche l'état et constate que ton envoi serait refusé : essaie de publier. Puis
récupère le travail distant en rejouant tes commits par-dessus, pour garder une
ligne droite.

Affiche l'historique compact, publie, et vérifie l'état. Termine par le détail du
dernier commit en résumé chiffré.""",
"""git status
git push
git pull --rebase
git log --oneline
git push
git status
git show HEAD --stat""",
["Le refus du premier envoi fait partie de l'exercice : lis bien ce que Git te répond.",
 "L'option de rejeu évite le commit de fusion que produirait un `pull` ordinaire.",
 "Après le rejeu, l'historique est en ligne droite : aucun commit n'a deux parents."],
seed="""git init --bare depot-club.git
git clone https://github.com/leonis-formation/depot-club.git amorce
cd amorce
printf "Club de randonnee\\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): le club"
git push origin main
cd ..
git clone https://github.com/leonis-formation/depot-club.git travail
cd amorce
printf "Sortie : dimanche 8h\\n" > sorties.txt
git add sorties.txt
git commit -m "feat(sorties): sortie du dimanche"
git push origin main
cd ..
rm -rf amorce
cd travail
printf "Cotisation : 25 euros\\n" > cotisation.txt
git add cotisation.txt
git commit -m "feat(cotisation): montant annuel\"""")

ajoute("ch6-b5-grand-final", 6, "BOSS", "Le grand final",
"""Dernier exercice de la plateforme. Tu mobilises tout ce que tu sais.

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
branches. Supprime enfin la branche fusionnée.""",
"""git switch -c feature/programme
printf "Samedi : concert\\nDimanche : a definir\\n" > programme.txt
git add programme.txt
git commit -m "feat(programme): concert du samedi"
printf "Samedi : concert\\nDimanche : brocante\\n" > programme.txt
git commit -am "feat(programme): brocante le dimanche"
git switch main
printf "Samedi : a definir\\nDimanche : vide-grenier\\n" > programme.txt
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
git branch -d feature/programme""",
["Vingt commandes, quatre parties. Traite-les une par une, en relisant l'énoncé à chaque fois.",
 "La branche et `main` touchent la même ligne du même fichier : le conflit est garanti.",
 "La suppression de la branche n'est possible qu'après la fusion, sinon l'option prudente refuse."],
seed=D % ("final", "final") + """printf "Fete du village\\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): la fete\"""")


def main():
    os.makedirs(BASE, exist_ok=True)
    for e in EX:
        p = os.path.join(BASE, e["ident"])
        os.makedirs(p, exist_ok=True)
        json.dump({"ident": e["ident"], "chapitre": e["chapitre"],
                   "niveau": e["niveau"], "titre": e["titre"]},
                  open(os.path.join(p, "meta.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        open(os.path.join(p, "enonce.md"), "w", encoding="utf-8").write(
            "# %s\n\n%s\n" % (e["titre"], e["enonce"]))
        open(os.path.join(p, "solution.sh"), "w", encoding="utf-8").write(
            e["solution"] + "\n")
        open(os.path.join(p, "indices.md"), "w", encoding="utf-8").write(
            "\n".join("%d. %s" % (i + 1, t) for i, t in enumerate(e["indices"])) + "\n")
        if e["seed"]:
            open(os.path.join(p, "seed.sh"), "w", encoding="utf-8").write(
                e["seed"] + "\n")
    print("%d exercices crees" % len(EX))


if __name__ == "__main__":
    main()
