git init asso
cd asso
printf "Slogan : ensemble, plus forts\nContact : contact@asso.fr\n" > accueil.txt
git add accueil.txt
git commit -m "feat(accueil): page d'accueil"
git switch -c feature/refonte
printf "Slogan : agir ensemble\nContact : contact@asso.fr\n" > accueil.txt
git commit -am "feat(accueil): nouveau slogan"
git switch main
printf "Slogan : ensemble, plus forts depuis 1998\nContact : contact@asso.fr\n" > accueil.txt
git commit -am "feat(accueil): slogan avec la date"
