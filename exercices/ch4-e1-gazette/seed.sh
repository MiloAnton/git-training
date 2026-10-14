git init gazette
cd gazette
printf "La Gazete du lycee\nNumero 1\n" > une.txt
git add une.txt
git commit -m "feat(une): premiere une"
git switch -c fix/titre
printf "La Gazette du lycee\nNumero 1\n" > une.txt
git commit -am "fix(une): correction du titre"
git switch main
