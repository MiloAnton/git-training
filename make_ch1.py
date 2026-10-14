import os, json, re

_PHRASES = [('A la fin', 'À la fin'), ('Celui-la', 'Celui-là'), ('des maintenant', 'dès maintenant'), ('` a ', '` à '), ('branche a jour', 'branche à jour'), ("c'est a toi", "c'est à toi"), ("d'avoir a te", "d'avoir à te"), ('distant a ce', 'distant à ce'), ('dit a Git', 'dit à Git'), ('enregistre-le a ton', 'enregistre-le à ton'), ('est a la', 'est à la'), ('exactement la que', 'exactement là que'), ('fichier a cô', 'fichier à cô'), ('fichiers a ', 'fichiers à '), ('génère a cô', 'génère à cô'), ("ignores a l'avenir", "ignorés à l'avenir"), ('menu a jour', 'menu à jour'), ('place a la', 'place à la'), ('publie sur', 'publié sur'), ('regarde ou en', 'regarde où en'), ('rien a y', 'rien à y'), ('réflexe a prendre', 'réflexe à prendre'), ("t'oblige a tout", "t'oblige à tout"), ('titre a la', 'titre à la'), ("toucher a l'autre", "toucher à l'autre"), ('éléments a sortir', 'éléments à sortir'), ('être a jour', 'être à jour'), ('a te rattraper', 'à te rattraper'), ("Rien n'est encore envoyé", "Rien n'est encore envoyé"), ('sans etre', 'sans être'), ('enregistre dans', 'enregistré dans'), ('a publie la', 'a publié la'), ('est enregistre et', 'est enregistré et'), ('Numerote', 'Numérote'), ('ne doit jamais etre', 'ne doit jamais être'), ('doit etre', 'doit être'), ('peut etre', 'peut être'), ('tu as deja', 'tu as déjà'), ("n'a rien a y faire", "n'a rien à y faire")]

_DICO = {'Apres': 'Après', 'Cree': 'Crée', 'Ecris': 'Écris', 'Recupere': 'Récupère', 'Scenario': 'Scénario', 'Verifie': 'Vérifie', "L'etoile": "L'étoile", 'apparaitre': 'apparaître', 'apres': 'après', 'bibliotheque': 'bibliothèque', 'caracteres': 'caractères', 'cles': 'clés', 'cote': 'côté', 'cree': 'crée', "d'athletisme": "d'athlétisme", "d'ecrire": "d'écrire", "d'entrainement": "d'entraînement", 'definitives': 'définitives', 'deja': 'déjà', 'demarres': 'démarres', 'depose': 'dépose', 'depot': 'dépôt', 'derniere': 'dernière', 'designe': 'désigne', 'desordre': 'désordre', 'differents': 'différents', 'disparaitre': 'disparaître', 'ecrase': 'écrase', 'ecrire': 'écrire', 'editeur': 'éditeur', 'elements': 'éléments', 'entree': 'entrée', 'entrees': 'entrées', 'envoye': 'envoyé', 'etape': 'étape', 'ete': 'été', 'etre': 'être', 'evite': 'évite', 'evites': 'évites', 'fougere': 'fougère', 'genere': 'génère', 'impose': 'imposé', "l'etape": "l'étape", "l'etat": "l'état", "l'hebergeur": "l'hébergeur", "l'interet": "l'intérêt", 'ludotheque': 'ludothèque', 'materiel': 'matériel', 'meme': 'même', 'partagees': 'partagées', 'piege': 'piège', 'precedent': 'précédent', 'premiere': 'première', 'premieres': 'premières', 'prepares': 'prépares', 'recuperation': 'récupération', 'recupere': 'récupère', 'recuperes': 'récupères', 'reflexe': 'réflexe', 'refuse': 'refusé', 'reglage': 'réglage', 'regle': 'règle', 'reintroduit': 'réintroduit', 'reorganise': 'réorganise', 'repertoire': 'répertoire', 'repond': 'répond', 'retroactif': 'rétroactif', 'revision': 'révision', 'seances': 'séances', 'selectionnes': 'sélectionnes', 'separes': 'séparés', 'soiree': 'soirée', 'supprimees': 'supprimées', 'systeme': 'système', 'trainer': 'traîner', 'traversee': 'traversée', 'verifiant': 'vérifiant', 'verifie': 'vérifie', 'veloute': 'velouté', 'chevre': 'chèvre', 'fractionne': 'fractionné', 'president': 'président', 'cafe': 'café', 'depart': 'départ', 'Etranger': 'Étranger', 'invites': 'invités'}


