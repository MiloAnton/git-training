git init musique
cd musique
printf "Ecole de musique du Parc\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): l'ecole"
printf "Piano : salle 1\n" > salles.txt
printf "Lundi 17h : solfege\n" > planning.txt
printf "Guitare : 3 professeurs\n" > professeurs.txt
git add .
