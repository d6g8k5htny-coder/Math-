import pathlib,json,difflib,hashlib
p=pathlib.Path('/workspace/scratch/gap-conditional-morse-distinct-construct')
s=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceGapConditionalMorseDistinct.lean').read_text()
names=['global-cover','incidence','finite-frame','lifetime-geometry','actual-controls']
originals={n:(p/('helper-'+n+'-frozen')/'SECTION.lean.txt').read_text() for n in names}
starts={n:originals[n].splitlines()[0] for n in names}
sections={}
for i,n in enumerate(names[:4]):
 a=s.index(starts[n]);b=s.index(starts[names[i+1]],a) if i<3 else s.index('private theorem source_directionX_eq',a)
 sections[n]=s[a:b]
c=(p/'GapMorseDistinctControls.lean').read_text();sections['actual-controls']=c[c.index(starts['actual-controls']):]
o=p/'helper-amendments';o.mkdir(exist_ok=True)
records=[]
patch=''
for n in names:
 (o/(n+'-actual-section.lean.txt')).write_text(sections[n])
 d=''.join(difflib.unified_diff(originals[n].splitlines(True),sections[n].splitlines(True),fromfile='frozen-original/'+n,tofile='qualified-integration/'+n))
 (o/(n+'.patch')).write_text(d);patch+=d
 records.append({'helper':n,'original_directory':'helper-'+n+'-frozen/','original_identity_source':{'global-cover':'HELPER_D_ORIGINAL_IDENTITIES.json','incidence':'helper-incidence-frozen/FROZEN_HELPER.json','finite-frame':'helper-finite-frame-frozen/FROZEN_HELPER.json','lifetime-geometry':'helper-lifetime-geometry-frozen/FROZEN_IDENTITIES.json','actual-controls':'helper-actual-controls-frozen/FROZEN_HELPER.json'}[n],'one_integration_record':'HELPER_INTEGRATION.json','integration_count':1,'helper_executions':0,'complete_actual_section_snapshot':str(o/(n+'-actual-section.lean.txt')),'full_actual_amendment_patch':str(o/(n+'.patch')),'coverage':'Positive scratch Controls qualification only; NOT production kernel' if n=='actual-controls' else 'Final production strict/full actual module inventory/one production kernel'})
(o/'ALL_HELPER_AMENDMENTS.patch').write_text(patch)
draft=(p/'runs/complete-assembly-009/SourceGapConditionalMorseDistinct.lean').read_text()
(o/'PUBLIC_PROOF_PASSED009_TO_FINAL_PRIVATE_CONTROLS.patch').write_text(''.join(difflib.unified_diff(draft.splitlines(True),s.splitlines(True),fromfile='passed009-draft',tofile='final-source')))
(p/'AUTHOR_HELPER_LINEAGE.json').write_text(json.dumps({'originals_preserved_immutable':True,'original_old_file_hash_operations':0,'records':records,'root_original_reading_reused':'/workspace/scratch/gap-conditional-morse-distinct-publication/ROOT_ORIGINAL_HELPER_READING59.json','actual_amendments':'helper-amendments/ALL_HELPER_AMENDMENTS.patch','coverage_boundary':'Four production helper sections in one production object; fifth Controls-only helper in one separately qualified scratch object. No helper objects or independent executions. Evidence snapshots are copies for reading, not reintegrations.'},indent=2)+'\n')
