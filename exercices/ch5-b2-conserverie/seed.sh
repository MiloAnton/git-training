git init conserverie
cd conserverie
printf "Bocaux 500 ml : 200\n" > bocaux.txt
git add bocaux.txt
git commit -m "feat(bocaux): stock de 500 ml"
printf "Bocaux 500 ml : 200\nBocaux 1 l : 120\n" > bocaux.txt
git commit -am "feat(bocaux): stock de 1 litre"
