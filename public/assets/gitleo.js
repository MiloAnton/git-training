/* gitleo.js - moteur Git pedagogique Leonis
   Reimplemente le modele objet de Git et un mini-shell, en reproduisant
   les messages du vrai Git. Fonctionne dans le navigateur et sous Node.
   Aucune dependance. */
(function (global) {
  'use strict';

  var RACINE = '/home/eleve';
  var GITHUB = 'https://github.com/leonis-formation/';

  // ------------------------------------------------------------- utilitaires

  function hash(texte) {
    var h1 = 0x811c9dc5, h2 = 0x01000193;
    for (var i = 0; i < texte.length; i++) {
      var c = texte.charCodeAt(i);
      h1 = (h1 ^ c) >>> 0;
      h1 = Math.imul(h1, 16777619) >>> 0;
      h2 = (h2 + Math.imul(c + i, 2654435761)) >>> 0;
    }
    var s = ('00000000' + h1.toString(16)).slice(-8) +
            ('00000000' + h2.toString(16)).slice(-8);
    return s.slice(0, 7);
  }

  function normalise(chemin) {
    var abs = chemin.charAt(0) === '/';
    var parts = chemin.split('/');
    var out = [];
    for (var i = 0; i < parts.length; i++) {
      var p = parts[i];
      if (p === '' || p === '.') continue;
      if (p === '..') { out.pop(); continue; }
      out.push(p);
    }
    return (abs ? '/' : '') + out.join('/');
  }

  function joindre(base, rel) {
    if (rel.charAt(0) === '/') return normalise(rel);
    return normalise(base + '/' + rel);
  }

  function relatif(base, chemin) {
    if (chemin === base) return '';
    if (chemin.indexOf(base + '/') === 0) return chemin.slice(base.length + 1);
    return chemin;
  }

  function trie(a) { return a.slice().sort(function (x, y) { return x < y ? -1 : x > y ? 1 : 0; }); }

  function titreMsg(m) { return String(m).split('\n')[0]; }

  function pluriel(n, mot) { return n + ' ' + mot + (n > 1 ? 's' : ''); }

  // ------------------------------------------------------- systeme de fichiers

  function VM() {
    this.cwd = RACINE;
    this.horloge = 0;   // avance d'un cran a chaque commande executee
    this.files = {};          // chemin absolu -> contenu
    this.dirs = {};           // chemin absolu -> true
    this.repos = {};          // racine absolue -> Repo
    this.dirs[RACINE] = true;
    this.dirs['/home'] = true;
    this.dirs['/'] = true;
  }

  VM.prototype.mkdirp = function (chemin) {
    var parts = chemin.split('/');
    var cur = '';
    for (var i = 1; i < parts.length; i++) {
      cur += '/' + parts[i];
      this.dirs[cur] = true;
    }
  };

  VM.prototype.ecrire = function (chemin, contenu) {
    var parent = chemin.slice(0, chemin.lastIndexOf('/'));
    this.mkdirp(parent);
    this.files[chemin] = contenu;
  };

  VM.prototype.existe = function (chemin) {
    return Object.prototype.hasOwnProperty.call(this.files, chemin) ||
           Object.prototype.hasOwnProperty.call(this.dirs, chemin);
  };

  VM.prototype.estDossier = function (chemin) {
    return Object.prototype.hasOwnProperty.call(this.dirs, chemin);
  };

  VM.prototype.supprimer = function (chemin) {
    delete this.files[chemin];
    var self = this;
    Object.keys(this.files).forEach(function (f) {
      if (f.indexOf(chemin + '/') === 0) delete self.files[f];
    });
    Object.keys(this.dirs).forEach(function (d) {
      if (d === chemin || d.indexOf(chemin + '/') === 0) delete self.dirs[d];
    });
    Object.keys(this.repos).forEach(function (r) {
      if (r === chemin || r.indexOf(chemin + '/') === 0) delete self.repos[r];
    });
  };

  VM.prototype.lister = function (chemin) {
    var noms = {};
    var prefixe = chemin === '/' ? '/' : chemin + '/';
    Object.keys(this.files).forEach(function (f) {
      if (f.indexOf(prefixe) === 0) {
        var reste = f.slice(prefixe.length);
        noms[reste.split('/')[0]] = true;
      }
    });
    Object.keys(this.dirs).forEach(function (d) {
      if (d.indexOf(prefixe) === 0) {
        var reste = d.slice(prefixe.length);
        if (reste) noms[reste.split('/')[0]] = true;
      }
    });
    return trie(Object.keys(noms));
  };

  // fichiers d'un depot, chemins relatifs a la racine, .git exclu
  VM.prototype.fichiersDe = function (racine) {
    var out = [];
    var prefixe = racine + '/';
    Object.keys(this.files).forEach(function (f) {
      if (f.indexOf(prefixe) !== 0) return;
      out.push(f.slice(prefixe.length));
    });
    return trie(out);
  };

  VM.prototype.depotPour = function (chemin) {
    var cur = chemin;
    while (true) {
      if (this.repos[cur]) return { racine: cur, repo: this.repos[cur] };
      if (cur === '/' || cur === '') return null;
      cur = cur.slice(0, cur.lastIndexOf('/')) || '/';
    }
  };

  // -------------------------------------------------------------------- depot

  function Repo(bare) {
    this.bare = !!bare;
    this.objets = {};                 // hash -> {type, ...}
    this.index = {};                  // chemin -> hash
    this.refs = {};                   // 'main' -> hash
    this.suivi = {};                  // 'origin/main' -> hash
    this.branche = 'main';
    this.remote = null;               // url
    this.compteur = 0;
  }

  Repo.prototype.tete = function () { return this.refs[this.branche] || null; };

  Repo.prototype.commit = function (h) { return h ? this.objets[h] : null; };

  Repo.prototype.arbreDe = function (h) {
    var c = this.commit(h);
    return c ? c.arbre : {};
  };

  Repo.prototype.ancetres = function (h) {
    var vus = {}, pile = h ? [h] : [];
    while (pile.length) {
      var x = pile.pop();
      if (!x || vus[x]) continue;
      vus[x] = true;
      var c = this.commit(x);
      if (c) (c.parents || []).forEach(function (p) { pile.push(p); });
    }
    return vus;
  };

  Repo.prototype.compte = function (de, borne) {
    var stop = this.ancetres(borne);
    var vus = {}, pile = de ? [de] : [], n = 0;
    while (pile.length) {
      var x = pile.pop();
      if (!x || vus[x] || stop[x]) continue;
      vus[x] = true; n++;
      var c = this.commit(x);
      if (c) (c.parents || []).forEach(function (p) { pile.push(p); });
    }
    return n;
  };

  Repo.prototype.base = function (a, b) {
    var aa = this.ancetres(a);
    var file = b ? [b] : [], vus = {};
    while (file.length) {
      var x = file.shift();
      if (!x || vus[x]) continue;
      vus[x] = true;
      if (aa[x]) return x;
      var c = this.commit(x);
      if (c) (c.parents || []).forEach(function (p) { file.push(p); });
    }
    return null;
  };

  Repo.prototype.nouveauCommit = function (arbre, parents, message, date) {
    this.compteur++;
    var cle = JSON.stringify(arbre) + '|' + parents.join(',') + '|' + message +
              '|' + this.compteur + '|' + date;
    var h = '';
    for (var k = 0; h.length < 40; k++) h += hash(cle + '#' + k);
    h = h.slice(0, 40);
    this.objets[h] = { type: 'commit', arbre: arbre, parents: parents,
                       message: message, date: date };
    return h;
  };

  function copieArbre(a) {
    var o = {};
    Object.keys(a).forEach(function (k) { o[k] = a[k]; });
    return o;
  }

  // ---------------------------------------------------------------- gitignore

  function motifsIgnore(vm, racine) {
    var contenu = vm.files[racine + '/.gitignore'];
    if (contenu === undefined) return [];
    var out = [];
    contenu.split('\n').forEach(function (ligne) {
      var l = ligne.trim();
      if (!l || l.charAt(0) === '#') return;
      var neg = false;
      if (l.charAt(0) === '!') { neg = true; l = l.slice(1); }
      var dossier = l.charAt(l.length - 1) === '/';
      if (dossier) l = l.slice(0, -1);
      var ancre = l.charAt(0) === '/';
      if (ancre) l = l.slice(1);
      var rx = '^' + l.split('').map(function (c) {
        if (c === '*') return '[^/]*';
        if (c === '?') return '[^/]';
        return c.replace(/[.+^${}()|[\]\\]/g, '\\$&');
      }).join('') + '$';
      out.push({ rx: new RegExp(rx), neg: neg, dossier: dossier, ancre: ancre });
    });
    return out;
  }

  function estIgnore(motifs, chemin) {
    var ignore = false;
    var segments = chemin.split('/');
    for (var i = 0; i < motifs.length; i++) {
      var m = motifs[i];
      var touche = false;
      if (m.ancre) {
        touche = m.dossier ? m.rx.test(segments[0]) && segments.length > 1
                           : m.rx.test(chemin);
      } else if (m.dossier) {
        for (var j = 0; j < segments.length - 1; j++) {
          if (m.rx.test(segments[j])) { touche = true; break; }
        }
      } else {
        for (var k = 0; k < segments.length; k++) {
          if (m.rx.test(segments[k])) { touche = true; break; }
        }
      }
      if (touche) ignore = !m.neg;
    }
    return ignore;
  }

  // ------------------------------------------------------------------- status

  function etat(vm, racine, repo) {
    var enConflit = repo.conflits || {};
    var motifs = motifsIgnore(vm, racine);
    var wd = {};
    vm.fichiersDe(racine).forEach(function (f) {
      wd[f] = hash(vm.files[racine + '/' + f]);
    });
    var tete = repo.tete();
    var arbre = repo.arbreDe(tete);
    var index = repo.index;

    var stage = [], nonStage = [], nonSuivis = [];

    Object.keys(index).concat(Object.keys(arbre)).forEach(function (f) { wd[f] = wd[f]; });

    var tous = {};
    [wd, index, arbre].forEach(function (m) {
      Object.keys(m).forEach(function (k) { tous[k] = true; });
    });

    trie(Object.keys(tous)).forEach(function (f) {
      if (enConflit[f]) return;
      var dansWd = Object.prototype.hasOwnProperty.call(wd, f) && wd[f] !== undefined;
      var dansIdx = Object.prototype.hasOwnProperty.call(index, f);
      var dansHead = Object.prototype.hasOwnProperty.call(arbre, f);

      if (dansIdx && !dansHead) stage.push({ etat: 'new file', f: f });
      else if (dansIdx && dansHead && index[f] !== arbre[f]) stage.push({ etat: 'modified', f: f });
      else if (!dansIdx && dansHead) stage.push({ etat: 'deleted', f: f });

      if (dansIdx && dansWd && wd[f] !== index[f]) nonStage.push({ etat: 'modified', f: f });
      else if (dansIdx && !dansWd) nonStage.push({ etat: 'deleted', f: f });

      // c'est l'index qui definit le suivi : un fichier retire de l'index
      // mais toujours sur le disque redevient non suivi
      if (!dansIdx && dansWd && !estIgnore(motifs, f)) nonSuivis.push(f);
    });

    // git regroupe un dossier entierement non suivi sous "dossier/"
    var groupes = [], vusDossiers = {};
    nonSuivis.forEach(function (f) {
      var i = f.indexOf('/');
      if (i === -1) { groupes.push(f); return; }
      var d = f.slice(0, i);
      var suiviDansDossier = Object.keys(index).concat(Object.keys(arbre))
        .some(function (k) { return k.indexOf(d + '/') === 0; });
      if (suiviDansDossier) { groupes.push(f); return; }
      if (!vusDossiers[d]) { vusDossiers[d] = true; groupes.push(d + '/'); }
    });

    return { stage: stage, nonStage: nonStage, nonSuivis: trie(groupes), wd: wd, arbre: arbre };
  }

  function ligneSuivi(repo) {
    if (!repo.remote) return null;
    var amont = repo.suivi['origin/' + repo.branche];
    if (amont === undefined) return null;
    var local = repo.tete();
    var avance = repo.compte(local, amont);
    var retard = repo.compte(amont, local);
    var nom = "'origin/" + repo.branche + "'";
    if (avance === 0 && retard === 0) {
      return ['Your branch is up to date with ' + nom + '.'];
    }
    if (avance > 0 && retard === 0) {
      return ['Your branch is ahead of ' + nom + ' by ' + pluriel(avance, 'commit') + '.',
              '  (use "git push" to publish your local commits)'];
    }
    if (avance === 0 && retard > 0) {
      return ['Your branch is behind ' + nom + ' by ' + pluriel(retard, 'commit') +
              ', and can be fast-forwarded.',
              '  (use "git pull" to update your local branch)'];
    }
    return ['Your branch and ' + nom + ' have diverged,',
            'and have ' + avance + ' and ' + retard + ' different commits each, respectively.',
            '  (use "git pull" if you want to integrate the remote branch with yours)'];
  }

  function rendStatus(vm, racine, repo) {
    var e = etat(vm, racine, repo);
    var sansCommit = !repo.tete();
    var out = ['On branch ' + repo.branche];

    if (sansCommit) out.push('', 'No commits yet', '');
    else {
      var t = ligneSuivi(repo);
      if (t) { out = out.concat(t); out.push(''); }
      if (repo.fusion) {
        if (repo.conflits && Object.keys(repo.conflits).length) {
          out.push('You have unmerged paths.',
                   '  (fix conflicts and run "git commit")',
                   '  (use "git merge --abort" to abort the merge)', '');
        } else {
          out.push('All conflicts fixed but you are still merging.',
                   '  (use "git commit" to conclude merge)', '');
        }
      }
    }

    var sections = [];
    if (e.stage.length) {
      var aide = sansCommit ? '  (use "git rm --cached <file>..." to unstage)'
                            : '  (use "git restore --staged <file>..." to unstage)';
      var s = repo.fusion ? ['Changes to be committed:']
                          : ['Changes to be committed:', aide];
      e.stage.forEach(function (x) { s.push('\t' + etiquette(x.etat) + x.f); });
      sections.push(s);
    }
    if (repo.conflits && Object.keys(repo.conflits).length) {
      var sc = ['Unmerged paths:', '  (use "git add <file>..." to mark resolution)'];
      trie(Object.keys(repo.conflits)).forEach(function (f) {
        sc.push(repo.conflits[f].genre === 'add/add'
                ? '\tboth added:      ' + f
                : '\tboth modified:   ' + f);
      });
      sections.push(sc);
    }
    if (e.nonStage.length) {
      var s2 = ['Changes not staged for commit:',
                '  (use "git add <file>..." to update what will be committed)',
                '  (use "git restore <file>..." to discard changes in working directory)'];
      e.nonStage.forEach(function (x) { s2.push('\t' + etiquette(x.etat) + x.f); });
      sections.push(s2);
    }
    if (e.nonSuivis.length) {
      var s3 = ['Untracked files:',
                '  (use "git add <file>..." to include in what will be committed)'];
      e.nonSuivis.forEach(function (f) { s3.push('\t' + f); });
      sections.push(s3);
    }

    sections.forEach(function (s, i) {
      if (i > 0) out.push('');
      out = out.concat(s);
    });

    var resume = null;
    if (repo.fusion && !(repo.conflits && Object.keys(repo.conflits).length)) {
      while (out.length && out[out.length - 1] === '') out.pop();
      return out;
    }
    if (repo.conflits && Object.keys(repo.conflits).length) {
      resume = 'no changes added to commit (use "git add" and/or "git commit -a")';
      if (sections.length) out.push('');
      out.push(resume);
      return out;
    }
    if (!e.stage.length) {
      if (e.nonStage.length) resume = 'no changes added to commit (use "git add" and/or "git commit -a")';
      else if (e.nonSuivis.length) resume = 'nothing added to commit but untracked files present (use "git add" to track)';
      else resume = 'nothing to commit, working tree clean';
    }
    if (resume) {
      if (sections.length) out.push('');
      out.push(resume);
    }
    return out;
  }

  function etiquette(e) {
    if (e === 'new file') return 'new file:   ';
    if (e === 'modified') return 'modified:   ';
    if (e === 'deleted') return 'deleted:    ';
    return e + ': ';
  }

  // ------------------------------------------------------------------ diffstat

  function lignesDe(t) {
    if (t === undefined || t === '') return [];
    var l = t.split('\n');
    if (l[l.length - 1] === '') l.pop();
    return l;
  }

  function statDe(vm, racine, repo, avant, apres) {
    var fichiers = {};
    Object.keys(avant).concat(Object.keys(apres)).forEach(function (f) { fichiers[f] = true; });
    var details = [], ajouts = 0, retraits = 0, crees = [], supprimes = [];
    trie(Object.keys(fichiers)).forEach(function (f) {
      var a = avant[f], b = apres[f];
      if (a === b) return;
      var ta = a === undefined ? '' : (repo.blobs && repo.blobs[a] !== undefined ? repo.blobs[a] : '');
      var tb = b === undefined ? '' : (repo.blobs && repo.blobs[b] !== undefined ? repo.blobs[b] : '');
      var la = lignesDe(ta).length, lb = lignesDe(tb).length;
      var plus, moins;
      if (a === undefined) { plus = lb; moins = 0; crees.push(f); }
      else if (b === undefined) { plus = 0; moins = la; supprimes.push(f); }
      else { plus = Math.max(0, lb - la) || (lb === la ? lb : 0); moins = Math.max(0, la - lb); if (lb === la) { plus = lb; moins = la; } }
      ajouts += plus; retraits += moins;
      details.push({ f: f, n: plus + moins, plus: plus, moins: moins });
    });
    return { details: details, ajouts: ajouts, retraits: retraits, crees: crees, supprimes: supprimes };
  }

  function rendStat(st, avecDetail) {
    var out = [];
    var largeur = 0, maxN = 0;
    st.details.forEach(function (d) {
      if (d.f.length > largeur) largeur = d.f.length;
      if (String(d.n).length > maxN) maxN = String(d.n).length;
    });
    if (avecDetail) {
      st.details.forEach(function (d) {
        var nom = d.f + Array(largeur - d.f.length + 1).join(' ');
        var n = Array(maxN - String(d.n).length + 1).join(' ') + d.n;
        out.push(' ' + nom + ' | ' + n + ' ' +
                 Array(d.plus + 1).join('+') + Array(d.moins + 1).join('-'));
      });
    }
    var parts = [pluriel(st.details.length, 'file') + ' changed'];
    if (st.ajouts) parts.push(pluriel(st.ajouts, 'insertion') + '(+)');
    if (st.retraits) parts.push(pluriel(st.retraits, 'deletion') + '(-)');
    out.push(' ' + parts.join(', '));
    st.crees.forEach(function (f) { out.push(' create mode 100644 ' + f); });
    st.supprimes.forEach(function (f) { out.push(' delete mode 100644 ' + f); });
    return out;
  }

  // -------------------------------------------------------------------- shell

  function decoupe(ligne) {
    var out = [], cur = '', q = null, i;
    for (i = 0; i < ligne.length; i++) {
      var c = ligne.charAt(i);
      if (q) {
        if (c === q) { q = null; continue; }
        cur += c;
        continue;
      }
      if (c === '"' || c === "'") { q = c; cur += '\u0000'; continue; }
      if (c === ' ' || c === '\t') { if (cur !== '') { out.push(cur); cur = ''; } continue; }
      if (c === '>' ) {
        if (cur !== '') { out.push(cur); cur = ''; }
        if (ligne.charAt(i + 1) === '>') { out.push('>>'); i++; } else { out.push('>'); }
        continue;
      }
      cur += c;
    }
    if (cur !== '') out.push(cur);
    return out.map(function (t) { return t.replace(/\u0000/g, ''); });
  }

  function brut(ligne) {
    // conserve l'information de citation pour printf/echo
    var out = [], cur = '', cite = false, q = null, i;
    function pousse() { if (cur !== '' || cite) { out.push({ t: cur, cite: cite }); cur = ''; cite = false; } }
    for (i = 0; i < ligne.length; i++) {
      var c = ligne.charAt(i);
      if (q) { if (c === q) { q = null; continue; } cur += c; continue; }
      if (c === '"' || c === "'") { q = c; cite = true; continue; }
      if (c === ' ' || c === '\t') { pousse(); continue; }
      if (c === '>') {
        pousse();
        if (ligne.charAt(i + 1) === '>') { out.push({ t: '>>', op: true }); i++; }
        else out.push({ t: '>', op: true });
        continue;
      }
      cur += c;
    }
    pousse();
    return out;
  }

  function echappe(s) {
    return s.replace(/\\n/g, '\n').replace(/\\t/g, '\t').replace(/\\\\/g, '\\');
  }

  // --------------------------------------------------------------------- git

  function Resultat() { this.lignes = []; this.code = 0; }
  Resultat.prototype.dire = function () {
    for (var i = 0; i < arguments.length; i++) {
      var a = arguments[i];
      if (Array.isArray(a)) this.lignes = this.lignes.concat(a);
      else this.lignes.push(a);
    }
  };

  function blobs(repo) { if (!repo.blobs) repo.blobs = {}; return repo.blobs; }

  function enregistreBlob(repo, contenu) {
    var h = hash(contenu);
    blobs(repo)[h] = contenu;
    return h;
  }

  function cheminsCibles(vm, racine, repo, args) {
    var motifs = motifsIgnore(vm, racine);
    var out = [];
    args.forEach(function (a) {
      var abs = joindre(vm.cwd, a);
      var rel = relatif(racine, abs);
      if (a === '.' || a === '' || rel === '') {
        vm.fichiersDe(racine).forEach(function (f) {
          if (!estIgnore(motifs, f)) out.push(f);
        });
        Object.keys(repo.index).forEach(function (f) {
          if (vm.files[racine + '/' + f] === undefined) out.push(f);
        });
        return;
      }
      if (vm.files[abs] !== undefined) { out.push(rel); return; }
      if (vm.estDossier(abs)) {
        vm.fichiersDe(racine).forEach(function (f) {
          if (f.indexOf(rel + '/') === 0 && !estIgnore(motifs, f)) out.push(f);
        });
        return;
      }
      out.push(rel);
    });
    var vus = {}, res = [];
    out.forEach(function (f) { if (!vus[f]) { vus[f] = true; res.push(f); } });
    return trie(res);
  }

  var GIT = {};

  GIT.init = function (vm, args, r) {
    var bare = args.indexOf('--bare') !== -1;
    var reste = args.filter(function (a) { return a.charAt(0) !== '-'; });
    var nom = reste[0];
    var cible = nom ? joindre(vm.cwd, nom) : vm.cwd;
    vm.mkdirp(cible);
    vm.repos[cible] = new Repo(bare);
    r.dire('Initialized empty Git repository in ' + cible + (bare ? '/' : '/.git/'));
  };

  GIT.status = function (vm, args, r, ctx) {
    r.dire(rendStatus(vm, ctx.racine, ctx.repo));
  };

  GIT.add = function (vm, args, r, ctx) {
    var repo = ctx.repo, racine = ctx.racine;
    var cibles = args.filter(function (a) { return a.charAt(0) !== '-'; });
    if (args.indexOf('-A') !== -1 || args.indexOf('--all') !== -1) cibles = ['.'];
    if (!cibles.length) { r.dire('Nothing specified, nothing added.'); r.code = 1; return; }
    var fichiers = cheminsCibles(vm, racine, repo, cibles);
    var arbre = repo.arbreDe(repo.tete());
    var trouve = false;
    fichiers.forEach(function (f) {
      var contenu = vm.files[racine + '/' + f];
      if (contenu === undefined) {
        if (repo.index[f] !== undefined || arbre[f] !== undefined) { delete repo.index[f]; trouve = true; }
        return;
      }
      repo.index[f] = enregistreBlob(repo, contenu);
      if (repo.conflits && repo.conflits[f]) {
        delete repo.conflits[f];
        if (!Object.keys(repo.conflits).length) repo.conflits = null;
      }
      trouve = true;
    });
    if (!trouve) {
      r.dire("fatal: pathspec '" + cibles[0] + "' did not match any files");
      r.code = 1;
    }
  };

  GIT.reset = function (vm, args, r, ctx) {
    var repo = ctx.repo, racine = ctx.racine;
    var cibles = args.filter(function (a) { return a.charAt(0) !== '-'; });
    var arbre = repo.arbreDe(repo.tete());
    if (!cibles.length) {
      Object.keys(repo.index).forEach(function (f) { delete repo.index[f]; });
      Object.keys(arbre).forEach(function (f) { repo.index[f] = arbre[f]; });
      return;
    }
    cibles.forEach(function (a) {
      var abs = joindre(vm.cwd, a);
      var rel = relatif(racine, abs);
      var touches = Object.keys(repo.index).filter(function (f) {
        return f === rel || f.indexOf(rel + '/') === 0;
      });
      if (!touches.length) touches = [rel];
      touches.forEach(function (f) {
        if (arbre[f] !== undefined) repo.index[f] = arbre[f];
        else delete repo.index[f];
      });
    });
  };

  GIT.rm = function (vm, args, r, ctx) {
    var repo = ctx.repo, racine = ctx.racine;
    var cache = args.indexOf('--cached') !== -1;
    var cibles = args.filter(function (a) { return a.charAt(0) !== '-'; });
    cibles.forEach(function (a) {
      var abs = joindre(vm.cwd, a);
      var rel = relatif(racine, abs);
      delete repo.index[rel];
      if (!cache) vm.supprimer(abs);
      r.dire("rm '" + rel + "'");
    });
  };

  GIT.commit = function (vm, args, r, ctx) {
    var repo = ctx.repo, racine = ctx.racine;
    var message = null, tout = false, amend = false;
    for (var i = 0; i < args.length; i++) {
      var a = args[i];
      if (a === '-m') { message = args[i + 1]; i++; }
      else if (a === '-am' || a === '-ma') { tout = true; message = args[i + 1]; i++; }
      else if (a === '-a') tout = true;
      else if (a === '--amend') amend = true;
    }
    if (tout) {
      var arbreA = repo.arbreDe(repo.tete());
      Object.keys(repo.index).concat(Object.keys(arbreA)).forEach(function (f) {
        var contenu = vm.files[racine + '/' + f];
        if (contenu === undefined) delete repo.index[f];
        else repo.index[f] = enregistreBlob(repo, contenu);
      });
    }
    // un commit qui termine une fusion en conflit
    if (repo.fusion && !amend) {
      if (repo.conflits && Object.keys(repo.conflits).length) {
        r.dire('error: Committing is not possible because you have unmerged files.',
               "hint: Fix them up in the work tree, and then use 'git add/rm <file>'",
               'hint: as appropriate to mark resolution and make a commit.',
               'fatal: Exiting because of an unresolved conflict.');
        r.code = 1; return;
      }
      var arbreFin = copieArbre(repo.index);
      var msgFin = message !== null ? message : "Merge branch '" + repo.fusion.nom + "'";
      var localF = repo.tete();
      var avantF = contenusDe(repo, localF);
      var hF = repo.nouveauCommit(arbreFin, [localF, repo.fusion.cible], msgFin,
                                  vm.horloge);
      repo.refs[repo.branche] = hF;
      appliqueCommit(vm, racine, repo, hF);
      note(repo, 'commit (merge): ' + msgFin);
      repo.fusion = null; repo.conflits = null;
      r.dire('[' + repo.branche + ' ' + hF.slice(0, 7) + '] ' + msgFin);
      return;
    }
    if (amend) {
      var ancien = repo.tete();
      if (!ancien) { r.dire('fatal: You have nothing to amend.'); r.code = 1; return; }
      var ca = repo.commit(ancien);
      var msgA = message !== null ? message : ca.message;
      var arbreA = copieArbre(repo.index);
      var baseA = ca.parents.length ? contenusDe(repo, ca.parents[0]) : {};
      var hA = repo.nouveauCommit(arbreA, ca.parents, msgA, ca.date);
      repo.refs[repo.branche] = hA;
      note(repo, 'commit (amend): ' + msgA);
      var racineA = ca.parents.length ? '' : '(root-commit) ';
      r.dire('[' + repo.branche + ' ' + racineA + hA.slice(0, 7) + '] ' + msgA);
      r.dire(' Date: ' + dateDe(ca.date));
      r.dire(resumeCommit(diffEnsembles(baseA, contenusDe(repo, hA), [])));
      return;
    }
    if (message === null) {
      r.dire('fatal: no commit message supplied'); r.code = 1; return;
    }
    var tete = repo.tete();
    var arbre = repo.arbreDe(tete);
    var memeChose = Object.keys(arbre).length === Object.keys(repo.index).length &&
      Object.keys(repo.index).every(function (f) { return arbre[f] === repo.index[f]; });
    if (memeChose) {
      r.dire(rendStatus(vm, racine, repo));
      r.code = 1;
      return;
    }
    var nouveau = copieArbre(repo.index);
    var avantC = contenusDe(repo, tete);
    var h = repo.nouveauCommit(nouveau, tete ? [tete] : [], message, vm.horloge);
    repo.refs[repo.branche] = h;
    var racineTxt = tete ? '' : '(root-commit) ';
    note(repo, 'commit' + (tete ? '' : ' (initial)') + ': ' + message);
    r.dire('[' + repo.branche + ' ' + racineTxt + h.slice(0, 7) + '] ' + message);
    r.dire(resumeCommit(diffEnsembles(avantC, contenusDe(repo, h), [])));
  };

  GIT.clone = function (vm, args, r, ctx) {
    var reste = args.filter(function (a) { return a.charAt(0) !== '-'; });
    var url = reste[0];
    var nom = reste[1] || url.replace(/\/$/, '').split('/').pop().replace(/\.git$/, '');
    var source = vm.repos[urlVersChemin(vm, url)];
    if (!source) { r.dire("fatal: repository '" + url + "' does not exist"); r.code = 1; return; }
    var cible = joindre(vm.cwd, nom);
    r.dire("Cloning into '" + nom + "'...");
    var copie = new Repo(false);
    copie.objets = JSON.parse(JSON.stringify(source.objets));
    copie.blobs = JSON.parse(JSON.stringify(source.blobs || {}));
    copie.branche = source.branche;
    copie.refs[source.branche] = source.refs[source.branche];
    copie.suivi['origin/' + source.branche] = source.refs[source.branche];
    copie.remote = url;
    vm.mkdirp(cible);
    vm.repos[cible] = copie;
    var arbre = copie.arbreDe(copie.tete());
    Object.keys(arbre).forEach(function (f) {
      copie.index[f] = arbre[f];
      vm.ecrire(cible + '/' + f, copie.blobs[arbre[f]]);
    });
    r.dire('done.');
  };

  function urlVersChemin(vm, url) {
    if (url.indexOf(GITHUB) === 0) {
      return joindre(RACINE, url.slice(GITHUB.length));
    }
    return joindre(vm.cwd, url);
  }

  function cheminVersUrl(chemin) {
    var nom = chemin.split('/').pop();
    return GITHUB + nom;
  }

  GIT.push = function (vm, args, r, ctx) {
    var repo = ctx.repo;
    var url = repo.remote;
    if (!url) { r.dire('fatal: No configured push destination.'); r.code = 1; return; }
    var distant = vm.repos[urlVersChemin(vm, url)];
    var local = repo.tete();
    var amont = distant.refs[repo.branche];
    r.dire('To ' + url);
    if (amont === local) { r.lignes.pop(); r.dire('Everything up-to-date'); return; }
    var descend = repo.ancetres(local)[amont] || amont === undefined;
    if (!descend) {
      var enRetard = repo.ancetres(amont) && repo.ancetres(amont)[local];
      var motif = enRetard ? 'non-fast-forward' : 'fetch first';
      r.dire(' ! [rejected]        ' + repo.branche + ' -> ' + repo.branche + ' (' + motif + ')');
      r.dire("error: failed to push some refs to '" + url + "'");
      if (enRetard) {
        r.dire('hint: Updates were rejected because the tip of your current branch is behind',
               'hint: its remote counterpart. If you want to integrate the remote changes,',
               "hint: use 'git pull' before pushing again.");
      } else {
        r.dire('hint: Updates were rejected because the remote contains work that you do not',
               'hint: have locally. This is usually caused by another repository pushing to',
               "hint: the same ref. If you want to integrate the remote changes, use",
               "hint: 'git pull' before pushing again.");
      }
      r.dire("hint: See the 'Note about fast-forwards' in 'git push --help' for details.");
      r.code = 1;
      return;
    }
    distant.objets = JSON.parse(JSON.stringify(repo.objets));
    distant.blobs = JSON.parse(JSON.stringify(repo.blobs || {}));
    distant.refs[repo.branche] = local;
    distant.branche = repo.branche;
    repo.suivi['origin/' + repo.branche] = local;
    if (amont === undefined) {
      r.dire(' * [new branch]      ' + repo.branche + ' -> ' + repo.branche);
    } else {
      r.dire('   ' + amont.slice(0, 7) + '..' + local.slice(0, 7) + '  ' + repo.branche + ' -> ' + repo.branche);
    }
  };

  GIT.pull = function (vm, args, r, ctx) {
    var repo = ctx.repo, racine = ctx.racine;
    var url = repo.remote;
    var distant = vm.repos[urlVersChemin(vm, url)];
    var avant = repo.suivi['origin/' + repo.branche];
    var cible = distant.refs[repo.branche];
    var local = repo.tete();

    if (cible !== avant) {
      r.dire('From ' + url);
      r.dire('   ' + String(avant).slice(0, 7) + '..' + cible.slice(0, 7) + '  ' +
             repo.branche + '       -> origin/' + repo.branche);
      Object.keys(distant.objets).forEach(function (k) { repo.objets[k] = distant.objets[k]; });
      Object.keys(distant.blobs || {}).forEach(function (k) { blobs(repo)[k] = distant.blobs[k]; });
      repo.suivi['origin/' + repo.branche] = cible;
    }

    if (cible === local || repo.ancetres(local)[cible]) {
      r.dire('Already up to date.');
      return;
    }
    if (args.indexOf('--rebase') !== -1) {
      rejoue(vm, racine, repo, cible, 'origin/' + repo.branche, r);
      return;
    }
    var arbreAvant = repo.arbreDe(local);
    if (!local || repo.ancetres(cible)[local]) {
      repo.refs[repo.branche] = cible;
      var arbreFF = repo.arbreDe(cible);
      appliqueArbre(vm, racine, repo, arbreFF);
      r.dire('Updating ' + String(local).slice(0, 7) + '..' + cible.slice(0, 7), 'Fast-forward');
      var eFF = diffEnsembles(contenusDe(repo, local), contenusDe(repo, cible), []);
      r.dire(rendDiffStat(eFF));
      r.dire(modesCrees(eFF));
      return;
    }
    // fusion a trois points
    var base = repo.base(local, cible);
    var aB = repo.arbreDe(base), aL = arbreAvant, aD = repo.arbreDe(cible);
    var fusion = {}, conflits = [];
    var noms = {};
    [aB, aL, aD].forEach(function (m) { Object.keys(m).forEach(function (k) { noms[k] = true; }); });
    trie(Object.keys(noms)).forEach(function (f) {
      var b = aB[f], l = aL[f], d = aD[f];
      if (l === d) { if (l !== undefined) fusion[f] = l; return; }
      if (l === b) { if (d !== undefined) fusion[f] = d; return; }
      if (d === b) { if (l !== undefined) fusion[f] = l; return; }
      conflits.push(f);
      fusion[f] = l;
    });
    if (conflits.length) {
      conflits.forEach(function (f) { r.dire('Auto-merging ' + f); });
      conflits.forEach(function (f) { r.dire('CONFLICT (content): Merge conflict in ' + f); });
      r.dire('Automatic merge failed; fix conflicts and then commit the result.');
      r.code = 1;
      return;
    }
    var msg = "Merge branch '" + repo.branche + "' of " + url.replace(/\.git$/, '') +
              ' into ' + repo.branche;
    var h = repo.nouveauCommit(fusion, [local, cible], msg, vm.horloge);
    repo.refs[repo.branche] = h;
    Object.keys(fusion).forEach(function (f) { repo.index[f] = fusion[f]; });
    appliqueArbre(vm, racine, repo, fusion);
    r.dire("Merge made by the 'ort' strategy.");
    var eM = diffEnsembles(contenusDe(repo, local), contenusDe(repo, h), []);
    r.dire(rendDiffStat(eM));
    r.dire(modesCrees(eM));
  };

  function appliqueArbre(vm, racine, repo, arbre) {
    var actuels = vm.fichiersDe(racine);
    actuels.forEach(function (f) {
      if (arbre[f] === undefined && repo.index[f] !== undefined) {
        vm.supprimer(racine + '/' + f);
      }
    });
    Object.keys(arbre).forEach(function (f) {
      vm.ecrire(racine + '/' + f, blobs(repo)[arbre[f]]);
      repo.index[f] = arbre[f];
    });
  }

  // =================================================== chapitre 2 : historique

  var JOURS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  var MOIS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  // Le 5 janvier 2026 est un lundi. Chaque commande executee avance
  // l'horloge de 7 minutes, comme le fait le generateur.
  function dateDe(n) {
    var total = 9 * 60 + n * 7;
    var h = Math.floor(total / 60), m = total % 60;
    return JOURS[1] + ' ' + MOIS[0] + ' 5 ' +
      ('0' + h).slice(-2) + ':' + ('0' + m).slice(-2) + ':00 2026 +0100';
  }

  function lignes(t) {
    if (t === undefined || t === null || t === '') return [];
    var l = t.split('\n');
    if (l[l.length - 1] === '') l.pop();
    return l;
  }

  // plus longue sous-sequence commune, suffisant pour des fichiers de TP
  function diffLignes(a, b) {
    var n = a.length, m = b.length;
    var dp = [];
    for (var i = 0; i <= n; i++) {
      dp.push(new Array(m + 1).fill(0));
    }
    for (i = n - 1; i >= 0; i--) {
      for (var j = m - 1; j >= 0; j--) {
        dp[i][j] = a[i] === b[j] ? dp[i + 1][j + 1] + 1
                                 : Math.max(dp[i + 1][j], dp[i][j + 1]);
      }
    }
    var out = [];
    i = 0; j = 0;
    while (i < n && j < m) {
      if (a[i] === b[j]) { out.push({ t: ' ', l: a[i] }); i++; j++; }
      else if (dp[i + 1][j] >= dp[i][j + 1]) { out.push({ t: '-', l: a[i] }); i++; }
      else { out.push({ t: '+', l: b[j] }); j++; }
    }
    while (i < n) { out.push({ t: '-', l: a[i] }); i++; }
    while (j < m) { out.push({ t: '+', l: b[j] }); j++; }
    return out;
  }

  function hunks(ops, contexte) {
    var groupes = [], courant = null;
    var posA = 0, posB = 0;
    var marques = [];
    ops.forEach(function (o) {
      marques.push({ o: o, a: posA, b: posB });
      if (o.t === ' ') { posA++; posB++; }
      else if (o.t === '-') posA++;
      else posB++;
    });
    var changes = [];
    marques.forEach(function (x, k) { if (x.o.t !== ' ') changes.push(k); });
    if (!changes.length) return [];
    changes.forEach(function (k) {
      if (courant && k - courant.fin - 1 <= contexte * 2) { courant.fin = k; return; }
      courant = { debut: k, fin: k };
      groupes.push(courant);
    });
    return groupes.map(function (g) {
      var d = Math.max(0, g.debut - contexte);
      var f = Math.min(marques.length - 1, g.fin + contexte);
      var corps = [], aDeb = null, bDeb = null, aLen = 0, bLen = 0;
      for (var k = d; k <= f; k++) {
        var x = marques[k];
        if (aDeb === null) { aDeb = x.a; bDeb = x.b; }
        corps.push(x.o.t + x.o.l);
        if (x.o.t === ' ') { aLen++; bLen++; }
        else if (x.o.t === '-') aLen++;
        else bLen++;
      }
      return { aDeb: aDeb, bDeb: bDeb, aLen: aLen, bLen: bLen, corps: corps };
    });
  }

  function portee(debut, longueur) {
    // git ecrit "-1,3" mais "-1" quand la portee tient sur une ligne
    var d = longueur === 0 ? debut : debut + 1;
    return longueur === 1 ? String(d) : d + ',' + longueur;
  }

  // git affiche apres @@ la derniere ligne au-dessus du bloc qui ressemble
  // a un debut de section : par defaut, une ligne commencant par une lettre
  function contexteFonction(lignesA, debut) {
    for (var i = debut - 1; i >= 0; i--) {
      if (/^[A-Za-z$_]/.test(lignesA[i])) return ' ' + lignesA[i];
    }
    return '';
  }

  function diffFichier(chemin, avant, apres) {
    if (avant === apres) return [];
    var out = ['diff --git a/' + chemin + ' b/' + chemin];
    var hAvant = avant === undefined ? '0000000' : hash(avant);
    var hApres = apres === undefined ? '0000000' : hash(apres);
    if (avant === undefined) out.push('new file mode 100644');
    else if (apres === undefined) out.push('deleted file mode 100644');
    var mode = (avant === undefined || apres === undefined) ? '' : ' 100644';
    out.push('index ' + hAvant + '..' + hApres + mode);
    out.push('--- ' + (avant === undefined ? '/dev/null' : 'a/' + chemin));
    out.push('+++ ' + (apres === undefined ? '/dev/null' : 'b/' + chemin));
    var la = lignes(avant);
    var ops = diffLignes(la, lignes(apres));
    hunks(ops, 3).forEach(function (h) {
      out.push('@@ -' + portee(h.aDeb, h.aLen) + ' +' + portee(h.bDeb, h.bLen) +
               ' @@' + contexteFonction(la, h.aDeb));
      h.corps.forEach(function (c) { out.push(c); });
    });
    return out;
  }

  function comptesDiff(avant, apres) {
    var plus = 0, moins = 0;
    diffLignes(lignes(avant), lignes(apres)).forEach(function (o) {
      if (o.t === '+') plus++;
      else if (o.t === '-') moins++;
    });
    return { plus: plus, moins: moins };
  }

  // compare deux ensembles {chemin: contenu}
  function diffEnsembles(avant, apres, filtres) {
    var noms = {};
    [avant, apres].forEach(function (m) {
      Object.keys(m).forEach(function (k) { noms[k] = true; });
    });
    var liste = trie(Object.keys(noms));
    if (filtres && filtres.length) {
      liste = liste.filter(function (f) {
        return filtres.some(function (p) { return f === p || f.indexOf(p + '/') === 0; });
      });
    }
    var res = [];
    liste.forEach(function (f) {
      if (avant[f] === apres[f]) return;
      var c = comptesDiff(avant[f], apres[f]);
      res.push({ f: f, avant: avant[f], apres: apres[f], plus: c.plus, moins: c.moins });
    });
    return res;
  }

  function rendDiffStat(entrees) {
    if (!entrees.length) return [];
    var out = [];
    var largeur = 0, maxN = 0, totalPlus = 0, totalMoins = 0;
    entrees.forEach(function (e) {
      if (e.f.length > largeur) largeur = e.f.length;
      var n = e.plus + e.moins;
      if (String(n).length > maxN) maxN = String(n).length;
      totalPlus += e.plus; totalMoins += e.moins;
    });
    entrees.forEach(function (e) {
      var n = e.plus + e.moins;
      var nom = e.f + Array(largeur - e.f.length + 1).join(' ');
      var num = Array(maxN - String(n).length + 1).join(' ') + n;
      out.push(' ' + nom + ' | ' + num + ' ' +
               Array(e.plus + 1).join('+') + Array(e.moins + 1).join('-'));
    });
    var parts = [pluriel(entrees.length, 'file') + ' changed'];
    if (totalPlus) parts.push(pluriel(totalPlus, 'insertion') + '(+)');
    if (totalMoins) parts.push(pluriel(totalMoins, 'deletion') + '(-)');
    out.push(' ' + parts.join(', '));
    return out;
  }

  // ------------------------------------------------------------- references

  function resoudre(repo, ref) {
    if (!ref) return repo.tete();
    var jr = /^HEAD@\{(\d+)\}$/.exec(ref);
    if (jr) {
      var e = journal(repo)[parseInt(jr[1], 10)];
      return e ? e.h : null;
    }
    var m = /^(.*?)(([~^])(\d*))?$/.exec(ref);
    var base = ref, pas = 0;
    var mm = /^(.+?)((~|\^)(\d*))$/.exec(ref);
    if (mm) {
      base = mm[1];
      pas = mm[3] === '^' ? (mm[4] === '' ? 1 : parseInt(mm[4], 10))
                          : (mm[4] === '' ? 1 : parseInt(mm[4], 10));
    }
    var h = null;
    if (base === 'HEAD') h = repo.tete();
    else if (repo.refs[base] !== undefined) h = repo.refs[base];
    else if (repo.suivi[base] !== undefined) h = repo.suivi[base];
    else if (repo.objets[base]) h = base;
    else {
      var trouve = Object.keys(repo.objets).filter(function (k) {
        return k.indexOf(base) === 0;
      });
      if (trouve.length === 1) h = trouve[0];
    }
    for (var i = 0; i < pas && h; i++) {
      var c = repo.commit(h);
      h = c && c.parents.length ? c.parents[0] : null;
    }
    return h;
  }

  function contenusDe(repo, h) {
    var arbre = repo.arbreDe(h), out = {};
    Object.keys(arbre).forEach(function (f) { out[f] = blobs(repo)[arbre[f]]; });
    return out;
  }

  function contenusIndex(repo) {
    var out = {};
    Object.keys(repo.index).forEach(function (f) { out[f] = blobs(repo)[repo.index[f]]; });
    return out;
  }

  function contenusWD(vm, racine, repo) {
    var out = {};
    Object.keys(repo.index).forEach(function (f) {
      var c = vm.files[racine + '/' + f];
      if (c !== undefined) out[f] = c;
    });
    return out;
  }

  // --------------------------------------------------------------- commandes

  function commitsAccessibles(repo, depuis) {
    var vus = {}, pile = depuis.slice(), liste = [];
    while (pile.length) {
      var h = pile.pop();
      if (!h || vus[h]) continue;
      vus[h] = true;
      var c = repo.commit(h);
      if (!c) continue;
      liste.push({ h: h, c: c });
      c.parents.forEach(function (p) { pile.push(p); });
    }
    liste.sort(function (x, y) {
      if (y.c.date !== x.c.date) return y.c.date - x.c.date;
      return x.h < y.h ? 1 : -1;
    });
    return liste;
  }

  function entetesCommit(repo, h, c, decorer) {
    var deco = '';
    if (decorer) {
      var noms = [];
      if (repo.refs[repo.branche] === h) noms.push('HEAD -> ' + repo.branche);
      Object.keys(repo.refs).forEach(function (b) {
        if (b !== repo.branche && repo.refs[b] === h) noms.push(b);
      });
      Object.keys(repo.suivi).forEach(function (b) {
        if (repo.suivi[b] === h) noms.push(b);
      });
      if (noms.length) deco = ' (' + noms.join(', ') + ')';
    }
    var tete = ['commit ' + h + deco];
    if (c.parents.length > 1) {
      tete.push('Merge: ' + c.parents.map(function (p) {
        return p.slice(0, 7);
      }).join(' '));
    }
    return tete.concat([
            'Author: Eleve Leonis <eleve@leonis.fr>',
            'Date:   ' + dateDe(c.date),
            ''].concat(String(c.message).split('\n').map(function (l) {
              return '    ' + l;
            })));
  }

  GIT.log = function (vm, args, r, ctx) {
    var repo = ctx.repo;
    var oneline = false, graph = false, decorer = false, tous = false;
    var stat = false, patch = false, limite = null, chemins = [], refs = [];
    for (var i = 0; i < args.length; i++) {
      var a = args[i];
      if (a === '--oneline') oneline = true;
      else if (a === '--graph') graph = true;
      else if (a === '--decorate') decorer = true;
      else if (a === '--all') tous = true;
      else if (a === '--stat') stat = true;
      else if (a === '-p' || a === '--patch') patch = true;
      else if (a === '-n') { limite = parseInt(args[i + 1], 10); i++; }
      else if (/^-\d+$/.test(a)) limite = parseInt(a.slice(1), 10);
      else if (a === '--') { chemins = args.slice(i + 1); break; }
      else if (a.charAt(0) !== '-') refs.push(a);
    }
    var depuis = [];
    if (tous) {
      Object.keys(repo.refs).forEach(function (b) { depuis.push(repo.refs[b]); });
      Object.keys(repo.suivi).forEach(function (b) { depuis.push(repo.suivi[b]); });
    } else if (refs.length) {
      refs.forEach(function (x) { depuis.push(resoudre(repo, x)); });
    } else depuis.push(repo.tete());

    if (!depuis.filter(Boolean).length) {
      r.dire("fatal: your current branch '" + repo.branche +
             "' does not have any commits yet");
      r.code = 1;
      return;
    }
    var liste = commitsAccessibles(repo, depuis.filter(Boolean));
    if (chemins.length) {
      liste = liste.filter(function (x) {
        var apres = contenusDe(repo, x.h);
        var avant = x.c.parents.length ? contenusDe(repo, x.c.parents[0]) : {};
        return diffEnsembles(avant, apres, chemins).length > 0;
      });
    }
    if (limite !== null) liste = liste.slice(0, limite);

    var out = [];
    if (oneline && graph) {
      artGraphe(repo, liste).forEach(function (l) {
        if (l.commit) out.push(l.art + ' ' + l.commit.h.slice(0, 7) + ' ' + titreMsg(l.commit.c.message));
        else out.push(l.art);
      });
      r.dire(out);
      return;
    }
    liste.forEach(function (x, k) {
      if (oneline) {
        out.push((graph ? '* ' : '') + x.h.slice(0, 7) + ' ' + titreMsg(x.c.message));
        return;
      }
      if (k > 0) out.push('');
      entetesCommit(repo, x.h, x.c, decorer).forEach(function (l) { out.push(l); });
      if (stat || patch) {
        var apres = contenusDe(repo, x.h);
        var avant = x.c.parents.length ? contenusDe(repo, x.c.parents[0]) : {};
        var entrees = diffEnsembles(avant, apres, chemins);
        out.push('');
        if (stat) rendDiffStat(entrees).forEach(function (l) { out.push(l); });
        if (patch) {
          entrees.forEach(function (e) {
            diffFichier(e.f, e.avant, e.apres).forEach(function (l) { out.push(l); });
          });
        }
      }
    });
    r.dire(out);
  };

  GIT.show = function (vm, args, r, ctx) {
    var repo = ctx.repo;
    var cible = args.filter(function (a) { return a.charAt(0) !== '-'; })[0] || 'HEAD';
    var stat = args.indexOf('--stat') !== -1;
    if (cible.indexOf(':') !== -1) {
      var bout = cible.split(':');
      var h0 = resoudre(repo, bout[0] || 'HEAD');
      var contenu = contenusDe(repo, h0)[bout[1]];
      if (contenu === undefined) {
        r.dire("fatal: path '" + bout[1] + "' does not exist in '" + bout[0] + "'");
        r.code = 1; return;
      }
      r.dire(lignes(contenu));
      return;
    }
    var h = resoudre(repo, cible);
    if (!h) {
      r.dire("fatal: ambiguous argument '" + cible +
             "': unknown revision or path not in the working tree.");
      r.code = 1; return;
    }
    var c = repo.commit(h);
    var out = entetesCommit(repo, h, c, args.indexOf('--decorate') !== -1);
    var apres = contenusDe(repo, h);
    var avant = c.parents.length ? contenusDe(repo, c.parents[0]) : {};
    var entrees = diffEnsembles(avant, apres, []);
    if (entrees.length) {
      out.push('');
      if (stat) rendDiffStat(entrees).forEach(function (l) { out.push(l); });
      else {
        entrees.forEach(function (e) {
          diffFichier(e.f, e.avant, e.apres).forEach(function (l) { out.push(l); });
        });
      }
    }
    r.dire(out);
  };

  GIT.diff = function (vm, args, r, ctx) {
    var repo = ctx.repo, racine = ctx.racine;
    var stage = false, stat = false, nomsSeuls = false, filtreU = false;
    var refs = [], chemins = [];
    for (var i = 0; i < args.length; i++) {
      var a = args[i];
      if (a === '--staged' || a === '--cached') stage = true;
      else if (a === '--stat') stat = true;
      else if (a === '--name-only') nomsSeuls = true;
      else if (a === '--diff-filter=U') filtreU = true;
      else if (a === '--') { chemins = args.slice(i + 1); break; }
      else if (a.charAt(0) !== '-') refs.push(a);
    }
    var avant, apres;
    if (stage) {
      avant = contenusDe(repo, repo.tete());
      apres = contenusIndex(repo);
    } else if (refs.length >= 2) {
      avant = contenusDe(repo, resoudre(repo, refs[0]));
      apres = contenusDe(repo, resoudre(repo, refs[1]));
    } else if (refs.length === 1) {
      avant = contenusDe(repo, resoudre(repo, refs[0]));
      apres = contenusWD(vm, racine, repo);
    } else {
      avant = contenusIndex(repo);
      apres = contenusWD(vm, racine, repo);
    }
    var entrees = diffEnsembles(avant, apres, chemins);
    if (filtreU) {
      r.dire(repo.conflits ? trie(Object.keys(repo.conflits)) : []);
      return;
    }
    if (nomsSeuls) { r.dire(entrees.map(function (e) { return e.f; })); return; }
    if (stat) { r.dire(rendDiffStat(entrees)); return; }
    var out = [];
    entrees.forEach(function (e) {
      diffFichier(e.f, e.avant, e.apres).forEach(function (l) { out.push(l); });
    });
    r.dire(out);
  };

  function modesCrees(entrees) {
    var out = [];
    entrees.forEach(function (e) {
      if (e.avant === undefined) out.push(' create mode 100644 ' + e.f);
    });
    entrees.forEach(function (e) {
      if (e.apres === undefined) out.push(' delete mode 100644 ' + e.f);
    });
    return out;
  }

  function resumeCommit(entrees) {
    var plus = 0, moins = 0;
    entrees.forEach(function (e) { plus += e.plus; moins += e.moins; });
    var parts = [pluriel(entrees.length, 'file') + ' changed'];
    if (plus) parts.push(pluriel(plus, 'insertion') + '(+)');
    if (moins) parts.push(pluriel(moins, 'deletion') + '(-)');
    return [' ' + parts.join(', ')].concat(modesCrees(entrees));
  }


  // ====================================================== chapitre 3 : branches

  function appliqueCommit(vm, racine, repo, h) {
    var arbre = repo.arbreDe(h);
    vm.fichiersDe(racine).forEach(function (f) {
      if (arbre[f] === undefined && repo.index[f] !== undefined) {
        vm.supprimer(racine + '/' + f);
      }
    });
    repo.index = {};
    Object.keys(arbre).forEach(function (f) {
      repo.index[f] = arbre[f];
      vm.ecrire(racine + '/' + f, blobs(repo)[arbre[f]]);
    });
  }

  GIT.branch = function (vm, args, r, ctx) {
    var repo = ctx.repo;
    var verbeux = args.indexOf('-v') !== -1;
    var noms = args.filter(function (a) { return a.charAt(0) !== '-'; });
    var iD = args.indexOf('-d') !== -1 || args.indexOf('--delete') !== -1;
    var iForce = args.indexOf('-D') !== -1;
    var iM = args.indexOf('-m') !== -1 || args.indexOf('--move') !== -1;

    if (iM) {
      var ancien = noms.length > 1 ? noms[0] : repo.branche;
      var neuf = noms.length > 1 ? noms[1] : noms[0];
      repo.refs[neuf] = repo.refs[ancien];
      delete repo.refs[ancien];
      if (repo.branche === ancien) repo.branche = neuf;
      return;
    }
    if (iD || iForce) {
      noms.forEach(function (n) {
        if (repo.refs[n] === undefined) {
          r.dire("error: branch '" + n + "' not found."); r.code = 1; return;
        }
        if (n === repo.branche) {
          r.dire("error: Cannot delete branch '" + n + "' checked out at '" +
                 ctx.racine + "'");
          r.code = 1; return;
        }
        var fusionnee = repo.ancetres(repo.tete())[repo.refs[n]];
        if (iD && !fusionnee) {
          r.dire("error: the branch '" + n + "' is not fully merged.",
                 "If you are sure you want to delete it, run 'git branch -D " + n + "'");
          r.code = 1; return;
        }
        r.dire('Deleted branch ' + n + ' (was ' + repo.refs[n].slice(0, 7) + ').');
        delete repo.refs[n];
      });
      return;
    }
    if (noms.length) {
      if (repo.refs[noms[0]] !== undefined) {
        r.dire("fatal: a branch named '" + noms[0] + "' already exists");
        r.code = 1; return;
      }
      repo.refs[noms[0]] = repo.tete();
      return;
    }
    var liste = trie(Object.keys(repo.refs));
    if (!verbeux) {
      r.dire(liste.map(function (b) {
        return (b === repo.branche ? '* ' : '  ') + b;
      }));
      return;
    }
    var largeur = 0;
    liste.forEach(function (b) { if (b.length > largeur) largeur = b.length; });
    r.dire(liste.map(function (b) {
      var c = repo.commit(repo.refs[b]);
      return (b === repo.branche ? '* ' : '  ') + b +
        Array(largeur - b.length + 1).join(' ') + ' ' +
        repo.refs[b].slice(0, 7) + ' ' + (c ? titreMsg(c.message) : '');
    }));
  };

  function basculer(vm, args, r, ctx, creer, nom) {
    var repo = ctx.repo, racine = ctx.racine;
    if (creer) {
      if (repo.refs[nom] !== undefined) {
        r.dire("fatal: a branch named '" + nom + "' already exists");
        r.code = 1; return;
      }
      var ancienne = repo.branche;
      repo.refs[nom] = repo.tete();
      repo.branche = nom;
      note(repo, 'checkout: moving from ' + ancienne + ' to ' + nom);
      r.dire("Switched to a new branch '" + nom + "'");
      return;
    }
    if (repo.refs[nom] === undefined) {
      r.dire("fatal: invalid reference: " + nom);
      r.code = 1; return;
    }
    if (nom === repo.branche) { r.dire("Already on '" + nom + "'"); return; }
    // Git refuse la bascule si un fichier suivi et modifie serait ecrase
    var e = etat(vm, racine, repo);
    var cible = repo.arbreDe(repo.refs[nom]);
    var actuel = repo.arbreDe(repo.tete());
    var genants = [];
    e.nonStage.concat(e.stage).forEach(function (x) {
      if (cible[x.f] !== actuel[x.f] && genants.indexOf(x.f) === -1) genants.push(x.f);
    });
    if (genants.length) {
      r.dire('error: Your local changes to the following files would be overwritten by checkout:');
      trie(genants).forEach(function (f) { r.dire('\t' + f); });
      r.dire('Please commit your changes or stash them before you switch branches.',
             'Aborting');
      r.code = 1; return;
    }
    var ancienneB = repo.branche;
    var emportes = e.nonStage.map(function (x) { return x.f; });
    var contenusAvant = {};
    emportes.forEach(function (f) { contenusAvant[f] = vm.files[racine + '/' + f]; });
    repo.branche = nom;
    appliqueCommit(vm, racine, repo, repo.refs[nom]);
    emportes.forEach(function (f) {
      if (contenusAvant[f] !== undefined) vm.ecrire(racine + '/' + f, contenusAvant[f]);
    });
    note(repo, 'checkout: moving from ' + ancienneB + ' to ' + nom);
    r.dire("Switched to branch '" + nom + "'");
    trie(emportes).forEach(function (f) { r.dire('M\t' + f); });
  }

  GIT.switch = function (vm, args, r, ctx) {
    var creer = args.indexOf('-c') !== -1 || args.indexOf('-C') !== -1;
    var noms = args.filter(function (a) { return a.charAt(0) !== '-'; });
    basculer(vm, args, r, ctx, creer, noms[0]);
  };

  GIT.checkout = function (vm, args, r, ctx) {
    var creer = args.indexOf('-b') !== -1;
    var noms = args.filter(function (a) { return a.charAt(0) !== '-'; });
    basculer(vm, args, r, ctx, creer, noms[0]);
  };

  GIT.merge = function (vm, args, r, ctx) {
    var repo = ctx.repo, racine = ctx.racine;
    var noFF = args.indexOf('--no-ff') !== -1;
    var ffOnly = args.indexOf('--ff-only') !== -1;
    var noms = args.filter(function (a) { return a.charAt(0) !== '-'; });
    var nom = noms[0];
    var cible = repo.refs[nom] !== undefined ? repo.refs[nom] : resoudre(repo, nom);
    if (!cible) {
      r.dire('merge: ' + nom + ' - not something we can merge');
      r.code = 1; return;
    }
    var local = repo.tete();
    if (repo.ancetres(local)[cible]) { r.dire('Already up to date.'); return; }

    var avant = contenusDe(repo, local);
    if (repo.ancetres(cible)[local] && !noFF) {
      repo.refs[repo.branche] = cible;
      appliqueCommit(vm, racine, repo, cible);
      r.dire('Updating ' + local.slice(0, 7) + '..' + cible.slice(0, 7), 'Fast-forward');
      var eFF = diffEnsembles(avant, contenusDe(repo, cible), []);
      r.dire(rendDiffStat(eFF));
      r.dire(modesCrees(eFF));
      return;
    }
    if (ffOnly) {
      r.dire('fatal: Not possible to fast-forward, aborting.');
      r.code = 1; return;
    }
    var base = repo.base(local, cible);
    var aB = repo.arbreDe(base), aL = repo.arbreDe(local), aD = repo.arbreDe(cible);
    var fusion = {}, conflits = [], noms2 = {};
    [aB, aL, aD].forEach(function (m) {
      Object.keys(m).forEach(function (k) { noms2[k] = true; });
    });
    trie(Object.keys(noms2)).forEach(function (f) {
      var b = aB[f], l = aL[f], d = aD[f];
      if (l === d) { if (l !== undefined) fusion[f] = l; return; }
      if (l === b) { if (d !== undefined) fusion[f] = d; return; }
      if (d === b) { if (l !== undefined) fusion[f] = l; return; }
      conflits.push(f);
      fusion[f] = l;
    });
    if (conflits.length) {
      conflits.forEach(function (f) { r.dire('Auto-merging ' + f); });
      conflits.forEach(function (f) {
        r.dire('CONFLICT (content): Merge conflict in ' + f);
      });
      r.dire('Automatic merge failed; fix conflicts and then commit the result.');
      r.code = 1; return;
    }
    var h = repo.nouveauCommit(fusion, [local, cible], "Merge branch '" + nom + "'",
                               vm.horloge);
    repo.refs[repo.branche] = h;
    appliqueCommit(vm, racine, repo, h);
    r.dire("Merge made by the 'ort' strategy.");
    var eM = diffEnsembles(avant, contenusDe(repo, h), []);
    r.dire(rendDiffStat(eM));
    r.dire(modesCrees(eM));
  };

  // --------------------------------------- etat du graphe, pour le schema SVG

  function graphe(vm) {
    var d = vm.depotPour(vm.cwd);
    if (!d) return null;
    var repo = d.repo;
    var depuis = [];
    Object.keys(repo.refs).forEach(function (b) { depuis.push(repo.refs[b]); });
    if (!depuis.filter(Boolean).length) {
      return { commits: [], branches: {}, tete: repo.branche };
    }
    var liste = commitsAccessibles(repo, depuis.filter(Boolean));
    var etiquettes = {};
    Object.keys(repo.refs).forEach(function (b) {
      var h = repo.refs[b];
      if (!etiquettes[h]) etiquettes[h] = [];
      etiquettes[h].push(b);
    });
    Object.keys(repo.suivi).forEach(function (b) {
      var h = repo.suivi[b];
      if (!h) return;
      if (!etiquettes[h]) etiquettes[h] = [];
      etiquettes[h].push(b);
    });
    return {
      commits: liste.map(function (x) {
        return {
          h: x.h, court: x.h.slice(0, 7), message: x.c.message,
          parents: x.c.parents, date: x.c.date,
          etiquettes: etiquettes[x.h] || []
        };
      }),
      tete: repo.branche,
      teteHash: repo.tete()
    };
  }


  // ============================ chapitres 3 a 6 : stash, reparation, conflits

  function journal(repo) { if (!repo.reflog) repo.reflog = []; return repo.reflog; }

  function note(repo, action) {
    journal(repo).unshift({ h: repo.tete(), action: action });
  }

  function pile(repo) { if (!repo.stash) repo.stash = []; return repo.stash; }

  // ------------------------------------------------------------------- stash

  GIT.stash = function (vm, args, r, ctx) {
    var repo = ctx.repo, racine = ctx.racine;
    var sous = args.filter(function (a) { return a.charAt(0) !== '-'; })[0] || 'push';
    var avecNonSuivis = args.indexOf('-u') !== -1 ||
                        args.indexOf('--include-untracked') !== -1;

    if (sous === 'list') {
      r.dire(pile(repo).map(function (s, i) {
        return 'stash@{' + i + '}: ' + s.titre;
      }));
      return;
    }
    if (sous === 'push' || sous === 'save') {
      var e = etat(vm, racine, repo);
      var aQuoiFaire = e.stage.length || e.nonStage.length ||
                       (avecNonSuivis && e.nonSuivis.length);
      if (!aQuoiFaire) { r.dire('No local changes to save'); return; }
      var tete = repo.tete();
      var c = repo.commit(tete);
      var fichiers = {};
      vm.fichiersDe(racine).forEach(function (f) {
        var suivi = repo.index[f] !== undefined;
        if (suivi || avecNonSuivis) fichiers[f] = vm.files[racine + '/' + f];
      });
      var motifs = motifsIgnore(vm, racine);
      Object.keys(fichiers).forEach(function (f) {
        if (repo.index[f] === undefined && estIgnore(motifs, f)) delete fichiers[f];
      });
      pile(repo).unshift({
        titre: 'WIP on ' + repo.branche + ': ' + tete.slice(0, 7) + ' ' + titreMsg(c.message),
        fichiers: fichiers,
        index: copieArbre(repo.index),
        base: tete,
        nonSuivis: e.nonSuivis.slice()
      });
      Object.keys(fichiers).forEach(function (f) {
        if (repo.index[f] === undefined) vm.supprimer(racine + '/' + f);
      });
      appliqueCommit(vm, racine, repo, tete);
      r.dire('Saved working directory and index state WIP on ' + repo.branche +
             ': ' + tete.slice(0, 7) + ' ' + titreMsg(c.message));
      return;
    }
    if (sous === 'pop' || sous === 'apply') {
      if (!pile(repo).length) { r.dire('No stash entries found.'); r.code = 1; return; }
      var s = pile(repo)[0];
      Object.keys(s.fichiers).forEach(function (f) {
        vm.ecrire(racine + '/' + f, s.fichiers[f]);
      });
      r.dire(rendStatus(vm, racine, repo));
      if (sous === 'pop') {
        pile(repo).shift();
        var faux = hash(s.titre + '|drop');
        var long = '';
        for (var k = 0; long.length < 40; k++) long += hash(s.titre + '#' + k);
        r.dire('Dropped refs/stash@{0} (' + long.slice(0, 40) + ')');
      }
      return;
    }
    if (sous === 'drop') {
      if (!pile(repo).length) { r.dire('No stash entries found.'); r.code = 1; return; }
      pile(repo).shift();
      r.dire('Dropped refs/stash@{0}');
      return;
    }
    r.dire("error: unknown subcommand: `" + sous + "'");
    r.code = 1;
  };

  // --------------------------------------------------------------- restore

  GIT.restore = function (vm, args, r, ctx) {
    var repo = ctx.repo, racine = ctx.racine;
    var staged = args.indexOf('--staged') !== -1 || args.indexOf('--cached') !== -1;
    var ours = args.indexOf('--ours') !== -1;
    var theirs = args.indexOf('--theirs') !== -1;
    var source = null;
    for (var i = 0; i < args.length; i++) {
      if (args[i] === '--source' || args[i] === '-s') { source = args[i + 1]; i++; }
      else if (args[i].indexOf('--source=') === 0) source = args[i].slice(9);
    }
    var cibles = [];
    var apresTirets = false;
    args.forEach(function (a, k) {
      if (a === '--') { apresTirets = true; return; }
      if (a.charAt(0) === '-') return;
      if (k > 0 && (args[k - 1] === '--source' || args[k - 1] === '-s')) return;
      cibles.push(a);
    });
    if (!cibles.length) {
      r.dire('fatal: you must specify path(s) to restore'); r.code = 1; return;
    }
    cibles.forEach(function (a) {
      var rel = relatif(racine, joindre(vm.cwd, a));
      if (repo.conflits && repo.conflits[rel] && (ours || theirs)) {
        var c = repo.conflits[rel];
        vm.ecrire(racine + '/' + rel, ours ? c.nous : c.eux);
        return;
      }
      if (staged) {
        var arbre = repo.arbreDe(source ? resoudre(repo, source) : repo.tete());
        if (arbre[rel] !== undefined) repo.index[rel] = arbre[rel];
        else delete repo.index[rel];
        return;
      }
      if (source) {
        var a2 = repo.arbreDe(resoudre(repo, source));
        if (a2[rel] === undefined) {
          r.dire("error: pathspec '" + a + "' did not match any file(s) known to git");
          r.code = 1; return;
        }
        vm.ecrire(racine + '/' + rel, blobs(repo)[a2[rel]]);
        repo.index[rel] = a2[rel];
        return;
      }
      if (repo.index[rel] === undefined) {
        r.dire("error: pathspec '" + a + "' did not match any file(s) known to git");
        r.code = 1; return;
      }
      vm.ecrire(racine + '/' + rel, blobs(repo)[repo.index[rel]]);
    });
  };

  // ----------------------------------------------------------------- reset

  GIT.reset = function (vm, args, r, ctx) {
    var repo = ctx.repo, racine = ctx.racine;
    var mode = null;
    if (args.indexOf('--soft') !== -1) mode = 'soft';
    else if (args.indexOf('--hard') !== -1) mode = 'hard';
    else if (args.indexOf('--mixed') !== -1) mode = 'mixed';
    var reste = args.filter(function (a) { return a.charAt(0) !== '-'; });

    // sans mode et avec des chemins : on retire du panier
    var estChemin = reste.length && reste.every(function (a) {
      var abs = joindre(vm.cwd, a);
      return vm.existe(abs) || repo.index[relatif(racine, abs)] !== undefined;
    });
    if (!mode && (estChemin || !reste.length)) {
      var arbre0 = repo.arbreDe(repo.tete());
      var touches = [];
      if (!reste.length) {
        Object.keys(repo.index).concat(Object.keys(arbre0)).forEach(function (f) {
          if (touches.indexOf(f) === -1) touches.push(f);
        });
      } else {
        reste.forEach(function (a) {
          var rel = relatif(racine, joindre(vm.cwd, a));
          Object.keys(repo.index).concat(Object.keys(arbre0)).forEach(function (f) {
            if ((f === rel || f.indexOf(rel + '/') === 0) && touches.indexOf(f) === -1) {
              touches.push(f);
            }
          });
          if (!touches.length) touches.push(rel);
        });
      }
      touches.forEach(function (f) {
        if (arbre0[f] !== undefined) repo.index[f] = arbre0[f];
        else delete repo.index[f];
      });
      if (!reste.length) {
        var e0 = etat(vm, racine, repo);
        if (e0.nonStage.length) {
          r.dire('Unstaged changes after reset:');
          e0.nonStage.forEach(function (x) {
            r.dire((x.etat === 'deleted' ? 'D' : 'M') + '\t' + x.f);
          });
        }
      }
      return;
    }

    var cible = resoudre(repo, reste[0] || 'HEAD');
    if (!cible) {
      r.dire("fatal: ambiguous argument '" + (reste[0] || '') +
             "': unknown revision or path not in the working tree.");
      r.code = 1; return;
    }
    repo.refs[repo.branche] = cible;
    var arbre = repo.arbreDe(cible);
    if (mode === 'hard') {
      appliqueCommit(vm, racine, repo, cible);
      note(repo, 'reset: moving to ' + (reste[0] || 'HEAD'));
      r.dire('HEAD is now at ' + cible.slice(0, 7) + ' ' + titreMsg(repo.commit(cible).message));
      return;
    }
    if (mode !== 'soft') {
      repo.index = {};
      Object.keys(arbre).forEach(function (f) { repo.index[f] = arbre[f]; });
    }
    note(repo, 'reset: moving to ' + (reste[0] || 'HEAD'));
    if (mode !== 'soft') {
      var e = etat(vm, racine, repo);
      if (e.nonStage.length) {
        r.dire('Unstaged changes after reset:');
        e.nonStage.forEach(function (x) {
          r.dire((x.etat === 'deleted' ? 'D' : 'M') + '\t' + x.f);
        });
      }
    }
  };

  // ---------------------------------------------------------------- reflog

  GIT.reflog = function (vm, args, r, ctx) {
    var repo = ctx.repo;
    var j = journal(repo);
    if (!j.length) { r.dire([]); return; }
    r.dire(j.map(function (e, i) {
      return (e.h ? e.h.slice(0, 7) : '0000000') + ' HEAD@{' + i + '}: ' + e.action;
    }));
  };

  // ---------------------------------------------------------------- revert

  GIT.revert = function (vm, args, r, ctx) {
    var repo = ctx.repo, racine = ctx.racine;
    var parent = null;
    for (var i = 0; i < args.length; i++) {
      if (args[i] === '-m') { parent = parseInt(args[i + 1], 10); i++; }
    }
    var reste = args.filter(function (a, k) {
      return a.charAt(0) !== '-' && args[k - 1] !== '-m';
    });
    var h = resoudre(repo, reste[0] || 'HEAD');
    if (!h) {
      r.dire('fatal: bad revision \'' + (reste[0] || '') + '\''); r.code = 1; return;
    }
    var c = repo.commit(h);
    if (c.parents.length > 1 && parent === null) {
      r.dire('error: commit ' + h + ' is a merge but no -m option was given.',
             'fatal: revert failed');
      r.code = 1; return;
    }
    var refParent = c.parents.length > 1 ? c.parents[parent - 1] : c.parents[0];
    var avantC = contenusDe(repo, refParent);
    var apresC = contenusDe(repo, h);
    var courantC = contenusDe(repo, repo.tete());

    // on applique l'inverse : ce que le commit a fait, on le defait
    var nouveau = copieArbre(repo.arbreDe(repo.tete()));
    var conflit = false;
    var noms = {};
    [avantC, apresC].forEach(function (m) {
      Object.keys(m).forEach(function (k) { noms[k] = true; });
    });
    Object.keys(noms).forEach(function (f) {
      if (avantC[f] === apresC[f]) return;
      if (courantC[f] !== apresC[f]) { conflit = true; return; }
      if (avantC[f] === undefined) delete nouveau[f];
      else nouveau[f] = enregistreBlob(repo, avantC[f]);
    });
    if (conflit) {
      r.dire('error: could not revert ' + h.slice(0, 7) + '... ' + c.message,
             'hint: After resolving the conflicts, mark them with',
             'hint: "git add/rm <pathspec>", then run',
             'hint: "git revert --continue".');
      r.code = 1; return;
    }
    var sales = [];
    Object.keys(noms).forEach(function (f) {
      if (avantC[f] === apresC[f]) return;
      var surDisque = vm.files[racine + '/' + f];
      var dansIndex = repo.index[f] !== undefined ? blobs(repo)[repo.index[f]] : undefined;
      if (surDisque !== dansIndex) sales.push(f);
    });
    if (sales.length) {
      r.dire('error: Your local changes to the following files would be overwritten by merge:');
      trie(sales).forEach(function (f) { r.dire('\t' + f); });
      r.dire('Please commit your changes or stash them before you merge.',
             'Aborting');
      r.code = 1; return;
    }
    var msg = 'Revert "' + titreMsg(c.message) + '"\n\nThis reverts commit ' + h + '.';
    var tete = repo.tete();
    var nh = repo.nouveauCommit(nouveau, [tete], msg, vm.horloge);
    repo.refs[repo.branche] = nh;
    appliqueCommit(vm, racine, repo, nh);
    note(repo, 'revert: ' + titreMsg(msg));
    r.dire('[' + repo.branche + ' ' + nh.slice(0, 7) + '] ' + titreMsg(msg));
    r.dire(' Date: ' + dateDe(vm.horloge));
    r.dire(resumeCommit(diffEnsembles(contenusDe(repo, tete),
                                      contenusDe(repo, nh), [])));
  };

  // -------------------------------------------- fusion a trois avec conflits

  function morceaux(base, cote) {
    // regions de "base" remplacees par "cote"
    var ops = diffLignes(base, cote);
    var out = [], ib = 0, ic = 0, cour = null;
    ops.forEach(function (o) {
      if (o.t === ' ') {
        if (cour) { out.push(cour); cour = null; }
        ib++; ic++;
        return;
      }
      if (!cour) cour = { debut: ib, fin: ib, lignes: [] };
      if (o.t === '-') { ib++; cour.fin = ib; }
      else { cour.lignes.push(o.l); ic++; }
    });
    if (cour) out.push(cour);
    return out;
  }

  function fusionTexte(base, nous, eux, nomNous, nomEux) {
    var lb = lignes(base), ln = lignes(nous), le = lignes(eux);
    var mn = morceaux(lb, ln), me = morceaux(lb, le);

    // groupes : intervalles de base touches par au moins un cote, fusionnes
    // des qu'ils se chevauchent ou se touchent
    var bornes = [];
    mn.concat(me).forEach(function (m) {
      bornes.push({ d: m.debut, f: Math.max(m.fin, m.debut) });
    });
    bornes.sort(function (a, b) { return a.d - b.d || a.f - b.f; });
    var groupes = [];
    bornes.forEach(function (b) {
      var dernier = groupes[groupes.length - 1];
      if (dernier && b.d <= dernier.f) {
        dernier.f = Math.max(dernier.f, b.f);
      } else {
        groupes.push({ d: b.d, f: b.f });
      }
    });

    function reconstruit(segments, d, f) {
      var out = [], k = d;
      while (k < f) {
        var seg = null;
        segments.forEach(function (m) { if (m.debut === k && m.fin > m.debut) seg = m; });
        var ins = null;
        segments.forEach(function (m) { if (m.debut === k && m.fin === m.debut) ins = m; });
        if (ins) ins.lignes.forEach(function (l) { out.push(l); });
        if (seg) {
          seg.lignes.forEach(function (l) { out.push(l); });
          k = seg.fin;
        } else {
          out.push(lb[k]);
          k++;
        }
      }
      segments.forEach(function (m) {
        if (m.debut === f && m.fin === f) m.lignes.forEach(function (l) { out.push(l); });
      });
      return out;
    }

    function touche(segments, d, f) {
      var oui = false;
      segments.forEach(function (m) {
        var mf = Math.max(m.fin, m.debut);
        if (m.debut < f || (m.debut === f && m.fin === m.debut)) {
          if (mf > d || (m.debut >= d && m.fin === m.debut)) oui = true;
        }
      });
      return oui;
    }

    var res = [], conflit = false, i = 0;
    groupes.forEach(function (g) {
      while (i < g.d) { res.push(lb[i]); i++; }
      var gn = reconstruit(mn, g.d, g.f);
      var ge = reconstruit(me, g.d, g.f);
      var tn = touche(mn, g.d, g.f), te = touche(me, g.d, g.f);
      if (!tn) { ge.forEach(function (l) { res.push(l); }); }
      else if (!te) { gn.forEach(function (l) { res.push(l); }); }
      else if (gn.join('\n') === ge.join('\n')) { gn.forEach(function (l) { res.push(l); }); }
      else {
        conflit = true;
        res.push('<<<<<<< ' + nomNous);
        gn.forEach(function (l) { res.push(l); });
        res.push('=======');
        ge.forEach(function (l) { res.push(l); });
        res.push('>>>>>>> ' + nomEux);
      }
      i = g.f;
    });
    while (i < lb.length) { res.push(lb[i]); i++; }
    return { texte: res.join('\n') + '\n', conflit: conflit };
  }

  function fusionne(vm, racine, repo, cible, nomCible, r, options) {
    options = options || {};
    var local = repo.tete();
    var base = repo.base(local, cible);
    var aB = contenusDe(repo, base), aL = contenusDe(repo, local),
        aD = contenusDe(repo, cible);
    var arbre = copieArbre(repo.arbreDe(local));
    var conflits = {}, auto = [];
    var noms = {};
    [aB, aL, aD].forEach(function (m) {
      Object.keys(m).forEach(function (k) { noms[k] = true; });
    });
    trie(Object.keys(noms)).forEach(function (f) {
      var b = aB[f], l = aL[f], d = aD[f];
      if (l === d) { return; }
      if (l === b) {
        if (d === undefined) delete arbre[f];
        else arbre[f] = enregistreBlob(repo, d);
        return;
      }
      if (d === b) { return; }
      auto.push(f);
      var fu = fusionTexte(b === undefined ? '' : b,
                           l === undefined ? '' : l,
                           d === undefined ? '' : d, 'HEAD', nomCible);
      if (fu.conflit) {
        conflits[f] = { base: b, nous: l, eux: d, texte: fu.texte,
                        genre: b === undefined ? 'add/add' : 'content' };
      } else {
        arbre[f] = enregistreBlob(repo, fu.texte);
      }
    });
    auto.forEach(function (f) {
      r.dire('Auto-merging ' + f);
      if (conflits[f]) {
        r.dire('CONFLICT (' + conflits[f].genre + '): Merge conflict in ' + f);
      }
    });
    if (Object.keys(conflits).length) {
      Object.keys(conflits).forEach(function (f) {
        vm.ecrire(racine + '/' + f, conflits[f].texte);
      });
      repo.conflits = conflits;
      repo.fusion = { cible: cible, nom: nomCible, local: local,
                      arbre: arbre, squash: !!options.squash };
      Object.keys(arbre).forEach(function (f) {
        if (!conflits[f]) {
          repo.index[f] = arbre[f];
          if (blobs(repo)[arbre[f]] !== undefined) {
            vm.ecrire(racine + '/' + f, blobs(repo)[arbre[f]]);
          }
        }
      });
      r.dire('Automatic merge failed; fix conflicts and then commit the result.');
      r.code = 1;
      return null;
    }
    return arbre;
  }

  function finitFusion(vm, racine, repo, arbre, cible, nomCible, message, r) {
    var local = repo.tete();
    var avant = contenusDe(repo, local);
    var h = repo.nouveauCommit(arbre, [local, cible], message, vm.horloge);
    repo.refs[repo.branche] = h;
    appliqueCommit(vm, racine, repo, h);
    note(repo, 'merge ' + nomCible + ': Merge made by the \'ort\' strategy.');
    repo.conflits = null; repo.fusion = null;
    r.dire("Merge made by the 'ort' strategy.");
    var e = diffEnsembles(avant, contenusDe(repo, h), []);
    r.dire(rendDiffStat(e));
    r.dire(modesCrees(e));
  }

  GIT.merge = function (vm, args, r, ctx) {
    var repo = ctx.repo, racine = ctx.racine;
    if (args.indexOf('--abort') !== -1) {
      if (!repo.fusion) {
        r.dire('fatal: There is no merge to abort (MERGE_HEAD missing).');
        r.code = 1; return;
      }
      appliqueCommit(vm, racine, repo, repo.fusion.local);
      repo.conflits = null; repo.fusion = null;
      return;
    }
    if (args.indexOf('--continue') !== -1) {
      if (!repo.fusion) {
        r.dire('fatal: There is no merge in progress (MERGE_HEAD missing).');
        r.code = 1; return;
      }
      if (repo.conflits && Object.keys(repo.conflits).length) {
        r.dire('error: Committing is not possible because you have unmerged files.',
               'hint: Fix them up in the work tree, and then use \'git add/rm <file>\'',
               'hint: as appropriate to mark resolution and make a commit.',
               'fatal: Exiting because of an unresolved conflict.');
        r.code = 1; return;
      }
      var arbreF = copieArbre(repo.index);
      finitFusion(vm, racine, repo, arbreF, repo.fusion.cible, repo.fusion.nom,
                  "Merge branch '" + repo.fusion.nom + "'", r);
      return;
    }
    var noFF = args.indexOf('--no-ff') !== -1;
    var ffOnly = args.indexOf('--ff-only') !== -1;
    var squash = args.indexOf('--squash') !== -1;
    var noms = args.filter(function (a) { return a.charAt(0) !== '-'; });
    var nom = noms[0];
    var cible = repo.refs[nom] !== undefined ? repo.refs[nom] : resoudre(repo, nom);
    if (!cible) {
      r.dire('merge: ' + nom + ' - not something we can merge');
      r.code = 1; return;
    }
    var local = repo.tete();
    if (repo.ancetres(local)[cible]) { r.dire('Already up to date.'); return; }
    var avant = contenusDe(repo, local);

    if (squash) {
      var ffS = repo.ancetres(cible)[local];
      if (ffS) {
        r.dire('Updating ' + local.slice(0, 7) + '..' + cible.slice(0, 7), 'Fast-forward',
               'Squash commit -- not updating HEAD');
        var arbreS = repo.arbreDe(cible);
        Object.keys(repo.index).forEach(function (f) {
          if (arbreS[f] === undefined) delete repo.index[f];
        });
        Object.keys(arbreS).forEach(function (f) {
          repo.index[f] = arbreS[f];
          vm.ecrire(racine + '/' + f, blobs(repo)[arbreS[f]]);
        });
        var eS = diffEnsembles(avant, contenusDe(repo, cible), []);
        r.dire(rendDiffStat(eS));
        r.dire(modesCrees(eS));
        return;
      }
      var arbreSq = fusionne(vm, racine, repo, cible, nom, r, { squash: true });
      if (!arbreSq) return;
      r.dire('Squash commit -- not updating HEAD');
      Object.keys(arbreSq).forEach(function (f) {
        repo.index[f] = arbreSq[f];
        vm.ecrire(racine + '/' + f, blobs(repo)[arbreSq[f]]);
      });
      var eSq = diffEnsembles(avant, contenusIndex(repo), []);
      r.dire(rendDiffStat(eSq));
      r.dire(modesCrees(eSq));
      return;
    }

    if (repo.ancetres(cible)[local] && !noFF) {
      repo.refs[repo.branche] = cible;
      appliqueCommit(vm, racine, repo, cible);
      note(repo, 'merge ' + nom + ': Fast-forward');
      r.dire('Updating ' + local.slice(0, 7) + '..' + cible.slice(0, 7), 'Fast-forward');
      var eFF = diffEnsembles(avant, contenusDe(repo, cible), []);
      r.dire(rendDiffStat(eFF));
      r.dire(modesCrees(eFF));
      return;
    }
    if (ffOnly) {
      r.dire("hint: Diverging branches can't be fast-forwarded, you need to either:",
             'hint: ',
             'hint: \tgit merge --no-ff',
             'hint: ',
             'hint: or:',
             'hint: ',
             'hint: \tgit rebase',
             'hint: ',
             'hint: Disable this message with "git config advice.diverging false"',
             'fatal: Not possible to fast-forward, aborting.');
      r.code = 1; return;
    }
    var arbre = fusionne(vm, racine, repo, cible, nom, r, {});
    if (!arbre) return;
    finitFusion(vm, racine, repo, arbre, cible, nom, "Merge branch '" + nom + "'", r);
  };

  // --------------------------------------------------------- log --graph art

  function artGraphe(repo, liste) {
    // colonnes : une par branche active au moment ou on descend l'historique
    var lignesArt = [], colonnes = [];
    liste.forEach(function (x) {
      var i = colonnes.indexOf(x.h);
      if (i === -1) { colonnes.push(x.h); i = colonnes.length - 1; }
      var avant = colonnes.slice();
      var parents = x.c.parents;
      var tete = [];
      for (var k = 0; k < colonnes.length; k++) {
        tete.push(k === i ? '*' : '|');
      }
      var sup = Array(parents.length).join('  ');
      lignesArt.push({ art: tete.join(' ') + sup, commit: x });

      // remplace la colonne par le premier parent, ajoute les autres
      var nouvelles = colonnes.slice();
      nouvelles[i] = parents[0] || null;
      for (var p = 1; p < parents.length; p++) {
        nouvelles.splice(i + p, 0, parents[p]);
      }
      // deduplique en gardant la premiere occurrence
      var vus = {}, propre = [];
      nouvelles.forEach(function (h) {
        if (h === null) return;
        if (vus[h]) return;
        vus[h] = true; propre.push(h);
      });
      if (parents.length > 1) {
        lignesArt.push({ art: separateur(avant.length, i, 'ouvre'), commit: null });
      }
      if (propre.length < colonnes.length && parents.length === 1) {
        lignesArt.push({ art: separateur(colonnes.length, i, 'ferme'), commit: null });
      }
      colonnes = propre;
    });
    return lignesArt;
  }

  function separateur(n, i, sens) {
    var t = [];
    for (var k = 0; k < n; k++) {
      if (sens === 'ouvre') t.push(k === i ? '|\\' : '|');
      else t.push(k === i ? '|/' : '|');
    }
    return t.join(' ') + '  ';
  }

  // ------------------------------------------------------------------ rebase

  GIT.rebase = function (vm, args, r, ctx) {
    var repo = ctx.repo, racine = ctx.racine;
    var noms = args.filter(function (a) { return a.charAt(0) !== '-'; });
    var nom = noms[0];
    var cible = repo.refs[nom] !== undefined ? repo.refs[nom] : resoudre(repo, nom);
    if (!cible) { r.dire('fatal: invalid upstream \'' + nom + '\''); r.code = 1; return; }
    rejoue(vm, racine, repo, cible, nom, r);
  };

  function rejoue(vm, racine, repo, cible, nom, r) {
    var local = repo.tete();
    if (repo.ancetres(cible)[local]) {
      repo.refs[repo.branche] = cible;
      appliqueCommit(vm, racine, repo, cible);
      r.dire('Successfully rebased and updated refs/heads/' + repo.branche + '.');
      return true;
    }
    var base = repo.base(local, cible);
    var aRejouer = [];
    var h = local;
    while (h && h !== base) {
      aRejouer.unshift(h);
      var c = repo.commit(h);
      h = c.parents[0];
    }
    var tete = cible;
    for (var i = 0; i < aRejouer.length; i++) {
      var cc = repo.commit(aRejouer[i]);
      var avant = contenusDe(repo, cc.parents[0]);
      var apres = contenusDe(repo, aRejouer[i]);
      var arbre = copieArbre(repo.arbreDe(tete));
      var noms2 = {};
      [avant, apres].forEach(function (m) {
        Object.keys(m).forEach(function (k) { noms2[k] = true; });
      });
      Object.keys(noms2).forEach(function (f) {
        if (avant[f] === apres[f]) return;
        if (apres[f] === undefined) delete arbre[f];
        else arbre[f] = enregistreBlob(repo, apres[f]);
      });
      tete = repo.nouveauCommit(arbre, [tete], cc.message, cc.date);
    }
    repo.refs[repo.branche] = tete;
    appliqueCommit(vm, racine, repo, tete);
    var n = aRejouer.length;
    r.dire('Rebasing (' + n + '/' + n + ')', '', Array(81).join(' '));
    r.dire('Successfully rebased and updated refs/heads/' + repo.branche + '.');
    return true;
  }

  // -------------------------------------------------------------- interpreteur

  function executeLigne(vm, ligne) {
    var r = new Resultat();
    vm.horloge++;
    var jetons = brut(ligne);
    if (!jetons.length) return r;

    // redirection
    var redir = null, cible = null, args = [];
    for (var i = 0; i < jetons.length; i++) {
      var j = jetons[i];
      if (j.op) { redir = j.t; cible = jetons[i + 1] ? jetons[i + 1].t : null; i++; continue; }
      args.push(j);
    }
    var cmd = args[0] ? args[0].t : '';
    var reste = args.slice(1);
    var simples = reste.map(function (x) { return x.t; });

    var sortie = [];
    var texteBrut = null;   // printf n'ajoute pas de saut de ligne final

    if (cmd === 'echo') {
      sortie = [simples.join(' ')];
    } else if (cmd === 'printf') {
      var fmtArgs = simples[0] === '--' ? simples.slice(1) : simples;
      texteBrut = echappe(fmtArgs.join(' '));
      if (!redir) {
        sortie = texteBrut.split('\n');
        if (sortie[sortie.length - 1] === '') sortie.pop();
        r.lignes = sortie;
        return r;
      }
    } else if (cmd === 'cat') {
      simples.forEach(function (f) {
        var abs = joindre(vm.cwd, f);
        if (vm.files[abs] === undefined) {
          r.dire('cat: ' + f + ': No such file or directory'); r.code = 1; return;
        }
        var t = vm.files[abs];
        var l = t.split('\n');
        if (l[l.length - 1] === '') l.pop();
        r.dire(l);
      });
      return r;
    } else if (cmd === 'ls') {
      var opts = simples.filter(function (x) { return x.charAt(0) === '-'; });
      var chemins = simples.filter(function (x) { return x.charAt(0) !== '-'; });
      var d = chemins.length ? joindre(vm.cwd, chemins[0]) : vm.cwd;
      var noms = vm.lister(d);
      if (opts.indexOf('-a') === -1) {
        noms = noms.filter(function (n) { return n.charAt(0) !== '.'; });
      } else {
        noms = trie(['.', '..'].concat(noms));
      }
      r.dire(noms);
      return r;
    } else if (cmd === 'mkdir') {
      simples.filter(function (x) { return x.charAt(0) !== '-'; })
        .forEach(function (d2) { vm.mkdirp(joindre(vm.cwd, d2)); });
      return r;
    } else if (cmd === 'cd') {
      var dest = simples[0] ? joindre(vm.cwd, simples[0]) : RACINE;
      if (!vm.estDossier(dest)) {
        r.dire('bash: cd: ' + simples[0] + ': No such file or directory'); r.code = 1; return r;
      }
      vm.cwd = dest;
      return r;
    } else if (cmd === 'rm') {
      simples.filter(function (x) { return x.charAt(0) !== '-'; })
        .forEach(function (f) { vm.supprimer(joindre(vm.cwd, f)); });
      return r;
    } else if (cmd === 'pwd') {
      r.dire(vm.cwd); return r;
    } else if (cmd === 'git') {
      var sous = simples[0];
      var fn = GIT[sous];
      if (!fn) {
        r.dire("git: '" + (sous || '') + "' is not a git command. See 'git --help'.");
        r.code = 1; return r;
      }
      var ctx = {};
      if (sous !== 'init' && sous !== 'clone') {
        var d3 = vm.depotPour(vm.cwd);
        if (!d3) {
          r.dire('fatal: not a git repository (or any of the parent directories): .git');
          r.code = 1; return r;
        }
        ctx.racine = d3.racine; ctx.repo = d3.repo;
      }
      fn(vm, simples.slice(1), r, ctx);
      return r;
    } else if (cmd === '') {
      return r;
    } else {
      r.dire('bash: ' + cmd + ': command not found');
      r.code = 127;
      return r;
    }

    if (redir) {
      var texteOut = texteBrut !== null ? texteBrut : sortie.join('\n') + '\n';
      var absC = joindre(vm.cwd, cible);
      if (redir === '>>' && vm.files[absC] !== undefined) {
        vm.ecrire(absC, vm.files[absC] + texteOut);
      } else {
        vm.ecrire(absC, texteOut);
      }
      return r;
    }
    r.lignes = sortie;
    return r;
  }

  // ------------------------------------------------------------------- public

  function creerSession(seed) {
    var vm = new VM();
    if (seed) {
      seed.split('\n').forEach(function (l) {
        if (l.trim() && l.trim().charAt(0) !== '#') executeLigne(vm, l.trim());
      });
    }
    return vm;
  }

  function jouer(vm, script, options) {
    options = options || {};
    var limite = options.limiteMs || 4000;
    var debut = Date.now();
    var lignes = [];
    var cmds = script.split('\n');
    for (var i = 0; i < cmds.length; i++) {
      var c = cmds[i].trim();
      if (!c || c.charAt(0) === '#') continue;
      lignes.push('$ ' + c);
      var r = executeLigne(vm, c);
      r.lignes.forEach(function (l) { lignes.push(l); });
      if (lignes.length > 4000) {
        lignes.push('[execution interrompue : sortie trop longue]');
        break;
      }
      if (Date.now() - debut > limite) {
        lignes.push('[execution interrompue apres ' + (limite / 1000) +
                    ' secondes : ton programme tourne trop longtemps]');
        break;
      }
    }
    return lignes;
  }

  var API = {
    creerSession: creerSession,
    graphe: graphe,
    jouer: jouer,
    executeLigne: executeLigne,
    RACINE: RACINE,
    GITHUB: GITHUB
  };

  if (typeof module !== 'undefined' && module.exports) module.exports = API;
  else global.Gitleo = API;
})(typeof window !== 'undefined' ? window : globalThis);
