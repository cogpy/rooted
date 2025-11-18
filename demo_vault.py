#!/usr/bin/env python3
"""
Demo script showing all features of the Obsidian vault-style bijection.

This script demonstrates:
1. Scanning markdown files for bracket links
2. Building folder tree and link graph
3. Converting both to rooted trees
4. Comparing structures using parentheses notation
5. Generating suggestions
6. Exporting graphs
"""

from obsidian_vault import MarkdownVault
from vault_tree_bijection import VaultTreeBijection


def separator(title):
    """Print a nice separator with title."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def demo_vault_analysis():
    """Demonstrate vault analysis features."""
    separator("VAULT ANALYSIS")
    
    vault = MarkdownVault(".")
    print("Scanning vault...")
    vault.scan()
    
    print(f"\n📊 Found {len(vault.files)} markdown files")
    print(f"📊 Found {sum(len(targets) for targets in vault.links.values())} total links")
    
    # Show most connected files
    print("\n🔗 Top 5 Most Connected Files:")
    by_connections = sorted(
        vault.files.keys(),
        key=lambda k: len(vault.links.get(k, [])) + len(vault.backlinks.get(k, [])),
        reverse=True
    )
    
    for i, file_key in enumerate(by_connections[:5], 1):
        out = len(vault.links.get(file_key, []))
        inc = len(vault.backlinks.get(file_key, []))
        total = out + inc
        print(f"  {i}. {file_key}: {total} ({out} out, {inc} in)")
    
    # Check for issues
    broken = vault.get_broken_links()
    if broken:
        print(f"\n⚠️  Found broken links in {len(broken)} files")
    
    orphaned = vault.get_orphaned_files()
    if orphaned:
        print(f"⚠️  Found {len(orphaned)} orphaned files")


def demo_tree_bijection():
    """Demonstrate tree-graph bijection."""
    separator("TREE-GRAPH BIJECTION")
    
    vault = MarkdownVault(".")
    vault.scan()
    
    bijection = VaultTreeBijection(vault)
    
    # Build trees
    print("Building rooted tree representations...\n")
    folder_tree = bijection.folder_structure_to_tree()
    link_tree = bijection.link_graph_to_tree()
    
    # Compare structures
    comparison = bijection.compare_structures()
    
    print("📁 Folder Tree Structure:")
    for key, value in comparison['folder_tree'].items():
        if key != 'parentheses':
            print(f"  {key}: {value}")
    
    print("\n🔗 Link Graph Structure:")
    for key, value in comparison['link_graph'].items():
        if key != 'parentheses':
            print(f"  {key}: {value}")
    
    print("\n🌲 Rooted Tree Representations (Parentheses Notation):")
    print(f"  Folder: {comparison['folder_tree']['parentheses']}")
    print(f"  Links:  {comparison['link_graph']['parentheses']}")
    
    print("\nℹ️  These parentheses match the notation used in OEIS A000081!")
    print("   They represent unlabeled rooted trees, just like the")
    print("   algorithms in list-rooted-trees-optimized.py")


def demo_suggestions():
    """Demonstrate suggestion features."""
    separator("SUGGESTIONS")
    
    vault = MarkdownVault(".")
    vault.scan()
    
    bijection = VaultTreeBijection(vault)
    
    # Link suggestions
    link_suggestions = bijection.suggest_links_from_structure()
    if link_suggestions:
        print("💡 Suggested Links (based on folder structure):\n")
        for file_key, targets in sorted(link_suggestions.items())[:3]:
            print(f"  In {file_key}.md, consider adding:")
            for target in targets[:3]:
                print(f"    [[{target}]]")
            print()
    
    # Folder suggestions
    folder_suggestions = bijection.suggest_structure_from_links()
    if folder_suggestions:
        print("📂 Suggested Folder Structure (based on links):\n")
        for folder, files in sorted(folder_suggestions.items())[:3]:
            folder_name = folder if folder else "(root)"
            print(f"  {folder_name}/ ({len(files)} files)")
            for file_key in files[:3]:
                print(f"    - {file_key}.md")
            if len(files) > 3:
                print(f"    ... and {len(files) - 3} more")
            print()


def demo_exports():
    """Demonstrate export features."""
    separator("GRAPH EXPORTS")
    
    vault = MarkdownVault(".")
    vault.scan()
    
    print("📤 Available export formats:")
    print("  - JSON (for programmatic use)")
    print("  - GraphViz DOT (for visualization with Graphviz)")
    print("  - Mermaid (for GitHub/documentation)")
    
    print("\n📝 Example exports:")
    print("  python3 obsidian_vault.py --export json --output my-vault")
    print("  python3 obsidian_vault.py --export dot --output my-vault")
    print("  python3 obsidian_vault.py --export mermaid --output my-vault")
    
    # Show a sample of the graph structure
    graph = vault.build_link_graph()
    print(f"\n📊 Graph contains {len(graph['nodes'])} nodes and {len(graph['edges'])} edges")


def demo_connection_to_rooted_trees():
    """Show connection to repository's core algorithms."""
    separator("CONNECTION TO ROOTED TREES")
    
    print("This vault bijection feature connects directly to the repository's")
    print("core theme: rooted trees and their algebraic structure!\n")
    
    print("🌳 ALGEBRAIC CORRESPONDENCE:")
    print("  • Nesting (temporal) ↔ Folder hierarchy (parent/child)")
    print("  • Branching (spatial) ↔ Link patterns (sibling connections)")
    
    print("\n📐 MATHEMATICAL REPRESENTATION:")
    print("  Both folder trees and link graphs can be expressed as:")
    print("  1. Rooted trees (nodes + edges)")
    print("  2. Parentheses notation (canonical form)")
    print("  3. OEIS A000081 structures (unlabeled rooted trees)")
    
    print("\n💡 PRACTICAL APPLICATION:")
    print("  The vault bijection shows how the abstract math of rooted trees")
    print("  applies to real-world knowledge management:")
    print("  • File systems = rooted trees")
    print("  • Link graphs = rooted trees (via clustering)")
    print("  • Parentheses notation = universal representation")
    
    print("\n🔬 TRY IT:")
    print("  Compare your vault's structure with a 5-tree from A000081:")
    print("  $ python3 vault_tree_bijection.py --compare")
    print("  $ cd rootrees && python3 list-rooted-trees-optimized.py 5")


def main():
    """Run all demos."""
    print("\n" + "🌲" * 35)
    print("  OBSIDIAN VAULT-STYLE BIJECTION DEMO")
    print("🌲" * 35)
    
    demo_vault_analysis()
    demo_tree_bijection()
    demo_suggestions()
    demo_exports()
    demo_connection_to_rooted_trees()
    
    print("\n" + "=" * 70)
    print("  Demo complete! Try the tools yourself:")
    print("  • python3 obsidian_vault.py")
    print("  • python3 vault_tree_bijection.py")
    print("  • python3 test_vault.py")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    main()
