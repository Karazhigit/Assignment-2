TREE = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F", "G"],
    "D": ["H", "I"],
    "E": ["J", "K"],
    "F": ["L", "M"],
    "G": ["N", "O"],
}

UTILITY = {
    "H": 3,
    "I": 12,
    "J": 8,
    "K": 2,
    "L": 4,
    "M": 6,
    "N": 14,
    "O": 5,
}


def children(node, reverse):
    result = TREE[node]
    return result[::-1] if reverse else result


def minimax(node, maximizing, stats, reverse=False):
    stats["nodes"] += 1

    if node in UTILITY:
        return UTILITY[node], None

    best_value = float("-inf") if maximizing else float("inf")
    best_move = None

    for child in children(node, reverse):
        value, _ = minimax(child, not maximizing, stats, reverse)

        if (
            best_move is None
            or (maximizing and value > best_value)
            or (not maximizing and value < best_value)
        ):
            best_value = value
            best_move = child

    return best_value, best_move


def alpha_beta(
    node, maximizing, alpha, beta, stats, reverse=False
):
    stats["nodes"] += 1

    if node in UTILITY:
        return UTILITY[node], None

    best_value = float("-inf") if maximizing else float("inf")
    best_move = None
    ordered = children(node, reverse)

    for index, child in enumerate(ordered):
        value, _ = alpha_beta(
            child, not maximizing, alpha, beta, stats, reverse
        )

        if (
            best_move is None
            or (maximizing and value > best_value)
            or (not maximizing and value < best_value)
        ):
            best_value = value
            best_move = child

        if maximizing:
            alpha = max(alpha, best_value)
        else:
            beta = min(beta, best_value)

        if alpha >= beta:
            for skipped in ordered[index + 1:]:
                stats["pruned_branches"].append((node, skipped))
            break

    return best_value, best_move


def run_experiment(reverse=False):
    mm_stats = {"nodes": 0}
    ab_stats = {"nodes": 0, "pruned_branches": []}

    mm_value, mm_move = minimax("A", True, mm_stats, reverse)

    ab_value, ab_move = alpha_beta(
        "A",
        True,
        float("-inf"),
        float("inf"),
        ab_stats,
        reverse,
    )

    assert (mm_value, mm_move) == (ab_value, ab_move)

    print("Order:", "Right-to-left" if reverse else "Left-to-right")
    print("Depth:", 3)
    print("Minimax nodes:", mm_stats["nodes"])
    print("Alpha-beta nodes:", ab_stats["nodes"])
    print("Pruned nodes:", mm_stats["nodes"] - ab_stats["nodes"])
    print("Pruned branches:", ab_stats["pruned_branches"])
    print("Decision:", ab_move)
    print("Utility:", ab_value)
    print()


run_experiment()
run_experiment(reverse=True)
