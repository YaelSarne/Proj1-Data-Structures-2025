import time
import matplotlib.pyplot as plt
import random
from AVLTree import AVLTree, AVLNode




# --- פונקציות חדשות לבניית עצי פיבונאצ'י וניתוחם ---

def create_min_nodes_avl_tree_by_height(h, current_key):
    """
    Creates an AVL tree with the minimum number of nodes for a given height h.
    This corresponds to the Fibonacci tree definition based on height.
    
    Parameters:
    h (int): The desired height of the tree.
    current_key (list): A list containing the next key to use, to ensure uniqueness.
    
    Returns:
    AVLNode: The root of the created subtree.
    """
    if h == -1: # Base case for virtual child
        return AVLNode() 
    if h == 0: # Base case: a single node tree (leaf)
        current_key[0] += 1
        node = AVLNode(current_key[0], f"Val_{current_key[0]}")
        node.height = 0
        node.BF = 0 # Leaf has BF = 0
        return node
    
    current_key[0] += 1
    root = AVLNode(current_key[0], f"Val_{current_key[0]}")
    
    # Left child is tree of height h-1
    root.left = create_min_nodes_avl_tree_by_height(h - 1, current_key)
    if root.left.is_real_node():
        root.left.parent = root
    
    # Right child is tree of height h-2
    root.right = create_min_nodes_avl_tree_by_height(h - 2, current_key)
    if root.right.is_real_node():
        root.right.parent = root
    
    # Update height and BF based on children's heights
    left_h = root.left.height 
    right_h = root.right.height
    
    root.height = 1 + max(left_h, right_h)
    root.BF = left_h - right_h
    
    return root

def build_fibonacci_avl_tree_by_height(h):
    """
    Builds an AVLTree object representing a Fibonacci tree of a given height h.
    
    Parameters:
    h (int): The desired height of the Fibonacci tree.
    
    Returns:
    AVLTree: An AVLTree object.
    """
    tree = AVLTree()
    if h == -1: # Represents an empty tree or virtual root for recursive calls
        return tree 
    
    key_counter = [0] 
    tree.root = create_min_nodes_avl_tree_by_height(h, key_counter)
    
    # Initialize _size and bf_zero_cnt after building the tree
    def count_nodes_recursive(node):
        if not node or not node.is_real_node():
            return 0
        return 1 + count_nodes_recursive(node.left) + count_nodes_recursive(node.right)

    def count_bf_zero_recursive(node):
        if not node or not node.is_real_node():
            return 0
        count = 0
        if node.BF == 0:
            count = 1
        return count + count_bf_zero_recursive(node.left) + count_bf_zero_recursive(node.right)

    tree._size = count_nodes_recursive(tree.root)
    tree.bf_zero_cnt = count_bf_zero_recursive(tree.root)
    
    # Set max_node for the created tree (it's the largest key)
    if tree.root:
        curr = tree.root
        while curr.right.is_real_node():
            curr = curr.right
        tree.max_node = curr
    
    return tree

# This function was missing and caused the NameError
def count_leaves_in_avl(node):
    """
    Counts leaves in a given AVL tree (considering virtual nodes).
    Leaves are real nodes whose children are virtual.
    """
    if not node or not node.is_real_node():
        return 0
    if not node.left.is_real_node() and not node.right.is_real_node():
        return 1 # This is a real node and its children are virtual, so it's a leaf
    return count_leaves_in_avl(node.left) + count_leaves_in_avl(node.right)


def analyze_fibonacci_trees_by_height(max_height):
    """
    Builds Fibonacci trees for various heights, calculates ratios, and displays them in a table.
    
    Parameters:
    max_height (int): The maximum height of the Fibonacci tree to test.
    """
    results = []
    print("\n--- Fibonacci Tree Data Table (by Height) ---")
    print(f"{'Height (h)':<10} | {'Total Nodes (n)':<17} | {'Number of Leaves':<18} | {'Leaf-to-Total Ratio':<20}")
    print("-" * 70)

    for h in range(0, max_height + 1): # Start from height 0
        fib_tree_avl = build_fibonacci_avl_tree_by_height(h)
        
        total_nodes = fib_tree_avl.size()
        leaves_count = fib_tree_avl.bf_zero_cnt # Using bf_zero_cnt

        ratio = leaves_count / total_nodes if total_nodes > 0 else 0
        
        results.append({
            'height': h,
            'total_nodes': total_nodes,
            'leaves': leaves_count,
            'ratio': ratio
        })

        print(f"{h:<10} | {total_nodes:<17} | {leaves_count:<18} | {ratio:<20.4f}")

    # Final validation message
    print("-" * 70)
    # Perform a quick check to see if count_leaves_in_avl matches bf_zero_cnt
    all_matched = True
    for res in results:
        temp_tree = build_fibonacci_avl_tree_by_height(res['height']) # Rebuild for verification
        # The line below caused the NameError, now fixed by adding count_leaves_in_avl back
        if temp_tree.size() > 0 and count_leaves_in_avl(temp_tree.get_root()) != res['leaves']:
            all_matched = False
            break

    if all_matched:
        print("**Validation: The number of leaves (by definition) matches the count of nodes with BF=0. The hint was accurate!**")
    else:
        print("**Warning: There is a discrepancy between leaf count by definition and BF=0 count.**")
    print("-------------------------------------------\n")

    return results 

# --- פונקציות גרף (ללא שינוי מהותי, רק עדכון שם הקריאה לנתונים) ---
import matplotlib.pyplot as plt

def plot_fibonacci_tree_ratio(data_for_plot, save_path=None):
    """
    Plots the Leaf-to-Total-Nodes Ratio vs. Tree Height based on provided data.
    
    Parameters:
    data_for_plot (list of dict): A list of dictionaries containing tree data (heights and ratios).
    save_path (str, optional): The file path to save the graph image (e.g., "fibonacci_ratio_graph.png").
                               If None, the graph will not be saved to a file.
    """
    # Note: 'height' is now directly from the data_for_plot, which makes the x-axis clean
    heights = [d['height'] for d in data_for_plot]
    ratios = [d['ratio'] for d in data_for_plot]

    plt.figure(figsize=(10, 6))
    plt.plot(heights, ratios, marker='o', linestyle='-', color='blue')
    
    plt.title('Leaf-to-Total-Nodes Ratio in Fibonacci AVL Tree vs. Tree Height')
    plt.xlabel('Tree Height')
    plt.ylabel('Leaf-to-Total-Nodes Ratio')
    plt.grid(True)
    
    unique_heights = sorted(list(set(heights)))
    plt.xticks(unique_heights) 
    
    plt.ylim(0, max(ratios) * 1.1)
    
    for i, txt in enumerate(ratios):
        plt.annotate(f'{txt:.4f}', (heights[i], ratios[i]), textcoords="offset points", xytext=(0,10), ha='center')

    if save_path:
        plt.savefig(save_path)
        print(f"Graph saved successfully to: {save_path}")

    plt.show()

# --- הפעלת הניתוח והגרף ---
if __name__ == "__main__":
    max_tree_height = 15 # Define the maximum height to test. (F15 from before goes up to height 9)

    # First, analyze and print the table based on height
    analysis_results_by_height = analyze_fibonacci_trees_by_height(max_tree_height)
    
    # Then, plot the graph using the collected results
    print("\n--- Creating Graph ---")
    plot_fibonacci_tree_ratio(analysis_results_by_height, save_path="fibonacci_ratio_graph_by_height.png")
