git init restaurant
cd restaurant
printf -- "- salade de chevre\n" > entrees.txt
printf -- "- poulet basquaise\n" > plats.txt
git add entrees.txt plats.txt
git commit -m "feat(menu): premier menu de la saison"
