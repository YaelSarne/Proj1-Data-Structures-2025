import time
import random
import matplotlib.pyplot as plt
import os

# Assuming AVLTree.py is in the same directory or accessible via PYTHONPATH
# If AVLTree.py is not in the same directory, you might need to adjust the import path.
from AVLTree import AVLTree  

def generate_permutation_with_inversions(n, k):
    """
    Generates a permutation of numbers from 0 to n-1 with exactly k inversions.
    This is a simplified approach and might not always generate *exactly* k inversions
    for all k, but it provides a way to control the 'sortedness' of the input.
    For precise k inversions, a more complex algorithm is needed.
    """
    result = []
    available = list(range(n))
    for i in range(n):
        pos = min(k, len(available) - 1)
        result.append(available.pop(pos))
        k -= pos
    return result


def benchmark_avl_inserts(n=100000, step=500000000):
    """
    Benchmarks AVL tree insertion performance based on the number of inversions
    in the input key sequence, using the original looping and permutation logic.
    
    Args:
        n (int): The number of keys to insert in each benchmark run.
        step (int): The increment for the number of inversions
                    between benchmark runs.
    """
    max_inversions = n * (n - 1) // 2
    
    inversions_data = []
    duration_data = []

    print(f"Benchmarking AVL tree insertions with n={n} keys...")
    print(f"Testing inversions from 0 to {max_inversions} with step {step}...")

    for inversions in range(0, max_inversions + 1, step):
        keys = generate_permutation_with_inversions(n, inversions)
        tree = AVLTree()

        start = time.perf_counter()
        for key in keys:
            tree.insert(key, "value", "max") # Reverted to "max" as per original logic
        end = time.perf_counter()

        duration = (end - start) * 1e6  # microseconds
        inversions_data.append(inversions)
        duration_data.append(duration)
        print(f"Inversions: {inversions:8d} -> Time: {duration:12.2f} µs")

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.plot(inversions_data, duration_data, marker='o', linestyle='-', color='skyblue')
    plt.title(f'AVL Tree Insertion Performance (n={n} keys)')
    plt.xlabel('Number of Inversions in Input Sequence')
    plt.ylabel('Total Insertion Time (microseconds)')
    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a file
    output_filename = 'avl_insertion_benchmark.png'
    plt.savefig(output_filename)
    print(f"\nBenchmark plot saved as '{output_filename}'")


if __name__ == "__main__":
    # Ensure your AVLTree.py is in the same directory as this script
    # or add its directory to sys.path if it's elsewhere.
    # import sys
    # sys.path.append('/path/to/your/AVLTree/directory')
    
    benchmark_avl_inserts()
