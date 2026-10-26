import pathlib,re,json,hashlib,datetime,collections
b=pathlib.Path('/workspace/scratch/remote-jet-gaussian-construct');src=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceRemoteJetGaussian.lean');s=src.read_text();stream=(b/'runs/inventory-001/stdout.log').read_text()
written={};namespace='I4SourceRemoteJetGaussian'
for private,kind,name in re.findall(r'^(private )?(theorem|lemma|def) (\w+)',s,re.M):
 key=f'_private.SourceRemoteJetGaussian.0.{namespace}.{name}' if private else f'{namespace}.{name}'
 written[key]=('written_private_' if private else 'written_public_')+('theorem' if kind in ['theorem','lemma'] else 'def')
entries=[]
for kind,name in re.findall(r'^INVENTORY\|(\w+)\|(.+)$',stream,re.M):
 axs=re.search(r'^AXIOMS\|'+re.escape(name)+r'\|\[([^]]*)\]',stream,re.M).group(1)
 axioms=[x.strip() for x in axs.split(',') if x.strip()]
 assert set(axioms)<= {'propext','Classical.choice','Quot.sound'}
 category=written.get(name,'generated_theorem' if kind=='theorem' else 'generated_'+kind)
 entries.append({'name':name,'kind':kind,'classification':category,'axioms':axioms,'foreign_namespace_generated':not name.startswith(namespace+'.') and not name.startswith('_private.SourceRemoteJetGaussian.')})
assert len(entries)==int(re.search(r'COMPLETE_NEW_MODULE_INVENTORY\|SourceRemoteJetGaussian\|(\d+)',stream).group(1))==28
assert set(written)=={e['name'] for e in entries if e['classification'].startswith('written_')}
counts=dict(collections.Counter(e['classification'] for e in entries));assert counts['written_public_theorem']==4 and counts['written_public_def']==6
obj={'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'inventory_run':'inventory-001','constant_count':len(entries),'counts':counts,'foreign_namespace_generated':[e['name'] for e in entries if e['foreign_namespace_generated']],'entries':entries,'complete_actual_module_index':True,'foreign_namespace_inclusion_method':'env.getModuleIdxFor? equals actual module index, not namespace filter','standard_axioms_only':True,'written_research_targets':4,'generated_private_data_inventory_only':True}
(b/'INVENTORY.json').write_text(json.dumps(obj,indent=2)+'\n');(b/'TARGET_CLASSIFICATION.json').write_text(json.dumps({'counts':counts,'written_targets':[e for e in entries if e['classification']=='written_public_theorem'],'inventory_only':[e for e in entries if e['classification']!='written_public_theorem'],'foreign_namespace_generated':obj['foreign_namespace_generated']},indent=2)+'\n')
print(json.dumps({'count':len(entries),'counts':counts,'foreign':obj['foreign_namespace_generated']},indent=2))
