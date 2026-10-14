git init playlist
cd playlist
echo "Daft Punk - Around the World" > titres.txt
echo "demander la sono au BDE" > notes.txt
git status
git add titres.txt
git status
git commit -m "feat(titres): ajout du premier morceau"
git status
ls
