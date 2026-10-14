#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chapitres 3 (branches, stash) et 4 (fusionner)."""
import os, json

BASE = "exercices"
EX = []


def ajoute(ident, chapitre, niveau, titre, enonce, solution, indices, seed=None):
    EX.append(dict(ident=ident, chapitre=chapitre, niveau=niveau, titre=titre,
                   enonce=enonce, solution=solution, indices=indices, seed=seed))


DEPART = """git init %s
cd %s
"""

# =========================================================== CHAPITRE 3

ajoute("ch3-e1-fanfare", 3, "Echauffement", "La fanfare du village",
"""La fanfare veut tester un nouveau morceau sans toucher au répertoire officiel.

Crée une branche `feature/nouveau-morceau` et bascule dessus en une seule
commande. Vérifie que tu es bien dessus, ajoute le morceau au répertoire et
enregistre. Reviens enfin sur `main` et regarde le fichier : il ne doit plus
contenir le nouveau morceau.""",
"""git switch -c feature/nouveau-morceau
git branch
printf "Marche de la Saint-Jean\\nValse du 14 juillet\\nSamba de la kermesse\\n" > repertoire.txt
git commit -am "feat(repertoire): ajout de la samba"
git switch main
cat repertoire.txt""",
["Une seule commande crée la branche et bascule dessus : cherche l'option de `git switch`.",
 "`git branch` sans argument liste les branches et marque la courante d'une étoile.",
 "Le `cat` final est la preuve que les deux branches sont bien indépendantes."],
seed=DEPART % ("fanfare", "fanfare") + """printf "Marche de la Saint-Jean\\nValse du 14 juillet\\n" > repertoire.txt
git add repertoire.txt
git commit -m "feat(repertoire): repertoire de la saison\"""")

ajoute("ch3-e2-potager", 3, "Echauffement", "Le potager partagé",
"""Le potager partagé a déjà deux branches en cours. Tu arrives et tu dois
d'abord te repérer.

Liste les branches, puis liste-les à nouveau avec, pour chacune, l'empreinte et
le message de son dernier commit. Bascule ensuite sur la branche
`feature/serre` et affiche le contenu du dossier.""",
"""git branch
git branch -v
git switch feature/serre
ls""",
["La liste détaillée s'obtient avec une option d'une seule lettre.",
 "Pour basculer sur une branche qui existe déjà, pas besoin de l'option de création.",
 "Le `ls` final doit montrer un fichier de plus que sur `main`."],
seed=DEPART % ("potager", "potager") + """printf "tomates\\ncourgettes\\n" > parcelles.txt
git add parcelles.txt
git commit -m "feat(parcelles): premieres parcelles"
git switch -c feature/serre
printf "serre 1 : semis\\n" > serre.txt
git add serre.txt
git commit -m "feat(serre): plan de la serre"
git switch main
printf "tomates\\ncourgettes\\nharicots\\n" > parcelles.txt
git commit -am "feat(parcelles): ajout des haricots\"""")

ajoute("ch3-e3-escape-game", 3, "Echauffement", "L'escape game",
"""La branche de travail s'appelle `enigmes`, mais l'équipe utilise une
convention : les nouvelles fonctionnalités commencent par `feature/`.

Bascule sur la branche, renomme-la en `feature/enigmes` sans perdre son
historique, puis vérifie la liste détaillée des branches. L'empreinte du
dernier commit doit être exactement la même qu'avant le renommage.""",
"""git switch enigmes
git branch -v
git branch -m feature/enigmes
git branch -v""",
["L'option de renommage est une seule lettre, celle de « move » en anglais.",
 "Donne-lui simplement le nouveau nom : la branche courante est renommée.",
 "Compare les deux `git branch -v` : seul le nom change, pas l'empreinte."],
seed=DEPART % ("escape", "escape") + """printf "Salle 1 : le coffre\\n" > salles.txt
git add salles.txt
git commit -m "feat(salles): premiere salle"
git switch -c enigmes
printf "Enigme du cadran\\n" > enigmes.txt
git add enigmes.txt
git commit -m "feat(enigmes): enigme du cadran"
git switch main""")

ajoute("ch3-e4-radio", 3, "Echauffement", "La radio associative",
"""Tu es en train de modifier la grille des programmes quand on te demande en
urgence de regarder un détail sur `main`. Ton travail n'est pas fini, il ne
mérite pas un commit.

Mets-le de côté, vérifie que le dossier est propre, bascule sur `main`, reviens
sur ta branche et récupère ton travail. Termine en affichant le fichier pour
prouver que rien n'a été perdu.""",
"""printf "6h Reveil\\n9h Chronique\\n12h Journal\\n" > grille.txt
git stash
git status
git switch main
git switch feature/grille
git stash pop
cat grille.txt""",
["La commande qui met de côté porte le nom anglais d'une cachette.",
 "Après l'avoir utilisée, `git status` doit annoncer un dossier propre.",
 "Pour récupérer, une sous-commande réapplique et retire de la pile."],
seed=DEPART % ("radio", "radio") + """printf "6h Reveil\\n9h Chronique\\n" > grille.txt
git add grille.txt
git commit -m "feat(grille): premiere grille"
git switch -c feature/grille""")

