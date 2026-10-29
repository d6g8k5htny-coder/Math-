"""Isolated native checker controls, never admitted owned proof modules."""
import re

REASONS = {"wrong_type": "OWN_REJECT_BODY_TYPE", "open_body": "OWN_REJECT_OPEN_BODY",
           "universe": "OWN_REJECT_DECLARATION", "axiom": "OWN_REJECT_FORBIDDEN_AXIOM"}


def require(condition, message):
    if not condition: raise ValueError(message)


def render_control(kind, namespace="OwnedKernelAudit"):
    require(namespace in {"OwnedKernelAudit", "OwnedKernelAuditMutation"}, "unknown control namespace")
    require(kind in REASONS, "unknown native rejection control")
    header="import "+namespace+".Support\nopen Lean\n"
    if kind=="axiom":
        body=r'''
axiom OwnedKernelControl.Bad : False
#eval show CoreM Unit from do
  let ci : ConstantInfo := .thmInfo {
    name := `OwnedKernelControl.Fabricated,
    levelParams := [], type := mkConst ``False, value := mkConst ``OwnedKernelControl.Bad}
  let (_, closure) ← (CHECKER.collectEntry (← getEnv) ci).run {}
  CHECKER.permitted closure
  IO.println "OWN_CONTROL_ESCAPED|axiom"
'''
    elif kind=="universe":
        body=r'''
#eval show CoreM Unit from do
  let u := Level.param `unlistedUniverse
  let type := Expr.forallE `α (.sort u) (.forallE `x (.bvar 0) (.bvar 1) .default) .default
  let value := Expr.lam `α (.sort u) (.lam `x (.bvar 0) (.bvar 0) .default) .default
  let ci : ConstantInfo := .defnInfo {
    name := `OwnedKernelControl.BadUniverse,
    levelParams := [], type := type, value := value, hints := .opaque, safety := .safe}
  CHECKER.checkedBody (← getEnv) ci
  IO.println "OWN_CONTROL_ESCAPED|universe"
'''
    else:
        value="mkConst ``True.intro" if kind=="wrong_type" else "Expr.bvar 0"
        body=("#eval show CoreM Unit from do\n"
              "  let ci : ConstantInfo := .thmInfo {\n"
              "    name := `OwnedKernelControl.Fabricated,\n"
              "    levelParams := [], type := mkConst ``False, value := "+value+"}\n"
              "  CHECKER.checkedBody (← getEnv) ci\n"
              '  IO.println "OWN_CONTROL_ESCAPED|'+kind+'"\n')
    return header+body.replace("CHECKER",namespace)


def render_insertion_mutant(support):
    marker="match env.addDeclCore 0 0 declaration none true with"
    require(support.count(marker)==1, "checked-insertion mutation anchor changed")
    require(support.count("#eval OwnedKernelAudit.dumpInventory")==1, "inventory mutation anchor changed")
    return support.replace(marker,"match env.addDeclCore 0 0 declaration none false with").replace(
        "#eval OwnedKernelAudit.dumpInventory","").replace("OwnedKernelAudit","OwnedKernelAuditMutation")


def validate_rejection(receipt, text, kind):
    require(kind in REASONS,"unknown rejection expectation")
    require(type(receipt["returncode"]) is int and receipt["returncode"]>0
            and receipt["succeeded"] is False and receipt["timed_out"] is False
            and receipt["output_limit_exceeded"] is False and receipt["failure"] is None,
            "expected rejection was not an ordinary bounded compiler failure")
    # A reason embedded in a path, echoed source, or an unrelated diagnostic is
    # not evidence that the intended checker branch rejected the control.
    diagnostic = re.compile(r"(?:.*:\d+:\d+:\s*)?error:\s*"+re.escape(REASONS[kind]))
    require(any(diagnostic.fullmatch(line) for line in text.splitlines())
            and ("OWN_CONTROL_ESCAPED|"+kind) not in text.splitlines(),
            "native control failed for the wrong reason or escaped")
    return {"control":kind,"expected_rejection":REASONS[kind],"observed":True}


