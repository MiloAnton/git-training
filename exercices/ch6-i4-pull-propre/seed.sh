git init --bare depot-asso.git
git clone https://github.com/leonis-formation/depot-asso.git amorce
cd amorce
printf "Association du quartier\n" > accueil.txt
git add accueil.txt
git commit -m "feat(accueil): presentation"
git push origin main
cd ..
git clone https://github.com/leonis-formation/depot-asso.git travail
cd amorce
printf "Reunion le 12 mars\n" > reunion.txt
git add reunion.txt
git commit -m "feat(reunion): date de la reunion"
git push origin main
cd ..
rm -rf amorce
cd travail
printf "Adhesion : 15 euros\n" > adhesion.txt
git add adhesion.txt
git commit -m "feat(adhesion): montant de l'adhesion"