def _recolle(trouve, remplacement):
    """Garde le retour a la ligne d'origine si la phrase etait coupee."""
    if "\n" in trouve:
        mots = remplacement.split(" ")
        bouts = re.split(r"(\s+)", trouve)
        sep = [b for b in bouts if b.strip() == ""]
        out = mots[0]
        for k in range(1, len(mots)):
            out += (sep[k - 1] if k - 1 < len(sep) else " ") + mots[k]
        return out
    return remplacement


def acc(t):
    """Retablit les accents du texte francais affiche. Jamais applique au shell."""
    def rempl(m):
        mot = m.group(0)
        if mot in _DICO:
            return _DICO[mot]
        bas = mot.lower()
        if bas in _DICO:
            r = _DICO[bas]
            return r[0].upper() + r[1:] if mot[0].isupper() else r
        return mot
    # le contenu entre backticks est du code : on n'y touche jamais
    morceaux = re.split(r"(`[^`]*`)", t)
    for i in range(0, len(morceaux), 2):
        morceaux[i] = re.sub(r"[A-Za-z\u00c0-\u00ff']+", rempl, morceaux[i])
        for a, b in _PHRASES:
            rx = re.compile(r"\s+".join(re.escape(x) for x in a.split(" ")))
            morceaux[i] = rx.sub(lambda m, b=b: _recolle(m.group(0), b), morceaux[i])
    return "".join(morceaux)


BASE = "exercices"

EX = []

def ajoute(ident, niveau, titre, enonce, solution, indices, seed=None):
    EX.append(dict(ident=ident, niveau=niveau, titre=acc(titre), enonce=acc(enonce),
                   solution=solution, indices=[acc(i) for i in indices], seed=seed))

# ---------------------------------------------------------------- ECHAUFFEMENT

ajoute("ch1-e1-carnet-recettes", "Echauffement", "Le carnet de recettes",
"""Tu demarres un carnet de recettes. Cree le depot, ajoute une premiere recette,
puis enregistre-la dans l'historique.

Entre chaque etape, regarde ou en est Git : c'est le reflexe a prendre des
maintenant. Ton message de commit respecte le format `type(scope): description`.""",
"""git init carnet-recettes
cd carnet-recettes
echo "Tarte aux pommes" > recettes.txt
git status
git add recettes.txt
git status
git commit -m "feat(recettes): ajout de la tarte aux pommes"
git status""",
["Trois zones, donc trois moments : tu modifies, tu selectionnes, tu enregistres.",
 "Lis `git status` avant et apres chaque commande. Les deux affichages ne disent pas la meme chose, et c'est tout l'interet.",
 "Six commandes en tout. L'avant-derniere met le fichier au panier, la derniere valide avec `-m`."])

ajoute("ch1-e2-playlist", "Echauffement", "La playlist de la soiree",
"""Tu prepares la playlist de la soiree de promo. Tu as deux fichiers : la liste
des titres, que tu veux partager, et tes notes personnelles, que tu veux garder
pour toi pour l'instant.

Enregistre uniquement la liste des titres. Les notes doivent rester hors de
l'historique, sans etre supprimees pour autant.""",
"""git init playlist
cd playlist
echo "Daft Punk - Around the World" > titres.txt
echo "demander la sono au BDE" > notes.txt
git status
git add titres.txt
git status
git commit -m "feat(titres): ajout du premier morceau"
git status
ls""",
["`git add` prend un nom de fichier. Rien ne t'oblige a tout ajouter d'un coup.",
 "Apres le commit, `git status` doit encore parler de `notes.txt`. C'est normal et c'est le but.",
 "Finis par un `ls` : le fichier est toujours sur le disque, Git ne le suit simplement pas."])

