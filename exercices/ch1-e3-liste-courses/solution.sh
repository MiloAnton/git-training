echo "- pain" >> courses.txt
git status
git add courses.txt
git commit -m "feat(courses): ajout du pain"
echo "- lait" >> courses.txt
git commit -am "feat(courses): ajout du lait"
git status
cat courses.txt
