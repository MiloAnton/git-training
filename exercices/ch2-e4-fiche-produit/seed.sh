git init boutique
cd boutique
printf "Cafetiere italienne\nPrix : 24 euros\n" > fiche.txt
printf "Capacite : 6 tasses\n" > description.txt
git add .
git commit -m "feat(fiche): premiere fiche produit"
