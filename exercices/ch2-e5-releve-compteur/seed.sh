git init immeuble
cd immeuble
printf "Compteur A : 1240\nCompteur B : 980\nCompteur C : 1105\n" > compteurs.txt
git add compteurs.txt
git commit -m "feat(compteurs): releve de janvier"
printf "Compteur A : 1240\nCompteur B : 1080\nCompteur C : 1105\nCompteur D : 640\n" > compteurs.txt
git commit -am "fix(compteurs): correction du compteur B et ajout du D"
