# ARM custody diagnostic

This temporary workflow executes the exact same real-Git and child-process controls in both modes on GitHub's ARM runner. It exists to observe defects while the x86 runner queue is saturated. Its result is diagnostic for that source and platform; it does not replace the documented x86 component, mutation, Lean or final federation gates. Run by pushing this branch or by workflow_dispatch once available. The workflow itself is verified by its actual hosted job admission and the unchanged test controls. Owner: none.
