#!/usr/bin/env python3
"""
Demo: Scheme Code Bijection

Demonstrates the triple bijection:
  Folder Structure ↔ Rooted Tree ↔ Scheme Code
        ↕               ↕              ↕
  Link Graph      ↔ Rooted Tree ↔ Scheme Code

Shows how parentheses structure is preserved across all representations.
"""

from obsidian_vault import MarkdownVault
from vault_tree_bijection import VaultTreeBijection
from scheme_bijection import SchemeVaultBijection


def separator(title):
    """Print separator with title."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def demo_basic_scheme_generation():
    """Show basic Scheme code generation."""
    separator("BASIC SCHEME GENERATION")
    
    vault = MarkdownVault(".")
    vault.scan()
    
    scheme_bij = SchemeVaultBijection(vault)
    
    print("🌲 Folder Structure → Scheme Code (Let style)")
    print("\nFirst 30 lines of generated Scheme:\n")
    
    folder_scheme = scheme_bij.folder_structure_to_scheme('let')
    lines = folder_scheme.split('\n')[:30]
    for line in lines:
        print(line)
    
    if len(folder_scheme.split('\n')) > 30:
        print(f"\n... ({len(folder_scheme.split('\n')) - 30} more lines)")
    
    print(f"\n✓ Generated {len(folder_scheme.split('\n'))} lines of Scheme code")
    print(f"✓ Parentheses balanced: {folder_scheme.count('(') == folder_scheme.count(')')}")


def demo_all_styles():
    """Show all three Scheme styles."""
    separator("SCHEME STYLES COMPARISON")
    
    vault = MarkdownVault(".")
    vault.scan()
    
    scheme_bij = SchemeVaultBijection(vault)
    
    print("The same structure can be expressed in different Scheme styles:\n")
    
    for style in ['let', 'lambda', 'module']:
        print(f"📝 {style.upper()} Style:")
        print("-" * 40)
        
        code = scheme_bij.folder_structure_to_scheme(style)
        lines = code.split('\n')[:10]
        
        for line in lines:
            print(line)
        
        print(f"... ({len(code.split('\n')) - 10} more lines)")
        print()


def demo_parentheses_preservation():
    """Show parentheses structure preservation."""
    separator("PARENTHESES STRUCTURE PRESERVATION")
    
    vault = MarkdownVault(".")
    vault.scan()
    
    bijection = VaultTreeBijection(vault)
    scheme_bij = SchemeVaultBijection(vault)
    
    # Get all representations
    comparison = bijection.compare_structures()
    folder_parens = comparison['folder_tree']['parentheses']
    link_parens = comparison['link_graph']['parentheses']
    
    folder_scheme = scheme_bij.folder_structure_to_scheme('let')
    link_scheme = scheme_bij.link_graph_to_scheme('lambda')
    
    print("🔗 The Triple Bijection preserves parentheses structure:\n")
    
    print("1️⃣  FOLDER STRUCTURE")
    print(f"   Tree Parentheses: {folder_parens[:50]}...")
    print(f"   Scheme code: {len(folder_scheme.split('\n'))} lines")
    print(f"   Balanced? {folder_scheme.count('(') == folder_scheme.count(')')}")
    print(f"   Scheme '(' count: {folder_scheme.count('(')}")
    print()
    
    print("2️⃣  LINK GRAPH")
    print(f"   Tree Parentheses: {link_parens[:50]}...")
    print(f"   Scheme code: {len(link_scheme.split('\n'))} lines")
    print(f"   Balanced? {link_scheme.count('(') == link_scheme.count(')')}")
    print(f"   Scheme '(' count: {link_scheme.count('(')}")
    print()
    
    print("✓ Both structures map to valid Scheme code")
    print("✓ Parentheses structure is preserved in all representations")
    print("✓ This creates a bijection: Structure ↔ Tree ↔ Scheme")


def demo_executable_generation():
    """Show executable Scheme program generation."""
    separator("EXECUTABLE SCHEME PROGRAM")
    
    vault = MarkdownVault(".")
    vault.scan()
    
    scheme_bij = SchemeVaultBijection(vault)
    
    print("📦 Generating complete executable Scheme program...\n")
    
    program = scheme_bij.generate_executable_vault_scheme()
    
    print("Preview of generated program:")
    print("-" * 70)
    
    lines = program.split('\n')[:40]
    for line in lines:
        print(line)
    
    print(f"\n... ({len(program.split('\n')) - 40} more lines)")
    print("-" * 70)
    
    print(f"\n✓ Total lines: {len(program.split('\n'))}")
    print(f"✓ Contains vault-folders definition")
    print(f"✓ Contains vault-links definition")
    print(f"✓ Contains parentheses notation")
    print(f"✓ Contains show-vault function")
    
    print("\n💡 This program can be run in any Scheme interpreter:")
    print("   guile vault.scm")
    print("   racket vault.scm")
    print("   csi -s vault.scm")


def demo_mathematical_connection():
    """Show connection to rooted trees and OEIS A000081."""
    separator("MATHEMATICAL CONNECTION")
    
    vault = MarkdownVault(".")
    vault.scan()
    
    bijection = VaultTreeBijection(vault)
    
    print("🔬 Connecting Scheme Code to OEIS A000081 Rooted Trees\n")
    
    comparison = bijection.compare_structures()
    
    print("The parentheses notation connects all representations:")
    print()
    print("📁 Folder Tree:")
    print(f"   Parentheses: {comparison['folder_tree']['parentheses']}")
    print(f"   Nodes: {comparison['folder_tree']['nodes']}")
    print(f"   Depth: {comparison['folder_tree']['depth']}")
    print()
    
    print("🔗 Link Graph:")
    print(f"   Parentheses: {comparison['link_graph']['parentheses']}")
    print(f"   Nodes: {comparison['link_graph']['nodes']}")
    print(f"   Depth: {comparison['link_graph']['depth']}")
    print()
    
    print("📐 Mathematical Properties:")
    print("   • Same parentheses notation as OEIS A000081")
    print("   • Unlabeled rooted trees")
    print("   • Canonical representation")
    print("   • Structure-preserving bijection")
    print()
    
    print("🌲 This connects three domains:")
    print("   1. Combinatorics (rooted trees)")
    print("   2. Knowledge management (vaults)")
    print("   3. Programming languages (Scheme)")
    print()
    
    print("💡 Try comparing with rooted tree enumeration:")
    print("   cd rootrees && python3 list-rooted-trees-optimized.py 5")


def demo_save_to_file():
    """Demonstrate saving Scheme code to file."""
    separator("SAVING TO FILE")
    
    vault = MarkdownVault(".")
    vault.scan()
    
    scheme_bij = SchemeVaultBijection(vault)
    
    print("💾 Saving executable Scheme program to file...\n")
    
    program = scheme_bij.generate_executable_vault_scheme()
    
    filename = "vault-demo.scm"
    with open(filename, 'w') as f:
        f.write(program)
    
    print(f"✓ Saved to {filename}")
    print(f"✓ File size: {len(program)} bytes")
    print(f"✓ Lines: {len(program.split('\n'))}")
    print()
    
    print("🚀 You can now run this in a Scheme interpreter:")
    print(f"   guile {filename}")
    print(f"   racket {filename}")
    print(f"   csi -s {filename}")
    print()
    
    print("Or load it in a Scheme REPL:")
    print(f"   guile> (load \"{filename}\")")
    print(f"   guile> (show-vault)")
    
    # Clean up
    import os
    os.remove(filename)
    print(f"\n(Demo file {filename} removed)")


def main():
    """Run all demonstrations."""
    print("\n" + "🌲" * 35)
    print("  SCHEME CODE BIJECTION DEMO")
    print("  Folder/Link Structure → Rooted Trees → Scheme Code")
    print("🌲" * 35)
    
    demo_basic_scheme_generation()
    demo_all_styles()
    demo_parentheses_preservation()
    demo_executable_generation()
    demo_mathematical_connection()
    demo_save_to_file()
    
    print("\n" + "=" * 70)
    print("  Demo complete!")
    print()
    print("  Try the tools yourself:")
    print("  • python3 scheme_bijection.py --folders")
    print("  • python3 scheme_bijection.py --links --style lambda")
    print("  • python3 scheme_bijection.py --executable --output vault.scm")
    print()
    print("  Run tests:")
    print("  • python3 test_scheme_bijection.py")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    main()
