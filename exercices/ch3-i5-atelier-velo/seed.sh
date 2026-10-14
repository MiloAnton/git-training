git init velo
cd velo
printf "Cles plates\n" > outils.txt
git add outils.txt
git commit -m "feat(outils): inventaire des outils"
git switch -c brouillon
printf "Reparation : changer les patins\n" > reparations.txt
git add reparations.txt
git commit -m "feat(reparations): premiere fiche"
git switch main
git switch -c essai
printf "idee abandonnee\n" > essai.txt
git add essai.txt
git commit -m "feat(essai): piste abandonnee"
git switch main
