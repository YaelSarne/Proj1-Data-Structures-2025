import time
import math                                   # <<< CHANGED >>>
import random
import matplotlib.pyplot as plt
from AVLTree import AVLTree                   # Make sure AVLTree.py is import-able


# ---------------------------------------------------------------------------
# Permutation generator  – unchanged
# ---------------------------------------------------------------------------
def generate_permutation_with_inversions(n, k):
    result = []
    available = list(range(n))
    for _ in range(n):
        pos = min(k, len(available) - 1)
        result.append(available.pop(pos))
        k -= pos
    return result


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark_avl_inserts(n, step, repeats=3):           # <<< CHANGED >>>
    """
    Run `repeats` independent measurements for every inversion count and
    return both the raw average time and a time normalised by log₂(n).
    """
    max_inv = n * (n - 1) // 2
    inv_list, raw_us, norm_us = [], [], []

    print(f"--- AVL insertion benchmark (N={n}, repeats={repeats}) ---")
    print(f"{'inversions':>12}   {'avg µs':>12}   {'µs / log₂(n)':>14}")
    print("-" * 44)

    for inv in range(0, max_inv + 1, step):
        k = min(inv, max_inv)
        keys = generate_permutation_with_inversions(n, k)

        run_times = []
        for _ in range(repeats):
            tree = AVLTree()
            t0 = time.perf_counter()
            for key in keys:
                tree.insert(key, "v", "max")
            run_times.append((time.perf_counter() - t0) * 1e6)  # µs

        avg = sum(run_times) / repeats
        inv_list.append(k)
        raw_us.append(avg)
        norm_us.append(avg / math.log2(n))                    # <<< CHANGED >>>

        print(f"{k:12d}   {avg:12.0f}   {norm_us[-1]:14.0f}")

        if k >= max_inv:
            break

    return inv_list, raw_us, norm_us


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------
import numpy as np  # חשוב לייבא את זה למטה או למעלה

def plot_results(inversions, raw, norm, n_value,
                 outfile="avl_inversions_plot.png"):
    plt.figure(figsize=(10, 6))

    # Plot only the average raw times
    plt.plot(inversions, raw, marker='o', linestyle='-', color='skyblue', label="avg µs")

    # הוספת קו מקוקו לפי הפונקציה n * log2(I/n + 2)
    inv_array = np.array(inversions)
    curve = n_value * np.log2(inv_array / n_value + 2)
    plt.plot(inv_array, curve, linestyle='--', color='red', label=r"$n \cdot \log_2(\frac{I}{n} + 2)$")

    plt.title(f"AVL insertion vs. inversions (N={n_value})")
    plt.xlabel("Number of Inversions")
    plt.ylabel("Execution Time (µs)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outfile, dpi=150)
    print(f"Graph saved to '{outfile}'")
    plt.show()

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_n      = 200_000                       # same N
    test_step   = 1_000_000                 # same step
    repeats     = 1                       # <<< CHANGED >>>
    plot_file   = "avl_inversions_runtime_graph3.png"

    inv, raw, norm = benchmark_avl_inserts(test_n, test_step, repeats)
    plot_results(inv, raw, norm, n_value=test_n, outfile=plot_file)
