git init noel
cd noel
printf "Marche de Noel, place centrale\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): le marche"
git switch -c feature/chalets
printf "20 chalets en bois\n" > chalets.txt
git add chalets.txt
git commit -m "feat(chalets): nombre de chalets"
git switch main
printf "Marche de Noel, place centrale\nDu 1er au 24 decembre\n" > presentation.txt
git commit -am "feat(presentation): ajout des dates"
git switch -c fix/affiche
printf "Affiche A3, fond rouge\n" > affiche.txt
git add affiche.txt
git commit -m "fix(affiche): format et couleur"
git switch main
