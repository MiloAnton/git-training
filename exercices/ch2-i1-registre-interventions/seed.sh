git init technique
cd technique
printf "01/01 : remplacement du filtre\n" > registre.txt
git add registre.txt
git commit -m "feat(registre): intervention du 1er janvier"
printf "08/01 : purge des radiateurs\n" >> registre.txt
git commit -am "feat(registre): intervention du 8 janvier"
printf "15/01 : controle electrique\n" >> registre.txt
git commit -am "feat(registre): intervention du 15 janvier"
printf "22/01 : reglage de la chaudiere\n" >> registre.txt
git commit -am "feat(registre): intervention du 22 janvier"
