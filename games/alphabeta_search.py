"""
Alpha-Beta pruning (manual section 5.2) + a counting version that also logs every cut.
Only the indentation of the manual function was fixed; the logic is unchanged.
"""

try:
    from .minimax_search import LeafCounter
except ImportError:
    from minimax_search import LeafCounter


# ---------------- manual code (section 5.2) ----------------
def alphabeta(depth, index, maxTurn, scores, target, alpha, beta):
    if depth == target:
        return scores[index]

    if maxTurn:
        value = float('-inf')
        for i in range(2):
            value = max(value, alphabeta(depth+1, index*2+i, False, scores, target, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for i in range(2):
            value = min(value, alphabeta(depth+1, index*2+i, True, scores, target, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value


MANUAL_AB_LEAVES = [3, 5, 2, 9, 3, 5, 2, 9]


# ---------------- my counting version ----------------
def alphabeta_count(depth, index, is_max, leaves, max_depth, alpha, beta, counter, cut_log):
    if depth == max_depth:
        counter.hit(index)
        return leaves[index]
    best = float("-inf") if is_max else float("inf")
    for child in (2 * index, 2 * index + 1):
        result = alphabeta_count(depth + 1, child, not is_max, leaves, max_depth,
                                 alpha, beta, counter, cut_log)
        if is_max:
            best = max(best, result)
            alpha = max(alpha, best)
        else:
            best = min(best, result)
            beta = min(beta, best)
        if alpha >= beta:
            if child == 2 * index:   # the right child is skipped
                role = "MAX" if is_max else "MIN"
                cut_log.append(f"{role} node at level {depth}, position {index}: "
                               f"alpha={alpha} >= beta={beta} -> right branch pruned")
            break
    return best
