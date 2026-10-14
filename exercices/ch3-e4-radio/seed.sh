git init radio
cd radio
printf "6h Reveil\n9h Chronique\n" > grille.txt
git add grille.txt
git commit -m "feat(grille): premiere grille"
git switch -c feature/grille
