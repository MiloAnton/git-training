echo "- velouté de potiron" >> entrees.txt
echo "- risotto aux champignons" >> plats.txt
echo "essai de mise en page" > test.txt
git add .
git status
git reset test.txt
git status
git commit -m "feat(menu): ajout du veloute et du risotto"
git status
