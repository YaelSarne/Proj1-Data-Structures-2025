import time
import matplotlib.pyplot as plt
from AVLTree import AVLTree, AVLNode

# -------------------------------------------------------------
# --- Helper functions to build minimum‑node AVL trees by height
# -------------------------------------------------------------

def create_min_nodes_avl_tree_by_height(h, current_key):
    """
    Recursively builds an AVL subtree that contains the *minimum* number of
    real nodes possible for a given height h (i.e. the classic Fibonacci
    construction for AVL worst‑case trees).

    Parameters
    ----------
    h : int
        Desired subtree height.
    current_key : list[int]
        Single‑item list that acts as a mutable counter to guarantee every
        key inserted is unique across the whole tree.

    Returns
    -------
    AVLNode
        Root node of the newly‑built subtree. (Virtual nodes are represented
        by AVLNode() instances for convenience.)
    """
    if h == -1:                      # virtual (external) node
        return AVLNode()
    if h == 0:                       # leaf – just one real node
        current_key[0] += 1
        node = AVLNode(current_key[0], f"Val_{current_key[0]}")
        node.height = 0
        node.BF = 0                  # balance factor is 0 for leaves
        return node

    current_key[0] += 1
    root = AVLNode(current_key[0], f"Val_{current_key[0]}")

    # Left child gets the bigger of the two sub‑heights (h‑1)
    root.left = create_min_nodes_avl_tree_by_height(h - 1, current_key)
    if root.left.is_real_node():
        root.left.parent = root

    # Right child gets the smaller sub‑height (h‑2)
    root.right = create_min_nodes_avl_tree_by_height(h - 2, current_key)
    if root.right.is_real_node():
        root.right.parent = root

    # Update cached metadata
    left_h  = root.left.height
    right_h = root.right.height
    root.height = 1 + max(left_h, right_h)
    root.BF     = left_h - right_h

    return root


def build_fibonacci_avl_tree_by_height(h):
    """Convenience wrapper that returns a full *AVLTree* object."""
    tree = AVLTree()
    if h == -1:
        return tree

    key_counter = [0]
    tree.root = create_min_nodes_avl_tree_by_height(h, key_counter)

    # --- compute auxiliary fields -------------------------------------
    def count_nodes(node):
        if not node or not node.is_real_node():
            return 0
        return 1 + count_nodes(node.left) + count_nodes(node.right)

    def count_bf_zero(node):
        if not node or not node.is_real_node():
            return 0
        here = 1 if node.BF == 0 else 0
        return here + count_bf_zero(node.left) + count_bf_zero(node.right)

    tree._size       = count_nodes(tree.root)
    tree.bf_zero_cnt = count_bf_zero(tree.root)

    # store pointer to maximum‑key node (useful for some ops)
    curr = tree.root
    while curr and curr.right.is_real_node():
        curr = curr.right
    tree.max_node = curr

    return tree

# ----------------------------------------------------------------------
# --- Utility: explicit leaf count (definition‑based, not BF‑based)
# ----------------------------------------------------------------------

def count_leaves_in_avl(node):
    """Returns the number of *real* leaf nodes in the subtree rooted at *node*."""
    if not node or not node.is_real_node():
        return 0
    if not node.left.is_real_node() and not node.right.is_real_node():
        return 1
    return count_leaves_in_avl(node.left) + count_leaves_in_avl(node.right)

# ----------------------------------------------------------------------
# --- Analysis & visualisation – *indexed by total node count* ---------
# ----------------------------------------------------------------------

def analyze_fibonacci_trees_by_nodes(max_total_nodes):
    """
    Build an increasing sequence of *minimum‑node* AVL trees until the number
    of nodes exceeds *max_total_nodes*.  For each tree collect:
        • height (h)
        • total real nodes (n)
        • number of leaves (== nodes with BF == 0)
        • leaves / total ratio

    Returned in a list of dicts (one per tree).
    """
    print("\n--- Fibonacci Tree Data Table (indexed by TOTAL NODES) ---")
    print(f"{'Nodes (n)':<12} | {'Height (h)':<10} | {'Leaves':<10} | {'Leaf/Total Ratio':<17}")
    print("-" * 60)

    results = []
    h = 0
    while True:
        fib_tree = build_fibonacci_avl_tree_by_height(h)
        total_nodes = fib_tree.size()
        if total_nodes == 0 or total_nodes > max_total_nodes:
            break

        leaves     = fib_tree.bf_zero_cnt
        ratio      = leaves / total_nodes

        results.append({
            'height': h,
            'total_nodes': total_nodes,
            'leaves': leaves,
            'ratio': ratio
        })

        print(f"{total_nodes:<12} | {h:<10} | {leaves:<10} | {ratio:<17.4f}")
        h += 1

    # quick consistency check – BF==0 vs explicit leaf definition
    print("-" * 60)
    mismatch = next((r for r in results if count_leaves_in_avl(build_fibonacci_avl_tree_by_height(r['height']).get_root()) != r['leaves']), None)
    if mismatch is None:
        print("**Validation: BF==0 count equals explicit leaf count for every tree.**")
    else:
        print("**WARNING: mismatch detected for height", mismatch['height'], "**")
    print("------------------------------------------------------------\n")

    return results

# ----------------------------------------------------------------------
# --- Plotting ---------------------------------------------------------
# ----------------------------------------------------------------------

def plot_fibonacci_tree_ratio_by_nodes(data, save_path=None):
    """Scatter/line plot of leaf/total ratio as a function of TOTAL NODES."""
    x_nodes = [d['total_nodes'] for d in data]
    ratios  = [d['ratio']       for d in data]

    plt.figure(figsize=(10, 6))
    plt.plot(x_nodes, ratios, marker='o', linestyle='-')  # default colour

    plt.title('Leaf‑to‑Total‑Nodes Ratio in Fibonacci AVL Tree vs. Total Nodes')
    plt.xlabel('Total Real Nodes (n)')
    plt.ylabel('Leaf‑to‑Total‑Nodes Ratio')
    plt.grid(True)

    for i, txt in enumerate(ratios):
        plt.annotate(f"{txt:.4f}", (x_nodes[i], ratios[i]), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.ylim(0, max(ratios) * 1.1)

    if save_path:
        plt.savefig(save_path)
        print(f"Graph saved successfully to: {save_path}")

    plt.show()

# ----------------------------------------------------------------------
# --- Main entry‑point -------------------------------------------------
# ----------------------------------------------------------------------

if __name__ == "__main__":
    # Experiment up to ~10k real nodes by default; tweak as you like.
    MAX_NODES = 70

    analysis_results = analyze_fibonacci_trees_by_nodes(MAX_NODES)

    print("\n--- Creating Graph ---")
    plot_fibonacci_tree_ratio_by_nodes(
        analysis_results,
        save_path="fibonacci_ratio_graph_by_nodes.png"
    )
