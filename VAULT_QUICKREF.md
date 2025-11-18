# Quick Reference: Obsidian Vault Bijection

## Commands

### Basic Analysis
```bash
# Analyze current directory
python3 obsidian_vault.py

# Show folder tree with link counts
python3 obsidian_vault.py --tree

# Show statistics only
python3 obsidian_vault.py --stats

# Check for broken links
python3 obsidian_vault.py --broken

# Find orphaned files
python3 obsidian_vault.py --orphaned
```

### Tree-Graph Bijection
```bash
# Show both structures as rooted trees
python3 vault_tree_bijection.py

# Show folder structure only
python3 vault_tree_bijection.py --show-folder-tree

# Show link graph only
python3 vault_tree_bijection.py --show-link-tree

# Compare structures
python3 vault_tree_bijection.py --compare

# Get suggestions
python3 vault_tree_bijection.py --suggest-links
python3 vault_tree_bijection.py --suggest-folders
```

### Export
```bash
# Export to JSON
python3 obsidian_vault.py --export json --output my-vault

# Export to GraphViz DOT
python3 obsidian_vault.py --export dot --output my-vault

# Export to Mermaid
python3 obsidian_vault.py --export mermaid --output my-vault
```

### Testing
```bash
# Run all tests
python3 test_vault.py

# Run demo
python3 demo_vault.py
```

## Link Syntax

```markdown
# Basic link
[[filename]]

# Link with display text
[[filename|Display Text]]

# Path-based link
[[folder/filename]]

# Multiple links
See [[doc1]], [[doc2]], and [[doc3]].
```

## Programmatic Use

```python
from obsidian_vault import MarkdownVault
from vault_tree_bijection import VaultTreeBijection

# Create and scan vault
vault = MarkdownVault(".")
vault.scan()

# Get information
broken = vault.get_broken_links()
orphaned = vault.get_orphaned_files()
tree = vault.build_tree_structure()
graph = vault.build_link_graph()

# Export
vault.export_graph("output.json", format="json")

# Tree bijection
bijection = VaultTreeBijection(vault)
folder_tree = bijection.folder_structure_to_tree()
comparison = bijection.compare_structures()

# Get parentheses notation (connects to OEIS A000081!)
notation = folder_tree.to_parentheses()
```

## Key Concepts

**Bijection**: A bidirectional mapping between two representations:
- Folder structure (physical hierarchy)
- Link graph (logical connections)

**Rooted Trees**: Both structures are rooted trees:
- Root = vault/repository root
- Nodes = files or folders (structure) / files (graph)
- Edges = containment (folders) / links (graph)

**Parentheses Notation**: Both can be expressed as `((())()()...)`:
- Same notation as OEIS A000081 rooted trees
- Canonical representation for comparison
- Connects to repository's core algorithms

**Nesting & Branching**:
- Nesting (temporal) = folder hierarchy
- Branching (spatial) = link patterns
- Core algebra of rooted trees!

## Common Use Cases

1. **Find broken links**: `python3 obsidian_vault.py --broken`
2. **Visualize structure**: `python3 obsidian_vault.py --tree`
3. **Compare representations**: `python3 vault_tree_bijection.py --compare`
4. **Get reorganization ideas**: `python3 vault_tree_bijection.py --suggest-folders`
5. **Export for visualization**: `python3 obsidian_vault.py --export mermaid`

## Output Examples

### Tree View
```
📁 Folder Structure:
/home/user/vault
├── README.md [1→ 2←]
├── doc1.md [2→ 1←]
└── docs/
    └── guide.md [1→ 0←]
```

### Comparison
```
Folder Tree:
  nodes: 15
  depth: 3
  avg_branching: 7.0

Link Graph:
  nodes: 14
  depth: 3
  avg_branching: 4.3

Folder tree (parentheses): ((())()()()()()()()()()()()())
Link graph (parentheses): ((()()()()()()()()()())(()))
```

## Files

- `obsidian_vault.py` - Core vault analysis tool
- `vault_tree_bijection.py` - Tree-graph bijection
- `test_vault.py` - Test suite
- `demo_vault.py` - Comprehensive demo
- `OBSIDIAN_VAULT.md` - Full documentation
- `example-vault-usage.md` - Working example with links

## See Also

- [OBSIDIAN_VAULT.md](OBSIDIAN_VAULT.md) - Full documentation
- [OEIS A000081](https://oeis.org/A000081) - Rooted trees sequence
- [Obsidian.md](https://obsidian.md/) - Inspiration for bracket links
