#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cree les 15 exercices du chapitre 2 sous exercices/.
Notions autorisees : tout le chapitre 1, plus log, log --oneline, --graph, --all,
-n, --stat, -p, les trois git diff, diff entre commits, show, HEAD~n."""
import os, json

BASE = "exercices"
EX = []


def ajoute(ident, niveau, titre, enonce, solution, indices, seed=None):
    EX.append(dict(ident=ident, niveau=niveau, titre=titre, enonce=enonce,
                   solution=solution, indices=indices, seed=seed))


# ---------------------------------------------------------------- ECHAUFFEMENT

ajoute("ch2-e1-station-meteo", "Echauffement", "Le journal de la station météo",
"""La station météo du lycée enregistre ses relevés depuis trois jours, un commit
par jour. Tu reprends le projet et tu veux savoir ce qui s'est passé.

Affiche l'historique complet, celui qui donne pour chaque commit son empreinte,
son auteur, sa date et son message. Affiche ensuite la version compacte, une
ligne par commit.""",
"""git log
git log --oneline""",
["Deux commandes suffisent, la même avec et sans une option.",
 "La version longue est celle par défaut, sans aucune option.",
 "La version compacte tient sur une ligne par commit : cherche l'option qui porte ce nom en anglais."],
seed="""git init station
cd station
printf "lundi : 8 degres, pluie\\n" > releves.txt
git add releves.txt
git commit -m "feat(releves): releve du lundi"
printf "mardi : 11 degres, nuageux\\n" >> releves.txt
git commit -am "feat(releves): releve du mardi"
printf "mercredi : 14 degres, soleil\\n" >> releves.txt
git commit -am "feat(releves): releve du mercredi\"""")

ajoute("ch2-e2-carnet-adresses", "Echauffement", "Le carnet d'adresses du club",
"""Le carnet d'adresses du club compte déjà cinq commits. Tu veux t'y retrouver
sans être noyé.

Affiche d'abord l'historique compact en entier. Affiche ensuite les deux
derniers commits seulement. Termine par la vue compacte avec le dessin des
branches à gauche.""",
"""git log --oneline
git log --oneline -n 2
git log --oneline --graph""",
["Trois affichages de la même commande, avec des options qui s'ajoutent.",
 "Pour limiter le nombre de commits, l'option prend un nombre juste après elle.",
 "Le dessin à gauche s'obtient avec une option dont le nom veut dire « graphe ». Ici l'historique est une ligne droite, donc tu verras une colonne d'étoiles."],
seed="""git init carnet
cd carnet
printf "Sarah Benali\\n" > adresses.txt
git add adresses.txt
git commit -m "feat(adresses): ajout de Sarah"
printf "Tom Rivet\\n" >> adresses.txt
git commit -am "feat(adresses): ajout de Tom"
printf "Amel Diarra\\n" >> adresses.txt
git commit -am "feat(adresses): ajout d'Amel"
printf "Reunions le mardi a 18h\\n" > infos.txt
git add infos.txt
git commit -m "feat(infos): horaire des reunions"
printf "Local : salle B12\\n" >> infos.txt
git commit -am "feat(infos): ajout du local\"""")

ajoute("ch2-e3-script-sauvegarde", "Echauffement", "Le script de sauvegarde",
"""Le dépôt contient la procédure de sauvegarde du serveur. Tu viens de corriger
l'heure de passage, qui était fausse.

Regarde ce que tu as changé avant de l'enregistrer. Mets la correction au
panier, puis regarde à nouveau, de deux façons : ce qui n'est pas encore au
panier, puis ce qui y est. Les deux réponses ne diront pas la même chose, et
c'est tout l'intérêt de l'exercice.""",
"""printf "Sauvegarde du serveur\\nPassage a 23h00\\nDestination : disque externe\\n" > procedure.txt
git status
git diff
git add procedure.txt
git diff
git diff --staged""",
["Trois zones, donc trois comparaisons possibles. Celle par défaut compare le disque au panier.",
 "Après le `git add`, la comparaison par défaut n'affiche plus rien : c'est normal, le disque et le panier sont redevenus identiques.",
 "Pour voir ce qui est dans le panier, il faut l'option qui veut dire « mis en scène » en anglais."],
seed="""git init serveur
cd serveur
printf "Sauvegarde du serveur\\nPassage a 02h00\\nDestination : disque externe\\n" > procedure.txt
git add procedure.txt
git commit -m "feat(procedure): premiere version\"""")

