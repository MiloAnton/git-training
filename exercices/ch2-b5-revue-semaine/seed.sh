git init equipe
cd equipe
printf "lundi : mise en route\n" > avancement.txt
git add avancement.txt
git commit -m "feat(avancement): point du lundi"
printf "Objectif : livrer la version 1\n" > objectifs.txt
git add objectifs.txt
git commit -m "feat(objectifs): objectif du trimestre"
printf "lundi : mise en route\nmercredi : premiers essais\n" > avancement.txt
git commit -am "feat(avancement): point du mercredi"