ajoute("ch3-e5-refuge", 3, "Echauffement", "Le refuge de montagne",
"""La branche `fix/tarifs` a été fusionnée la semaine dernière, elle ne sert plus
à rien et encombre la liste.

Liste les branches, supprime `fix/tarifs` avec l'option prudente, celle qui
refuse d'effacer une branche non fusionnée, puis vérifie qu'elle a bien
disparu.""",
"""git branch
git branch -d fix/tarifs
git branch""",
["L'option prudente est une seule lettre, en minuscule.",
 "Sa grande sœur en majuscule force la suppression : on ne l'utilise qu'en dernier recours.",
 "Le message de confirmation rappelle l'empreinte du dernier commit supprimé, au cas où."],
seed=DEPART % ("refuge", "refuge") + """printf "Nuitee : 22 euros\\n" > tarifs.txt
git add tarifs.txt
git commit -m "feat(tarifs): tarifs de base"
git switch -c fix/tarifs
printf "Nuitee : 24 euros\\nRepas : 18 euros\\n" > tarifs.txt
git commit -am "fix(tarifs): mise a jour 2026"
git switch main
git merge fix/tarifs""")

ajoute("ch3-i1-boulangerie", 3, "Intermediaire", "La boulangerie",
"""Deux chantiers démarrent le même jour dans la boulangerie : la carte des pains
spéciaux et la fiche des allergènes. Ils ne doivent pas se mélanger.

Crée une branche par chantier, en partant de `main` à jour à chaque fois, et
fais un commit sur chacune. Reviens sur `main` et affiche la liste détaillée
des branches : les trois doivent pointer sur des commits différents.""",
"""git switch -c feature/pains-speciaux
printf "Pain aux noix\\nPain de seigle\\n" > pains.txt
git add pains.txt
git commit -m "feat(pains): carte des pains speciaux"
git switch main
git switch -c feature/allergenes
printf "Gluten, fruits a coque\\n" > allergenes.txt
git add allergenes.txt
git commit -m "feat(allergenes): premiere fiche"
git switch main
git branch -v""",
["Attention au point de départ : la seconde branche doit partir de `main`, pas de la première.",
 "Il faut donc revenir sur `main` entre les deux créations.",
 "À la fin, les trois lignes de `git branch -v` doivent afficher trois empreintes différentes."],
seed=DEPART % ("boulangerie", "boulangerie") + """printf "Baguette\\nCroissant\\n" > produits.txt
git add produits.txt
git commit -m "feat(produits): produits de base\"""")

ajoute("ch3-i2-theatre", 3, "Intermediaire", "La troupe de théâtre",
"""Tu as commencé à retravailler la distribution, et tu as aussi créé un fichier
de notes personnelles que Git ne suit pas encore. On te demande de basculer sur
`main` tout de suite.

Mets de côté ton travail, **y compris le fichier non suivi**, vérifie que le
dossier est complètement propre, puis récupère tout. Affiche la liste de la
pile avant de récupérer.""",
"""printf "Hamlet : Lea\\nOphelie : Sarah\\n" > distribution.txt
printf "demander un rappel de texte a Lea\\n" > notes-perso.txt
git stash -u
git status
ls
git stash list
git stash pop
ls""",
["Par défaut, la mise de côté ignore les fichiers non suivis. Une option les embarque aussi.",
 "C'est la même lettre que dans « untracked ».",
 "Le `ls` juste après doit montrer un fichier de moins que le `ls` final."],
seed=DEPART % ("theatre", "theatre") + """printf "Hamlet : Tom\\n" > distribution.txt
git add distribution.txt
git commit -m "feat(distribution): premiere distribution\"""")

ajoute("ch3-i3-cinema", 3, "Intermediaire", "Le ciné-club",
"""Tu travailles sur la programmation du ciné-club, tu as modifié le fichier mais
tu n'as rien enregistré. Tu essaies de basculer sur `main`.

Tente la bascule et lis le refus de Git. Mets alors ton travail de côté,
bascule, reviens, et récupère-le. Le refus fait partie de l'exercice : ne
cherche pas à l'éviter.""",
"""printf "Lundi : Les Temps modernes\\nMardi : Le Cuirasse Potemkine\\n" > programme.txt
git switch main
git stash
git switch main
git switch feature/programme
git stash pop
cat programme.txt""",
["Git refuse de basculer quand un fichier suivi et modifié serait écrasé. C'est une protection.",
 "Le message te propose deux solutions : enregistrer, ou mettre de côté.",
 "Ici on choisit la seconde, puisque le travail n'est pas fini."],
seed=DEPART % ("cineclub", "cineclub") + """printf "Lundi : Les Temps modernes\\n" > programme.txt
git add programme.txt
git commit -m "feat(programme): premiere seance"
git switch -c feature/programme
printf "Lundi : Les Temps modernes\\nCycle Chaplin\\n" > programme.txt
git commit -am "feat(programme): cycle Chaplin\"""")

ajoute("ch3-i4-chorale", 3, "Intermediaire", "La chorale",
"""La chorale a trois branches en cours et personne ne sait plus où en est
chacune.

Produis l'état des lieux : la liste détaillée des branches, puis l'historique
compact avec le dessin à gauche et toutes les branches. Bascule ensuite sur
`feature/concert` et affiche à nouveau la liste détaillée, pour montrer que
l'étoile a changé de ligne.""",
"""git branch -v
git log --oneline --all
git switch feature/concert
git branch -v""",
["Trois commandes de lecture, aucune ne modifie quoi que ce soit.",
 "Le dessin à gauche montre les branches qui ont divergé : les barres verticales sont des lignes de temps parallèles.",
 "Compare les deux `git branch -v` : seule la position de l'étoile change."],
seed=DEPART % ("chorale", "chorale") + """printf "Ave Maria\\n" > repertoire.txt
git add repertoire.txt
git commit -m "feat(repertoire): premier chant"
git switch -c feature/concert
printf "Salle des fetes, 20h\\n" > concert.txt
git add concert.txt
git commit -m "feat(concert): lieu et horaire"
git switch main
git switch -c feature/costumes
printf "Tuniques bleues\\n" > costumes.txt
git add costumes.txt
git commit -m "feat(costumes): choix des tuniques"
git switch main
printf "Ave Maria\\nCantique de Jean Racine\\n" > repertoire.txt
git commit -am "feat(repertoire): ajout du cantique\"""")

