printf "*.tmp\nbrouillons/\n.DS_Store\n!rappel.tmp\n" > .gitignore
git status
git add .
git commit -m "config(depot): reglage du gitignore et ajout des fiches"
git status
cat .gitignore
