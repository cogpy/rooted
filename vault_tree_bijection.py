#!/usr/bin/env python3
"""
Bijection between Rooted Trees and Vault Link Structures

This module implements the mathematical bijection between:
1. Rooted tree structures (folder hierarchies)
2. Link graphs (markdown bracket link networks)

The bijection maps:
- Tree nodes ↔ Markdown files
- Parent-child edges ↔ Folder containment
- Sibling relationships ↔ Link patterns

This creates a bridge between the physical folder structure and the logical
link structure, similar to how Obsidian vaults work.
"""

import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from obsidian_vault import MarkdownVault


class TreeNode:
    """Represents a node in a rooted tree."""
    
    def __init__(self, name: str, is_file: bool = False):
        self.name = name
        self.is_file = is_file
        self.children: List[TreeNode] = []
        self.parent: Optional[TreeNode] = None
    
    def add_child(self, child: 'TreeNode') -> None:
        """Add a child node."""
        child.parent = self
        self.children.append(child)
    
    def to_parentheses(self) -> str:
        """
        Convert tree to parentheses notation (like rooted trees).
        
        This creates a canonical representation similar to the rooted tree
        algorithms in this repository.
        """
        if not self.children:
            return "()"
        
        # Sort children for canonical ordering
        child_strs = sorted([c.to_parentheses() for c in self.children])
        return "(" + "".join(child_strs) + ")"
    
    def __repr__(self) -> str:
        return f"TreeNode({self.name}, {len(self.children)} children)"