ajoute("ch2-e4-fiche-produit", "Echauffement", "La fiche produit",
"""La fiche d'un produit vient d'être retouchée à deux endroits : le prix a
changé, et une ligne de description a été ajoutée dans un autre fichier.

Mets uniquement le prix au panier. Affiche ensuite les trois comparaisons
possibles, dans cet ordre : ce qui reste hors du panier, ce qui est dans le
panier, puis tout ce qui te sépare du dernier commit.""",
"""printf "Cafetiere italienne\\nPrix : 29 euros\\n" > fiche.txt
printf "Capacite : 6 tasses\\nMatiere : aluminium\\n" > description.txt
git add fiche.txt
git diff
git diff --staged
git diff HEAD""",
["Les trois comparaisons sont les trois cas vus en cours. Chacune a sa commande.",
 "La troisième compare le disque au dernier commit : elle doit donc montrer les deux fichiers d'un coup.",
 "Si une des trois n'affiche rien, relis ce qu'elle compare avant de conclure à une erreur."],
seed="""git init boutique
cd boutique
printf "Cafetiere italienne\\nPrix : 24 euros\\n" > fiche.txt
printf "Capacite : 6 tasses\\n" > description.txt
git add .
git commit -m "feat(fiche): premiere fiche produit\"""")

ajoute("ch2-e5-releve-compteur", "Echauffement", "Le relevé du compteur",
"""Le relevé du compteur d'eau de l'immeuble a été corrigé au dernier commit, mais
tu ne sais plus ce qui a bougé exactement.

Affiche le dernier commit en entier : son en-tête et le détail des lignes
ajoutées et supprimées. Affiche ensuite le même commit sous forme de résumé
chiffré, sans le détail ligne par ligne.""",
"""git show HEAD
git show HEAD --stat""",
["Une seule commande, avec et sans option. Elle sert à regarder un commit précis.",
 "Le commit précis que tu veux voir est le dernier : il porte un nom court en Git.",
 "Pour le résumé chiffré, l'option est la même que celle qui donne les statistiques dans `git log`."],
seed="""git init immeuble
cd immeuble
printf "Compteur A : 1240\\nCompteur B : 980\\nCompteur C : 1105\\n" > compteurs.txt
git add compteurs.txt
git commit -m "feat(compteurs): releve de janvier"
printf "Compteur A : 1240\\nCompteur B : 1080\\nCompteur C : 1105\\nCompteur D : 640\\n" > compteurs.txt
git commit -am "fix(compteurs): correction du compteur B et ajout du D\"""")

# --------------------------------------------------------------- INTERMEDIAIRE

ajoute("ch2-i1-registre-interventions", "Intermediaire", "Le registre des interventions",
"""Le registre des interventions du service technique compte quatre commits. On te
demande de remonter dans le temps sans toucher à quoi que ce soit.

Affiche l'historique compact pour te repérer. Montre ensuite le commit qui se
trouve deux crans avant le dernier, puis celui qui se trouve juste avant le
dernier. Les deux se désignent à partir du dernier, sans jamais recopier une
empreinte.""",
"""git log --oneline
git show HEAD~2
git show HEAD~1""",
["Le dernier commit s'appelle HEAD. Les précédents se nomment à partir de lui.",
 "Le signe qui recule d'un cran s'écrit avec un petit chiffre collé derrière.",
 "Recopier une empreinte marcherait aussi, mais ce n'est pas ce qui est demandé : la notation relative est plus sûre, elle ne dépend pas du dépôt."],
seed="""git init technique
cd technique
printf "01/01 : remplacement du filtre\\n" > registre.txt
git add registre.txt
git commit -m "feat(registre): intervention du 1er janvier"
printf "08/01 : purge des radiateurs\\n" >> registre.txt
git commit -am "feat(registre): intervention du 8 janvier"
printf "15/01 : controle electrique\\n" >> registre.txt
git commit -am "feat(registre): intervention du 15 janvier"
printf "22/01 : reglage de la chaudiere\\n" >> registre.txt
git commit -am "feat(registre): intervention du 22 janvier\"""")

