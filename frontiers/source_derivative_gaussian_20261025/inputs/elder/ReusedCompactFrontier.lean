/-
Reused compact-image frontier support. No new mathematical target.
Exact accepted origin: commit 5f49444d13b9c322f5214e11bc3936b2271b615f
path frontiers/cap_first_exit_lean_20261002/CapFirstExit.lean, lines 357-369.
Original namespace and implicit context are retained. Only this theorem is extracted;
Mathlib's umbrella import is replaced by one finite topology import.
Accepted proof bytes and source custody: /workspace/scratch/reused-compact-frontier/BINDINGS.json.
-/
import Mathlib.Topology.Separation.Hausdorff

open Set

namespace CapFirstExit

variable {X : Type*} [TopologicalSpace X]

/-- Frontier of a compact image. If `e` is continuous and open, `X` is Hausdorff and `C` is
compact, every frontier point of `e '' C` is the image of a frontier point of `C`. -/
theorem frontier_image_subset {Y : Type*} [TopologicalSpace Y] [T2Space X] {e : Y → X}
    (hec : Continuous e) (heo : IsOpenMap e) {C : Set Y} (hC : IsCompact C) :
    frontier (e '' C) ⊆ e '' frontier C := by
  intro x hx
  have hcl : IsClosed (e '' C) := (hC.image hec).isClosed
  have hx1 : x ∈ e '' C := by
    have h := hx.1
    rwa [hcl.closure_eq] at h
  obtain ⟨y, hyC, rfl⟩ := hx1
  refine ⟨y, ⟨subset_closure hyC, fun hyi => hx.2 ?_⟩, rfl⟩
  exact interior_maximal (image_mono interior_subset) (heo _ isOpen_interior) ⟨y, hyi, rfl⟩

end CapFirstExit
