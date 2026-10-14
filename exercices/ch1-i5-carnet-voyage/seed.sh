git init --bare depot-voyage.git
git clone https://github.com/leonis-formation/depot-voyage.git amorce
cd amorce
printf "Jour 1 : Porto\nJour 2 : Coimbra\n" > etapes.txt
git add etapes.txt
git commit -m "feat(etapes): les deux premieres etapes"
git push origin main
cd ..
git clone https://github.com/leonis-formation/depot-voyage.git carnet
rm -rf amorce
cd carnet
