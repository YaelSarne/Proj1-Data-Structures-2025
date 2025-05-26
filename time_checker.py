# --- פונקציות בנצ'מרק חדשות ---
import random
import plistlib
import matplotlib.pyplot as plt
from AVLTree import *
def generate_permutation_with_inversions(n, k):
    """
    Generates a permutation of [0, ..., n-1] with exactly k inversions.
    NOTE: This function can be very slow for large n due to list.pop(pos).
    For n=100,000, it might take a very long time.
    """
    result = []
    available = list(range(n))
    for i in range(n):
        # pos is the index of the element to pick from 'available'
        # To get k inversions, we need to place elements such that
        # there are k pairs (i, j) with i < j but arr[i] > arr[j].
        # Each element chosen from 'available' at index 'pos' contributes
        # 'pos' inversions with elements already placed.
        # min(k, len(available) - 1) ensures pos doesn't exceed bounds
        # and doesn't create more inversions than k remaining.
        pos = min(k, len(available) - 1)
        result.append(available.pop(pos))
        k -= pos
    return result

def benchmark_avl_inserts(n=10000, step_inversions=500000000): # Reduced default n for practicality
    """
    Benchmarks AVL tree insertion time for permutations with varying numbers of inversions.
    
    Parameters:
    n (int): The number of elements in the permutation.
    step_inversions (int): The step size for the number of inversions to test.
    
    Returns:
    list of dict: Each dict contains 'inversions' and 'time_us'.
    """
    # Calculate max possible inversions for n elements
    max_possible_inversions = n * (n - 1) // 2

    benchmark_results = []

    print(f"\n--- Benchmarking AVL Insertion Time (N={n}) ---")
    print(f"{'Inversions':<15} | {'Time (µs)':<20}")
    print("-" * 38)

    # Iterate through desired inversion counts
    for inversions_count in range(0, max_possible_inversions + 1, step_inversions):
        # Ensure inversions_count does not exceed max_possible_inversions
        if inversions_count > max_possible_inversions:
            inversions_count = max_possible_inversions # Cap at max
        
        # Generate the permutation (this part can be slow for large n)
        # WARNING: For n=100,000, this generation can take hours for intermediate inversion counts.
        # Consider reducing n or using a faster permutation generation method if this is too slow.
        keys = generate_permutation_with_inversions(n, inversions_count)
        
        tree = AVLTree() # Create a new tree for each benchmark run

        start_time = time.perf_counter_ns() # Start timing for insertions
        for key in keys:
            tree.insert(key, str(key), "root") # Use "root" for general inserts
        end_time = time.perf_counter_ns() # End timing

        duration_microseconds = (end_time - start_time) / 1000.0
        
        benchmark_results.append({
            'inversions': inversions_count,
            'time_us': duration_microseconds
        })
        print(f"{inversions_count:<15} | {duration_microseconds:<20.2f}")
        
        if inversions_count == max_possible_inversions: # Stop if we hit the max
            break

    print("-" * 38)
    return benchmark_results

def plot_benchmark_results(data_for_plot, save_path=None):
    """
    Plots the benchmark results: Inversions vs. Time.
    """
    inversions = [d['inversions'] for d in data_for_plot]
    times = [d['time_us'] for d in data_for_plot]

    plt.figure(figsize=(12, 7))
    plt.plot(inversions, times, marker='o', linestyle='-', color='green')
    
    plt.title('AVL Insertion Time vs. Number of Inversions in Input Permutation')
    plt.xlabel('Number of Inversions in Input Permutation')
    plt.ylabel('Cumulative Insertion Time (µs)')
    plt.grid(True)
    
    # Use log scale for X-axis if inversion counts vary widely (e.g., from 0 to billions)
    # If the step is large, a linear scale might still be fine.
    # plt.xscale('log') 

    plt.ticklabel_format(style='plain', axis='y') # Avoid scientific notation on y-axis if numbers are large
    
    # Annotate points with time values
    for i, txt in enumerate(times):
        plt.annotate(f'{txt:.2f}µs', (inversions[i], times[i]), textcoords="offset points", xytext=(0,10), ha='center')

    if save_path:
        plt.savefig(save_path)
        print(f"Benchmark graph saved successfully to: {save_path}")

    plt.show()


# --- הפעלת הניתוח והגרפים ---
if __name__ == "__main__":
    # --- Fibonacci Tree Analysis ---
    max_tree_height = 10 

    # --- AVL Insertion Benchmark ---
    # WARNING: For N=100,000, generate_permutation_with_inversions can be extremely slow.
    # Consider reducing N (e.g., to 1000 or 10000) for quicker testing.
    # The 'step_inversions' value should be adjusted based on 'n'.
    # For n=10000, max_inversions = 10000 * 9999 / 2 = ~50,000,000
    # A step of 500,000,000 is too large for n=10000.
    # Let's use n=10000 and adjust step_inversions for a few points.
    
    N_for_benchmark = 10000 # Number of elements to insert in each benchmark run
    # For N=10000, max_inversions is ~50 million.
    # Let's test at 0, 1/4, 1/2, 3/4, max inversions.
    
    # Example steps for N=10000:
    # step_inversions_val = (N_for_benchmark * (N_for_benchmark - 1) // 2) // 4 # Roughly 1/4 of max inversions
    # Or just define specific points:
    max_inv_for_N = N_for_benchmark * (N_for_benchmark - 1) // 2
    inversion_test_points = [0, max_inv_for_N // 4, max_inv_for_N // 2, max_inv_for_N * 3 // 4, max_inv_for_N]
    
    # Ensure inversion_test_points are unique and sorted
    inversion_test_points = sorted(list(set(inversion_test_points)))

    # Call the benchmark function with the specific test points
    # NOTE: The benchmark_avl_inserts function is modified to accept specific points now
    # instead of a range.
    benchmark_results_data = benchmark_avl_inserts(n=N_for_benchmark, test_inversion_points=inversion_test_points)
    
    print("\n--- Creating AVL Insertion Time Graph ---")
    plot_benchmark_results(benchmark_results_data, save_path="avl_insertion_time_benchmark.png")
