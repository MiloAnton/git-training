printf "loyer : 820\ninternet : 30\n" > charges.txt
printf "courses du 3 janvier : 54\n" > courses-communes.txt
git status
git add charges.txt
git status
git commit -m "feat(charges): ajout des charges fixes"
git add courses-communes.txt
git commit -m "feat(courses): ajout des courses du 3 janvier"
git status
