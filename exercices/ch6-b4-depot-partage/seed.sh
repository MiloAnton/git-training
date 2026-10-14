git init --bare depot-club.git
git clone https://github.com/leonis-formation/depot-club.git amorce
cd amorce
printf "Club de randonnee\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): le club"
git push origin main
cd ..
git clone https://github.com/leonis-formation/depot-club.git travail
cd amorce
printf "Sortie : dimanche 8h\n" > sorties.txt
git add sorties.txt
git commit -m "feat(sorties): sortie du dimanche"
git push origin main
cd ..
rm -rf amorce
cd travail
printf "Cotisation : 25 euros\n" > cotisation.txt
git add cotisation.txt
git commit -m "feat(cotisation): montant annuel"
