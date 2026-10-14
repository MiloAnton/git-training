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
        titre: 'WIP on ' + repo.branche + ': ' + tete.slice(0, 7) + ' ' + c.message,
        fichiers: fichiers,
        index: copieArbre(repo.index),
        base: tete,
        nonSuivis: e.nonSuivis.slice()
      });
      appliqueCommit(vm, racine, repo, tete);
      r.dire('Saved working directory and index state WIP on ' + repo.branche +
             ': ' + tete.slice(0, 7) + ' ' + c.message);
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
      r.dire('HEAD is now at ' + cible.slice(0, 7) + ' ' + repo.commit(cible).message);
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
    var msg = 'Revert "' + c.message + '"';
    var tete = repo.tete();
    var nh = repo.nouveauCommit(nouveau, [tete], msg, vm.horloge);
    repo.refs[repo.branche] = nh;
    appliqueCommit(vm, racine, repo, nh);
    note(repo, 'revert: ' + msg);
    r.dire('[' + repo.branche + ' ' + nh.slice(0, 7) + '] ' + msg);
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
    var res = [], i = 0, conflit = false;
    function chevauche(a, b) { return a.debut <= b.fin && b.debut <= a.fin; }
    while (i <= lb.length) {
      var cn = null, ce = null;
      mn.forEach(function (m) { if (m.debut === i) cn = m; });
      me.forEach(function (m) { if (m.debut === i) ce = m; });
      if (cn && ce) {
        if (cn.lignes.join('\n') === ce.lignes.join('\n')) {
          cn.lignes.forEach(function (l) { res.push(l); });
        } else {
          conflit = true;
          res.push('<<<<<<< ' + nomNous);
          cn.lignes.forEach(function (l) { res.push(l); });
          res.push('=======');
          ce.lignes.forEach(function (l) { res.push(l); });
          res.push('>>>>>>> ' + nomEux);
        }
        i = Math.max(cn.fin, ce.fin);
        if (cn.fin !== ce.fin) {
          for (var k = Math.min(cn.fin, ce.fin); k < i; k++) { /* zone consommee */ }
        }
        continue;
      }
      if (cn) { cn.lignes.forEach(function (l) { res.push(l); }); i = cn.fin; continue; }
      if (ce) { ce.lignes.forEach(function (l) { res.push(l); }); i = ce.fin; continue; }
      if (i < lb.length) res.push(lb[i]);
      i++;
    }
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
        conflits[f] = { base: b, nous: l, eux: d, texte: fu.texte };
      } else {
        arbre[f] = enregistreBlob(repo, fu.texte);
      }
    });
    auto.forEach(function (f) { r.dire('Auto-merging ' + f); });
    if (Object.keys(conflits).length) {
      Object.keys(conflits).forEach(function (f) {
        vm.ecrire(racine + '/' + f, conflits[f].texte);
        r.dire('CONFLICT (content): Merge conflict in ' + f);
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
      r.dire('fatal: Not possible to fast-forward, aborting.');
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
      lignesArt.push({ art: tete.join(' '), commit: x });

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
      if (propre.length < colonnes.length && parents.length <= 1) {
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
      tete = repo.nouveauCommit(arbre, [tete], cc.message, vm.horloge);
    }
    repo.refs[repo.branche] = tete;
    appliqueCommit(vm, racine, repo, tete);
    r.dire('Successfully rebased and updated refs/heads/' + repo.branche + '.');
    return true;
  }
