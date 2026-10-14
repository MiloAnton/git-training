git init scierie
cd scierie
printf "Chene : 12 m3\nHetre : 8 m3\n" > stock.txt
git add stock.txt
git commit -m "feat(stock): inventaire du bois"
printf "idees en vrac pour la scierie\n" > brouillon.txt
git add brouillon.txt
printf "tout casse\n" > stock.txt
