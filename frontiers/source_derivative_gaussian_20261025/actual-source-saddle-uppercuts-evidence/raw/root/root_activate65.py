from pathlib import Path
from datetime import datetime,timezone
import json
pub=Path(__file__).resolve().parent
construct=Path("/workspace/scratch/actual-source-saddle-uppercuts-construct")
g=json.loads((pub/"ROOT_GO65_TEMPLATE.json").read_text())
if (construct/"ROOT_GO.json").exists() or Path(g["source_path"]).exists():raise RuntimeError("Unexpected65GO/sourcealreadyexists; do notrerun")
construct.mkdir(exist_ok=True)
source=Path("/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SOURCE_ACTUAL_SADDLE_UPPERCUTS_CONTROLS.md")
data=source.read_bytes()
if len(data)!=13258:raise RuntimeError("Unexpectedcompleteadoptedcontrolssize")
(construct/"CONTROL_CONTRACT.md").write_bytes(data)
copied={"completed_utc":datetime.now(timezone.utc).isoformat(),"source":str(source),"destination":str(construct/"CONTROL_CONTRACT.md"),"bytes":len(data),"sha256_reused":"7672542a7bb8bfeb2344770dbc0ce6e7c12c96cbe1b380fec700535419b9c6c8","origin":"Existingproper65FIRSTIDreused/EXACTbytecopy/NOREHASH","ordering":"COMPLETEcontrols copy BEFORE GO and ANY65source/helperproof/control/harness"}
(pub/"ROOT_CONTROL_CONTRACT_COPY.json").write_text(json.dumps(copied,indent=2)+"\n")
g["issued_utc"]=datetime.now(timezone.utc).isoformat();g["complete_controls_copy"]=copied
g["proper_PRECODE_publication"]={"normal_publication":"ee5b141d5ff41a0a9040256a8025690ec22d7266","push_completed_utc":"2026-10-28T20:50:41.964561+00:00","native_SPEC_blob":"0de1a743cae06244f261af371393f16d3dae8425","before_ANY65code":True,"excluded64_manifest_archive_registry":True,"four_initial_IDs_reused":True}
(construct/"ROOT_GO.json").write_text(json.dumps(g,indent=2)+"\n")
(pub/"ROOT_GO65_COPY.json").write_text(json.dumps(g,indent=2)+"\n")
(pub/"ROOT_PRECODE_PUBLICATION.json").write_text(json.dumps(g["proper_PRECODE_publication"],indent=2)+"\n")
print(json.dumps({"issued_utc":g["issued_utc"],"status":g["status"],"complete_controls_copy":copied,"source_path":g["source_path"],"helper":g["helpers"]["B"],"checkpoint_utc":g["checkpoint_utc"],"hard_terminal_utc":g["hard_terminal_utc"]},indent=2))