ajoute("ch3-i5-atelier-velo", 3, "Intermediaire", "L'atelier vélo",
"""L'atelier vélo a une branche `brouillon` qui contient du vrai travail, et une
branche `essai` qui n'a jamais rien donné.

Renomme `brouillon` en `feature/reparations` sans perdre son historique.
Essaie ensuite de supprimer `essai` avec l'option prudente et lis le refus de
Git. Supprime-la pour de bon avec l'option qui force, puisque ce travail est
réellement abandonné. Vérifie la liste à la fin.""",
"""git branch -m brouillon feature/reparations
git branch
git branch -d essai
git branch -D essai
git branch""",
["Le renommage accepte deux noms : l'ancien puis le nouveau, même si tu n'es pas dessus.",
 "L'option prudente refuse parce que le travail de `essai` n'a jamais été fusionné.",
 "L'option qui force est la même lettre, en majuscule. Lis bien le message avant de l'utiliser."],
seed=DEPART % ("velo", "velo") + """printf "Cles plates\\n" > outils.txt
git add outils.txt
git commit -m "feat(outils): inventaire des outils"
git switch -c brouillon
printf "Reparation : changer les patins\\n" > reparations.txt
git add reparations.txt
git commit -m "feat(reparations): premiere fiche"
git switch main
git switch -c essai
printf "idee abandonnee\\n" > essai.txt
git add essai.txt
git commit -m "feat(essai): piste abandonnee"
git switch main""")

ajoute("ch3-b1-librairie", 3, "BOSS", "La librairie de quartier",
"""Journée complète à la librairie. Tu dois mener deux chantiers en parallèle et
gérer une urgence au milieu.

Commence le chantier des rayons sur une branche dédiée, avec un commit. Reviens
sur `main`, commence le chantier du site sur une autre branche, fais un commit,
puis **modifie encore le fichier sans enregistrer**. L'urgence arrive : mets ton
travail en cours de côté, bascule sur `main`, et reviens aussitôt le récupérer.

Termine par la liste détaillée des branches et l'historique compact avec le
dessin et toutes les branches.""",
"""git switch -c feature/rayons
printf "Rayon poche\\nRayon jeunesse\\n" > rayons.txt
git add rayons.txt
git commit -m "feat(rayons): plan des rayons"
git switch main
git switch -c feature/site
printf "Page accueil\\n" > site.txt
git add site.txt
git commit -m "feat(site): page d'accueil"
printf "Page accueil\\nPage contact\\n" > site.txt
git stash
git switch main
git switch feature/site
git stash pop
git branch -v
git log --oneline --all""",
["Treize commandes, et deux retours sur `main` : un entre les chantiers, un pour l'urgence.",
 "La seconde branche doit partir de `main`, donc il faut y revenir avant de la créer.",
 "La mise de côté ne concerne que la modification non enregistrée, pas le commit déjà fait."],
seed=DEPART % ("librairie", "librairie") + """printf "Librairie du quartier\\n" > accueil.txt
git add accueil.txt
git commit -m "feat(accueil): presentation\"""")

ajoute("ch3-b2-musee", 3, "BOSS", "Le musée municipal",
"""Le musée te confie le ménage de ses branches. Il y en a quatre, dans des états
différents, et tu dois les remettre d'équerre.

Fais d'abord l'inventaire : liste détaillée, puis historique compact avec le
dessin et toutes les branches. Renomme ensuite `truc` en `feature/audioguide`,
qui décrit enfin ce qu'elle contient. Supprime `vieux-test` avec l'option
prudente, elle a déjà été fusionnée. Essaie de supprimer `jamais-fini` de la
même façon, constate le refus, et laisse-la en place : ce travail mérite peut
être d'être repris.

Termine par la liste détaillée.""",
"""git branch -v
git log --oneline --all
git branch -m truc feature/audioguide
git branch -d vieux-test
git branch -d jamais-fini
git branch -v""",
["Six commandes, dans l'ordre de l'énoncé.",
 "Une seule des deux suppressions aboutit : l'autre est refusée, et c'est voulu.",
 "Ne force rien : le message de refus est la bonne réponse de l'exercice."],
seed=DEPART % ("musee", "musee") + """printf "Salle antique\\n" > salles.txt
git add salles.txt
git commit -m "feat(salles): salle antique"
git switch -c truc
printf "Audioguide FR\\n" > audioguide.txt
git add audioguide.txt
git commit -m "feat(audioguide): version francaise"
git switch main
git switch -c vieux-test
printf "Salle antique\\nSalle moderne\\n" > salles.txt
git commit -am "feat(salles): salle moderne"
git switch main
git merge vieux-test
git switch -c jamais-fini
printf "projet en suspens\\n" > suspens.txt
git add suspens.txt
git commit -m "feat(suspens): piste non terminee"
git switch main""")

