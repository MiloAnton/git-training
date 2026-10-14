git init site
cd site
printf "titre = Accueil\ncouleur = bleu\n" > page.txt
git add page.txt
git commit -m "feat(page): page d'accueil"
printf "titre = Accueil\ncouleur = bleu\nmenu = visible\n" > page.txt
git commit -am "feat(page): ajout du menu"
printf "titre = Accueil\ncouleur = \nmenu = visible\n" > page.txt
git commit -am "style(page): nouvelle couleur"
printf "titre = Accueil\ncouleur = \nmenu = visible\npied = visible\n" > page.txt
git commit -am "feat(page): ajout du pied de page"
