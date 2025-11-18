# rooted

**Exploring the algebraic structure of rooted trees and their applications**

This repository implements optimized algorithms for generating and counting unlabeled rooted trees (OEIS A000081), demonstrating the fundamental algebra of "nesting" and "branching" operations.

## What are Rooted Trees?

Rooted trees are fundamental mathematical structures that appear across diverse fields:
- **Combinatorics**: OEIS A000081 - unlabeled rooted trees
- **Calculus**: Butcher trees for numerical integration
- **Computer Science**: Abstract syntax trees, data structures
- **Membrane Computing**: P-system hierarchies
- **Neural Networks**: Computational graph structures

## Features

✨ **Optimized Algorithms**
- Fast counting using Euler transform (O(n²) complexity)
- Efficient tree generation with canonical ordering
- Memoization for performance optimization

🚀 **Performance**
- Count trees with 20 nodes in milliseconds
- Generate trees efficiently without duplicates
- Benchmark tools for performance analysis

📚 **Educational**
- Multiple implementations in various languages
- Detailed documentation of algorithms
- Mathematical background and references

🔗 **Obsidian Vault Integration**
- Bidirectional mapping between markdown bracket links and folder structure
- Link graph analysis and visualization
- Broken link detection and validation
- **Scheme code bijection** - Convert vault structure to executable Scheme
- See [[OBSIDIAN_VAULT.md]] and [[SCHEME_BIJECTION.md]] for details

## Quick Start

### Rooted Tree Algorithms

```bash
# Count and display rooted trees with 5 nodes
cd rootrees
python3 list-rooted-trees-optimized.py 5

# Run performance benchmarks
python3 benchmark.py
```

### Obsidian Vault Features

```bash
# Analyze markdown links and folder structure
python3 obsidian_vault.py

# Show folder tree and link graph as rooted trees
python3 vault_tree_bijection.py

# Get suggestions for improving structure
python3 vault_tree_bijection.py --suggest-links

# Convert to Scheme code
python3 scheme_bijection.py --executable --output vault.scm
```

## Project Structure

```
rootrees/
├── README.md                        # Implementation documentation
├── list-rooted-trees-optimized.py  # Main optimized implementation
├── benchmark.py                     # Performance testing
├── list-rooted-trees-1.py          # Original implementation
├── list-rooted-trees-2.py          # Alternative implementation
└── [other language implementations]
```

## The Algebra of Nesting and Branching

Rooted trees embody two fundamental operations:

- **Nesting** (sequential/temporal): Parent-child relationships, composition
- **Branching** (parallel/spatial): Siblings at a node, products

This algebra appears in:
- Chain rule vs. product rule in calculus
- Serial vs. parallel composition in neural networks
- Sequential vs. concurrent operations in computation

See [nesting-branching.md](nesting-branching.md) for detailed mathematical exposition.

## "Evolve Roots for Optimal Grip"

The phrase captures our optimization philosophy:
- **Evolve**: Iteratively improve algorithms
- **Roots**: Work with fundamental tree structures
- **Optimal**: Achieve best performance and elegance
- **Grip**: Maintain stability and control in algorithms

## Contributing

Contributions welcome! Areas of interest:
- Additional language implementations
- Algorithm optimizations
- Applications in new domains
- Documentation improvements

## References

- [OEIS A000081](https://oeis.org/A000081) - The integer sequence
- [Rosetta Code: List Rooted Trees](http://rosettacode.org/wiki/List_rooted_trees)
- Knuth, TAOCP Vol. 4, Section 7.2.1.6

## License

See [LICENSE](LICENSE) for details.