class VaultTreeBijection:
    """
    Creates bidirectional mappings between folder trees and link graphs.
    
    This implements the core bijection feature that connects:
    - Physical structure (folders/files) with rooted trees
    - Logical structure (links) with graph relationships
    """
    
    def __init__(self, vault: MarkdownVault):
        self.vault = vault
        self.folder_tree = None
        self.link_graph = None
    
    def folder_structure_to_tree(self) -> TreeNode:
        """
        Convert folder structure to a rooted tree.
        
        Returns:
            TreeNode representing the root of the tree
        """
        root = TreeNode("vault", is_file=False)
        
        # Build tree from folder structure
        folder_tree = self.vault.build_tree_structure()
        
        def add_subtree(parent_node: TreeNode, subtree: Dict, path: str = ""):
            # Add files at this level
            files = subtree.get('_files', [])
            for file_key in files:
                file_node = TreeNode(file_key, is_file=True)
                parent_node.add_child(file_node)
            
            # Add subdirectories
            for name, sub_dict in sorted(subtree.items()):
                if name == '_files' or name == '_root':
                    continue
                
                dir_node = TreeNode(name, is_file=False)
                parent_node.add_child(dir_node)
                
                new_path = f"{path}/{name}" if path else name
                add_subtree(dir_node, sub_dict, new_path)
        
        # Handle root files
        if '_root' in folder_tree:
            for file_key in folder_tree['_root']:
                file_node = TreeNode(file_key, is_file=True)
                root.add_child(file_node)
        
        # Handle subdirectories
        for name, subtree in sorted(folder_tree.items()):
            if name == '_root':
                continue
            dir_node = TreeNode(name, is_file=False)
            root.add_child(dir_node)
            add_subtree(dir_node, subtree, name)
        
        self.folder_tree = root
        return root
    
    def link_graph_to_tree(self) -> TreeNode:
        """
        Convert link graph to a rooted tree using graph clustering.
        
        Uses the link structure to infer a hierarchical organization:
        - Files that link to each other are siblings
        - Files linked from a central file are its children
        
        Returns:
            TreeNode representing the inferred tree
        """
        root = TreeNode("link_graph", is_file=False)
        
        # Find hub nodes (files with most outgoing links)
        hubs = sorted(
            self.vault.files.keys(),
            key=lambda k: len(self.vault.links.get(k, [])),
            reverse=True
        )
        
        placed: Set[str] = set()
        
        # Create clusters around hubs
        for hub in hubs[:5]:  # Top 5 hubs become clusters
            if hub in placed:
                continue
            
            hub_node = TreeNode(hub, is_file=True)
            root.add_child(hub_node)
            placed.add(hub)
            
            # Add files this hub links to as children
            targets = self.vault.links.get(hub, set())
            for target in sorted(targets):
                if target in self.vault.files and target not in placed:
                    target_node = TreeNode(target, is_file=True)
                    hub_node.add_child(target_node)
                    placed.add(target)
        
        # Add remaining files
        for file_key in sorted(self.vault.files.keys()):
            if file_key not in placed:
                file_node = TreeNode(file_key, is_file=True)
                root.add_child(file_node)
        
        self.link_graph = root
        return root
    
    def compare_structures(self) -> Dict[str, any]:
        """
        Compare the folder tree and link graph structures.
        
        Returns:
            Dictionary with comparison metrics
        """
        if not self.folder_tree:
            self.folder_structure_to_tree()
        if not self.link_graph:
            self.link_graph_to_tree()
        
        def count_nodes(node: TreeNode) -> int:
            return 1 + sum(count_nodes(c) for c in node.children)
        
        def max_depth(node: TreeNode) -> int:
            if not node.children:
                return 1
            return 1 + max(max_depth(c) for c in node.children)
        
        def avg_branching(node: TreeNode) -> float:
            counts = []
            def collect(n):
                if n.children:
                    counts.append(len(n.children))
                for c in n.children:
                    collect(c)
            collect(node)
            return sum(counts) / len(counts) if counts else 0
        
        return {
            'folder_tree': {
                'nodes': count_nodes(self.folder_tree),
                'depth': max_depth(self.folder_tree),
                'avg_branching': avg_branching(self.folder_tree),
                'parentheses': self.folder_tree.to_parentheses()
            },
            'link_graph': {
                'nodes': count_nodes(self.link_graph),
                'depth': max_depth(self.link_graph),
                'avg_branching': avg_branching(self.link_graph),
                'parentheses': self.link_graph.to_parentheses()
            }
        }
    
    def print_tree(self, node: TreeNode, prefix: str = "", is_last: bool = True):
        """Print a tree in ASCII format."""
        connector = "└── " if is_last else "├── "
        icon = "📄" if node.is_file else "📁"
        
        # Add link info for files
        extra = ""
        if node.is_file and node.name in self.vault.files:
            out = len(self.vault.links.get(node.name, []))
            inc = len(self.vault.backlinks.get(node.name, []))
            if out > 0 or inc > 0:
                extra = f" [{out}→ {inc}←]"
        
        print(f"{prefix}{connector}{icon} {node.name}{extra}")
        
        if node.children:
            extension = "    " if is_last else "│   "
            for i, child in enumerate(node.children):
                self.print_tree(child, prefix + extension, i == len(node.children) - 1)
    
    def suggest_links_from_structure(self) -> Dict[str, List[str]]:
        """
        Suggest bracket links based on folder structure.
        
        Suggests that files in the same folder should link to each other,
        creating a correspondence between physical and logical structure.
        
        Returns:
            Dictionary mapping file -> suggested links
        """
        suggestions = {}
        
        for folder, files in self.vault.folder_tree.items():
            if len(files) <= 1:
                continue
            
            # Files in same folder should reference each other
            for file_key in files:
                current_links = self.vault.links.get(file_key, set())
                sibling_files = [f for f in files if f != file_key]
                
                # Suggest links to siblings that aren't already linked
                missing_links = [f for f in sibling_files if f not in current_links]
                
                if missing_links:
                    suggestions[file_key] = missing_links
        
        return suggestions
    
    def suggest_structure_from_links(self) -> Dict[str, List[str]]:
        """
        Suggest folder structure based on link patterns.
        
        Files that link to each other frequently should be in the same folder.
        
        Returns:
            Suggested folder structure
        """
        # Group files by link similarity
        from collections import defaultdict
        
        clusters = defaultdict(set)
        
        for file_key in self.vault.files.keys():
            # Get link neighborhood
            neighbors = (
                self.vault.links.get(file_key, set()) |
                self.vault.backlinks.get(file_key, set())
            )
            
            # Files with similar neighborhoods cluster together
            signature = frozenset(neighbors)
            clusters[signature].add(file_key)
        
        # Convert to folder suggestions
        suggestions = {}
        cluster_id = 0
        
        for sig, files in sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True):
            if len(files) > 1:
                folder_name = f"cluster_{cluster_id}"
                suggestions[folder_name] = sorted(files)
                cluster_id += 1
            else:
                # Orphaned files stay in root
                if 'root' not in suggestions:
                    suggestions['root'] = []
                suggestions['root'].extend(files)
        
        return suggestions


