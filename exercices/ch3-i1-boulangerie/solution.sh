git switch -c feature/pains-speciaux
printf "Pain aux noix\nPain de seigle\n" > pains.txt
git add pains.txt
git commit -m "feat(pains): carte des pains speciaux"
git switch main
git switch -c feature/allergenes
printf "Gluten, fruits a coque\n" > allergenes.txt
git add allergenes.txt
git commit -m "feat(allergenes): premiere fiche"
git switch main
git branch -v
