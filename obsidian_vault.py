#!/usr/bin/env python3
"""
Obsidian Vault-style Markdown Bracket Link <-> Folder Structure Bijection

This module provides tools to create a bidirectional mapping between:
1. Markdown files with wiki-style bracket links (e.g., [[filename]])
2. The repository folder structure

Features:
- Parse markdown files for [[bracket]] style links
- Build a graph of file connections
- Map folder hierarchy to tree structure
- Visualize connections and structure
- Validate links and detect issues
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
import json


class MarkdownVault:
    """Represents a collection of markdown files with bracket-style links."""
    
    def __init__(self, root_path: str):
        """
        Initialize the vault at the given root path.
        
        Args:
            root_path: Root directory containing markdown files
        """
        self.root = Path(root_path).resolve()
        self.files: Dict[str, Path] = {}  # filename -> full path
        self.links: Dict[str, Set[str]] = defaultdict(set)  # source -> {targets}
        self.backlinks: Dict[str, Set[str]] = defaultdict(set)  # target -> {sources}
        self.folder_tree: Dict[str, List[str]] = defaultdict(list)  # folder -> [files]
        
    def scan(self, exclude_dirs: Optional[Set[str]] = None) -> None:
        """
        Scan the vault directory for markdown files and extract links.
        
        Args:
            exclude_dirs: Set of directory names to exclude (e.g., {'.git', 'node_modules'})
        """
        if exclude_dirs is None:
            exclude_dirs = {'.git', '.github', 'node_modules', '__pycache__'}
        
        # Find all markdown files
        for md_file in self.root.rglob('*.md'):
            if any(excluded in md_file.parts for excluded in exclude_dirs):
                continue
                
            rel_path = md_file.relative_to(self.root)
            file_key = self._path_to_key(rel_path)
            self.files[file_key] = md_file
            
            # Track folder structure
            folder = str(rel_path.parent) if rel_path.parent != Path('.') else ''
            self.folder_tree[folder].append(file_key)
            
            # Extract links from file
            self._extract_links(file_key, md_file)
    
    def _path_to_key(self, path: Path) -> str:
        """Convert path to a standard key (without .md extension)."""
        return str(path.with_suffix(''))
    
    def _key_to_name(self, key: str) -> str:
        """Get just the filename from a key."""
        return Path(key).name
    
    def _extract_links(self, source_key: str, file_path: Path) -> None:
        """
        Extract [[bracket]] style links from a markdown file.
        
        Args:
            source_key: Key for the source file
            file_path: Path to the markdown file
        """
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Match [[link]] or [[link|display text]]
            pattern = r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'
            matches = re.findall(pattern, content)
            
            for match in matches:
                # Clean up the link
                target = match.strip()
                
                # Normalize the target (remove .md if present, handle paths)
                if target.endswith('.md'):
                    target = target[:-3]
                
                # Store link
                self.links[source_key].add(target)
                self.backlinks[target].add(source_key)
                
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}")
    
    def get_broken_links(self) -> Dict[str, List[str]]:
        """
        Find broken links (links to non-existent files).
        
        Returns:
            Dictionary mapping source file -> list of broken link targets
        """
        broken = {}
        for source, targets in self.links.items():
            broken_targets = []
            for target in targets:
                # Check if target exists (exact match or just filename)
                if target not in self.files:
                    # Try to find by filename only
                    target_name = self._key_to_name(target)
                    matches = [k for k in self.files.keys() if self._key_to_name(k) == target_name]
                    if not matches:
                        broken_targets.append(target)
            
            if broken_targets:
                broken[source] = broken_targets
        
        return broken
    
    def get_orphaned_files(self) -> List[str]:
        """
        Find files with no incoming or outgoing links.
        
        Returns:
            List of orphaned file keys
        """
        orphaned = []
        for file_key in self.files.keys():
            has_outgoing = len(self.links.get(file_key, [])) > 0
            has_incoming = len(self.backlinks.get(file_key, [])) > 0
            
            if not has_outgoing and not has_incoming:
                orphaned.append(file_key)
        
        return orphaned
    
    def build_tree_structure(self) -> Dict:
        """
        Build a tree representation of the folder structure.
        
        Returns:
            Nested dictionary representing folder tree
        """
        tree = {}
        
        for folder, files in sorted(self.folder_tree.items()):
            if folder == '':
                tree['_root'] = sorted(files)
            else:
                parts = Path(folder).parts
                current = tree
                for part in parts:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
                current['_files'] = sorted(files)
        
        return tree
    
    def build_link_graph(self) -> Dict:
        """
        Build a graph representation of file links.
        
        Returns:
            Dictionary with nodes and edges
        """
        nodes = {}
        for file_key, file_path in self.files.items():
            nodes[file_key] = {
                'path': str(file_path.relative_to(self.root)),
                'outgoing': len(self.links.get(file_key, [])),
                'incoming': len(self.backlinks.get(file_key, []))
            }
        
        edges = []
        for source, targets in self.links.items():
            for target in targets:
                edges.append({
                    'from': source,
                    'to': target,
                    'valid': target in self.files
                })
        
        return {
            'nodes': nodes,
            'edges': edges
        }
    
    def print_tree(self, max_depth: Optional[int] = None) -> None:
        """
        Print ASCII tree visualization of folder structure.
        
        Args:
            max_depth: Maximum depth to display (None for unlimited)
        """
        tree = self.build_tree_structure()
        
        def print_node(node, prefix="", depth=0):
            if max_depth is not None and depth > max_depth:
                return
            
            items = [(k, v) for k, v in node.items() if k != '_files']
            files = node.get('_files', [])
            
            # Print subdirectories
            for i, (name, subtree) in enumerate(items):
                is_last = (i == len(items) - 1) and not files
                print(f"{prefix}{'└── ' if is_last else '├── '}{name}/")
                extension = "    " if is_last else "│   "
                print_node(subtree, prefix + extension, depth + 1)
            
            # Print files
            for i, file_key in enumerate(files):
                is_last = i == len(files) - 1
                name = self._key_to_name(file_key)
                links_out = len(self.links.get(file_key, []))
                links_in = len(self.backlinks.get(file_key, []))
                print(f"{prefix}{'└── ' if is_last else '├── '}{name}.md [{links_out}→ {links_in}←]")
        
        print("\n📁 Folder Structure:")
        print(str(self.root))
        
        root_files = tree.get('_root', [])
        other = {k: v for k, v in tree.items() if k != '_root'}
        
        if root_files:
            for i, file_key in enumerate(root_files):
                is_last = i == len(root_files) - 1 and not other
                name = self._key_to_name(file_key)
                links_out = len(self.links.get(file_key, []))
                links_in = len(self.backlinks.get(file_key, []))
                print(f"{'└── ' if is_last else '├── '}{name}.md [{links_out}→ {links_in}←]")
        
        print_node(other)
    
    def print_graph_stats(self) -> None:
        """Print statistics about the link graph."""
        print("\n📊 Link Graph Statistics:")
        print(f"Total files: {len(self.files)}")
        print(f"Total links: {sum(len(targets) for targets in self.links.values())}")
        
        # Most connected files
        by_total = sorted(
            self.files.keys(),
            key=lambda k: len(self.links.get(k, [])) + len(self.backlinks.get(k, [])),
            reverse=True
        )[:5]
        
        print("\n🔗 Most connected files:")
        for file_key in by_total:
            out = len(self.links.get(file_key, []))
            inc = len(self.backlinks.get(file_key, []))
            total = out + inc
            if total > 0:
                print(f"  {self._key_to_name(file_key)}: {total} connections ({out}→ {inc}←)")
        
        # Check for issues
        broken = self.get_broken_links()
        if broken:
            print(f"\n⚠️  Broken links found in {len(broken)} files")
        
        orphaned = self.get_orphaned_files()
        if orphaned:
            print(f"⚠️  {len(orphaned)} orphaned files (no links)")
    
    def export_graph(self, output_path: str, format: str = 'json') -> None:
        """
        Export the link graph to a file.
        
        Args:
            output_path: Path to save the export
            format: Export format ('json', 'dot', 'mermaid')
        """
        graph = self.build_link_graph()
        
        if format == 'json':
            with open(output_path, 'w') as f:
                json.dump(graph, f, indent=2)
        
        elif format == 'dot':
            # GraphViz DOT format
            with open(output_path, 'w') as f:
                f.write("digraph vault {\n")
                f.write("  node [shape=box];\n")
                for node in graph['nodes']:
                    f.write(f'  "{node}";\n')
                for edge in graph['edges']:
                    style = "" if edge['valid'] else " [style=dashed, color=red]"
                    f.write(f'  "{edge["from"]}" -> "{edge["to"]}"{style};\n')
                f.write("}\n")
        
        elif format == 'mermaid':
            # Mermaid diagram format
            with open(output_path, 'w') as f:
                f.write("graph TD\n")
                for edge in graph['edges']:
                    from_name = edge['from'].replace('/', '_')
                    to_name = edge['to'].replace('/', '_')
                    style = "" if edge['valid'] else "-.->|broken|"
                    if style:
                        f.write(f'  {from_name} {style} {to_name}\n')
                    else:
                        f.write(f'  {from_name} --> {to_name}\n')
        
        print(f"\n✅ Graph exported to {output_path} ({format} format)")
    
    def suggest_folder_structure(self) -> Dict[str, List[str]]:
        """
        Suggest a folder structure based on link graph clustering.
        
        Uses simple heuristics:
        - Files that link to each other should be in same folder
        - Files with similar link patterns should be grouped
        
        Returns:
            Suggested folder structure as dict[folder] -> [files]
        """
        # Simple clustering: group files by their link neighborhoods
        clusters: Dict[str, Set[str]] = {}
        
        for file_key in self.files.keys():
            # Get neighbors (files this links to or that link to this)
            neighbors = self.links.get(file_key, set()) | self.backlinks.get(file_key, set())
            
            # Create a signature for clustering
            signature = frozenset(neighbors)
            
            if signature not in clusters:
                clusters[signature] = set()
            clusters[signature].add(file_key)
        
        # Convert to folder suggestions
        suggestions = {}
        for i, (sig, files) in enumerate(sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True)):
            if len(files) > 1:
                folder_name = f"cluster_{i+1}"
                suggestions[folder_name] = sorted(files)
            else:
                # Single files go to root
                suggestions[''] = suggestions.get('', []) + list(files)
        
        return suggestions


def main():
    """CLI interface for the vault tool."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Obsidian-style markdown vault analyzer'
    )
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Root path of the vault (default: current directory)'
    )
    parser.add_argument(
        '--tree',
        action='store_true',
        help='Show folder tree structure'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show link graph statistics'
    )
    parser.add_argument(
        '--broken',
        action='store_true',
        help='Show broken links'
    )
    parser.add_argument(
        '--orphaned',
        action='store_true',
        help='Show orphaned files'
    )
    parser.add_argument(
        '--export',
        choices=['json', 'dot', 'mermaid'],
        help='Export graph to file'
    )
    parser.add_argument(
        '--output',
        default='vault-graph',
        help='Output filename for export (without extension)'
    )
    parser.add_argument(
        '--suggest',
        action='store_true',
        help='Suggest folder structure based on links'
    )
    
    args = parser.parse_args()
    
    # Create and scan vault
    print(f"🔍 Scanning vault at: {args.path}")
    vault = MarkdownVault(args.path)
    vault.scan()
    
    # Default: show everything if no specific option selected
    show_all = not any([args.tree, args.stats, args.broken, args.orphaned, args.export, args.suggest])
    
    if args.tree or show_all:
        vault.print_tree()
    
    if args.stats or show_all:
        vault.print_graph_stats()
    
    if args.broken or show_all:
        broken = vault.get_broken_links()
        if broken:
            print("\n❌ Broken Links:")
            for source, targets in sorted(broken.items()):
                print(f"  {source}:")
                for target in targets:
                    print(f"    → [[{target}]] (not found)")
    
    if args.orphaned or show_all:
        orphaned = vault.get_orphaned_files()
        if orphaned:
            print(f"\n🔸 Orphaned Files ({len(orphaned)}):")
            for file_key in sorted(orphaned):
                print(f"  {file_key}.md")
    
    if args.export:
        ext = {'json': 'json', 'dot': 'dot', 'mermaid': 'mmd'}[args.export]
        output_path = f"{args.output}.{ext}"
        vault.export_graph(output_path, args.export)
    
    if args.suggest:
        suggestions = vault.suggest_folder_structure()
        print("\n💡 Suggested Folder Structure:")
        for folder, files in sorted(suggestions.items()):
            folder_display = folder if folder else "(root)"
            print(f"  {folder_display}:")
            for file_key in files[:5]:  # Show first 5
                print(f"    - {file_key}.md")
            if len(files) > 5:
                print(f"    ... and {len(files) - 5} more")


if __name__ == '__main__':
    main()