ajoute("ch3-b3-camping", 3, "BOSS", "Le camping des Pins",
"""Au camping, tu jongles entre deux chantiers et tu as en plus des notes
personnelles qui ne doivent jamais partir dans un commit.

Sur la branche `feature/emplacements`, modifie la carte sans enregistrer, et
crée un fichier `notes-perso.txt`. Mets tout de côté, fichier non suivi
compris. Bascule sur `main`, fais-y un commit sur le règlement, puis reviens et
récupère ton travail.

Enregistre alors uniquement la carte, pas les notes. Termine par un `git status`
qui doit encore signaler le fichier non suivi.""",
"""printf "Emplacement 1 : ombrage\\nEmplacement 2 : plein soleil\\n" > carte.txt
printf "penser a racheter des piquets\\n" > notes-perso.txt
git stash -u
git switch main
printf "Silence a partir de 22h\\n" > reglement.txt
git add reglement.txt
git commit -m "feat(reglement): horaires de silence"
git switch feature/emplacements
git stash pop
git add carte.txt
git commit -m "feat(carte): ajout du second emplacement"
git status""",
["L'option qui embarque les fichiers non suivis est indispensable ici, sinon les notes resteraient.",
 "Après la récupération, c'est à toi de choisir ce qui part au panier.",
 "Le `git status` final doit montrer `notes-perso.txt` comme non suivi : c'est la preuve qu'il n'est pas dans l'historique."],
seed=DEPART % ("camping", "camping") + """printf "Emplacement 1 : ombrage\\n" > carte.txt
git add carte.txt
git commit -m "feat(carte): premier emplacement"
git switch -c feature/emplacements""")

ajoute("ch3-b4-brasserie", 3, "BOSS", "La brasserie artisanale",
"""La brasserie veut trois recettes travaillées en parallèle, chacune sur sa
branche, toutes parties de `main`.

Crée les trois branches `feature/blonde`, `feature/ambree` et `feature/brune`,
avec un commit sur chacune, en revenant bien sur `main` entre chaque. Reviens
sur `main` et fais-y un commit sur le fichier commun des étiquettes.

Termine par la liste détaillée des branches et par l'historique compact avec le
dessin et toutes les branches. Le dessin doit montrer quatre lignes de temps
parallèles.""",
"""git switch -c feature/blonde
printf "Blonde : malt pale, houblon Saaz\\n" > blonde.txt
git add blonde.txt
git commit -m "feat(blonde): recette de la blonde"
git switch main
git switch -c feature/ambree
printf "Ambree : malt caramel\\n" > ambree.txt
git add ambree.txt
git commit -m "feat(ambree): recette de l'ambree"
git switch main
git switch -c feature/brune
printf "Brune : malt torrefie\\n" > brune.txt
git add brune.txt
git commit -m "feat(brune): recette de la brune"
git switch main
printf "Etiquettes rondes, papier kraft\\n" > etiquettes.txt
git add etiquettes.txt
git commit -m "feat(etiquettes): choix du support"
git branch -v
git log --oneline --all""",
["Le piège est de créer la deuxième branche depuis la première. Reviens sur `main` à chaque fois.",
 "Seize commandes en tout : trois blocs identiques, puis le commit sur `main`, puis les deux lectures.",
 "Dans le dessin final, les étoiles doivent apparaître sur des colonnes différentes."],
seed=DEPART % ("brasserie", "brasserie") + """printf "Brasserie des Trois Ponts\\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): la brasserie\"""")

ajoute("ch3-b5-ferme", 3, "BOSS", "La ferme pédagogique",
"""Scénario complet à la ferme. Tu vas enchaîner tout ce que tu sais sur les
branches.

Crée `feature/visites` et fais-y deux commits. Reviens sur `main`, crée
`brouillon-ateliers` et fais-y un commit. Renomme cette seconde branche en
`feature/ateliers`. Reviens sur `main` et fais-y un commit.

Bascule sur `feature/visites`, modifie le fichier sans enregistrer, mets de
côté, reviens sur `main`, puis retourne sur `feature/visites` et récupère.
Enregistre cette dernière modification.

Termine par la liste détaillée et l'historique complet de toutes les branches.""",
"""git switch -c feature/visites
printf "Visite 1 : la basse-cour\\n" > visites.txt
git add visites.txt
git commit -m "feat(visites): visite de la basse-cour"
printf "Visite 1 : la basse-cour\\nVisite 2 : la bergerie\\n" > visites.txt
git commit -am "feat(visites): visite de la bergerie"
git switch main
git switch -c brouillon-ateliers
printf "Atelier pain\\n" > ateliers.txt
git add ateliers.txt
git commit -m "feat(ateliers): atelier pain"
git branch -m feature/ateliers
git switch main
printf "Ferme ouverte du mardi au dimanche\\n" > horaires.txt
git add horaires.txt
git commit -m "feat(horaires): jours d'ouverture"
git switch feature/visites
printf "Visite 1 : la basse-cour\\nVisite 2 : la bergerie\\nVisite 3 : le potager\\n" > visites.txt
git stash
git switch main
git switch feature/visites
git stash pop
git commit -am "feat(visites): visite du potager"
git branch -v
git log --oneline --all""",
["Le renommage se fait depuis la branche elle-même : un seul nom suffit alors.",
 "Vingt commandes. Relis l'énoncé paragraphe par paragraphe, chacun est un bloc.",
 "La récupération ramène une modification non enregistrée : il reste donc un commit à faire après."],
seed=DEPART % ("ferme", "ferme") + """printf "Ferme pedagogique du Val\\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): la ferme\"""")

# =========================================================== CHAPITRE 4

ajoute("ch4-e1-gazette", 4, "Echauffement", "La gazette du lycée",
"""La correction d'une coquille a été faite sur la branche `fix/titre`, et `main`
n'a pas bougé depuis.

Bascule sur `main`, fusionne la branche, et lis bien la réponse de Git : il
annonce un fast-forward, c'est à dire qu'il a simplement avancé le pointeur
sans créer de commit de fusion. Termine par l'historique compact avec le
dessin : il doit rester une ligne droite.""",
"""git switch main
git merge fix/titre
git log --oneline --graph""",
["La fusion se lance depuis la branche qui reçoit, jamais depuis celle qui donne.",
 "Lis la première ligne de la réponse : elle contient le mot qui désigne ce type de fusion.",
 "Le dessin final ne doit comporter aucune barre oblique : l'historique est resté linéaire."],
seed=DEPART % ("gazette", "gazette") + """printf "La Gazete du lycee\\nNumero 1\\n" > une.txt
git add une.txt
git commit -m "feat(une): premiere une"
git switch -c fix/titre
printf "La Gazette du lycee\\nNumero 1\\n" > une.txt
git commit -am "fix(une): correction du titre"
git switch main""")

