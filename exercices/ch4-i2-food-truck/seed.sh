git init foodtruck
cd foodtruck
printf "Food truck Chez Lila\n" > carte.txt
git add carte.txt
git commit -m "feat(carte): ouverture"
git switch -c feature/burger
printf "Burger du jour : 9 euros\n" > burger.txt
git add burger.txt
git commit -m "feat(burger): burger du jour"
git switch main
git switch -c feature/dessert
printf "Tarte citron : 4 euros\n" > dessert.txt
git add dessert.txt
git commit -m "feat(dessert): tarte citron"
git switch main
git switch -c feature/boissons
printf "Limonade maison : 3 euros\n" > boissons.txt
git add boissons.txt
git commit -m "feat(boissons): limonade"
git switch main
