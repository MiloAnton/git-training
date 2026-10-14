printf "6h Reveil\n9h Chronique\n12h Journal\n" > grille.txt
git stash
git status
git switch main
git switch feature/grille
git stash pop
cat grille.txt
