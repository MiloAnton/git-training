git init --bare depot-asso.git
git clone https://github.com/leonis-formation/depot-asso.git amorce
cd amorce
printf "Association du quartier\n" > accueil.txt
git add accueil.txt
git commit -m "feat(site): page d'accueil"
git push origin main
cd ..
rm -rf amorce
git clone https://github.com/leonis-formation/depot-asso.git site
cd site
printf "erreur 500 du 2 janvier\n" > erreurs.log
cd ..
rm -rf site
