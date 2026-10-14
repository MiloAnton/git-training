git init service
cd service
printf "port = 8080\nmode = production\ntimeout = 30\n" > config.txt
git add config.txt
git commit -m "feat(config): configuration initiale"
printf "port = 8080\nmode = debug\ntimeout = 3000\n" > config.txt
git commit -am "fix(config): passage en debug"
