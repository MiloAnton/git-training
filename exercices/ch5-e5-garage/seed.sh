git init garage
cd garage
printf "Revision : 90 euros\n" > prestations.txt
git add prestations.txt
git commit -m "feat(prestations): revision"
printf "Revision : 90 euros\nVidange : 60 euros\n" > prestations.txt
git commit -am "feat(prestations): vidange"
git reset --hard HEAD~1
