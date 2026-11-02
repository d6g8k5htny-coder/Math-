import collections,json,pathlib,re,sys
BASE=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
scope=sys.argv[1] if len(sys.argv)>1 else 'production'
module='SourceActualSaddleUppercuts' if scope=='production' else 'SaddleUppercutsControls'
namespace='I4SourceActualSaddleUppercuts' if scope=='production' else 'ActualSaddleUppercutsControls'
source=BASE/'frozen/FINAL_SOURCE.lean' if scope=='production' else BASE/'SaddleUppercutsControls.lean'
label='inventory001' if scope=='production' else 'ordinary-inventory001'
raw=(BASE/'runs'/label/'stdout.log').read_text()
text=source.read_text()
authored={m.group(3):(m.group(1) or '',m.group(2)) for m in re.finditer(r'^(private )?(theorem|def|abbrev|structure) ([A-Za-z0-9_]+)',text,re.M)}
props={'ClosedBranchFacts','InheritedCollar','UpperClause','UniformCutResult','CutoffEquality','nonnegativeUpperMutation'}
rows=[]
for line in raw.splitlines():
    if not line.startswith('INVENTORY|'): continue
    _,kind,name=line.split('|',2)
    short=name.split(namespace+'.',1)[1] if namespace+'.' in name else None
    if short is None:
        category='foreign_generated'
        explanation='New module-owned generated declaration in foreign namespace; not authored public scientific API'
    elif short in authored:
        private,decl=authored[short]
        if not private:
            category='public_prop_definition' if decl=='def' else 'public_prop_theorem'
        elif short in props:
            category='private_prop_structure' if decl=='structure' else 'private_prop_definition'
        elif decl=='theorem': category='private_authored_theorem'
        else: category='private_authored_data_definition'
        explanation='Exact authored declaration in frozen owned source'
    else:
        category='private_generated'
        explanation='Owned structure projection/constructor/recursor/equation/simp/proof auxiliary; never a supplied foreign-private API'
    rows.append({'name':name,'lean_kind':kind,'classification':category,'explanation':explanation})
match=re.search(r'COMPLETE_NEW_MODULE_INVENTORY\|'+module+r'\|(\d+)',raw)
assert match and int(match.group(1))==len(rows)
assert len({r['name'] for r in rows})==len(rows)
counts=dict(collections.Counter(r['classification'] for r in rows))
record={'module':module,'namespace':namespace,'scope':scope,'owned_constants':len(rows),
 'classification_counts':counts,'all_rows':rows,'collector':str(BASE/('Inventory.lean' if scope=='production' else 'ControlsInventory.lean')),
 'qualification_receipt':str(BASE/'runs'/label/'receipt.json'),
 'raw_complete_axiom_stream':str(BASE/'runs'/label/'stdout.log'),
 'axioms':'Every exact-owned constant recursively restricted to propext/Classical.choice/Quot.sound by actually passed collector',
 'ordinary_kernel':'NONE; production exactly-one kernel separately authorized' if scope!='production' else 'Pending exactly-one final production kernel after root release',
 'no_old_verification':'Only genuinely new owned module scope; all prior checks reused'}
out=BASE/('INVENTORY_CLASSIFIED.json' if scope=='production' else 'CONTROLS_INVENTORY_CLASSIFIED.json')
out.write_text(json.dumps(record,indent=2)+'\n')
tsv=out.with_suffix('.tsv'); tsv.write_text('name\tlean_kind\tclassification\n'+''.join(r['name']+'\t'+r['lean_kind']+'\t'+r['classification']+'\n' for r in rows))
print(json.dumps({'scope':scope,'owned_constants':len(rows),'counts':counts,'classification':str(out)}))
