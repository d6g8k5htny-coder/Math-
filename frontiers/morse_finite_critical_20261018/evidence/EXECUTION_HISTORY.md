# Preserved execution and aggregation corrections

The first complete author proof compiled with four deprecated alias warnings.
Replacing only those aliases produced the frozen 9,445-byte clean proof; both
author attempts and their logs remain in the immutable native handoff. The
first root control attempt failed at scalar-product simplification and pair
syntax; the corrected source compiled cleanly and is included here.

The development axiom census reached its 240-second timeout. Its failure is
preserved. The final audit phase alone received a 900-second bound informed by
an actual earlier 458.5-second census; the present final audit completed in
173.75 seconds. This does not assert that 900 seconds was fully needed.

Final preparation twice stopped before freezing/building: it first incorrectly
required a compiled library directory for the uncompiled `Cli` package, then
compared Path-ordering to string-ordering despite identical 83,897 unique
artifact sets. Pin checks were retained, actual existing import roots were
used, and both sides were compared in canonical string order. Unique failed
starts and diagnostic evidence remain preserved. The third preparation
succeeded. All eight final execution phases passed without a failed final run.

Before the first artifact-master invocation, the nonauthor reviewer found that
its initial line-by-line census regex missed wrapped axiom lists (131 rather
than 169 declarations). The author replaced only that aggregation block with
a bounded full-text parser and raw-marker completeness checks. The exact
AST-extracted block passed the actual full census and rejected six malformed
controls. This check did not invoke or consume the final master. The master
still verifies artifact bindings; it is not a proof engine.

The first early native checkpoint used a non-UUID identifier and is retained as
history, not a valid R17 event. A later proper-UUID checkpoint explicitly
corrected it; the original valid claim was unaffected. The scheduled 02:45
checkpoint was missed and reported at the actual 02:57 renewal without
backdating. A subsequent actual 03:19 checkpoint was recorded before the
03:30 deadline. Transient transport failures were preserved and checked through
bounded readback; they are not credential or code failures.