ajoute("ch4-e2-salle-sport", 4, "Echauffement", "La salle de sport",
"""Pendant que le planning était retravaillé sur sa branche, quelqu'un a modifié
les tarifs sur `main`. Les deux lignes de temps ont donc divergé.

Fusionne `feature/planning` dans `main` et lis la réponse : cette fois Git crée
un commit de fusion. Termine par l'historique compact avec le dessin et toutes
les branches.""",
"""git switch main
git merge feature/planning
git log --oneline --all""",
["Même commande qu'au premier exercice, mais la situation de départ est différente.",
 "`main` a avancé depuis la divergence, donc le fast-forward est impossible.",
 "Dans le dessin, repère le commit de fusion : c'est celui qui a deux traits qui le rejoignent."],
seed=DEPART % ("sport", "sport") + """printf "Tarif annuel : 240 euros\\n" > tarifs.txt
git add tarifs.txt
git commit -m "feat(tarifs): tarif annuel"
git switch -c feature/planning
printf "Lundi 18h : cardio\\n" > planning.txt
git add planning.txt
git commit -m "feat(planning): creneau cardio"
git switch main
printf "Tarif annuel : 240 euros\\nTarif etudiant : 150 euros\\n" > tarifs.txt
git commit -am "feat(tarifs): tarif etudiant\"""")

ajoute("ch4-e3-poterie", 4, "Echauffement", "L'atelier poterie",
"""Le travail sur la branche `feature/four` est terminé, et `main` n'a pas bougé.
Un fast-forward serait donc possible, mais l'atelier veut garder une trace
explicite de ce lot de travail.

Force la création d'un commit de fusion avec l'option adaptée, puis affiche
l'historique de toutes les branches.""",
"""git switch main
git merge --no-ff feature/four
git log --oneline --all""",
["L'option demande à Git de ne pas faire de fast-forward, même quand il le pourrait.",
 "Elle s'écrit avec deux tirets et reprend le nom de la stratégie qu'on refuse.",
 "Le dessin montre alors un commit de fusion, alors que sans l'option la ligne serait restée droite."],
seed=DEPART % ("poterie", "poterie") + """printf "Atelier poterie du jeudi\\n" > atelier.txt
git add atelier.txt
git commit -m "feat(atelier): presentation"
git switch -c feature/four
printf "Four : cuisson 1000 degres\\n" > four.txt
git add four.txt
git commit -m "feat(four): fiche du four"
printf "Four : cuisson 1000 degres\\nEmaillage : apres biscuitage\\n" > four.txt
git commit -am "feat(four): procedure d'emaillage"
git switch main""")

ajoute("ch4-e4-marche", 4, "Echauffement", "Le marché de Noël",
"""L'équipe du marché de Noël exige un historique parfaitement linéaire. Toute
fusion qui créerait un commit de fusion doit échouer plutôt que d'être faite.

Essaie de fusionner `feature/chalets` avec l'option qui garantit la linéarité.
Lis le refus. Fusionne ensuite `fix/affiche`, qui elle est bien dans l'axe,
avec la même option. Termine par l'historique avec le dessin.""",
"""git switch main
git merge --ff-only feature/chalets
git merge --ff-only fix/affiche
git log --oneline --all""",
["L'option s'écrit avec deux tirets et contient les deux lettres du fast-forward.",
 "La première fusion échoue parce que `main` a avancé de son côté : c'est voulu.",
 "La seconde réussit, parce que cette branche est partie du commit où `main` se trouve encore."],
seed=DEPART % ("noel", "noel") + """printf "Marche de Noel, place centrale\\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): le marche"
git switch -c feature/chalets
printf "20 chalets en bois\\n" > chalets.txt
git add chalets.txt
git commit -m "feat(chalets): nombre de chalets"
git switch main
printf "Marche de Noel, place centrale\\nDu 1er au 24 decembre\\n" > presentation.txt
git commit -am "feat(presentation): ajout des dates"
git switch -c fix/affiche
printf "Affiche A3, fond rouge\\n" > affiche.txt
git add affiche.txt
git commit -m "fix(affiche): format et couleur"
git switch main""")

ajoute("ch4-e5-jardinerie", 4, "Echauffement", "La jardinerie",
"""La branche `feature/arrosage` est fusionnée et ne sert plus. On fait le ménage
dans la foulée, comme le recommande le cours.

Bascule sur `main`, fusionne la branche, supprime-la avec l'option prudente,
puis affiche la liste des branches et l'historique avec le dessin.""",
"""git switch main
git merge feature/arrosage
git branch -d feature/arrosage
git branch
git log --oneline --graph""",
["L'ordre compte : on ne supprime une branche qu'après l'avoir fusionnée.",
 "L'option prudente de suppression n'accepte que les branches déjà fusionnées, ce qui tombe bien.",
 "Supprimer la branche n'efface pas ses commits : ils sont désormais sur `main`."],
seed=DEPART % ("jardinerie", "jardinerie") + """printf "Jardinerie des Quatre Saisons\\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): la jardinerie"
git switch -c feature/arrosage
printf "Arrosage automatique : 6h et 20h\\n" > arrosage.txt
git add arrosage.txt
git commit -m "feat(arrosage): horaires d'arrosage"
git switch main""")

