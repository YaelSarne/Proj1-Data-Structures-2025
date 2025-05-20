import time
import matplotlib.pyplot as plt
import random
import math

# --- Helper functions for inversions ---

def count_inversions(arr):
    """
    Counts the number of inversions in an array using a merge sort based approach.
    """
    def merge_and_count(left, right):
        merged = []
        inversions = 0
        i, j = 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                inversions += (len(left) - i)
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, inversions

    def sort_and_count(arr):
        if len(arr) <= 1:
            return arr, 0
        mid = len(arr) // 2
        left_half, inversions_left = sort_and_count(arr[:mid])
        right_half, inversions_right = sort_and_count(arr[mid:])
        merged_arr, inversions_merge = merge_and_count(left_half, right_half)
        return merged_arr, inversions_left + inversions_right + inversions_merge

    _, inversions = sort_and_count(list(arr))
    return inversions

def create_array_by_reversing_prefix(size, prefix_length):
    """
    Creates an array [0, 1, ..., size-1] and reverses its first `prefix_length` elements.
    This generates (prefix_length * (prefix_length - 1)) / 2 inversions.
    """
    arr = list(range(size))
    if prefix_length > 0:
        arr[:prefix_length] = list(reversed(arr[:prefix_length]))
    return arr

# --- Insertion Sort Implementation ---

def insertion_sort(arr):
    """
    Implements the standard Insertion Sort algorithm on a list.
    """
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        # Move elements of arr[0..i-1], that are greater than key,
        # to one position ahead of their current position
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

# --- Experiment for Inversions (Insertion Sort) ---

def run_insertion_sort_inversion_experiment_simple(N_size, num_runs_per_point=5):
    inversion_counts = []
    average_execution_times = []

    # Define a range of prefix lengths to get varying inversion counts
    # Aim for a few points at the beginning (low inversions)
    # and then a good spread towards the end (high inversions)
    prefix_lengths_to_test = [0] # 0 inversions (sorted)
    
    # Add a few small prefix lengths for fine granularity at low inversions
    if N_size >= 2: prefix_lengths_to_test.append(2)
    if N_size >= 5: prefix_lengths_to_test.append(5)
    if N_size >= 10: prefix_lengths_to_test.append(10)

    # Add a range of prefix lengths covering the spectrum
    # Using a slightly higher step to avoid too many points for simplicity
    step_size_for_sampling = max(1, N_size // 15) # Roughly 15 points across the range
    for k in range(15, N_size + 1, step_size_for_sampling):
        if k not in prefix_lengths_to_test:
            prefix_lengths_to_test.append(k)
    
    # Ensure max inversions point is included
    if N_size not in prefix_lengths_to_test:
        prefix_lengths_to_test.append(N_size)
    
    prefix_lengths_to_test.sort() # Process in increasing order

    print(f"\nRunning Simple Insertion Sort experiment for N = {N_size} with {num_runs_per_point} runs per point...")

    for p_len in prefix_lengths_to_test:
        if p_len > N_size: # Safety check
            continue

        total_time_for_this_inversion_level = 0
        
        base_data = create_array_by_reversing_prefix(N_size, p_len)
        num_inversions = count_inversions(base_data)

        for _ in range(num_runs_per_point):
            arr_to_sort = list(base_data) # Use a copy for each run
            start_time = time.time()
            insertion_sort(arr_to_sort)
            end_time = time.time()
            total_time_for_this_inversion_level += (end_time - start_time)
        
        avg_time = total_time_for_this_inversion_level / num_runs_per_point

        inversion_counts.append(num_inversions)
        average_execution_times.append(avg_time)
        print(f"  Prefix Length {p_len} (Inversions = {num_inversions}): Avg Time = {avg_time:.6f} seconds")

    sorted_results = sorted(zip(inversion_counts, average_execution_times), key=lambda x: x[0])
    inversion_counts_sorted, average_execution_times_sorted = zip(*sorted_results)
    
    return inversion_counts_sorted, average_execution_times_sorted

# --- Main Execution ---

if __name__ == "__main__":
    N_size_for_inversions = 1000 # Increased N for clearer O(N^2) trend if possible, adjust if too slow.
    NUM_AVERAGE_RUNS = 10 # Number of times to run each test case and average

    # Run the experiment
    inversions, times = run_insertion_sort_inversion_experiment_simple(N_size_for_inversions, NUM_AVERAGE_RUNS)

    # Filter out cases where time is 0 (can happen with very small N or very fast machines)
    valid_inversions = []
    valid_times = []
    for inv, t in zip(inversions, times):
        if t > 0:
            valid_inversions.append(inv)
            valid_times.append(t)
    
    # --- Plotting Results (Simplified) ---
    plt.figure(figsize=(12, 7))

    # Plotting the data points with a line connecting them
    # No theoretical line, just the experimental data
    plt.plot(valid_inversions, valid_times, marker='o', linestyle='-', color='blue', label='Insertion Sort (Experimental Data)')

    plt.xlabel("Number of Inversions (I)", fontsize=12)
    plt.ylabel("Execution Time (seconds)", fontsize=12)
    plt.title(f"Insertion Sort Runtime vs. Inversions (N={N_size_for_inversions}) - Simple View", fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True)
    
    # Keep scales linear for direct visual interpretation of O(N+I) behavior
    # plt.xscale('linear') # Default
    # plt.yscale('linear') # Default

    plt.tight_layout()
    plt.savefig('insertion_sort_vs_inversions_simple.png')
    plt.close()

    print("\nSimple Insertion Sort inversion experiment completed. Plot saved as 'insertion_sort_vs_inversions_simple.png'.")