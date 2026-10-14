git init atelier
cd atelier
echo "perceuse à colonne" > inventaire.txt
echo "sauvegarde automatique" > inventaire.txt.bak
git status
printf "*.bak\n" > .gitignore
git status
git add .
git commit -m "config(depot): ajout du gitignore et de l'inventaire"
git status
