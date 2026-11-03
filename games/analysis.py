"""
Tasks 2 and 3 - compare Minimax and Alpha-Beta, then test move ordering.
"""
import math

try:
    from .alphabeta_search import MANUAL_AB_LEAVES, alphabeta, alphabeta_count
    from .minimax_search import LeafCounter, manual_tree, minimax, minimax_count
except ImportError:
    from alphabeta_search import MANUAL_AB_LEAVES, alphabeta, alphabeta_count
    from minimax_search import LeafCounter, manual_tree, minimax, minimax_count

INF = float("inf")

# my own extra tree for the ordering experiment
MY_TREE = [4, 8, 1, 6, 7, 2, 9, 3]


def both(leaves, depth):
    mm, ab, cuts = LeafCounter(), LeafCounter(), []
    v_mm = minimax_count(0, 0, True, leaves, depth, mm)
    v_ab = alphabeta_count(0, 0, True, leaves, depth, -INF, INF, ab, cuts)
    return v_mm, mm.count, v_ab, ab.count, ab.order, cuts


def flip_subtree(leaves, depth, level, position):
    """Swap the left and right halves under one node."""
    out = list(leaves)
    size = 2 ** (depth - level)
    start = position * size
    half = size // 2
    left, right = out[start:start + half], out[start + half:start + size]
    out[start:start + size] = right + left
    return out


def sort_children(leaves, depth, best_first):
    """Reorder every node so its best (or worst) child for that player comes first."""
    def build(lo, hi, level, is_max):
        if level == depth:
            return [leaves[lo]], leaves[lo]
        mid = (lo + hi) // 2
        left, lv = build(lo, mid, level + 1, not is_max)
        right, rv = build(mid, hi, level + 1, not is_max)
        left_is_best = lv >= rv if is_max else lv <= rv
        left_first = left_is_best if best_first else not left_is_best
        value = max(lv, rv) if is_max else min(lv, rv)
        return (left + right if left_first else right + left), value
    return build(0, len(leaves), 0, True)[0]


def compare_tree(name, leaves, depth):
    v_mm, n_mm, v_ab, n_ab, order, cuts = both(leaves, depth)
    print(f"{name}: leaves {leaves}")
    print(f"  Minimax    -> value {v_mm}, {n_mm} leaves evaluated")
    print(f"  Alpha-Beta -> value {v_ab}, {n_ab} leaves evaluated (positions {order})")
    for c in cuts:
        print(f"    cut: {c}")
    print(f"  same value: {v_mm == v_ab}, leaves saved: {n_mm - n_ab}")


def ordering_experiment(name, leaves, depth):
    tests = [
        ("best child first everywhere", sort_children(leaves, depth, True)),
        ("as given", leaves),
        ("root branches swapped", flip_subtree(leaves, depth, 0, 0)),
        ("left MIN children swapped", flip_subtree(leaves, depth, 1, 0)),
        ("right MIN children swapped", flip_subtree(leaves, depth, 1, 1)),
        ("worst child first everywhere", sort_children(leaves, depth, False)),
    ]
    print(f"{name}:")
    print("  ordering                     | value MM | value AB | leaves MM | leaves AB | pruned")
    for label, tree in tests:
        v_mm, n_mm, v_ab, n_ab, _, _ = both(tree, depth)
        print(f"  {label:<28} | {v_mm:<8} | {v_ab:<8} | {n_mm:<9} | {n_ab:<9} | {n_mm - n_ab}")


def run():
    mm_leaves, mm_depth = manual_tree()
    ab_leaves = list(MANUAL_AB_LEAVES)
    ab_depth = int(math.log2(len(ab_leaves)))
    my_depth = int(math.log2(len(MY_TREE)))

    print("-" * 70)
    print("Section 5.2 | Alpha-Beta on the manual scores")
    print("-" * 70)
    print("alphabeta(...) =", alphabeta(0, 0, True, ab_leaves, ab_depth, -INF, INF))
    print()
    print("-" * 70)
    print("Task 2 | Leaf evaluations: Minimax vs Alpha-Beta")
    print("-" * 70)
    compare_tree("Manual 5.2 tree", ab_leaves, ab_depth)
    print()
    compare_tree("Manual 5.1 tree (padded)", mm_leaves, mm_depth)
    print()
    compare_tree("My tree", MY_TREE, my_depth)
    print()
    print("Reference check with the manual functions (root values):")
    for label, leaves, depth in (("5.1", mm_leaves, mm_depth), ("5.2", ab_leaves, ab_depth), ("mine", MY_TREE, my_depth)):
        print(f"  {label}: minimax = {minimax(0, 0, True, leaves, depth)}, "
              f"alphabeta = {alphabeta(0, 0, True, leaves, depth, -INF, INF)}")
    print()
    print("-" * 70)
    print("Task 3 | Move ordering changes pruning, never the value")
    print("-" * 70)
    ordering_experiment("Manual 5.2 tree", ab_leaves, ab_depth)
    print()
    ordering_experiment("My tree", MY_TREE, my_depth)
    print()
    print("Note on padding (5.1 tree):")
    for pad in (0, 99):
        tree = [3, 5, 2, 9, 0, 7] + [pad, pad]
        print(f"  padding with {pad:<2} -> value {minimax(0, 0, True, tree, 3)}")
    print("  The padded zeros behave like real moves for MIN. Without them the right")
    print("  MIN node only has the branch (0, 7) = 7, so the true value would be 7.")