ajoute("ch2-i2-cahier-laboratoire", "Intermediaire", "Le cahier de laboratoire",
"""Le cahier de laboratoire suit trois expériences dans trois fichiers. Avant la
réunion, on te demande un état des lieux chiffré.

Affiche l'historique avec, sous chaque commit, le résumé des fichiers touchés et
du nombre de lignes modifiées. Affiche ensuite le même historique limité aux
deux derniers commits.""",
"""git log --stat
git log --stat -n 2""",
["L'option cherchée ajoute sous chaque commit un petit tableau des fichiers touchés.",
 "Son nom est l'abréviation anglaise de « statistiques ».",
 "Pour la seconde commande, ajoute simplement l'option de limitation vue à l'exercice précédent."],
seed="""git init laboratoire
cd laboratoire
printf "Experience A : temoin\\nResultat : stable\\n" > exp-a.txt
git add exp-a.txt
git commit -m "feat(exp-a): protocole temoin"
printf "Experience B : dose faible\\nResultat : en cours\\n" > exp-b.txt
git add exp-b.txt
git commit -m "feat(exp-b): protocole dose faible"
printf "Experience A : temoin\\nResultat : stable sur 48h\\n" > exp-a.txt
printf "Experience C : dose forte\\nResultat : en cours\\n" > exp-c.txt
git add .
git commit -m "feat(exp-c): protocole dose forte et mise a jour du temoin\"""")

ajoute("ch2-i3-checklist-vol", "Intermediaire", "La check-list avant vol",
"""L'aéroclub a modifié sa check-list deux fois depuis la version validée en
janvier. Le responsable sécurité veut savoir ce qui a changé entre la version de
janvier et celle d'aujourd'hui, en un seul affichage.

Repère d'abord les commits, puis compare directement le commit d'il y a deux
crans avec le dernier. Termine par le même écart sous forme de résumé chiffré.""",
"""git log --oneline
git diff HEAD~2 HEAD
git diff --stat HEAD~2 HEAD""",
["La comparaison accepte deux points de l'historique, séparés par une espace.",
 "Le plus ancien se met en premier, sinon les plus et les moins seront inversés.",
 "Le résumé chiffré utilise la même option que dans `git log`."],
seed="""git init aeroclub
cd aeroclub
printf "1. Verifier le niveau d'huile\\n2. Controler les gouvernes\\n3. Tester la radio\\n" > checklist.txt
git add checklist.txt
git commit -m "feat(checklist): version de janvier"
printf "1. Verifier le niveau d'huile\\n2. Controler les gouvernes\\n3. Tester la radio\\n4. Verifier le carburant\\n" > checklist.txt
git commit -am "feat(checklist): ajout du controle carburant"
printf "1. Verifier le niveau d'huile\\n2. Controler les gouvernes et les volets\\n3. Tester la radio\\n4. Verifier le carburant\\n" > checklist.txt
git commit -am "fix(checklist): precision sur les gouvernes\"""")

ajoute("ch2-i4-config-serveur", "Intermediaire", "La configuration du serveur",
"""Quelqu'un a modifié le fichier de configuration et le service ne démarre plus.
Tu veux relire l'ancienne version sans rien restaurer ni rien casser.

Affiche l'historique compact. Affiche ensuite le contenu du fichier
`config.txt` tel qu'il était au commit précédent, puis son contenu actuel, pour
comparer de visu. Termine en affichant proprement l'écart entre les deux.""",
"""git log --oneline
git show HEAD~1:config.txt
cat config.txt
git diff HEAD~1 HEAD""",
["Pour lire un fichier tel qu'il était à un commit, on donne au même outil le commit, puis le chemin du fichier.",
 "Les deux se séparent par un caractère de ponctuation, celui des rapports de deux-points.",
 "Attention à ne pas confondre : cette commande affiche le fichier, elle ne le remet pas en place."],
seed="""git init service
cd service
printf "port = 8080\\nmode = production\\ntimeout = 30\\n" > config.txt
git add config.txt
git commit -m "feat(config): configuration initiale"
printf "port = 8080\\nmode = debug\\ntimeout = 3000\\n" > config.txt
git commit -am "fix(config): passage en debug\"""")

ajoute("ch2-i5-planning-salles", "Intermediaire", "Le planning des salles",
"""Le planning des salles et la liste du matériel vivent dans le même dépôt, et
l'historique mélange les deux sujets.

Affiche l'historique compact complet. Affiche ensuite l'historique compact
limité au seul fichier `planning.txt`, pour ne voir que les commits qui l'ont
touché. Termine par la vue compacte avec le dessin à gauche et toutes les
références.""",
"""git log --oneline
git log --oneline -- planning.txt
git log --oneline --graph --all""",
["Pour ne garder que les commits touchant un fichier, on donne son nom à la fin de la commande.",
 "Deux tirets seuls séparent les options du nom de fichier : ils évitent toute ambiguïté si un fichier porte le nom d'une branche.",
 "Compare bien les deux premières sorties : il doit manquer des commits dans la seconde."],
seed="""git init batiment
cd batiment
printf "Lundi 9h : salle A\\n" > planning.txt
git add planning.txt
git commit -m "feat(planning): creneau du lundi"
printf "2 videoprojecteurs\\n" > materiel.txt
git add materiel.txt
git commit -m "feat(materiel): inventaire initial"
printf "Mardi 14h : salle B\\n" >> planning.txt
git commit -am "feat(planning): creneau du mardi"
printf "3 rallonges\\n" >> materiel.txt
git commit -am "feat(materiel): ajout des rallonges\"""")

