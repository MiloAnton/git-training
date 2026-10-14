git init livraison
cd livraison
printf "Version 2.0\nDate : 1 janvier\n" > version.txt
printf "Guide d'installation\n" > guide.txt
git add .
git commit -m "feat(livraison): version 2.0"
printf "Guide d'installation\nEtape 1 : telecharger\n" > guide.txt
git add guide.txt
