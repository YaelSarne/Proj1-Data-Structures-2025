import time
import matplotlib.pyplot as plt
import random
from AVLTree import AVLTree  # Import the AVLTree class from avl_tree.py
import math

# --- Binary Search Tree (BST) Implementation ---

class BSTNode:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

    def is_real_node(self):
        return self.key is not None

class BSTTree:
    def __init__(self):
        self.root = None
        self.max_node = None # Added for consistency with AVL's max_node concept

    def insert_from_root(self, key, value):
        new_node = BSTNode(key, value)
        if self.root is None:
            self.root = new_node
            self.max_node = new_node
            return

        current = self.root
        while True:
            if key < current.key:
                if current.left is None:
                    current.left = new_node
                    new_node.parent = current
                    break
                current = current.left
            else: # key >= current.key
                if current.right is None:
                    current.right = new_node
                    new_node.parent = current
                    if key > self.max_node.key: # Update max_node if necessary
                        self.max_node = new_node
                    break
                current = current.right

    def insert_from_max(self, key, value):
        new_node = BSTNode(key, value)
        if self.root is None:
            self.root = new_node
            self.max_node = new_node
            return

        # Go upwards from max_node until a node is found whose key is greater than or equal to the new key
        current = self.max_node
        while current and key < current.key:
            current = current.parent

        if current is None: # New key is smaller than all existing keys, insert from root as if from root
             self.insert_from_root(key, value) # Reuse insert_from_root for efficiency
             return

        # Now current.key <= key (if current is not None) or current is the root (if key is smaller than max_node but current's parent is None)
        # Descend from current to find the insertion point
        while True:
            if key < current.key:
                if current.left is None:
                    current.left = new_node
                    new_node.parent = current
                    break
                current = current.left
            else: # key >= current.key
                if current.right is None:
                    current.right = new_node
                    new_node.parent = current
                    if key > self.max_node.key: # Update max_node if necessary
                        self.max_node = new_node
                    break
                current = current.right

    def bst_to_array(self):
        result = []
        def inorder(node):
            if node is None:
                return
            inorder(node.left)
            result.append((node.key, node.value))
            inorder(node.right)
        inorder(self.root)
        return result

# --- Experiment Setup and Execution ---

def run_experiment(tree_type, insertion_method, input_type, data_sizes):
    times = []
    for size in data_sizes:
        if input_type == "sorted":
            data = list(range(size))
        elif input_type == "reversed":
            data = list(range(size - 1, -1, -1))
        else:
            raise ValueError("Invalid input_type")

        start_time = time.time()
        if tree_type == "BST":
            tree = BSTTree()
            if insertion_method == "root":
                for i, key in enumerate(data):
                    tree.insert_from_root(key, str(key))
            elif insertion_method == "max":
                for i, key in enumerate(data):
                    tree.insert_from_max(key, str(key))
            else:
                raise ValueError("Invalid insertion_method for BST")
            # For BST, we don't have avl_to_array, but we can verify it's sorted
            # tree_array = tree.bst_to_array()
            # assert [item[0] for item in tree_array] == sorted(data), f"BST {insertion_method} not sorted!"

        elif tree_type == "AVL":
            tree = AVLTree()
            if insertion_method == "root":
                for i, key in enumerate(data):
                    tree.insert(key, str(key), start="root")
            elif insertion_method == "max":
                for i, key in enumerate(data):
                    tree.insert(key, str(key), start="max")
            else:
                raise ValueError("Invalid insertion_method for AVL")
            # Verify sorting for AVL
            # tree_array = tree.avl_to_array()
            # assert [item[0] for item in tree_array] == sorted(data), f"AVL {insertion_method} not sorted!"
        else:
            raise ValueError("Invalid tree_type")

        end_time = time.time()
        times.append(end_time - start_time)
    return times

# --- Theoretical Complexity Functions ---
# Removed arbitrary scaling factors to show the true shape of the functions.
# Note: The absolute values of these theoretical functions might be very different
# from the experimental times, as Big O notation describes growth rate, not absolute time.

def n_log_n_func(n_values):
    return [n * math.log(n) if n > 0 else 0 for n in n_values]

def n_func(n_values):
    return [n for n in n_values]

def n_squared_func(n_values):
    return [n**2 for n in n_values]


# --- Main Execution ---

