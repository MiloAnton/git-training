git init --bare depot-serre.git
git clone https://github.com/leonis-formation/depot-serre.git amorce
cd amorce
printf "monstera\nficus\n" > catalogue.txt
git add catalogue.txt
git commit -m "feat(catalogue): premières plantes"
git push origin main
cd ..
rm -rf amorce
