#!/usr/bin/env python3
"""
List all rooted trees with n nodes.

This implementation uses a successor-based algorithm to generate all unlabeled
rooted trees. The algorithm is based on the observation that every tree has a
unique predecessor, and by inverting this relationship, we can generate all
successors systematically.

Algorithm:
The predecessor p of a tree t is:
  1. if the smallest subtree of t is a single node, then p is t minus that node
  2. otherwise, p is t with its smallest subtree "m" replaced by m's predecessor

The successors to tree t are:
  1. append a single node tree to t's root, or
  2. replace t's smallest subtree by its successors

We maintain canonical ordering: when replacing a subtree, the replacement must
not be larger than the next smallest subtree.
"""

treeid = {(): 0}

def succ(x):
    """Generate all canonical successors of tree x."""
    yield(((),) + x)
    if not x: return

    if len(x) == 1:
        for i in succ(x[0]): yield((i,))
        return

    head, rest = x[0], tuple(x[1:])
    top = treeid[rest[0]]

    for i in [i for i in succ(head) if treeid[i] <= top]:
        yield((i,) + rest)

def trees(n):
    """Generate all rooted trees with n nodes."""
    if n == 1:
        yield()
        return

    global treeid
    for x in trees(n-1):
        for a in succ(x):
            if not a in treeid: treeid[a] = len(treeid)
            yield(a)

def tostr(x):
    """Convert tree representation to parentheses notation."""
    return "(" + "".join(map(tostr, x)) + ")"

if __name__ == "__main__":
    import sys
    
    # Default: show trees with 5 nodes
    n = 5
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
            if n < 1:
                raise ValueError("n must be positive")
        except ValueError as e:
            print(f"Usage: {sys.argv[0]} [n]", file=sys.stderr)
            print(f"  n: number of nodes (default: 5, must be positive)", file=sys.stderr)
            sys.exit(1)
    
    count = 0
    for x in trees(n):
        print(tostr(x))
        count += 1
    
    print(f"Number of {n}-trees: {count}", file=sys.stderr)
