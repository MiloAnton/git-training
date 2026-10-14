git init coworking
cd coworking
printf "Espace Le Comptoir\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): l'espace"
git switch -c feature/salles
printf "Salle Atelier : 12 places\nSalle Focus : 4 places\n" > salles.txt
git add salles.txt
git commit -m "feat(salles): deux salles"
git switch main
git switch -c feature/tarifs
printf "Journee : 18 euros\nMois : 220 euros\n" > tarifs.txt
git add tarifs.txt
git commit -m "feat(tarifs): grille tarifaire"
git switch main
printf "Espace Le Comptoir\nOuvert 7j/7\n" > presentation.txt
git commit -am "feat(presentation): ouverture 7j/7"