def validate_mutant_escape(receipt,text):
    require(receipt["succeeded"] is True and type(receipt["returncode"])is int and receipt["returncode"]==0
            and receipt["timed_out"] is False and receipt["output_limit_exceeded"] is False
            and receipt["failure"] is None,"mutant did not execute successfully")
    require(text.splitlines().count("OWN_CONTROL_ESCAPED|universe")==1,"mutant control did not reach the weakened check")
    try: validate_rejection(receipt,text,"universe")
    except ValueError: return {"control":"checked-insertion-mutant","mutation_killed":True,"expected_control_escaped":True}
    raise ValueError("weakened checker survived its original rejection control")


def render_graph_control(kind):
    require(kind in {"self_cycle","mutual_cycle"},"unknown graph control")
    suffixes=["Self"] if kind=="self_cycle" else ["Left","Right"]
    names=["OwnedKernelControl."+x for x in suffixes]
    pairs=[(names[0],names[0])] if len(names)==1 else [(names[0],names[1]),(names[1],names[0])]
    source="import OwnedKernelAudit.Support\nopen Lean\n"
    source+="".join("theorem "+name+" : True := True.intro\n" for name in names)
    source+="#eval show CoreM Unit from do\n  let pairs : List (Name × Name) := ["+", ".join("(`"+a+", `"+b+")" for a,b in pairs)+"]\n"
    source+=r'''
  let names := pairs.map Prod.fst
  for (name, target) in pairs do
    let ci : ConstantInfo := .thmInfo {
      name := name, levelParams := [],
      type := mkConst ``True, value := mkConst target}
    OwnedKernelAudit.checkedBody (← getEnv) ci
    let mut dependencies : NameSet := {}
    for expr in OwnedKernelAudit.expressions ci do
      for dep in expr.getUsedConstants do
        if names.contains dep then dependencies := dependencies.insert dep
    let encoded := (dependencies.toArray.map OwnedKernelAudit.enc).qsort (· < ·)
    IO.println s!"OWN_GRAPH_NODE|{OwnedKernelAudit.enc name}|{String.intercalate "," encoded.toList}"
  IO.println s!"OWN_GRAPH_COMPLETE|{pairs.length}"
'''
    return source,names


def validate_graph_control(text,kind,encode_dotted,cycle_checker):
    _,names=render_graph_control(kind); expected={encode_dotted(name) for name in names}
    graph={};complete=None
    for line in text.splitlines():
        if not line:continue
        fields=line.split("|")
        if fields[0]=="OWN_GRAPH_NODE":
            require(len(fields)==3 and fields[1]in expected and fields[1]not in graph,"invalid native graph control row")
            deps=fields[2].split(",")if fields[2]else[]
            require(len(set(deps))==len(deps)and set(deps)<=expected,"foreign graph control dependency")
            graph[fields[1]]=deps
        elif fields[0]=="OWN_GRAPH_COMPLETE":
            require(len(fields)==2 and complete is None and re.fullmatch(r"[1-9][0-9]*",fields[1]),"invalid graph completion")
            complete=int(fields[1])
        else:raise ValueError("unexpected native graph output")
    require(set(graph)==expected and complete==len(expected),"native graph control omitted a node")
    rows=[{"name":name,"id":"control::"+name,"body":"body"}for name in sorted(graph)]
    dependencies={"control::"+name:deps for name,deps in graph.items()}
    try:cycle_checker(rows,dependencies)
    except ValueError as exc:
        require("cycle"in str(exc),"graph failed for a non-cycle reason")
        return {"control":kind,"kernel_copy_accepted_trusted_references":True,"dependency_cycle_rejected":True}
    raise ValueError("native cyclic dependency control escaped")