if __name__ == "__main__":
    data_sizes = [50, 100, 200, 400,600,800,1100, 1400,1800,2000] # Adjust as needed

    results_sorted = {}
    results_reversed = {}

    # Sorted Input
    print("Running experiments for sorted input...")
    results_sorted["BST_root"] = run_experiment("BST", "root", "sorted", data_sizes)
    results_sorted["BST_max"] = run_experiment("BST", "max", "sorted", data_sizes)
    results_sorted["AVL_root"] = run_experiment("AVL", "root", "sorted", data_sizes)
    results_sorted["AVL_max"] = run_experiment("AVL", "max", "sorted", data_sizes)

    # Reversed Input
    print("Running experiments for reversed input...")
    results_reversed["BST_root"] = run_experiment("BST", "root", "reversed", data_sizes)
    results_reversed["BST_max"] = run_experiment("BST", "max", "reversed", data_sizes)
    results_reversed["AVL_root"] = run_experiment("AVL", "root", "reversed", data_sizes)
    results_reversed["AVL_max"] = run_experiment("AVL", "max", "reversed", data_sizes)

    # Calculate theoretical complexities
    n_log_n_times = n_log_n_func(data_sizes)
    n_times = n_func(data_sizes)
    n_squared_times = n_squared_func(data_sizes)


    # --- Plotting Results ---

    # Plot for Sorted Input
    plt.figure(figsize=(12, 8)) # Increased figure size
    plt.plot(data_sizes, results_sorted["BST_root"], label="BST - Insertion from Root (Experimental)", marker='o', linestyle='-')
    plt.plot(data_sizes, results_sorted["BST_max"], label="BST - Insertion from Max (Experimental)", marker='x', linestyle='--')
    plt.plot(data_sizes, results_sorted["AVL_root"], label="AVL - Insertion from Root (Experimental)", marker='s', linestyle='-.')
    plt.plot(data_sizes, results_sorted["AVL_max"], label="AVL - Insertion from Max (Experimental)", marker='d', linestyle=':')

    # Add theoretical complexity lines
    plt.plot(data_sizes, n_log_n_times, label="$N \log N$", color='purple', linestyle='-', linewidth=2)
    plt.plot(data_sizes, n_times, label="$N$", color='green', linestyle='-', linewidth=2)
    plt.plot(data_sizes, n_squared_times, label="$N^2$", color='red', linestyle='-', linewidth=2)


    plt.xlabel("Input Size (N)", fontsize=12)
    plt.ylabel("Execution Time (seconds)", fontsize=12)
    plt.title("Tree Insertion Runtime: Sorted Input", fontsize=14)
    plt.legend(fontsize=10, loc='upper left') # Adjusted legend location
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('sorted_input_runtime_with_theoretical.png') # New filename
    plt.close() # Close the plot to free memory

    # Plot for Reversed Input
    plt.figure(figsize=(12, 8)) # Increased figure size
    plt.plot(data_sizes, results_reversed["BST_root"], label="BST - Insertion from Root (Experimental)", marker='o', linestyle='-')
    plt.plot(data_sizes, results_reversed["BST_max"], label="BST - Insertion from Max (Experimental)", marker='x', linestyle='--')
    plt.plot(data_sizes, results_reversed["AVL_root"], label="AVL - Insertion from Root (Experimental)", marker='s', linestyle='-.')
    plt.plot(data_sizes, results_reversed["AVL_max"], label="AVL - Insertion from Max (Experimental)", marker='d', linestyle=':')

    # Add theoretical complexity lines
    plt.plot(data_sizes, n_log_n_times, label="$N \log N$", color='purple', linestyle='-', linewidth=2)
    plt.plot(data_sizes, n_times, label="$N$", color='green', linestyle='-', linewidth=2)
    plt.plot(data_sizes, n_squared_times, label="$N^2$", color='red', linestyle='-', linewidth=2)

    plt.xlabel("Input Size (N)", fontsize=12)
    plt.ylabel("Execution Time (seconds)", fontsize=12)
    plt.title("Tree Insertion Runtime: Reversed Input", fontsize=14)
    plt.legend(fontsize=10, loc='upper left') # Adjusted legend location
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('reversed_input_runtime_with_theoretical.png') # New filename
    plt.close() # Close the plot to free memory

    print("\nExperiments completed. Plots saved as 'sorted_input_runtime_with_theoretical.png' and 'reversed_input_runtime_with_theoretical.png'.")
