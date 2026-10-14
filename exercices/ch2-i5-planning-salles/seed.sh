git init batiment
cd batiment
printf "Lundi 9h : salle A\n" > planning.txt
git add planning.txt
git commit -m "feat(planning): creneau du lundi"
printf "2 videoprojecteurs\n" > materiel.txt
git add materiel.txt
git commit -m "feat(materiel): inventaire initial"
printf "Mardi 14h : salle B\n" >> planning.txt
git commit -am "feat(planning): creneau du mardi"
printf "3 rallonges\n" >> materiel.txt
git commit -am "feat(materiel): ajout des rallonges"
