const fs=require('fs');const G=require('./public/assets/gitleo.js');
const src=fs.readFileSync('conformance.js','utf8');
const M=eval(src.slice(src.indexOf('const MASQUES'),src.indexOf('function masque'))+'MASQUES');
const m=l=>{M.forEach(([r,p])=>l=l.replace(r,p));return l;};
const d='exercices/'+process.argv[2];
const seed=fs.existsSync(d+'/seed.sh')?fs.readFileSync(d+'/seed.sh','utf8'):'';
const vm=G.creerSession(seed);
const obt=G.jouer(vm,fs.readFileSync(d+'/solution.sh','utf8')).map(m);
const att=fs.readFileSync(d+'/exemple.txt','utf8').replace(/\n$/,'').split('\n');
for(let i=0;i<Math.max(att.length,obt.length);i++){
 if(att[i]!==obt[i]){for(let k=Math.max(0,i-2);k<=i+4;k++)console.log(' a['+k+'] '+JSON.stringify(att[k])+'\n o['+k+'] '+JSON.stringify(obt[k]));break;}}
