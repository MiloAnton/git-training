git init brocante
cd brocante
printf "Brocante du dimanche\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): la brocante"
printf "Emplacement : 8 euros\n" > tarifs.txt
git add tarifs.txt
git commit -m "feat(tarifs): prix de l'emplacement"
printf "Emplacement : 8 euros\nEmplacement couvert : 800 euros\n" > tarifs.txt
git commit -am "feat(tarifs): emplacement couvert"
printf "Stand buvette\n" > stands.txt
git add stands.txt
git commit -m "feat(stands): stand buvette"
printf "Stand buvette\nStand livres\n" > stands.txt
git commit -am "stands"
printf "efface par erreur\n" > tarifs.txt
printf "notes en vrac\n" > brouillon.txt
git add brouillon.txt