ajoute("ch1-e3-liste-courses", "Echauffement", "La liste de courses",
"""Le depot existe deja et contient une liste de courses avec une ligne.

Ajoute le pain, enregistre-le. Ajoute ensuite le lait et enregistre-le a ton
tour, mais cette fois en une seule commande : pour un fichier que Git suit
deja, tu peux mettre au panier et valider d'un coup.""",
"""echo "- pain" >> courses.txt
git status
git add courses.txt
git commit -m "feat(courses): ajout du pain"
echo "- lait" >> courses.txt
git commit -am "feat(courses): ajout du lait"
git status
cat courses.txt""",
["Deux chevrons ajoutent une ligne, un seul ecrase tout le fichier. Verifie avec `cat` si tu as un doute.",
 "Pour le second ajout, cherche l'option de `git commit` qui fait le `git add` a ta place.",
 "Cette option ne marche que sur les fichiers deja suivis. Un fichier tout neuf serait ignore."],
seed="""git init courses
cd courses
printf -- "- cafe\\n" > courses.txt
git add courses.txt
git commit -m "feat(courses): premiere liste\"""")

ajoute("ch1-e4-journal-bord", "Echauffement", "Le journal de bord",
"""Tu tiens le journal de bord d'une traversee. Tu viens d'ecrire la premiere
entree, mais tu as aussi note le code du coffre dans un fichier a cote.

Par reflexe, tu mets tout au panier d'un coup. Rattrape-toi : retire le fichier
sensible du panier sans perdre son contenu, puis enregistre le reste.""",
"""echo "Jour 1 : départ du port de Brest" > journal.txt
echo "code du coffre : 4471" > prive.txt
git add .
git status
git reset prive.txt
git status
git commit -m "feat(journal): premiere entree de la traversee"
git status
cat prive.txt""",
["`git add .` prend tout le dossier. Pratique, et c'est exactement la que naissent les accidents.",
 "La commande qui retire du panier est au programme du cycle de base. Elle prend un nom de fichier.",
 "Elle ne touche pas au contenu du fichier : le `cat` final doit afficher ton texte intact."],
seed="""git init traversee
cd traversee""")

ajoute("ch1-e5-inventaire-atelier", "Echauffement", "L'inventaire de l'atelier",
"""L'atelier tient son inventaire dans un fichier texte. Le logiciel de saisie
genere a cote un fichier de sauvegarde automatique en `.bak` dont personne n'a
besoin dans l'historique.

Mets en place le reglage qui dit a Git d'ignorer tous les fichiers `.bak`, puis
enregistre l'inventaire et ce reglage.""",
"""git init atelier
cd atelier
echo "perceuse à colonne" > inventaire.txt
echo "sauvegarde automatique" > inventaire.txt.bak
git status
printf "*.bak\\n" > .gitignore
git status
git add .
git commit -m "config(depot): ajout du gitignore et de l'inventaire"
git status""",
["Le fichier de reglage se place a la racine du depot et son nom commence par un point.",
 "Une ligne = un motif. L'etoile remplace n'importe quelle suite de caracteres.",
 "Fais un `git status` avant et apres avoir cree le fichier : un nom doit disparaitre de la liste, un autre apparaitre."])

# --------------------------------------------------------------- INTERMEDIAIRE

ajoute("ch1-i1-budget-coloc", "Intermediaire", "Le budget de la coloc",
"""Tu ranges les comptes de la colocation. Deux sujets differents arrivent en
meme temps : les charges fixes d'un cote, les courses partagees de l'autre.

Enregistre-les en deux commits distincts, un par sujet, pour qu'on puisse
annuler l'un sans toucher a l'autre. Les deux fichiers existent avant ton
premier commit : c'est a toi de choisir ce qui part dans quel commit.""",
"""printf "loyer : 820\\ninternet : 30\\n" > charges.txt
printf "courses du 3 janvier : 54\\n" > courses-communes.txt
git status
git add charges.txt
git status
git commit -m "feat(charges): ajout des charges fixes"
git add courses-communes.txt
git commit -m "feat(courses): ajout des courses du 3 janvier"
git status""",
["Un commit = un sujet. Deux sujets, donc deux passages par le panier.",
 "Tu peux parfaitement laisser un fichier non suivi pendant que tu valides l'autre.",
 "Entre les deux commits, `git status` doit encore signaler le second fichier comme non suivi."],
seed="""git init coloc
cd coloc""")

