git init materiel
cd materiel
printf "Projecteur\nSono : a choisir\n" > materiel.txt
git add materiel.txt
git commit -m "feat(materiel): projecteur"
git switch -c feature/sono
printf "Projecteur\nSono : modele A\n" > materiel.txt
git commit -am "feat(materiel): sono modele A"
git switch main
printf "Projecteur\nSono : modele B\n" > materiel.txt
git commit -am "feat(materiel): sono modele B"
git merge feature/sono