ajoute("ch4-i1-auto-ecole", 4, "Intermediaire", "L'auto-école",
"""Deux branches attendent d'être intégrées, et elles ne relèvent pas du même
traitement. `fix/horaires` est une correction d'une ligne. `feature/simulateur`
est une vraie fonctionnalité, qui mérite une trace explicite.

Fusionne la correction en laissant Git choisir, puis la fonctionnalité en
forçant le commit de fusion. Termine par l'historique avec le dessin et toutes
les branches, puis supprime les deux branches fusionnées.""",
"""git switch main
git merge fix/horaires
git merge --no-ff feature/simulateur
git log --oneline --all
git branch -d fix/horaires
git branch -d feature/simulateur""",
["La règle du cours : si la fonctionnalité est importante, on préfère garder la trace.",
 "La première fusion se fait sans option, la seconde avec celle qui refuse le fast-forward.",
 "Les suppressions se font après les fusions, sinon l'option prudente refuserait."],
seed=DEPART % ("autoecole", "autoecole") + """printf "Auto-ecole du Centre\\nOuvert 9h-18h\\n" > infos.txt
git add infos.txt
git commit -m "feat(infos): informations generales"
git switch -c fix/horaires
printf "Auto-ecole du Centre\\nOuvert 8h-19h\\n" > infos.txt
git commit -am "fix(infos): correction des horaires"
git switch main
git switch -c feature/simulateur
printf "Simulateur : 2 postes\\n" > simulateur.txt
git add simulateur.txt
git commit -m "feat(simulateur): deux postes"
printf "Simulateur : 2 postes\\nSeances de 45 minutes\\n" > simulateur.txt
git commit -am "feat(simulateur): duree des seances"
git switch main""")

ajoute("ch4-i2-food-truck", 4, "Intermediaire", "Le food truck",
"""Trois branches sont prêtes et doivent rentrer dans `main` l'une après l'autre.
Tu vas voir que la première passe en fast-forward, et que les suivantes ne le
peuvent plus.

Fusionne-les dans l'ordre : `feature/burger`, puis `feature/dessert`, puis
`feature/boissons`. Lis chaque réponse. Termine par l'historique avec le dessin
et toutes les branches.""",
"""git switch main
git merge feature/burger
git merge feature/dessert
git merge feature/boissons
git log --oneline --all""",
["Quatre fusions à la suite, sans aucune option.",
 "La première avance simplement le pointeur, les deux autres créent un commit de fusion.",
 "Demande-toi après chaque fusion si `main` a bougé : c'est ça qui décide."],
seed=DEPART % ("foodtruck", "foodtruck") + """printf "Food truck Chez Lila\\n" > carte.txt
git add carte.txt
git commit -m "feat(carte): ouverture"
git switch -c feature/burger
printf "Burger du jour : 9 euros\\n" > burger.txt
git add burger.txt
git commit -m "feat(burger): burger du jour"
git switch main
git switch -c feature/dessert
printf "Tarte citron : 4 euros\\n" > dessert.txt
git add dessert.txt
git commit -m "feat(dessert): tarte citron"
git switch main
git switch -c feature/boissons
printf "Limonade maison : 3 euros\\n" > boissons.txt
git add boissons.txt
git commit -m "feat(boissons): limonade"
git switch main""")

ajoute("ch4-i3-ressourcerie", 4, "Intermediaire", "La ressourcerie",
"""Avant de fusionner, la ressourcerie veut savoir ce qu'elle intègre.

Bascule sur `main`, compare `main` et `feature/collecte` pour voir l'écart,
puis le même écart sous forme de résumé chiffré. Fusionne ensuite en forçant le
commit de fusion, et affiche le détail de ce commit de fusion.

Termine par l'historique de toutes les branches.""",
"""git switch main
git diff main feature/collecte
git diff --stat main feature/collecte
git merge --no-ff feature/collecte
git show HEAD --stat
git log --oneline --all""",
["Une comparaison accepte deux noms de branches, exactement comme deux commits.",
 "L'ordre compte : la branche de départ en premier, sinon les plus et les moins sont inversés.",
 "Après la fusion, le dernier commit est le commit de fusion : c'est lui que tu affiches."],
seed=DEPART % ("ressourcerie", "ressourcerie") + """printf "Ressourcerie du Pont\\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): la ressourcerie"
git switch -c feature/collecte
printf "Collecte : mardi et samedi\\n" > collecte.txt
git add collecte.txt
git commit -m "feat(collecte): jours de collecte"
git switch main
printf "Ressourcerie du Pont\\nOuverte a tous\\n" > presentation.txt
git commit -am "feat(presentation): precision\"""")

ajoute("ch4-i4-club-echecs", 4, "Intermediaire", "Le club d'échecs",
"""Le club veut comprendre la différence entre les deux stratégies, sur une même
situation de départ.

`main` n'a pas bougé depuis la divergence. Fusionne d'abord `feature/tournoi`
normalement et regarde le dessin. Puis fusionne `feature/cours` en forçant le
commit de fusion, et regarde à nouveau le dessin.

Deux fusions, deux dessins, et la différence doit sauter aux yeux.""",
"""git switch main
git merge feature/tournoi
git log --oneline --all
git merge --no-ff feature/cours
git log --oneline --all""",
["Les deux branches partent du même commit, donc les deux pourraient passer en fast-forward.",
 "C'est l'option de la seconde fusion qui change tout.",
 "Compare les deux dessins : le second fait apparaître une bifurcation qui n'existait pas."],
seed=DEPART % ("echecs", "echecs") + """printf "Club d'echecs de la Tour\\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): le club"
git switch -c feature/tournoi
printf "Tournoi : 12 janvier\\n" > tournoi.txt
git add tournoi.txt
git commit -m "feat(tournoi): date du tournoi"
git switch main
git switch -c feature/cours
printf "Cours debutants : mercredi\\n" > cours.txt
git add cours.txt
git commit -m "feat(cours): cours debutants"
git switch main""")

