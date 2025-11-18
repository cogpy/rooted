"""
Benchmark script to compare different rooted tree implementations.

Compares performance and correctness of various algorithms.
"""

import time
import sys


def benchmark_count(func, name, max_n=15):
    """Benchmark a tree counting function."""
    print(f"\n{name}")
    print("-" * 60)
    print(f"{'n':<5} {'count':<10} {'time (ms)':<15} {'per tree (μs)':<15}")
    print("-" * 60)
    
    for n in range(1, max_n + 1):
        start = time.perf_counter()
        count = func(n)
        elapsed = time.perf_counter() - start
        
        elapsed_ms = elapsed * 1000
        per_tree_us = (elapsed / count * 1000000) if count > 0 else 0
        
        print(f"{n:<5} {count:<10} {elapsed_ms:<15.3f} {per_tree_us:<15.3f}")
    
    print("-" * 60)


def benchmark_generate(func, name, max_n=10):
    """Benchmark a tree generation function."""
    print(f"\n{name}")
    print("-" * 60)
    print(f"{'n':<5} {'count':<10} {'time (ms)':<15} {'per tree (μs)':<15}")
    print("-" * 60)
    
    for n in range(1, max_n + 1):
        start = time.perf_counter()
        trees = list(func(n))
        elapsed = time.perf_counter() - start
        count = len(trees)
        
        elapsed_ms = elapsed * 1000
        per_tree_us = (elapsed / count * 1000000) if count > 0 else 0
        
        print(f"{n:<5} {count:<10} {elapsed_ms:<15.3f} {per_tree_us:<15.3f}")
    
    print("-" * 60)


if __name__ == "__main__":
    # Import the optimized version
    sys.path.insert(0, '.')
    exec(open('list-rooted-trees-optimized.py').read())
    
    print("=" * 60)
    print("ROOTED TREE ALGORITHM BENCHMARKS")
    print("=" * 60)
    
    # Benchmark counting
    print("\n\n### COUNTING BENCHMARKS ###")
    benchmark_count(count_rooted_trees, "Optimized Count (Euler Transform with Memoization)", max_n=20)
    
    # Benchmark generation
    print("\n\n### GENERATION BENCHMARKS ###")
    benchmark_generate(generate_rooted_trees, "Optimized Generation (Successor-based)", max_n=8)
    
    print("\n\n" + "=" * 60)
    print("PERFORMANCE SUMMARY")
    print("=" * 60)
    print("\nThe optimized implementation uses:")
    print("1. Euler transform with divisor-based recurrence (O(n²) for counting)")
    print("2. LRU cache for memoization (avoids redundant computation)")
    print("3. Successor-based generation (canonical ordering, no duplicates)")
    print("4. Efficient divisor generation (O(√n) per divisor call)")
    print("\nKey benefits:")
    print("- Fast counting without generation (can compute a(20) quickly)")
    print("- Efficient generation with automatic duplicate elimination")
    print("- Memory-efficient through proper caching strategy")
    print("=" * 60)
