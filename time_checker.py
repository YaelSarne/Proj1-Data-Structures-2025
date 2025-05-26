import time
import random
import matplotlib.pyplot as plt
import os
from AVLTree import AVLTree  # <-- IMPORTANT: Uncomment this line and ensure AVLTree.py is accessible

def generate_permutation_with_inversions(n, k):
    """
    Generates a permutation of numbers from 0 to n-1 with exactly k inversions.
    This function can be computationally intensive for very large n and k.
    """
    result = []
    available = list(range(n))
    for i in range(n):
        # Determine the position to pop from 'available' to create 'pos' inversions.
        # 'pos' is capped at len(available) - 1 to prevent index out of bounds.
        pos = min(k, len(available) - 1)
        result.append(available.pop(pos))
        k -= pos
    return result

def benchmark_avl_inserts(n, step):
    """
    Benchmarks AVL tree insertion time for varying numbers of inversions.

    Args:
        n (int): The number of elements to insert into the AVL tree.
        step (int): The step size for iterating through the number of inversions.

    Returns:
        tuple: Two lists, (inversions_list, durations_list), containing the
               number of inversions and corresponding execution times in microseconds.
    """
    max_inversions = n * (n - 1) // 2
    
    inversions_list = []
    durations_list = []

    print(f"--- Starting AVL Insertion Benchmark (N={n}) ---")
    print(f"{'Inversions':<15} {'Time (microseconds)':<25}")
    print(f"{'-'*15} {'-'*25}")

    for inversions in range(0, max_inversions + 1, step):
        # Ensure we don't exceed max_inversions due to step size
        current_inversions = min(inversions, max_inversions)

        # Generate the keys with the specified number of inversions
        # Note: generate_permutation_with_inversions can be slow for very large N.
        keys = generate_permutation_with_inversions(n, current_inversions)
        
        tree = AVLTree() # Create a new AVL tree for each benchmark run

        start = time.perf_counter()
        for key in keys:
            # The 'max' argument is passed but might not be used by your AVLTree implementation
            # if it's a standard insertion.
            tree.insert(key, "value", "max") 
        end = time.perf_counter()

        duration = (end - start) * 1e6  # Convert to microseconds
        
        # Store results
        inversions_list.append(current_inversions)
        durations_list.append(duration)
        
        # Print to console for real-time feedback
        print(f"{current_inversions:<15} {duration:<25.2f}")

        if current_inversions == max_inversions: # Stop if we hit max_inversions exactly
            break

    print(f"\nBenchmark complete for N={n}.")
    return inversions_list, durations_list

def plot_results(inversions_data, durations_data, n_value, output_plot_filename="avl_inversions_plot.png"):
    """
    Plots the benchmark results using matplotlib and saves the plot to a file.

    Args:
        inversions_data (list): List of inversion counts.
        durations_data (list): List of corresponding execution times.
        n_value (int): The N value used for the benchmark.
        output_plot_filename (str): The name of the image file to save the plot.
    """
    plt.figure(figsize=(10, 6)) # Set figure size
    plt.plot(inversions_data, durations_data, marker='o', linestyle='-', color='skyblue', label=f'AVL Insertion (N={n_value})')

    plt.title(f'AVL Insertion Runtime vs. Inversions (N={n_value})', fontsize=16)
    plt.xlabel('Number of Inversions', fontsize=14)
    plt.ylabel('Execution Time (microseconds)', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7) # Add grid for readability
    plt.legend(fontsize=12)
    plt.tight_layout() # Adjust layout to prevent labels from overlapping

    # Save the plot
    plt.savefig(output_plot_filename)
    print(f"Graph saved to '{output_plot_filename}'")
    plt.show() # Display the plot (optional, can be removed if only saving)


if __name__ == "__main__":
    # --- Configuration for the benchmark ---
    # N: The number of elements to insert.
    # Be cautious with very large N, as generate_permutation_with_inversions can be slow
    # and the benchmark itself will take longer.
    # For a quick test, start with N=1000 or N=5000.
    # For more meaningful results, you might need N=100000 or more, but it will take significant time.
    test_n = 100000 # Example: 2000 elements

    # Step: How many inversions to increment by between data points.
    # max_inversions = n * (n - 1) // 2.
    # For N=2000, max_inversions is 2000 * 1999 / 2 = 1,999,000.
    # A step of 100000 would give about 20 data points.
    test_step = 500000000 # Example: Check every 100,000 inversions

    # Output filename for the plot
    plot_filename = "avl_inversions_runtime_graph.png"

    # Run the benchmark and get the data
    inversions, durations = benchmark_avl_inserts(n=test_n, step=test_step)

    # Plot the results
    plot_results(inversions, durations, n_value=test_n, output_plot_filename=plot_filename)

    print("\nScript finished.")
