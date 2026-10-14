git init traduction
cd traduction
printf "accueil = Bienvenue\nquitter = Sortir\n" > fr.txt
git add fr.txt
git commit -m "feat(fr): premieres chaines"
printf "titre = Mon application\n" > en.txt
git add en.txt
git commit -m "feat(en): fichier anglais"
printf "accueil = Bienvenue chez vous\nquitter = Quitter\naide = Aide\n" > fr.txt
git commit -am "feat(fr): relecture et ajout de l'aide"
printf "accueil = Bienvenue chez vous\nquitter = Quitter\naide = Aide en ligne\n" > fr.txt
git commit -am "style(fr): precision sur l'aide"
