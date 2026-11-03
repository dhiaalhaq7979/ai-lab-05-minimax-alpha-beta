"""
Minimax (manual section 5.1) + my version that counts leaf evaluations.
The tree is a complete binary tree stored as a list of leaf scores.
Root = MAX, then the players alternate on every level.
"""
import math


# ---------------- manual code (section 5.1) ----------------
def minimax(curDepth, nodeIndex, maxTurn, scores, targetDepth):
    # Base case: targetDepth reached
    if curDepth == targetDepth:
        return scores[nodeIndex]

    if maxTurn:
        return max(
            minimax(curDepth + 1, nodeIndex * 2, False, scores, targetDepth),
            minimax(curDepth + 1, nodeIndex * 2 + 1, False, scores, targetDepth)
        )
    else:
        return min(
            minimax(curDepth + 1, nodeIndex * 2, True, scores, targetDepth),
            minimax(curDepth + 1, nodeIndex * 2 + 1, True, scores, targetDepth)
        )


def manual_tree():
    """Leaves from the manual, padded with zeros to a full binary tree."""
    scores = [3, 5, 2, 9, 0, 7]
    treeDepth = math.ceil(math.log2(len(scores)))
    scores += [0] * (2**treeDepth - len(scores))
    return scores, treeDepth


# ---------------- my additions ----------------
class LeafCounter:
    """Keeps track of how many leaves were evaluated and which ones."""

    def __init__(self):
        self.count = 0
        self.order = []

    def hit(self, index):
        self.count += 1
        self.order.append(index)


def minimax_count(depth, index, is_max, leaves, max_depth, counter):
    if depth == max_depth:
        counter.hit(index)
        return leaves[index]
    a = minimax_count(depth + 1, 2 * index, not is_max, leaves, max_depth, counter)
    b = minimax_count(depth + 1, 2 * index + 1, not is_max, leaves, max_depth, counter)
    return max(a, b) if is_max else min(a, b)


def backed_up_values(leaves, max_depth):
    """Value of every node, level by level (used to check my hand trace)."""
    levels = {max_depth: list(leaves)}
    for d in range(max_depth - 1, -1, -1):
        pick = max if d % 2 == 0 else min
        below = levels[d + 1]
        levels[d] = [pick(below[i], below[i + 1]) for i in range(0, len(below), 2)]
    return [levels[d] for d in range(max_depth + 1)]


def run():
    print("-" * 70)
    print("Task 1 | Minimax on the manual tree (section 5.1)")
    print("-" * 70)
    leaves, depth = manual_tree()
    print(f"leaves (padded) = {leaves}, depth = {depth}")
    print("The optimal value is:", minimax(0, 0, True, leaves, depth))
    print("Hand-trace check (backed-up values):")
    for d, values in enumerate(backed_up_values(leaves, depth)):
        who = "leaves" if d == depth else ("MAX" if d % 2 == 0 else "MIN")
        print(f"  level {d} [{who}]: {values}")
    counter = LeafCounter()
    value = minimax_count(0, 0, True, leaves, depth, counter)
    print(f"Counted minimax: value {value}, {counter.count}/{len(leaves)} leaves evaluated")


if __name__ == "__main__":
    run()
