git init affiche
cd affiche
printf "Visuel : a choisir\nFormat : A2\n" > affiche.txt
git add affiche.txt
git commit -m "feat(affiche): cahier des charges"
git switch -c feature/affiche
printf "Visuel : photo noir et blanc\nFormat : A2\n" > affiche.txt
git commit -am "feat(affiche): photo noir et blanc"
git switch main
printf "Visuel : illustration coloree\nFormat : A2\n" > affiche.txt
git commit -am "feat(affiche): illustration coloree"
