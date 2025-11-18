#!/usr/bin/env python3
"""
Comprehensive test suite for the optimized rooted tree implementation.
Verifies correctness against OEIS A000081 sequence.
"""

import sys

# Import the optimized implementation
exec(open('list-rooted-trees-optimized.py').read())


def test_count_correctness():
    """Test that count_rooted_trees matches OEIS A000081."""
    # First 32 terms of OEIS A000081
    expected = [
        0, 1, 1, 2, 4, 9, 20, 48, 115, 286, 719, 1842, 4766, 12486, 32973,
        87811, 235381, 634847, 1721159, 4688676, 12826228, 35221832
    ]
    
    print("Test: count_rooted_trees correctness")
    print("=" * 70)
    
    all_pass = True
    for n, exp in enumerate(expected):
        actual = count_rooted_trees(n)
        status = "✓ PASS" if actual == exp else "✗ FAIL"
        
        if actual != exp:
            all_pass = False
            print(f"{status} n={n:2d}: got {actual}, expected {exp}")
        elif n <= 10 or n % 5 == 0:  # Print sample results
            print(f"{status} a({n:2d}) = {actual}")
    
    print("=" * 70)
    if all_pass:
        print("✓ All counting tests PASSED!\n")
        return True
    else:
        print("✗ Some counting tests FAILED!\n")
        return False


def test_generation_count():
    """Test that generation produces the correct count of trees."""
    print("Test: Tree generation count matches counting function")
    print("=" * 70)
    
    all_pass = True
    max_n = 8  # Generation is slower, test up to 8
    
    for n in range(1, max_n + 1):
        expected = count_rooted_trees(n)
        trees = list(generate_rooted_trees(n))
        actual = len(trees)
        
        status = "✓ PASS" if actual == expected else "✗ FAIL"
        
        if actual != expected:
            all_pass = False
            print(f"{status} n={n}: generated {actual} trees, expected {expected}")
        else:
            print(f"{status} n={n}: generated {actual} trees")
    
    print("=" * 70)
    if all_pass:
        print("✓ All generation tests PASSED!\n")
        return True
    else:
        print("✗ Some generation tests FAILED!\n")
        return False


def test_tree_uniqueness():
    """Test that generated trees are all unique."""
    print("Test: Generated trees are unique (no duplicates)")
    print("=" * 70)
    
    all_pass = True
    max_n = 7
    
    for n in range(1, max_n + 1):
        trees = list(generate_rooted_trees(n))
        unique_trees = set(trees)
        
        status = "✓ PASS" if len(trees) == len(unique_trees) else "✗ FAIL"
        
        if len(trees) != len(unique_trees):
            all_pass = False
            duplicates = len(trees) - len(unique_trees)
            print(f"{status} n={n}: {duplicates} duplicate(s) found!")
        else:
            print(f"{status} n={n}: all {len(trees)} trees are unique")
    
    print("=" * 70)
    if all_pass:
        print("✓ All uniqueness tests PASSED!\n")
        return True
    else:
        print("✗ Some uniqueness tests FAILED!\n")
        return False


def test_string_conversion():
    """Test that tree string conversion works."""
    print("Test: Tree to string conversion")
    print("=" * 70)
    
    # Test a few known trees
    test_cases = [
        ((), "()"),
        (((),), "(())"),
        (((), ()), "(()())"),
    ]
    
    all_pass = True
    for tree, expected_parens in test_cases:
        actual = tree_to_string(tree, style='parens')
        status = "✓ PASS" if actual == expected_parens else "✗ FAIL"
        
        if actual != expected_parens:
            all_pass = False
            print(f"{status} {tree} -> got '{actual}', expected '{expected_parens}'")
        else:
            print(f"{status} {tree} -> '{actual}'")
    
    # Test bracket style doesn't crash
    for tree, _ in test_cases:
        try:
            result = tree_to_string(tree, style='brackets')
            print(f"✓ PASS {tree} -> '{result}' (brackets)")
        except Exception as e:
            all_pass = False
            print(f"✗ FAIL {tree} bracket conversion failed: {e}")
    
    print("=" * 70)
    if all_pass:
        print("✓ All string conversion tests PASSED!\n")
        return True
    else:
        print("✗ Some string conversion tests FAILED!\n")
        return False


def test_divisors():
    """Test the divisors function."""
    print("Test: Divisor generation")
    print("=" * 70)
    
    test_cases = [
        (1, [1]),
        (2, [1, 2]),
        (6, [1, 2, 3, 6]),
        (12, [1, 2, 3, 4, 6, 12]),
        (16, [1, 2, 4, 8, 16]),
    ]
    
    all_pass = True
    for n, expected in test_cases:
        actual = sorted(list(divisors(n)))
        status = "✓ PASS" if actual == expected else "✗ FAIL"
        
        if actual != expected:
            all_pass = False
            print(f"{status} divisors({n}) = {actual}, expected {expected}")
        else:
            print(f"{status} divisors({n}) = {actual}")
    
    print("=" * 70)
    if all_pass:
        print("✓ All divisor tests PASSED!\n")
        return True
    else:
        print("✗ Some divisor tests FAILED!\n")
        return False


def run_all_tests():
    """Run all tests and report results."""
    print("\n" + "=" * 70)
    print("ROOTED TREE IMPLEMENTATION - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    print()
    
    results = []
    
    results.append(("Divisor generation", test_divisors()))
    results.append(("Count correctness", test_count_correctness()))
    results.append(("Generation count", test_generation_count()))
    results.append(("Tree uniqueness", test_tree_uniqueness()))
    results.append(("String conversion", test_string_conversion()))
    
    print("=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} {name}")
    
    all_passed = all(result[1] for result in results)
    
    print("=" * 70)
    if all_passed:
        print("✓✓✓ ALL TESTS PASSED! ✓✓✓")
        print("The optimized implementation is correct and ready to use.")
    else:
        print("✗✗✗ SOME TESTS FAILED! ✗✗✗")
        print("Please review the failures above.")
    print("=" * 70)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
