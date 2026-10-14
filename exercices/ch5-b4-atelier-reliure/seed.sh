git init reliure
cd reliure
printf "Couture a la japonaise\n" > techniques.txt
git add techniques.txt
git commit -m "feat(techniques): couture japonaise"
printf "Couture a la japonaise\nDos carre colle\n" > techniques.txt
git commit -am "feat(techniques): dos carre colle"
printf "Couture a la japonaise\nDos carre colle\nReliure copte\n" > techniques.txt
git commit -am "feat(techniques): reliure copte"
