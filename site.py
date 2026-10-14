#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genere le site statique : donnees du chapitre, indices et corrections
chiffres en AES-GCM, pages HTML."""
import os, re, json, base64, html, hashlib, secrets, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

BASE = "exercices"
PUBLIC = "public"
ITER = 150000

CHAPITRES = {
    1: {"titre": "Du fichier au commit",
        "sous_titre": "init, status, add, commit, reset, .gitignore, clone, push, pull",
        "limites": [
            "Le dépôt distant est simulé dans la page : aucune connexion à GitHub, "
            "aucun identifiant ni jeton n'est demandé.",
            "Les commandes qui ouvrent un éditeur de texte (un commit sans -m, "
            "git rebase -i) ne sont pas disponibles ici.",
            "Le shell ne connaît que les quelques commandes utiles au TP : "
            "echo, printf, cat, ls, cd, mkdir, rm, pwd.",
        ]},
    2: {"titre": "Lire l'historique",
        "sous_titre": "log, --oneline, --graph, HEAD~n, les trois git diff, show",
        "limites": [
            "Les empreintes de commit sont fabriquées par le simulateur. Elles ont "
            "la bonne forme et la bonne longueur, mais ce ne sont pas de vraies "
            "empreintes SHA-1 : sur ta machine, les mêmes commits en auront d'autres.",
            "Sur une vraie machine, git log et git diff s'ouvrent dans un afficheur "
            "qui attend que tu tapes q pour rendre la main. Ici tout s'affiche d'un coup.",
            "Les dates de l'historique sont simulées : l'horloge avance de sept minutes "
            "à chaque commande, pour que les commits ne portent pas tous la même heure.",
            "Le dépôt distant est simulé dans la page : aucune connexion à GitHub.",
        ]},    3: {"titre": "Les branches",
        "sous_titre": "switch, branch, renommer, supprimer, stash",
        "limites": [
            "Le dessin de branches de git log --graph n'est rendu ici que pour un "
            "historique en ligne droite. Pour voir les branches, fie-toi au schéma "
            "affiché sous chaque exercice : il montre la même chose, en plus lisible.",
            "Les commandes qui ouvrent un éditeur de texte ne sont pas disponibles.",
            "Les empreintes de commit sont fabriquées par le simulateur : elles ont la "
            "bonne forme mais ce ne sont pas de vraies empreintes SHA-1.",
        ]},
    4: {"titre": "Fusionner",
        "sous_titre": "merge, fast-forward, --no-ff, --ff-only, choisir sa stratégie",
        "limites": [
            "Le dessin de branches de git log --graph n'est rendu ici que pour un "
            "historique en ligne droite. Le schéma sous chaque exercice montre les "
            "fusions de façon bien plus lisible.",
            "Les commandes qui ouvrent un éditeur de texte ne sont pas disponibles : "
            "les fusions se terminent donc avec git commit -m.",
            "Le dépôt distant est simulé dans la page : aucune connexion à GitHub.",
        ]},
    5: {"titre": "Réparer sans casser",
        "sous_titre": "amend, revert, les trois reset, reflog, restore, merge --squash",
        "limites": [
            "git rebase -i n'est pas disponible : il ouvre un éditeur de texte, ce que "
            "le navigateur ne sait pas simuler honnêtement. Le regroupement de commits "
            "se travaille ici avec git merge --squash.",
            "Le journal des déplacements de HEAD est simulé : il ne contient que les "
            "mouvements faits dans cette page, et il repart de zéro à chaque relance.",
            "Les empreintes de commit sont fabriquées par le simulateur : elles ont la "
            "bonne forme mais ce ne sont pas de vraies empreintes SHA-1.",
        ]},
    6: {"titre": "Les conflits",
        "sous_titre": "diagnostiquer, --ours et --theirs, terminer ou annuler, pull --rebase",
        "limites": [
            "La fusion à trois points est une version simplifiée de celle de Git. Elle "
            "donne les mêmes marqueurs sur des conflits de quelques lignes, mais elle "
            "peut diverger sur des fichiers longs et très remaniés.",
            "Les commandes qui ouvrent un éditeur de texte ne sont pas disponibles : "
            "une fusion se termine ici avec git commit -m, pas avec git merge --continue.",
            "Le dépôt distant est simulé dans la page : aucune connexion à GitHub, "
            "aucun identifiant ni jeton n'est demandé.",
        ]},
}

ORDRE = {"Echauffement": 0, "Intermediaire": 1, "BOSS": 2}
AFFICHAGE_NIVEAU = {"Echauffement": "\u00c9chauffement",
                    "Intermediaire": "Interm\u00e9diaire", "BOSS": "BOSS"}


def chiffre(texte, code):
    sel = secrets.token_bytes(16)
    cle = hashlib.pbkdf2_hmac("sha256", code.encode("utf-8"), sel, ITER, 32)
    iv = secrets.token_bytes(12)
    ct = AESGCM(cle).encrypt(iv, texte.encode("utf-8"), None)
    return base64.b64encode(sel + iv + ct).decode("ascii")


def md_vers_html(txt):
    txt = html.escape(txt)
    txt = re.sub(r"`([^`]+)`", r"<code>\1</code>", txt)
    txt = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", txt)
    blocs = [b.strip() for b in txt.split("\n\n") if b.strip()]
    return "\n".join("<p>%s</p>" % b.replace("\n", " ") for b in blocs)


def charge(chapitre):
    ex = []
    for d in sorted(os.listdir(BASE)):
        p = os.path.join(BASE, d)
        meta_p = os.path.join(p, "meta.json")
        if not os.path.exists(meta_p):
            continue
        meta = json.load(open(meta_p, encoding="utf-8"))
        if meta["chapitre"] != chapitre:
            continue
        lire = lambda n: open(os.path.join(p, n), encoding="utf-8").read() \
            if os.path.exists(os.path.join(p, n)) else ""
        enonce = lire("enonce.md").split("\n", 2)[2].strip()
        indices = [l.split(". ", 1)[1] for l in lire("indices.md").strip().split("\n") if l.strip()]
        ex.append({
            "ident": meta["ident"], "niveau": AFFICHAGE_NIVEAU[meta["niveau"]],
            "titre": meta["titre"],
            "enonce": md_vers_html(enonce),
            "exemple": lire("affichage.txt").rstrip("\n").split("\n"),
            "seed": lire("seed.sh"),
            "indices": indices,
            "correction": lire("solution.sh").rstrip("\n"),
            "graphe": json.loads(lire("graphe.json") or "null"),
        })
    ORDRE_AFF = {v: ORDRE[k] for k, v in AFFICHAGE_NIVEAU.items()}
    ex.sort(key=lambda e: (ORDRE_AFF[e["niveau"]], e["ident"]))
    return ex


def genere(chapitre, code_indices, code_corrections):
    ex = charge(chapitre)
    public = []
    coffre_ind, coffre_cor = {}, {}
    for e in ex:
        coffre_ind[e["ident"]] = e["indices"]
        coffre_cor[e["ident"]] = e["correction"]
        public.append({k: e[k] for k in ("ident", "niveau", "titre", "enonce",
                                         "exemple", "seed", "graphe")})
        public[-1]["nb_indices"] = len(e["indices"])

    donnees = {
        "chapitre": chapitre,
        "titre": CHAPITRES[chapitre]["titre"],
        "sous_titre": CHAPITRES[chapitre]["sous_titre"],
        "limites": CHAPITRES[chapitre]["limites"],
        "exercices": public,
        "indices": chiffre(json.dumps(coffre_ind, ensure_ascii=False), code_indices),
        "corrections": chiffre(json.dumps(coffre_cor, ensure_ascii=False), code_corrections),
        "iterations": ITER,
    }
    os.makedirs(os.path.join(PUBLIC, "data"), exist_ok=True)
    with open(os.path.join(PUBLIC, "data", "chapitre-%d.json" % chapitre), "w",
              encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, separators=(",", ":"))
    return len(ex)


if __name__ == "__main__":
    codes = json.load(open("codes.json", encoding="utf-8"))
    for ch, c in codes.items():
        n = genere(int(ch), c["indices"], c["corrections"])
        print("chapitre %s : %d exercices, indices et corrections chiffres" % (ch, n))
