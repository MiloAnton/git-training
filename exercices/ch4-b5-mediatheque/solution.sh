git switch -c feature/numerique
printf "Postes informatiques : 8\n" > numerique.txt
git add numerique.txt
git commit -m "feat(numerique): postes informatiques"
printf "Postes informatiques : 8\nPret de liseuses : 20\n" > numerique.txt
git commit -am "feat(numerique): pret de liseuses"
git switch main
printf "Ouvert mardi, jeudi, samedi\n" > horaires.txt
git add horaires.txt
git commit -m "feat(horaires): jours d'ouverture"
git switch -c fix/affichage
printf "Affichage : panneau a l'entree\n" > affichage.txt
git add affichage.txt
git commit -m "fix(affichage): panneau d'entree"
git switch main
git merge --ff-only fix/affichage
git merge --no-ff feature/numerique
git branch -d fix/affichage
git branch -d feature/numerique
git branch
git log --oneline --all
git show HEAD --stat
git diff HEAD~3 HEAD
