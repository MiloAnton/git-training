printf "Lundi : Les Temps modernes\nMardi : Le Cuirasse Potemkine\n" > programme.txt
git switch main
git stash
git switch main
git switch feature/programme
git stash pop
cat programme.txt
