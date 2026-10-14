#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rejoue une correction officielle avec le vrai Git et capture la transcription.
Usage: python3 run_solution.py <dossier-exercice>
Le dossier contient solution.sh (une commande par ligne, # = commentaire).
Produit exemple.txt : la transcription exacte, telle qu'elle sera affichee sur le site.
"""
import os, subprocess, sys, tempfile, shutil, re

ENV = {
    "LC_ALL": "C", "LANG": "C",
    "GIT_AUTHOR_NAME": "Eleve Leonis", "GIT_AUTHOR_EMAIL": "eleve@leonis.fr",
    "GIT_COMMITTER_NAME": "Eleve Leonis", "GIT_COMMITTER_EMAIL": "eleve@leonis.fr",
    "GIT_AUTHOR_DATE": "2026-01-05T09:00:00+0100",
    "GIT_COMMITTER_DATE": "2026-01-05T09:00:00+0100",
    "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null",
    "GIT_PAGER": "cat", "PAGER": "cat", "TERM": "dumb",
    "PATH": os.environ["PATH"], "HOME": "/tmp/fakehome",
    "GIT_CONFIG_COUNT": "3",
    "GIT_CONFIG_KEY_0": "init.defaultBranch", "GIT_CONFIG_VALUE_0": "main",
    "GIT_CONFIG_KEY_1": "advice.detachedHead", "GIT_CONFIG_VALUE_1": "false",
    "GIT_CONFIG_KEY_2": "core.pager", "GIT_CONFIG_VALUE_2": "cat",
}

PROMPT = "$ "

def normalise(txt, workdir):
    txt = txt.replace(workdir, "/home/eleve/depot")
    txt = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", txt)
    return txt

def main(path):
    sol = os.path.join(path, "solution.sh")
    with open(sol, encoding="utf-8") as f:
        lines = [l.rstrip("\n") for l in f]

    work = tempfile.mkdtemp(prefix="leonis-")
    os.makedirs("/tmp/fakehome", exist_ok=True)
    out = []
    cwd = work
    try:
        for raw in lines:
            cmd = raw.strip()
            if not cmd or cmd.startswith("#"):
                continue
            out.append(PROMPT + cmd)
            if cmd.startswith("cd "):
                target = cmd[3:].strip()
                cwd = os.path.normpath(os.path.join(cwd, target))
                continue
            p = subprocess.run(["bash", "-c", cmd], cwd=cwd, env=ENV,
                               capture_output=True, text=True)
            body = p.stdout + p.stderr
            body = normalise(body, work)
            if body:
                out.extend(body.rstrip("\n").split("\n"))
        transcript = "\n".join(out) + "\n"
    finally:
        shutil.rmtree(work, ignore_errors=True)

    with open(os.path.join(path, "exemple.txt"), "w", encoding="utf-8") as f:
        f.write(transcript)
    sys.stdout.write(transcript)

if __name__ == "__main__":
    main(sys.argv[1])
