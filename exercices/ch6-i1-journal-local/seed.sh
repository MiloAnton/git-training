git init journal
cd journal
printf "Une : a definir\nPages : 12\n" > une.txt
git add une.txt
git commit -m "feat(une): maquette"
git switch -c feature/edito
printf "Une : le marche renait\nPages : 12\n" > une.txt
git commit -am "feat(une): titre sur le marche"
git switch main
printf "Une : la piscine rouvre\nPages : 12\n" > une.txt
git commit -am "feat(une): titre sur la piscine"
