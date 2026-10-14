git init --bare depot-club.git
git clone https://github.com/leonis-formation/depot-club.git amorce
cd amorce
printf "L'Etranger\n" > ouvrages.txt
git add ouvrages.txt
git commit -m "feat(ouvrages): premier titre"
git push origin main
cd ..
git clone https://github.com/leonis-formation/depot-club.git bibliotheque
cd amorce
printf "Avis du club : à lire absolument\n" > avis.txt
git add avis.txt
git commit -m "feat(avis): ajout de la fiche des avis"
git push origin main
cd ..
rm -rf amorce
cd bibliotheque
printf "Le Mythe de Sisyphe\n" >> ouvrages.txt
git commit -am "feat(ouvrages): ajout du Mythe de Sisyphe"
