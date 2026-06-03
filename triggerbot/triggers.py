# vibecoded project, i take no credit for it

_L1 = {
    "pedophilie": (3, ["pedophil","pedofil","mineur nu","enfant nu","zoophil","necrophil","bestialit"]),
    "inceste": (3, ["inceste","incestueux","incestueuse"]),
    "agression_sexuelle": (2, ["viol","violee","viole","attouchement","agresse sexuellement","force a","forcee a","harcelement","harcele","rapports sexuels","couchee avec","baisee"]),
    "automutilation": (2, ["scarif","scarrif","se couper","mutilation","mutiler","bruler la peau","se blesser","plaie ouverte","blessure ouverte","amputation","amputee","se fait saigner","saigner avec une lame","lame efficace"]),
    "suicide": (2, ["suicid","me tuer","en finir","idees noires","plus envie de vivre","passer a l'acte","tentative","mourir"]),
    "violence_meurtre": (2, ["je te tue","chte tue","je vais te tuer","te fracasser","te crever les yeux","te massacrer","te buter","te mettre a terre","arme a feu","flingue","pistolet","va crever","va mourir","creve","disparais"]),
    "domination_contexte": (2, ["t'es mon esclave","tes mon esclave","je te domine sale","a ma merci","tu m'appartiens","tu mappartiens","sale esclave","mon esclave"]),
}

_L2_extra = {
    "tca": (2, ["tca","anorexie","boulimie","se faire vomir","purge","restriction alimentaire"]),
    "drogues": (2, ["cocaine","heroine","crack","overdose","se droguer","se defoncer","shoot","avaler des cachets","surdose"]),
    "humiliation_grave": (2, ["tu fais pitie","t fais pitie","tant mieux que tu souffres","bien fait pour toi","tu meriterais","tu merites de souffrir","sale victime","sale faible","tes une sale","t'es une sale","personne t'aime","personne taime","tout le monde te deteste","personne te voudrait","t'es pas malade","tes pas malade","t'inventes","tinventes","c'est dans ta tete","cest dans ta tete","fais pas semblant","arrete de faire semblant"]),
    "couteau": (2, ["couteau","lame","rasoir","cutter"]),
    "mort_contexte": (2, ["cadavre","morgue","accident grave","hopital psychiatrique","hp psychiatrique"]),
}

_L3_extra = {
    "insultes_lourdes": (1, ["sale pute","grosse pute","sale chienne","sale merde","connasse","truie","cochonne","salope","grosse salope","sale salope","petasse","gouine","fdp","fils de pute","batard","batarde","ordure","dechet","poubelle humaine","rebut","garage a bites","je te chie","chie dessus","tu pues","t'es degueulasse","tes degueulasse","t'es repoussante","tes repoussante","t'es moche","tes moche","trop laide","immonde","hideuse","difforme"]),
    "domination_simple": (1, ["esclave","soumise","soumis","je te domine","chte domine","inferieure","a genoux","rampe","obeis","t'es rien","tes rien","t'es personne","tes personne","t'existes pas","texistes pas"]),
    "violence_verbale": (1, ["ta gueule","ferme ta gueule","je me moque","tout le monde se moque"]),
    "humiliation_corporelle": (1, ["trop grosse","trop moche","sale fragile","toute faible","sans defense","t'es faible","tes faible","t'es inferieure","tes inferieure"]),
    "isolement": (1, ["abandonne","abandonnee","rejete","rejetee","isole","isolee","tout seul","toute seule"]),
    "phobies_sensorielles": (1, ["araignee","arachnophobie","bruit fort","bruit soudain","bruits de bouche"]),
    "grossesse": (1, ["fausse couche","grossesse non desiree","avortement","ivg"]),
    "sang_mort_simple": (1, ["sang","saigner","mort","deces","enterrement"]),
}

LEVELS = {
    1: _L1,
    2: {**_L1, **_L2_extra},
    3: {**_L1, **_L2_extra, **_L3_extra},
}

THRESHOLDS = {1: 3, 2: 2, 3: 1}
