#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generateur Leonis : rejoue chaque correction officielle avec le vrai Git
et produit exemple.txt. Un exercice = un dossier contenant
meta.json, enonce.md, solution.sh, indices.md et eventuellement seed.sh.
"""
import os, re, json, subprocess, sys, tempfile, shutil

BASE_CFG = [
    ("init.defaultBranch", "main"),
    ("advice.detachedHead", "false"),
    ("core.pager", "cat"),
    ("protocol.file.allow", "always"),
    ("pull.rebase", "false"),
    ("push.default", "simple"),
]

GITHUB = "https://github.com/leonis-formation/"


def horodate(n):
    """Heure du commit n. Chaque commande executee avance l'horloge de 7 minutes,
    pour que l'historique ait des dates credibles et reproductibles."""
    total = 9 * 60 + n * 7
    return "2026-01-05T%02d:%02d:00+0100" % (total // 60, total % 60)


def env_pour(work, n):
    e = {
        "LC_ALL": "C", "LANG": "C",
        "GIT_AUTHOR_NAME": "Eleve Leonis", "GIT_AUTHOR_EMAIL": "eleve@leonis.fr",
        "GIT_COMMITTER_NAME": "Eleve Leonis", "GIT_COMMITTER_EMAIL": "eleve@leonis.fr",
        "GIT_AUTHOR_DATE": horodate(n),
        "GIT_COMMITTER_DATE": horodate(n),
        "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null",
        "GIT_PAGER": "cat", "PAGER": "cat", "TERM": "dumb",
        "GIT_EDITOR": "true", "GIT_SEQUENCE_EDITOR": "true", "EDITOR": "true",
        "HOME": "/tmp/leonis-home", "PATH": os.environ["PATH"],
    }
    cfg = list(BASE_CFG) + [("url." + work + "/.insteadOf", GITHUB)]
    e["GIT_CONFIG_COUNT"] = str(len(cfg))
    for i, (k, v) in enumerate(cfg):
        e["GIT_CONFIG_KEY_%d" % i] = k
        e["GIT_CONFIG_VALUE_%d" % i] = v
    return e


RACINE = "/home/eleve"
PROMPT = "$ "

# Masquage des hashs : un hash n'est jamais compare, le reste de la ligne si.
MASQUES = [
    (re.compile(r"^\[([\w./-]+) \(root-commit\) [0-9a-f]{7,40}\]"), r"[\1 (root-commit) ...]"),
    (re.compile(r"^\[([\w./-]+) [0-9a-f]{7,40}\]"), r"[\1 ...]"),
    (re.compile(r"^commit [0-9a-f]{40}"), "commit ..."),
    (re.compile(r"^([*|\\/ ]*)([0-9a-f]{7,8}) "), r"\1... "),
    (re.compile(r"\b[0-9a-f]{7,8}\.\.[0-9a-f]{7,8}\b"), "..."),
    (re.compile(r"^index [0-9a-f]{7,40}\.\.[0-9a-f]{7,40}"), "index ..."),
    (re.compile(r"\(commit: [0-9a-f]{7,40}\)"), "(commit: ...)"),
    (re.compile(r"^([ *]\s+[\w./-]+\s+)[0-9a-f]{7,8} "), r"\1... "),
    (re.compile(r"\(was [0-9a-f]{7,40}\)"), "(was ...)"),
    (re.compile(r"^Merge: [0-9a-f]{7,40} [0-9a-f]{7,40}"), "Merge: ..."),
    (re.compile(r"^(    This reverts commit )[0-9a-f]{40}\."), r"\1...."),
    (re.compile(r"(WIP on [\w./-]+: )[0-9a-f]{7,40} "), r"\1... "),
    (re.compile(r"^(HEAD is now at )[0-9a-f]{7,40} "), r"\1... "),
    (re.compile(r"^(Dropped refs/stash@\{\d+\} \()[0-9a-f]{40}\)"), r"\1...)"),


]


def masque(ligne):
    for rx, rep in MASQUES:
        ligne = rx.sub(rep, ligne)
    return ligne


def joue(path, commandes, work, transcrire, depart=0):
    """Execute une liste de commandes. Renvoie (lignes, cwd_final, horloge)."""
    sortie = []
    cwd = work
    n = depart
    for raw in commandes:
        cmd = raw.strip()
        if not cmd or cmd.startswith("#"):
            continue
        if transcrire:
            sortie.append(PROMPT + cmd)
        n += 1
        if cmd.startswith("cd "):
            cible = cmd[3:].strip()
            cwd = os.path.normpath(os.path.join(cwd, cible))
            if not os.path.isdir(cwd):
                raise RuntimeError("cd vers un dossier inexistant : %s" % cwd)
            continue
        p = subprocess.run(["bash", "-c", cmd], cwd=cwd, env=env_pour(work, n),
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           text=True)
        corps = p.stdout
        corps = corps.replace(work, RACINE)
        corps = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", corps)
        # un depot distant s'affiche comme une adresse GitHub, pas comme un chemin
        corps = re.sub(r"%s/(depot-[\w-]+?)(\.git)?(?=[\s'\"]|$)" % re.escape(RACINE),
                       lambda m: GITHUB + m.group(1) + ".git", corps)
        if transcrire and corps.strip("\n"):
            for l in corps.rstrip("\n").split("\n"):
                sortie.append(masque(l))
    return sortie, cwd, n


def construit(path):
    meta = json.load(open(os.path.join(path, "meta.json"), encoding="utf-8"))
    os.makedirs("/tmp/leonis-home", exist_ok=True)
    work = tempfile.mkdtemp(prefix="leonis-")
    try:
        seed = os.path.join(path, "seed.sh")
        if os.path.exists(seed):
            cmds = open(seed, encoding="utf-8").read().splitlines()
            _, work_cwd, horloge = joue(path, cmds, work, transcrire=False)
        else:
            work_cwd = work
            horloge = 0
        sol = open(os.path.join(path, "solution.sh"), encoding="utf-8").read().splitlines()
        # le cwd de depart de la solution est celui laisse par le seed
        rel = os.path.relpath(work_cwd, work)
        cmds = ([] if rel == "." else ["cd " + rel]) + sol
        # le cd technique issu du seed ne doit pas avancer l'horloge :
        # le moteur du site ne le rejoue pas
        depart = horloge - (1 if rel != "." else 0)
        lignes, _, _ = joue(path, cmds, work, transcrire=True, depart=depart)
        if rel != ".":
            lignes = lignes[1:]  # on n'affiche pas le cd technique du seed
        texte = "\n".join(lignes) + "\n"
    finally:
        shutil.rmtree(work, ignore_errors=True)
    with open(os.path.join(path, "exemple.txt"), "w", encoding="utf-8") as f:
        f.write(texte)

    # Version affichee a l'etudiant : les commandes sont masquees, sinon
    # l'exemple donne la solution. Un exercice peut demander l'inverse
    # avec "montrer_commandes": true dans meta.json.
    if meta.get("montrer_commandes"):
        affiche = texte
    else:
        affiche = "\n".join(
            (PROMPT + "...") if l.startswith(PROMPT) else l
            for l in texte.rstrip("\n").split("\n")) + "\n"
    with open(os.path.join(path, "affichage.txt"), "w", encoding="utf-8") as f:
        f.write(affiche)
    return meta, texte


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "exercices"
    dossiers = sorted(d for d in os.listdir(base)
                      if os.path.isdir(os.path.join(base, d)))
    for d in dossiers:
        p = os.path.join(base, d)
        if not os.path.exists(os.path.join(p, "meta.json")):
            continue
        meta, texte = construit(p)
        n = len(texte.rstrip("\n").split("\n"))
        print("OK  %-28s %-14s %3d lignes" % (d, meta["niveau"], n))


if __name__ == "__main__":
    main()
