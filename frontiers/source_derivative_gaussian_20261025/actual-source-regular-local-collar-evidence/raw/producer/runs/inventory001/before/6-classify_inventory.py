import collections,json,pathlib,re,sys
B=pathlib.Path('/workspace/scratch/actual-source-regular-local-collar-construct')
scope=sys.argv[1] if len(sys.argv)>1 else 'production'
module='SourceActualRegularLocalCollar' if scope=='production' else 'RegularLocalCollarControls'
namespace='I4SourceActualRegularLocalCollar' if scope=='production' else 'RegularLocalCollarControls'
source=B/'frozen/FINAL_SOURCE.lean' if scope=='production' else B/'RegularLocalCollarControls.lean'
label='inventory001' if scope=='production' else 'ordinary-inventory001'
raw=(B/'runs'/label/'stdout.log').read_text()
text=source.read_text()
authored={m.group(3):(m.group(1) or '',m.group(2)) for m in re.finditer(r'^(private )?(theorem|def|abbrev|structure) ([A-Za-z0-9_]+)',text,re.M)}
props={'FixedCutChecks','FixtureOutput','omittedNonzeroDerivativeMutation'}
rows=[]
for line in raw.splitlines():
 if not line.startswith('INVENTORY|'):continue
 _,kind,name=line.split('|',2)
 short=name.split(namespace+'.',1)[1] if namespace+'.' in name else None
 if short is None:category='foreign_generated'
 elif short in authored:
  private,decl=authored[short]
  if not private:category='public_prop_definition' if decl=='def' else 'public_prop_theorem'
  elif short in props:category='private_prop_structure' if decl=='structure' else 'private_prop_definition'
  elif decl=='theorem':category='private_authored_theorem'
  else:category='private_authored_data_definition'
 else:category='private_generated'
 rows.append({'name':name,'lean_kind':kind,'classification':category})
match=re.search(r'COMPLETE_NEW_MODULE_INVENTORY\|'+module+r'\|(\d+)',raw)
assert match and int(match.group(1))==len(rows)
assert len({r['name'] for r in rows})==len(rows)
counts=dict(collections.Counter(r['classification'] for r in rows))
if scope=='production':assert counts.get('public_prop_theorem')==1 and not counts.get('public_prop_definition')
record={'module':module,'namespace':namespace,'scope':scope,'owned_constants':len(rows),'classification_counts':counts,'all_rows':rows,'collector':str(B/('Inventory.lean' if scope=='production' else 'ControlsInventory.lean')),'qualification_receipt':str(B/'runs'/label/'receipt.json'),'raw_complete_axiom_stream':str(B/'runs'/label/'stdout.log'),'standard_three_guard':'PASS: each exact owned constant recursively restricted to propext/Classical.choice/Quot.sound by actually passed collector','ordinary_kernel':'NONE; never covered by production kernel','production_kernel':'Pending separate root release; no preliminary own kernel','old_verification_replays':0}
out=B/('INVENTORY_CLASSIFIED.json' if scope=='production' else 'CONTROLS_INVENTORY_CLASSIFIED.json')
out.write_text(json.dumps(record,indent=2)+'\n')
out.with_suffix('.tsv').write_text('name\tlean_kind\tclassification\n'+''.join(r['name']+'\t'+r['lean_kind']+'\t'+r['classification']+'\n' for r in rows))
print(json.dumps({'scope':scope,'owned_constants':len(rows),'counts':counts,'classification':str(out)}))