# ---------------------------------------------------------------------- BOSS

ajoute("ch2-b1-enquete-panne", "BOSS", "L'enquête sur la panne",
"""Le site affiche une erreur depuis ce matin. Quatre commits ont été poussés
hier soir, et personne ne sait lequel a cassé quoi.

Mène l'enquête sans rien modifier. Affiche l'historique compact pour avoir la
liste. Affiche ensuite l'historique avec le détail des lignes de chaque commit,
ce qui te montre d'un coup tout ce qui a été touché. Puis isole le commit
suspect, celui d'il y a deux crans, et affiche-le seul.

Termine en comparant l'avant-dernier commit au dernier, pour vérifier que la
correction attendue n'a jamais été faite.""",
"""git log --oneline
git log -p
git show HEAD~2
git diff HEAD~1 HEAD""",
["Quatre commandes, dans l'ordre de l'énoncé, et aucune ne modifie le dépôt.",
 "Pour voir le détail des lignes sous chaque commit de l'historique, l'option est la même lettre que « patch ».",
 "Le commit d'il y a deux crans se désigne à partir du dernier, pas par son empreinte."],
seed="""git init site
cd site
printf "titre = Accueil\\ncouleur = bleu\\n" > page.txt
git add page.txt
git commit -m "feat(page): page d'accueil"
printf "titre = Accueil\\ncouleur = bleu\\nmenu = visible\\n" > page.txt
git commit -am "feat(page): ajout du menu"
printf "titre = Accueil\\ncouleur = \\nmenu = visible\\n" > page.txt
git commit -am "style(page): nouvelle couleur"
printf "titre = Accueil\\ncouleur = \\nmenu = visible\\npied = visible\\n" > page.txt
git commit -am "feat(page): ajout du pied de page\"""")

ajoute("ch2-b2-fichier-traduction", "BOSS", "Le fichier de traduction",
"""Le fichier de traduction a été retouché trois fois. La relectrice veut savoir
ce qui a changé entre la toute première version et l'avant-dernière, uniquement
pour ce fichier, et pas pour le reste du dépôt.

Repère les commits. Compare ensuite ces deux versions en limitant la
comparaison au seul fichier `fr.txt`. Affiche aussi le contenu complet du
fichier à la première version, pour la citer dans son rapport.

Termine par le résumé chiffré de l'écart entre ces deux mêmes versions.""",
"""git log --oneline
git diff HEAD~3 HEAD~1 -- fr.txt
git show HEAD~3:fr.txt
git diff --stat HEAD~3 HEAD~1 -- fr.txt""",
["Deux points de l'historique, puis deux tirets, puis le fichier à surveiller.",
 "La première version est trois crans avant le dernier commit, l'avant-dernière est un cran avant.",
 "Pour afficher un fichier à un commit donné, c'est la commande d'affichage de commit, avec deux-points entre le commit et le chemin."],
seed="""git init traduction
cd traduction
printf "accueil = Bienvenue\\nquitter = Sortir\\n" > fr.txt
git add fr.txt
git commit -m "feat(fr): premieres chaines"
printf "titre = Mon application\\n" > en.txt
git add en.txt
git commit -m "feat(en): fichier anglais"
printf "accueil = Bienvenue chez vous\\nquitter = Quitter\\naide = Aide\\n" > fr.txt
git commit -am "feat(fr): relecture et ajout de l'aide"
printf "accueil = Bienvenue chez vous\\nquitter = Quitter\\naide = Aide en ligne\\n" > fr.txt
git commit -am "style(fr): precision sur l'aide\"""")