ajoute("ch1-i2-fiches-revision", "Intermediaire", "Les fiches de revision",
"""Ton dossier de fiches de revision est en desordre : des fiches definitives,
un dossier de brouillons, des fichiers temporaires, et un fichier systeme que
ton ordinateur depose partout.

Ecris le reglage qui ignore les fichiers temporaires, le dossier de brouillons
et le fichier systeme, mais qui garde quand meme `rappel.tmp`, dont tu as
besoin. Enregistre ensuite ce qui reste.""",
"""printf "*.tmp\\nbrouillons/\\n.DS_Store\\n!rappel.tmp\\n" > .gitignore
git status
git add .
git commit -m "config(depot): reglage du gitignore et ajout des fiches"
git status
cat .gitignore""",
["Quatre lignes suffisent, une par motif. L'ordre compte : l'exception se place apres la regle qu'elle annule.",
 "Un nom suivi d'une barre oblique designe un dossier entier.",
 "Le point d'exclamation reintroduit un fichier qu'un motif precedent avait exclu."],
seed="""git init revisions
cd revisions
printf "chapitre 1\\n" > fiche-git.txt
printf "chapitre 2\\n" > fiche-reseau.txt
printf "note rapide\\n" > rappel.tmp
printf "au propre plus tard\\n" > essai.tmp
mkdir brouillons
printf "illisible\\n" > brouillons/jet1.txt
printf "0\\n" > .DS_Store""")

ajoute("ch1-i3-catalogue-plantes", "Intermediaire", "Le catalogue de plantes",
"""La serre partage son catalogue sur un depot distant. Recupere-le sur ta
machine, ajoute la fougere au catalogue et enregistre ton travail en local.

Rien n'est encore envoye au depot distant a ce stade : tu travailles sur ta
copie.""",
"""git clone https://github.com/leonis-formation/depot-serre.git catalogue
cd catalogue
ls
cat catalogue.txt
echo "fougère" >> catalogue.txt
git status
git add catalogue.txt
git commit -m "feat(catalogue): ajout de la fougere"
git status""",
["Une seule commande recupere les fichiers, l'historique et l'adresse du depot distant.",
 "Apres la recuperation, tu dois entrer dans le dossier cree avant de travailler.",
 "Le `git status` final signale que ta branche est en avance : ton commit est bien local, pas encore envoye."],
seed="""git init --bare depot-serre.git
git clone https://github.com/leonis-formation/depot-serre.git amorce
cd amorce
printf "monstera\\nficus\\n" > catalogue.txt
git add catalogue.txt
git commit -m "feat(catalogue): premières plantes"
git push origin main
cd ..
rm -rf amorce""")

ajoute("ch1-i4-menu-restaurant", "Intermediaire", "Le menu du restaurant",
"""Le restaurant met son menu a jour. Tu as modifie trois fichiers d'un coup :
les entrees, les plats, et un fichier de test que tu avais laisse trainer.

Tu mets tout au panier par reflexe. Retire le fichier de test, verifie que le
panier ne contient plus que ce qu'il faut, puis valide.""",
"""echo "- velouté de potiron" >> entrees.txt
echo "- risotto aux champignons" >> plats.txt
echo "essai de mise en page" > test.txt
git add .
git status
git reset test.txt
git status
git commit -m "feat(menu): ajout du veloute et du risotto"
git status""",
["Le piege est a la ligne `git add .` : regarde ce qu'elle a vraiment ramasse.",
 "Un seul fichier doit sortir du panier. Les deux autres y restent.",
 "Apres le commit, le fichier de test doit toujours apparaitre comme non suivi : il n'a jamais ete enregistre."],
seed="""git init restaurant
cd restaurant
printf -- "- salade de chevre\\n" > entrees.txt
printf -- "- poulet basquaise\\n" > plats.txt
git add entrees.txt plats.txt
git commit -m "feat(menu): premier menu de la saison\"""")

ajoute("ch1-i5-carnet-voyage", "Intermediaire", "Le carnet de voyage",
"""Tu tiens un carnet de voyage partage avec deux amis sur un depot distant.
Tu as deja recupere le depot.

Ajoute l'etape de Lisbonne, enregistre-la, puis envoie-la pour que les autres
la voient. Verifie l'etat avant et apres l'envoi : les deux affichages ne
disent pas la meme chose.""",
"""echo "Jour 3 : Lisbonne, tramway 28" >> etapes.txt
git add etapes.txt
git commit -m "feat(etapes): ajout de l'étape de Lisbonne"
git status
git push
git status""",
["Enregistrer en local et publier sont deux gestes separes. Git ne fait jamais le second tout seul.",
 "Avant l'envoi, `git status` parle d'une branche en avance. Apres, il parle d'une branche a jour.",
 "Le depot distant est deja connu de ta copie : la commande d'envoi n'a besoin d'aucun argument."],
seed="""git init --bare depot-voyage.git
git clone https://github.com/leonis-formation/depot-voyage.git amorce
cd amorce
printf "Jour 1 : Porto\\nJour 2 : Coimbra\\n" > etapes.txt
git add etapes.txt
git commit -m "feat(etapes): les deux premieres etapes"
git push origin main
cd ..
git clone https://github.com/leonis-formation/depot-voyage.git carnet
rm -rf amorce
cd carnet""")

