git init cantine
cd cantine
printf "Lundi : gratin\nMardi : a definir\n" > menu.txt
git add menu.txt
git commit -m "feat(menu): debut de semaine"
git switch -c feature/mardi
printf "Lundi : gratin\nMardi : poisson pane\n" > menu.txt
git commit -am "feat(menu): poisson le mardi"
git switch main
printf "Lundi : gratin\nMardi : lasagnes\n" > menu.txt
git commit -am "feat(menu): lasagnes le mardi"
