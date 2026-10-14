echo "Jour 1 : départ du port de Brest" > journal.txt
echo "code du coffre : 4471" > prive.txt
git add .
git status
git reset prive.txt
git status
git commit -m "feat(journal): premiere entree de la traversee"
git status
cat prive.txt
