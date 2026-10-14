git init imprimerie
cd imprimerie
printf "Affiche A3 : 12 euros\n" > tarifs.txt
git add tarifs.txt
git commit -m "feat(tarifs): premiers tarifs"
printf "Affiche A3 : 12 euros\nAffiche A2 : 18 euros\n" > tarifs.txt
git commit -am "truc"
