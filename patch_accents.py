# -*- coding: utf-8 -*-
"""Pose les accents sur tout le texte francais affiche a l'etudiant."""
import re

DICO = {
 "Apres": "Après", "Cree": "Crée", "Ecris": "Écris", "Recupere": "Récupère",
 "Scenario": "Scénario", "Verifie": "Vérifie", "L'etoile": "L'étoile",
 "apparaitre": "apparaître", "apres": "après", "bibliotheque": "bibliothèque",
 "caracteres": "caractères", "cles": "clés", "cote": "côté", "cree": "crée",
 "d'athletisme": "d'athlétisme", "d'ecrire": "d'écrire", "d'entrainement": "d'entraînement",
 "definitives": "définitives", "deja": "déjà", "demarres": "démarres", "depose": "dépose",
 "depot": "dépôt", "derniere": "dernière", "designe": "désigne", "desordre": "désordre",
 "differents": "différents", "disparaitre": "disparaître", "ecrase": "écrase",
 "ecrire": "écrire", "editeur": "éditeur", "elements": "éléments", "entree": "entrée",
 "entrees": "entrées", "envoye": "envoyé", "etape": "étape", "ete": "été", "etre": "être",
 "evite": "évite", "evites": "évites", "fougere": "fougère", "genere": "génère",
 "impose": "imposé", "l'etape": "l'étape", "l'etat": "l'état", "l'hebergeur": "l'hébergeur",
 "l'interet": "l'intérêt", "ludotheque": "ludothèque", "materiel": "matériel",
 "meme": "même", "partagees": "partagées", "piege": "piège", "precedent": "précédent",
 "premiere": "première", "premieres": "premières", "prepares": "prépares",
 "recuperation": "récupération", "recupere": "récupère", "recuperes": "récupères",
 "reflexe": "réflexe", "refuse": "refusé", "reglage": "réglage", "regle": "règle",
 "reintroduit": "réintroduit", "reorganise": "réorganise", "repertoire": "répertoire",
 "repond": "répond", "retroactif": "rétroactif", "revision": "révision",
 "seances": "séances", "selectionnes": "sélectionnes", "separes": "séparés",
 "soiree": "soirée", "supprimees": "supprimées", "systeme": "système",
 "trainer": "traîner", "traversee": "traversée", "verifiant": "vérifiant",
 "verifie": "vérifie", "veloute": "velouté", "chevre": "chèvre",
 "fractionne": "fractionné", "president": "président", "cafe": "café",
 "depart": "départ", "Etranger": "Étranger", "invites": "invités",
}


_PHRASES = [
    ("A la fin", "À la fin"), ("Celui-la", "Celui-là"), ("des maintenant", "dès maintenant"),
    ("` a ", "` à "), ("branche a jour", "branche à jour"), ("c'est a toi", "c'est à toi"),
    ("d'avoir a te", "d'avoir à te"), ("distant a ce", "distant à ce"), ("dit a Git", "dit à Git"),
    ("enregistre-le a ton", "enregistre-le à ton"), ("est a la", "est à la"),
    ("exactement la que", "exactement là que"), ("fichier a cô", "fichier à cô"),
    ("fichiers a ", "fichiers à "), ("génère a cô", "génère à cô"),
    ("ignores a l'avenir", "ignorés à l'avenir"), ("menu a jour", "menu à jour"),
    ("place a la", "place à la"), ("publie sur", "publié sur"), ("regarde ou en", "regarde où en"),
    ("rien a y", "rien à y"), ("réflexe a prendre", "réflexe à prendre"),
    ("t'oblige a tout", "t'oblige à tout"), ("titre a la", "titre à la"),
    ("toucher a l'autre", "toucher à l'autre"), ("éléments a sortir", "éléments à sortir"),
    ("être a jour", "être à jour"), ("a te rattraper", "à te rattraper"),
    ("Rien n'est encore envoyé", "Rien n'est encore envoyé"),
    ("sans etre", "sans être"), ("enregistre dans", "enregistré dans"), ("a publie la", "a publié la"), ("est enregistre et", "est enregistré et"), ("Numerote", "Numérote"),
    ("ne doit jamais etre", "ne doit jamais être"), ("doit etre", "doit être"),
    ("peut etre", "peut être"), ("tu as deja", "tu as déjà"), ("n'a rien a y faire", "n'a rien à y faire"),
]

FONCTION = '''
_PHRASES = %r

_DICO = %r


def _recolle(trouve, remplacement):
    """Garde le retour a la ligne d'origine si la phrase etait coupee."""
    if "\\n" in trouve:
        mots = remplacement.split(" ")
        bouts = re.split(r"(\\s+)", trouve)
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
        morceaux[i] = re.sub(r"[A-Za-z\\u00c0-\\u00ff']+", rempl, morceaux[i])
        for a, b in _PHRASES:
            rx = re.compile(r"\\s+".join(re.escape(x) for x in a.split(" ")))
            morceaux[i] = rx.sub(lambda m, b=b: _recolle(m.group(0), b), morceaux[i])
    return "".join(morceaux)

''' % (_PHRASES, DICO)

# contenus de fichiers et messages de commit, poses a la main
LITTERAUX = [
    ('- cafe\\n', '- café\\n'),
    ('Jour 1 : depart du port de Brest', 'Jour 1 : départ du port de Brest'),
    ('perceuse a colonne', 'perceuse à colonne'),
    ('echo "fougere"', 'echo "fougère"'),
    ('- salade de chevre\\n', '- salade de chèvre\\n'),
    ('- veloute de potiron', '- velouté de potiron'),
    ("L'Etranger\\n", "L'Étranger\\n"),
    ('Avis du club : a lire absolument', 'Avis du club : à lire absolument'),
    ('mardi : fractionne\\n', 'mardi : fractionné\\n'),
    ('demander une augmentation au president', 'demander une augmentation au président'),
    ("ajout des listes de courses et d'invites", "ajout des listes de courses et d'invités"),
    ('retrait des cles du suivi', 'retrait des clés du suivi'),
    ("ajout de l'etape de Lisbonne", "ajout de l'étape de Lisbonne"),
    ('ajout des seances de la semaine', 'ajout des séances de la semaine'),
    ('ajout du materiel du club', 'ajout du matériel du club'),
    ('feat(catalogue): premieres plantes', 'feat(catalogue): premières plantes'),
    ('feat(contacts): premier repertoire', 'feat(contacts): premier répertoire'),
    ('feat(avis): ajout de la fiche des avis', 'feat(avis): ajout de la fiche des avis'),
]


def main():
    s = open('make_ch1.py', encoding='utf-8').read()
    if '_DICO' not in s:
        s = s.replace('import os, json\n', 'import os, json, re\n' + FONCTION, 1)
        s = s.replace(
            "    EX.append(dict(ident=ident, niveau=niveau, titre=titre, enonce=enonce,\n"
            "                   solution=solution, indices=indices, seed=seed))",
            "    EX.append(dict(ident=ident, niveau=niveau, titre=acc(titre), enonce=acc(enonce),\n"
            "                   solution=solution, indices=[acc(i) for i in indices], seed=seed))")
    for a, b in LITTERAUX:
        s = s.replace(a, b)
    open('make_ch1.py', 'w', encoding='utf-8').write(s)
    print('make_ch1.py mis a jour')


if __name__ == '__main__':
    main()