# ---------------------------------------------------------------------- BOSS

ajoute("ch1-b1-repertoire-contacts", "BOSS", "Le repertoire de contacts",
"""Mauvaise nouvelle : le fichier `cles-api.txt` a ete enregistre dans
l'historique au commit precedent, et le depot est public.

Ajouter le fichier au `.gitignore` ne suffira pas, le reglage n'est pas
retroactif. Il faut d'abord retirer le fichier du suivi de Git tout en le
gardant sur ton disque, puis ecrire le reglage pour que l'accident ne se
reproduise pas, et enregistrer le tout.

Termine en verifiant que le fichier est bien toujours sur ton disque.""",
"""git status
git rm --cached cles-api.txt
git status
printf "cles-api.txt\\n" > .gitignore
git status
git add .gitignore
git commit -m "config(depot): retrait des clés du suivi et ajout du gitignore"
git status
ls
cat cles-api.txt""",
["Le reglage n'agit que sur les fichiers que Git ne suit pas encore. Celui-la, il le suit deja.",
 "Cherche la commande qui retire un fichier du depot sans le supprimer du disque. C'est une option de `git rm`.",
 "Fais-le dans cet ordre : retirer du suivi, puis ecrire le reglage, puis valider. Le `ls` final doit encore montrer le fichier."],
seed="""git init contacts
cd contacts
printf "Sarah : 06 11 22 33 44\\n" > contacts.txt
printf "token-prod : abcd1234\\n" > cles-api.txt
git add .
git commit -m "feat(contacts): premier répertoire\"""")

ajoute("ch1-b2-bibliotheque", "BOSS", "La bibliotheque du club",
"""Le club de lecture partage sa liste d'ouvrages. Pendant que tu lisais,
quelqu'un a publie la fiche des avis sur le depot distant, et toi tu as ajoute
un titre a la liste en local, sans etre a jour.

Constate d'abord que ton envoi est refuse, et lis ce que Git te repond. Mets-toi
a jour, verifie ce que tu as recupere, puis renvoie ton travail.

Les deux modifications portent sur des fichiers differents : Git sait les
combiner tout seul.""",
"""git status
git push
git pull --no-edit
ls
cat ouvrages.txt
git status
git push
git status""",
["Commence par tenter l'envoi sans rien faire d'autre. Le message de refus fait partie de l'exercice.",
 "Git te dit quoi faire dans son message : il faut d'abord rapatrier ce que tu n'as pas.",
 "L'option `--no-edit` evite que Git ouvre un editeur pour le message de fusion. Le `ls` te montrera le fichier arrive du depot distant."],
seed="""git init --bare depot-club.git
git clone https://github.com/leonis-formation/depot-club.git amorce
cd amorce
printf "L'Etranger\\n" > ouvrages.txt
git add ouvrages.txt
git commit -m "feat(ouvrages): premier titre"
git push origin main
cd ..
git clone https://github.com/leonis-formation/depot-club.git bibliotheque
cd amorce
printf "Avis du club : à lire absolument\\n" > avis.txt
git add avis.txt
git commit -m "feat(avis): ajout de la fiche des avis"
git push origin main
cd ..
rm -rf amorce
cd bibliotheque
printf "Le Mythe de Sisyphe\\n" >> ouvrages.txt
git commit -am "feat(ouvrages): ajout du Mythe de Sisyphe\"""")