ajoute("ch4-i5-pepiniere", 4, "Intermediaire", "La pépinière",
"""La pépinière applique une règle stricte : tout ce qui entre dans `main` doit
être tracé par un commit de fusion, et les branches doivent être supprimées
derrière.

Fusionne `feature/semis` et `feature/greffes` en forçant la trace à chaque
fois, supprime les deux branches, puis affiche la liste des branches
restantes et l'historique avec le dessin.""",
"""git switch main
git merge --no-ff feature/semis
git merge --no-ff feature/greffes
git branch -d feature/semis
git branch -d feature/greffes
git branch
git log --oneline --all""",
["Sept commandes, deux fusions et deux suppressions.",
 "L'option qui force la trace s'applique à chaque fusion, il faut la répéter.",
 "À la fin, `git branch` ne doit plus afficher qu'une seule ligne."],
seed=DEPART % ("pepiniere", "pepiniere") + """printf "Pepiniere des Coteaux\\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): la pepiniere"
git switch -c feature/semis
printf "Semis : fevrier sous abri\\n" > semis.txt
git add semis.txt
git commit -m "feat(semis): calendrier des semis"
git switch main
git switch -c feature/greffes
printf "Greffes : mars\\n" > greffes.txt
git add greffes.txt
git commit -m "feat(greffes): calendrier des greffes"
git switch main""")

ajoute("ch4-b1-festival", 4, "BOSS", "Le festival de musique",
"""Veille de bouclage du festival. Quatre branches attendent, et chacune relève
d'un traitement différent.

Place-toi sur `main`. Fusionne `fix/typo`, une correction d'une ligne, sans
option. Fusionne `feature/scene` en forçant la trace, c'est un gros lot.
Essaie de fusionner `feature/buvette` avec l'option qui exige la linéarité,
constate le refus, puis fusionne-la normalement. Laisse `abandonnee` de côté.

Supprime les trois branches fusionnées avec l'option prudente, essaie de
supprimer `abandonnee` de la même façon et constate le second refus. Termine
par la liste des branches et l'historique complet de toutes les branches.""",
"""git switch main
git merge fix/typo
git merge --no-ff feature/scene
git merge --ff-only feature/buvette
git merge feature/buvette
git branch -d fix/typo
git branch -d feature/scene
git branch -d feature/buvette
git branch -d abandonnee
git branch
git log --oneline --all""",
["Onze commandes. Deux d'entre elles doivent échouer, et c'est l'énoncé qui le demande.",
 "Après la première fusion forcée, `main` a avancé : la linéarité devient impossible.",
 "La suppression d'une branche jamais fusionnée est refusée par l'option prudente. On ne force pas."],
seed=DEPART % ("festival", "festival") + """printf "Festival des Rives\\nEdition 2026\\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): le festival"
git switch -c fix/typo
printf "Festival des Rives\\nEdition 2026, 3 jours\\n" > presentation.txt
git commit -am "fix(presentation): precision sur la duree"
git switch main
git switch -c feature/scene
printf "Scene principale : 2000 places\\n" > scene.txt
git add scene.txt
git commit -m "feat(scene): capacite"
printf "Scene principale : 2000 places\\nScene acoustique : 300 places\\n" > scene.txt
git commit -am "feat(scene): seconde scene"
git switch main
git switch -c feature/buvette
printf "Buvette : 4 points de vente\\n" > buvette.txt
git add buvette.txt
git commit -m "feat(buvette): points de vente"
git switch main
git switch -c abandonnee
printf "idee non retenue\\n" > idee.txt
git add idee.txt
git commit -m "feat(idee): piste non retenue"
git switch main""")

ajoute("ch4-b2-coworking", 4, "BOSS", "L'espace de coworking",
"""L'espace de coworking veut comprendre ce qu'il intègre avant de l'intégrer.
Tu vas donc inspecter, puis fusionner, puis vérifier.

Place-toi sur `main`. Affiche l'écart entre `main` et `feature/salles`, puis son
résumé chiffré. Fusionne en forçant la trace. Affiche le commit de fusion avec
son résumé chiffré, puis l'historique compact de toutes les branches.

Recommence le même cycle complet avec `feature/tarifs`, puis supprime les deux
branches.""",
"""git switch main
git diff --stat main feature/salles
git merge --no-ff feature/salles
git show HEAD --stat
git log --oneline --all
git diff --stat main feature/tarifs
git merge --no-ff feature/tarifs
git show HEAD --stat
git branch -d feature/salles
git branch -d feature/tarifs
git log --oneline --all""",
["Onze commandes : deux cycles identiques, puis le ménage et la vue finale.",
 "Le commit de fusion est toujours le dernier : `HEAD` le désigne juste après la fusion.",
 "Les deux fusions forcent la trace, donc l'historique final compte deux bifurcations."],
seed=DEPART % ("coworking", "coworking") + """printf "Espace Le Comptoir\\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): l'espace"
git switch -c feature/salles
printf "Salle Atelier : 12 places\\nSalle Focus : 4 places\\n" > salles.txt
git add salles.txt
git commit -m "feat(salles): deux salles"
git switch main
git switch -c feature/tarifs
printf "Journee : 18 euros\\nMois : 220 euros\\n" > tarifs.txt
git add tarifs.txt
git commit -m "feat(tarifs): grille tarifaire"
git switch main
printf "Espace Le Comptoir\\nOuvert 7j/7\\n" > presentation.txt
git commit -am "feat(presentation): ouverture 7j/7\"""")

