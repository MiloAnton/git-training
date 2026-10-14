#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, json, sys
BASE="exercices"
CH=int(sys.argv[1]) if len(sys.argv)>1 else 1
TITRES={1:"Du fichier au commit",2:"Lire l'historique",3:"Les branches",4:"Fusionner",5:"Réparer sans casser",6:"Les conflits"}
ORDRE={"Echauffement":0,"Intermediaire":1,"BOSS":2}
items=[]
for d in sorted(os.listdir(BASE)):
    p=os.path.join(BASE,d)
    if not os.path.isdir(p): continue
    m=json.load(open(os.path.join(p,"meta.json"),encoding="utf-8"))
    if m["chapitre"]!=CH: continue
    items.append((ORDRE[m["niveau"]], d, m, p))
items.sort()
out=["# Chapitre %d - %s" % (CH, TITRES[CH]),
"",
"15 exercices. Chaque bloc terminal est la sortie d'une execution reelle de la",
"correction officielle avec Git 2.43, horloge et identite figees. Les hashs sont",
"masques par `...` et ne sont pas compares.",
""]
niv=None
for _,d,m,p in items:
    if m["niveau"]!=niv:
        niv=m["niveau"]
        out+=["", "## Niveau %s" % niv, ""]
    out+=["### %s" % m["titre"], "", "Identifiant : `%s`" % d, ""]
    en=open(os.path.join(p,"enonce.md"),encoding="utf-8").read().split("\n",2)[2].strip()
    out+=[en, "", "**Exemple**", "", "```"]
    out+=open(os.path.join(p,"exemple.txt"),encoding="utf-8").read().rstrip("\n").split("\n")
    out+=["```", "", "**Indices**", ""]
    out+=open(os.path.join(p,"indices.md"),encoding="utf-8").read().rstrip("\n").split("\n")
    out+=["", "**Correction officielle**", "", "```bash"]
    out+=open(os.path.join(p,"solution.sh"),encoding="utf-8").read().rstrip("\n").split("\n")
    out+=["```", ""]
open("Chapitre%d_exercices_a_valider.md" % CH,"w",encoding="utf-8").write("\n".join(out)+"\n")
print("ecrit", len(out), "lignes")