ajoute("ch1-b3-planning-entrainement", "BOSS", "Le planning d'entrainement",
"""Le club d'athletisme reorganise sa saison. Trois sujets arrivent en vrac dans
ton dossier : le planning des seances, la liste du materiel, et un brouillon
personnel qui ne doit jamais etre publie.

Produis un historique propre : un commit par sujet, dans cet ordre, le planning
puis le materiel. Le brouillon ne doit apparaitre dans aucun commit, et tu dois
mettre en place le reglage qui garantit qu'il n'y arrivera jamais, meme si
quelqu'un fait un `git add .` plus tard.

Le reglage part dans son propre commit, en dernier.""",
"""printf "mardi : fractionne\\njeudi : endurance\\n" > planning.txt
printf "12 plots\\n4 chronos\\n" > materiel.txt
printf "demander une augmentation au président\\n" > brouillon-perso.txt
git status
git add planning.txt
git commit -m "feat(planning): ajout des séances de la semaine"
git add materiel.txt
git commit -m "feat(materiel): ajout du matériel du club"
printf "brouillon-perso.txt\\n" > .gitignore
git status
git add .gitignore
git commit -m "config(depot): exclusion du brouillon personnel"
git status""",
["Trois commits, donc trois passages par le panier. Ne mets jamais `git add .` tant que le reglage n'existe pas.",
 "L'ordre impose : planning, materiel, puis reglage. Chaque commit ne contient qu'un seul fichier.",
 "A la fin, `git status` ne doit plus rien signaler du tout : ni fichier modifie, ni fichier non suivi."],
seed="""git init athletisme
cd athletisme""")

ajoute("ch1-b4-inventaire-jeux", "BOSS", "L'inventaire de la ludotheque",
"""La ludotheque fait son inventaire. Tu as travaille vite : tu as fait un
`git add .` alors que le dossier contient aussi un export temporaire et un
dossier de photos trop lourd.

Rattrape le coup sans rien perdre. Sors du panier ce qui n'a rien a y faire,
mets en place le reglage pour que ces deux elements soient ignores a l'avenir,
puis enregistre l'inventaire et le reglage ensemble.""",
"""git add .
git status
git reset export.tmp
git reset photos
git status
printf "*.tmp\\nphotos/\\n" > .gitignore
git status
git add .
git commit -m "config(depot): inventaire et exclusion des fichiers temporaires"
git status
ls""",
["Deux elements a sortir du panier : un fichier et un dossier. La commande accepte les deux.",
 "Ecris le reglage apres avoir vide le panier, sinon `git status` continuera de te montrer ce que tu viens de retirer.",
 "Une fois le reglage en place, un second `git add .` devient sans danger : c'est tout l'interet."],
seed="""git init ludotheque
cd ludotheque
printf "Catan\\nCarcassonne\\n" > inventaire.txt
printf "export du 3 janvier\\n" > export.tmp
mkdir photos
printf "binaire\\n" > photos/catan.jpg""")

ajoute("ch1-b5-atelier-complet", "BOSS", "La reprise du site de l'asso",
"""Scenario complet. L'association partage le contenu de son site sur un depot
distant. Tu recuperes le projet, tu ajoutes la page des horaires, tu mets en
place le reglage qui ignore les journaux d'erreur produits par l'hebergeur,
puis tu publies ton travail.

Attention : un fichier de journal existe deja dans ton dossier de travail des
la recuperation. Il ne doit jamais partir sur le depot distant.

Termine par un `git status` qui prouve que tout est enregistre et publie.""",
"""git clone https://github.com/leonis-formation/depot-asso.git site
cd site
ls
git status
printf "*.log\\n" > .gitignore
git status
printf "Permanence : mardi 18h-20h\\n" > horaires.txt
git add .gitignore horaires.txt
git status
git commit -m "feat(horaires): ajout des horaires et exclusion des journaux"
git push
git status""",
["Fais le reglage avant d'ajouter quoi que ce soit : tu evites d'avoir a te rattraper ensuite.",
 "Tu peux donner plusieurs fichiers a `git add` en une seule commande.",
 "Le `git status` final doit indiquer une branche a jour et un dossier propre, sans mentionner le journal."],
seed="""git init --bare depot-asso.git
git clone https://github.com/leonis-formation/depot-asso.git amorce
cd amorce
printf "Association du quartier\\n" > accueil.txt
git add accueil.txt
git commit -m "feat(site): page d'accueil"
git push origin main
cd ..
rm -rf amorce
git clone https://github.com/leonis-formation/depot-asso.git site
cd site
printf "erreur 500 du 2 janvier\\n" > erreurs.log
cd ..
rm -rf site""")


def main():
    os.makedirs(BASE, exist_ok=True)
    for e in EX:
        p = os.path.join(BASE, e["ident"])
        os.makedirs(p, exist_ok=True)
        json.dump({"ident": e["ident"], "chapitre": 1, "niveau": e["niveau"],
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
