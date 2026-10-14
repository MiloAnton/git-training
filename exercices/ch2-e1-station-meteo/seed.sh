git init station
cd station
printf "lundi : 8 degres, pluie\n" > releves.txt
git add releves.txt
git commit -m "feat(releves): releve du lundi"
printf "mardi : 11 degres, nuageux\n" >> releves.txt
git commit -am "feat(releves): releve du mardi"
printf "mercredi : 14 degres, soleil\n" >> releves.txt
git commit -am "feat(releves): releve du mercredi"