ajoute("ch2-b3-audit-depot", "BOSS", "L'audit avant livraison",
"""Veille de livraison, et le dépôt est en désordre : un fichier modifié mais pas
au panier, un autre déjà au panier, et un troisième que Git ne suit pas encore.

Produis l'audit dans cet ordre précis. L'état général d'abord. Puis les trois
comparaisons, hors panier, dans le panier, et l'écart total avec le dernier
commit. Enfin, la liste des seuls noms de fichiers qui séparent le disque du
dernier commit, sans le détail des lignes.

Tu ne dois rien enregistrer : à la fin, l'état doit être exactement celui du
début.""",
"""git status
printf "Version 2.1\\nDate : 5 janvier\\n" > version.txt
printf "correction du calcul de TVA\\n" > notes-internes.txt
git add version.txt
git status
git diff
git diff --staged
git diff HEAD
git diff HEAD --name-only""",
["Les trois comparaisons sont celles du cours, dans l'ordre : sans option, puis l'option du panier, puis le dernier commit.",
 "La dernière commande demande les noms seuls : l'option contient le mot « name ».",
 "Le fichier que Git ne suit pas n'apparaîtra dans aucune comparaison. C'est normal, et c'est une bonne question à se poser."],
seed="""git init livraison
cd livraison
printf "Version 2.0\\nDate : 1 janvier\\n" > version.txt
printf "Guide d'installation\\n" > guide.txt
git add .
git commit -m "feat(livraison): version 2.0"
printf "Guide d'installation\\nEtape 1 : telecharger\\n" > guide.txt
git add guide.txt""")

ajoute("ch2-b4-rapport-incident", "BOSS", "Le rapport d'incident",
"""Un incident a eu lieu et tu dois écrire le rapport. Tout ce dont tu as besoin
est dans l'historique, il suffit d'aller le chercher dans le bon ordre.

Commence par la vue d'ensemble : l'historique compact, avec le dessin à gauche
et toutes les références. Donne ensuite le volume de chaque commit avec le
résumé chiffré sous chacun. Isole le commit de bascule, deux crans avant le
dernier, et montre-le en entier.

Pour finir, cite l'état du fichier `seuils.txt` juste avant l'incident, c'est
à dire au commit qui précède celui de bascule, et montre l'écart entre cet état
et le dernier.""",
"""git log --oneline --graph --all
git log --stat
git show HEAD~2
git show HEAD~3:seuils.txt
git diff HEAD~3 HEAD -- seuils.txt""",
["Cinq commandes, et aucune ne modifie quoi que ce soit : un rapport se lit, il ne se construit pas.",
 "Le commit de bascule est deux crans avant le dernier ; celui d'avant est donc trois crans avant.",
 "Pour citer un fichier à un commit, pense aux deux-points entre le commit et le chemin."],
seed="""git init supervision
cd supervision
printf "cpu = 80\\nmemoire = 75\\n" > seuils.txt
git add seuils.txt
git commit -m "feat(seuils): seuils d'alerte initiaux"
printf "Alerte par courriel\\n" > alertes.txt
git add alertes.txt
git commit -m "feat(alertes): canal courriel"
printf "cpu = 99\\nmemoire = 98\\n" > seuils.txt
git commit -am "fix(seuils): seuils remontes en urgence"
printf "cpu = 99\\nmemoire = 98\\ndisque = 95\\n" > seuils.txt
git commit -am "feat(seuils): ajout du seuil disque\"""")

ajoute("ch2-b5-revue-semaine", "BOSS", "La revue de la semaine",
"""Chaque vendredi, l'équipe fait le point. C'est ton tour de préparer la revue,
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
écart.""",
"""printf "lundi : mise en route\\nmercredi : premiers essais\\nvendredi : revue de la semaine\\n" > avancement.txt
git add avancement.txt
git diff
git diff --staged
git commit -m "feat(avancement): point du vendredi"
git log --oneline --graph
git log --stat -n 3
git diff HEAD~3 HEAD
git diff HEAD~3 HEAD --name-only""",
["Neuf commandes en tout, dans l'ordre des trois parties de l'énoncé.",
 "Après le `git add`, la comparaison sans option n'affiche rien : c'est le résultat attendu, ne cherche pas d'erreur.",
 "Pour la dernière, l'option des noms seuls se place après les deux points de l'historique."],
seed="""git init equipe
cd equipe
printf "lundi : mise en route\\n" > avancement.txt
git add avancement.txt
git commit -m "feat(avancement): point du lundi"
printf "Objectif : livrer la version 1\\n" > objectifs.txt
git add objectifs.txt
git commit -m "feat(objectifs): objectif du trimestre"
printf "lundi : mise en route\\nmercredi : premiers essais\\n" > avancement.txt
git commit -am "feat(avancement): point du mercredi\"""")


def main():
    os.makedirs(BASE, exist_ok=True)
    for e in EX:
        p = os.path.join(BASE, e["ident"])
        os.makedirs(p, exist_ok=True)
        json.dump({"ident": e["ident"], "chapitre": 2, "niveau": e["niveau"],
                   "titre": e["titre"]},
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