ajoute("ch4-b3-epicerie", 4, "BOSS", "L'épicerie coopérative",
"""L'épicerie travaille en parallèle sur trois sujets, et tu dois tout intégrer
en respectant une consigne précise sur chaque.

Crée d'abord `feature/vrac` depuis `main` et fais-y deux commits. Reviens sur
`main` et fais-y un commit sur les horaires. Crée `fix/etiquette` depuis `main`
et fais-y un commit.

Intègre ensuite : `fix/etiquette` sans option, puis `feature/vrac` en forçant
la trace. Supprime les deux branches. Termine par l'historique avec le dessin
et toutes les branches, puis par le détail du dernier commit de fusion.""",
"""git switch -c feature/vrac
printf "Vrac : legumineuses\\n" > vrac.txt
git add vrac.txt
git commit -m "feat(vrac): legumineuses"
printf "Vrac : legumineuses\\nVrac : cereales\\n" > vrac.txt
git commit -am "feat(vrac): cereales"
git switch main
printf "Ouvert du mardi au samedi\\n" > horaires.txt
git add horaires.txt
git commit -m "feat(horaires): jours d'ouverture"
git switch -c fix/etiquette
printf "Etiquettes : prix au kilo\\n" > etiquettes.txt
git add etiquettes.txt
git commit -m "fix(etiquettes): prix au kilo"
git switch main
git merge fix/etiquette
git merge --no-ff feature/vrac
git branch -d fix/etiquette
git branch -d feature/vrac
git log --oneline --all
git show HEAD --stat""",
["Attention au point de départ de `fix/etiquette` : elle part de `main` après le commit des horaires.",
 "La première fusion passe en fast-forward, la seconde ne le peut pas et on force en plus la trace.",
 "Dix-sept commandes. Traite l'énoncé paragraphe par paragraphe."],
seed=DEPART % ("epicerie", "epicerie") + """printf "Epicerie La Commune\\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): l'epicerie\"""")

ajoute("ch4-b4-studio", 4, "BOSS", "Le studio d'enregistrement",
"""Le studio veut deux historiques différents pour comparer, et c'est à toi de
les produire.

Première partie. Fusionne `feature/micros` normalement, puis affiche
l'historique avec le dessin. Note qu'il est resté linéaire.

Deuxième partie. Fusionne `feature/cabine` en forçant la trace, puis affiche à
nouveau l'historique de toutes les branches.

Troisième partie. Affiche le détail du commit de fusion, puis compare le
commit d'il y a deux crans au dernier, et termine par le résumé chiffré de cet
écart.""",
"""git switch main
git merge feature/micros
git log --oneline --graph
git merge --no-ff feature/cabine
git log --oneline --all
git show HEAD --stat
git diff HEAD~2 HEAD
git diff --stat HEAD~2 HEAD""",
["Huit commandes, trois parties, et la bascule se joue sur une seule option.",
 "`HEAD~2` depuis un commit de fusion suit le premier parent : c'est la ligne de `main`.",
 "Les deux dessins doivent être visiblement différents, c'est tout l'objet de l'exercice."],
seed=DEPART % ("studio", "studio") + """printf "Studio Les Ondes\\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): le studio"
git switch -c feature/micros
printf "Micro statique : 2\\nMicro dynamique : 4\\n" > micros.txt
git add micros.txt
git commit -m "feat(micros): parc de micros"
git switch main
git switch -c feature/cabine
printf "Cabine : 12 m2, traitement acoustique\\n" > cabine.txt
git add cabine.txt
git commit -m "feat(cabine): dimensions"
git switch main""")

ajoute("ch4-b5-mediatheque", 4, "BOSS", "La médiathèque",
"""Dernier exercice du chapitre : tu produis seul un historique précis.

Depuis `main`, crée `feature/numerique` et fais-y deux commits. Reviens sur
`main` et fais-y un commit sur les horaires. Crée ensuite `fix/affichage`
depuis `main` et fais-y un commit.

Intègre `fix/affichage` avec l'option qui exige la linéarité, puis
`feature/numerique` en forçant la trace. Supprime les deux branches.

Vérifie enfin ton travail : liste des branches, historique avec le dessin et
toutes les branches, détail du commit de fusion, et écart entre le commit
d'il y a trois crans et le dernier.""",
"""git switch -c feature/numerique
printf "Postes informatiques : 8\\n" > numerique.txt
git add numerique.txt
git commit -m "feat(numerique): postes informatiques"
printf "Postes informatiques : 8\\nPret de liseuses : 20\\n" > numerique.txt
git commit -am "feat(numerique): pret de liseuses"
git switch main
printf "Ouvert mardi, jeudi, samedi\\n" > horaires.txt
git add horaires.txt
git commit -m "feat(horaires): jours d'ouverture"
git switch -c fix/affichage
printf "Affichage : panneau a l'entree\\n" > affichage.txt
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
git diff HEAD~3 HEAD""",
["Vingt commandes. Les sept premières construisent la situation, les autres l'intègrent et la vérifient.",
 "`fix/affichage` part de `main` après le commit des horaires : la fusion linéaire est donc possible.",
 "`HEAD~3` depuis le commit de fusion remonte la ligne de `main`, pas celle de la branche."],
seed=DEPART % ("mediatheque", "mediatheque") + """printf "Mediatheque des Tilleuls\\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): la mediatheque\"""")


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