def main():
    """CLI for tree-graph bijection analysis."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Analyze bijection between folder trees and link graphs'
    )
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Root path of the vault'
    )
    parser.add_argument(
        '--show-folder-tree',
        action='store_true',
        help='Show folder structure as rooted tree'
    )
    parser.add_argument(
        '--show-link-tree',
        action='store_true',
        help='Show link graph as rooted tree'
    )
    parser.add_argument(
        '--compare',
        action='store_true',
        help='Compare folder and link structures'
    )
    parser.add_argument(
        '--suggest-links',
        action='store_true',
        help='Suggest links based on folder structure'
    )
    parser.add_argument(
        '--suggest-folders',
        action='store_true',
        help='Suggest folder structure based on links'
    )
    
    args = parser.parse_args()
    
    # Create vault and bijection
    print(f"🔍 Analyzing vault at: {args.path}\n")
    vault = MarkdownVault(args.path)
    vault.scan()
    
    bijection = VaultTreeBijection(vault)
    
    # Default: show everything
    show_all = not any([
        args.show_folder_tree,
        args.show_link_tree,
        args.compare,
        args.suggest_links,
        args.suggest_folders
    ])
    
    if args.show_folder_tree or show_all:
        print("📁 Folder Structure as Rooted Tree:")
        tree = bijection.folder_structure_to_tree()
        bijection.print_tree(tree)
        print()
    
    if args.show_link_tree or show_all:
        print("🔗 Link Graph as Rooted Tree:")
        tree = bijection.link_graph_to_tree()
        bijection.print_tree(tree)
        print()
    
    if args.compare or show_all:
        print("📊 Structure Comparison:")
        comparison = bijection.compare_structures()
        
        print("\nFolder Tree:")
        for key, value in comparison['folder_tree'].items():
            if key != 'parentheses':
                print(f"  {key}: {value}")
        
        print("\nLink Graph:")
        for key, value in comparison['link_graph'].items():
            if key != 'parentheses':
                print(f"  {key}: {value}")
        
        print(f"\nFolder tree (parentheses): {comparison['folder_tree']['parentheses']}")
        print(f"Link graph (parentheses): {comparison['link_graph']['parentheses']}")
        print()
    
    if args.suggest_links or show_all:
        suggestions = bijection.suggest_links_from_structure()
        if suggestions:
            print("💡 Suggested Links (based on folder structure):")
            for file_key, targets in sorted(suggestions.items())[:5]:
                print(f"\n  In {file_key}.md, consider adding:")
                for target in targets[:3]:
                    print(f"    [[{target}]]")
            print()
    
    if args.suggest_folders or show_all:
        suggestions = bijection.suggest_structure_from_links()
        if suggestions:
            print("📂 Suggested Folder Structure (based on links):")
            for folder, files in sorted(suggestions.items()):
                print(f"\n  {folder}/")
                for file_key in files[:5]:
                    print(f"    - {file_key}.md")
                if len(files) > 5:
                    print(f"    ... and {len(files) - 5} more")
            print()


if __name__ == '__main__':
    main()
