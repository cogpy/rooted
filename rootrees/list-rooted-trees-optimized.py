"""
Optimized algorithms for generating and counting rooted trees.

This implementation uses the efficient Euler transform method and memoization
for optimal performance, based on OEIS A000081.

The recurrence relation from OEIS:
    a(n+1) = (1/n) * Sum_{k=1..n} ( Sum_{d|k} d*a(d) ) * a(n-k+1)

Where a(n) is the number of unlabeled rooted trees with n nodes.
"""

from functools import lru_cache


@lru_cache(maxsize=None)
def count_rooted_trees(n):
    """
    Count the number of unlabeled rooted trees with n nodes.
    
    Uses the efficient Euler transform method with memoization.
    This is the OEIS A000081 sequence.
    
    Args:
        n: Number of nodes in the tree
        
    Returns:
        Number of distinct unlabeled rooted trees with n nodes
        
    Examples:
        >>> count_rooted_trees(1)
        1
        >>> count_rooted_trees(2)
        1
        >>> count_rooted_trees(3)
        2
        >>> count_rooted_trees(4)
        4
        >>> count_rooted_trees(5)
        9
    """
    if n <= 1:
        return n
    
    # Using the recurrence relation with divisor sum
    total = 0
    for j in range(1, n):
        # Sum over divisors of j
        divisor_sum = sum(d * count_rooted_trees(d) for d in divisors(j))
        total += divisor_sum * count_rooted_trees(n - j)
    
    return total // (n - 1)


def divisors(n):
    """
    Generate all divisors of n efficiently.
    
    Args:
        n: A positive integer
        
    Yields:
        All divisors of n in ascending order
    """
    i = 1
    while i * i <= n:
        if n % i == 0:
            yield i
            if i != n // i:
                yield n // i
        i += 1


def generate_rooted_trees(n):
    """
    Generate all unlabeled rooted trees with n nodes.
    
    Uses a successor-based algorithm that ensures canonical ordering
    and avoids duplicates.
    
    Args:
        n: Number of nodes in the trees
        
    Yields:
        Trees represented as nested tuples
    """
    if n == 1:
        yield ()
        return
    
    # Use the predecessor-successor relationship
    treeid = {(): 0}
    
    def successors(tree):
        """Generate all valid successors of a tree."""
        # Add a single node to the root
        yield ((),) + tree
        
        if not tree:
            return
        
        if len(tree) == 1:
            for subtree in successors(tree[0]):
                yield (subtree,)
            return
        
        # Replace smallest subtree with its successors
        head = tree[0]
        rest = tree[1:]
        
        # Get the id of the next smallest subtree for comparison
        if rest:
            next_smallest_id = treeid.get(rest[0], float('inf'))
        else:
            next_smallest_id = float('inf')
        
        # Only yield successors that maintain canonical ordering
        for new_head in successors(head):
            new_head_id = treeid.get(new_head)
            if new_head_id is None:
                new_head_id = len(treeid)
                treeid[new_head] = new_head_id
            
            if new_head_id <= next_smallest_id:
                yield (new_head,) + rest
    
    # Generate trees of increasing size
    prev_trees = [()]
    for size in range(2, n + 1):
        curr_trees = []
        for tree in prev_trees:
            for successor in successors(tree):
                if successor not in treeid:
                    treeid[successor] = len(treeid)
                    curr_trees.append(successor)
        prev_trees = curr_trees
    
    yield from prev_trees


def tree_to_string(tree, style='parens'):
    """
    Convert a tree (nested tuple) to string representation.
    
    Args:
        tree: Tree represented as nested tuple
        style: Output style - 'parens' for parentheses, 'brackets' for mixed brackets
        
    Returns:
        String representation of the tree
    """
    if not tree:
        return "()"
    
    if style == 'brackets':
        # Use different brackets at different depths for readability
        return _tree_to_brackets(tree, 0)
    else:
        # Standard parentheses notation
        return "(" + "".join(tree_to_string(subtree, style) for subtree in tree) + ")"


def _tree_to_brackets(tree, depth):
    """Helper for bracket-style output with varying bracket types."""
    if not tree:
        brackets = ["()", "[]", "{}"]
        return brackets[depth % 3]
    
    open_bracket = "([{"[depth % 3]
    close_bracket = ")]}"[depth % 3]
    
    inner = "".join(_tree_to_brackets(subtree, depth + 1) for subtree in tree)
    return open_bracket + inner + close_bracket


def print_trees(n, style='brackets', show_count=True):
    """
    Print all rooted trees with n nodes.
    
    Args:
        n: Number of nodes
        style: Output style ('parens' or 'brackets')
        show_count: Whether to show the count at the end
    """
    trees = list(generate_rooted_trees(n))
    
    for i, tree in enumerate(trees, 1):
        print(f"{i:2d}. {tree_to_string(tree, style)}")
    
    if show_count:
        expected = count_rooted_trees(n)
        actual = len(trees)
        print(f"\nGenerated {actual} trees (expected {expected})")
        if actual == expected:
            print("✓ Count matches OEIS A000081")
        else:
            print("✗ Count mismatch!")


def print_sequence(max_n):
    """
    Print the OEIS A000081 sequence up to max_n.
    
    Args:
        max_n: Maximum n value
    """
    print("OEIS A000081: Number of unlabeled rooted trees with n nodes")
    print("n  | a(n)")
    print("---|------")
    for n in range(0, max_n + 1):
        count = count_rooted_trees(n)
        print(f"{n:2d} | {count}")


if __name__ == "__main__":
    import sys
    
    # Default: show trees with 5 nodes
    n = 5
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except ValueError:
            print(f"Usage: {sys.argv[0]} [n]")
            print(f"  n: number of nodes (default: 5)")
            sys.exit(1)
    
    print(f"Rooted trees with {n} nodes:")
    print("=" * 40)
    print_trees(n)
    
    print("\n" + "=" * 40)
    print("OEIS A000081 sequence (first 10 terms):")
    print("=" * 40)
    print_sequence(10)
