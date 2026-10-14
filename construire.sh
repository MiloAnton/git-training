#!/bin/bash
# Fabrique le site d'entrainement de bout en bout.
set -e
cd "$(dirname "$0")"

echo "== 1/5  exemples rejoues avec le vrai Git"
python3 build.py exercices

echo
echo "== 2/5  conformite du moteur du site"
node conformance.js

echo
echo "== 3/5  extraction des schemas de graphe"
node graphes.js

echo
echo "== 4/5  chiffrement et generation du site"
python3 site.py

echo
echo "== 5/5  test dans un vrai navigateur"
if node -e "require('playwright')" 2>/dev/null; then
  node test_navigateur.js
else
  echo "playwright absent, etape ignoree (npm install playwright)"
fi

echo
echo "Termine. Mettez en ligne le contenu du dossier public/."
