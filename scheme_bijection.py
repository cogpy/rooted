#!/usr/bin/env python3
"""
Scheme Code Bijection for Rooted Trees

This module implements a bijection between:
1. Rooted tree parentheses notation (OEIS A000081)
2. Scheme code with matching parentheses structure

The mapping represents:
- Folder hierarchy → Scheme execution contexts (nested scopes)
- Files → Functions and variables
- Nesting → Nested let/lambda expressions
- Branching → Multiple definitions in same scope

This creates executable Scheme code that mirrors the structure of the vault.
"""

from typing import Dict, List, Optional, Tuple
from pathlib import Path
from obsidian_vault import MarkdownVault
from vault_tree_bijection import VaultTreeBijection, TreeNode


class SchemeCodeGenerator:
    """
    Converts rooted trees to Scheme code with matching parentheses structure.
    
    The bijection preserves the tree structure in the code:
    - Tree nodes → Scheme definitions (define, let, lambda)
    - Nesting → Nested scopes/contexts
    - Branching → Multiple bindings in same scope
    """
    
    def __init__(self):
        self.indent_level = 0
        self.indent_str = "  "
    
    def _indent(self) -> str:
        """Get current indentation string."""
        return self.indent_str * self.indent_level
    
    def _sanitize_name(self, name: str) -> str:
        """
        Convert file/folder names to valid Scheme identifiers.
        
        Rules:
        - Replace special chars with hyphens
        - Convert to lowercase
        - Ensure valid Scheme identifier
        """
        # Replace path separators and special chars
        sanitized = name.replace('/', '-').replace('_', '-')
        sanitized = sanitized.replace('.', '-').replace(' ', '-')
        
        # Convert to lowercase
        sanitized = sanitized.lower()
        
        # Remove leading/trailing hyphens
        sanitized = sanitized.strip('-')
        
        # Ensure it starts with a letter or special char allowed in Scheme
        if sanitized and sanitized[0].isdigit():
            sanitized = 'n' + sanitized
        
        # Replace multiple hyphens
        while '--' in sanitized:
            sanitized = sanitized.replace('--', '-')
        
        return sanitized or 'unnamed'
    
    def tree_to_scheme_function(self, tree: TreeNode, style: str = 'let') -> str:
        """
        Convert a rooted tree to Scheme code.
        
        Args:
            tree: TreeNode representing the tree
            style: Scheme style - 'let', 'lambda', or 'module'
            
        Returns:
            Scheme code as string
        """
        if style == 'let':
            return self._tree_to_let_form(tree)
        elif style == 'lambda':
            return self._tree_to_lambda_form(tree)
        elif style == 'module':
            return self._tree_to_module_form(tree)
        else:
            raise ValueError(f"Unknown style: {style}")
    
    def _tree_to_let_form(self, tree: TreeNode, depth: int = 0) -> str:
        """
        Convert tree to nested let expressions.
        
        Structure:
        (let ((child1 value1)
              (child2 value2))
          body)
        """
        lines = []
        name = self._sanitize_name(tree.name)
        
        if not tree.children:
            # Leaf node - return a simple value
            if tree.is_file:
                return f"'{name}"
            else:
                return "'()"
        
        # Has children - create let binding
        indent = self.indent_str * depth
        
        if tree.is_file:
            # File with structure
            lines.append(f"{indent}(let ((file '{name})")
        else:
            # Folder/scope
            lines.append(f"{indent}(let ((scope '{name})")
        
        # Add child bindings
        for i, child in enumerate(tree.children):
            child_name = self._sanitize_name(child.name)
            
            if not child.children:
                # Simple binding
                if child.is_file:
                    lines.append(f"{indent}      ({child_name} 'file)")
                else:
                    lines.append(f"{indent}      ({child_name} 'folder)")
            else:
                # Nested structure - recurse
                child_code = self._tree_to_let_form(child, depth + 3)
                # Extract the binding part
                lines.append(f"{indent}      ({child_name}")
                # Add indented child code
                for line in child_code.split('\n'):
                    if line.strip():
                        lines.append(f"{indent}        {line.strip()}")
                lines.append(f"{indent}       )")
        
        lines.append(f"{indent}      )")
        
        # Body - return list of all bindings
        binding_names = ['file' if tree.is_file else 'scope'] + \
                       [self._sanitize_name(c.name) for c in tree.children]
        lines.append(f"{indent}  (list {' '.join(binding_names)}))")
        
        return '\n'.join(lines)
    
    def _tree_to_lambda_form(self, tree: TreeNode, depth: int = 0) -> str:
        """
        Convert tree to nested lambda expressions.
        
        Structure:
        ((lambda (child1 child2)
           body)
         value1 value2)
        """
        lines = []
        indent = self.indent_str * depth
        name = self._sanitize_name(tree.name)
        
        if not tree.children:
            # Leaf - simple value
            return f"'{name}"
        
        # Create lambda
        child_names = [self._sanitize_name(c.name) for c in tree.children]
        lines.append(f"{indent}((lambda ({' '.join(child_names)})")
        
        # Body - construct result
        result_expr = f"(list '{name} {' '.join(child_names)})"
        lines.append(f"{indent}   {result_expr})")
        
        # Arguments - evaluate children
        for child in tree.children:
            if child.children:
                child_code = self._tree_to_lambda_form(child, depth + 1)
                lines.append(f" {child_code}")
            else:
                lines.append(f" '{self._sanitize_name(child.name)}")
        
        lines.append(")")
        
        return '\n'.join(lines)
    
    def _tree_to_module_form(self, tree: TreeNode, depth: int = 0) -> str:
        """
        Convert tree to module/define structure.
        
        Structure:
        (define (module-name)
          (define child1 value1)
          (define child2 value2)
          (list child1 child2))
        """
        lines = []
        indent = self.indent_str * depth
        name = self._sanitize_name(tree.name)
        
        if not tree.children:
            # Leaf - just a definition
            return f"{indent}(define {name} '{name})"
        
        # Module definition
        lines.append(f"{indent}(define ({name})")
        
        # Define children
        for child in tree.children:
            child_name = self._sanitize_name(child.name)
            
            if not child.children:
                # Simple definition
                kind = 'file' if child.is_file else 'folder'
                lines.append(f"{indent}  (define {child_name} '{kind})")
            else:
                # Nested module
                child_code = self._tree_to_module_form(child, depth + 1)
                lines.append(child_code)
        
        # Return list of children
        child_names = [self._sanitize_name(c.name) for c in tree.children]
        lines.append(f"{indent}  (list {' '.join(child_names)}))")
        
        return '\n'.join(lines)
    
    def parentheses_to_scheme(self, parentheses: str, names: List[str]) -> str:
        """
        Convert parentheses notation directly to Scheme S-expression.
        
        Args:
            parentheses: String like "((())()())"
            names: List of names to assign to nodes
            
        Returns:
            Scheme S-expression
        """
        # Parse parentheses to build tree structure
        stack = []
        current = []
        name_idx = 0
        
        for char in parentheses:
            if char == '(':
                stack.append(current)
                current = []
            elif char == ')':
                # Close current scope
                if current:
                    # Has children - create list
                    expr = f"(list {' '.join(current)})"
                else:
                    # Empty - use name
                    if name_idx < len(names):
                        expr = f"'{names[name_idx]}"
                        name_idx += 1
                    else:
                        expr = "'()"
                
                if stack:
                    parent = stack.pop()
                    parent.append(expr)
                    current = parent
                else:
                    # Top level
                    current = [expr]
        
        return current[0] if current else "'()"


class SchemeVaultBijection:
    """
    Creates bijection between vault structure and Scheme code.
    
    This extends the tree-graph bijection to include Scheme code representation:
    - Folder tree → Scheme execution contexts
    - Link graph → Scheme data structures
    - Files → Functions/variables
    """
    
    def __init__(self, vault: MarkdownVault):
        self.vault = vault
        self.tree_bijection = VaultTreeBijection(vault)
        self.scheme_gen = SchemeCodeGenerator()
    
    def folder_structure_to_scheme(self, style: str = 'let') -> str:
        """
        Convert folder structure to Scheme code.
        
        Args:
            style: 'let', 'lambda', or 'module'
            
        Returns:
            Scheme code representing the folder structure
        """
        tree = self.tree_bijection.folder_structure_to_tree()
        return self.scheme_gen.tree_to_scheme_function(tree, style)
    
    def link_graph_to_scheme(self, style: str = 'let') -> str:
        """
        Convert link graph to Scheme code.
        
        Args:
            style: 'let', 'lambda', or 'module'
            
        Returns:
            Scheme code representing the link graph
        """
        tree = self.tree_bijection.link_graph_to_tree()
        return self.scheme_gen.tree_to_scheme_function(tree, style)
    
    def parentheses_to_scheme(self, parentheses: str, names: List[str]) -> str:
        """
        Convert parentheses notation to Scheme S-expression.
        
        Args:
            parentheses: Parentheses string like "((())())"
            names: Names for the nodes
            
        Returns:
            Scheme S-expression
        """
        return self.scheme_gen.parentheses_to_scheme(parentheses, names)
    
    def generate_executable_vault_scheme(self) -> str:
        """
        Generate complete executable Scheme program representing the vault.
        
        Returns:
            Complete Scheme program with all mappings
        """
        lines = [
            ";; Vault Structure as Scheme Code",
            ";; Auto-generated bijection from folder/link structure",
            ";; to Scheme execution contexts",
            "",
            ";; Folder Structure (Let-binding style)",
            "(define vault-folders",
        ]
        
        folder_code = self.folder_structure_to_scheme('let')
        for line in folder_code.split('\n'):
            lines.append("  " + line)
        lines.append(")")
        
        lines.extend([
            "",
            ";; Link Graph (Lambda style)",
            "(define vault-links",
        ])
        
        link_code = self.link_graph_to_scheme('lambda')
        for line in link_code.split('\n'):
            lines.append("  " + line)
        lines.append(")")
        
        lines.extend([
            "",
            ";; Parentheses Notation",
            "(define folder-parentheses",
            f"  '{self.tree_bijection.compare_structures()['folder_tree']['parentheses']})",
            "",
            "(define link-parentheses",
            f"  '{self.tree_bijection.compare_structures()['link_graph']['parentheses']})",
            "",
            ";; Display structure",
            "(define (show-vault)",
            "  (display \"Vault Folder Structure:\\n\")",
            "  (display vault-folders)",
            "  (newline)",
            "  (display \"\\nVault Link Graph:\\n\")",
            "  (display vault-links)",
            "  (newline)",
            "  (display \"\\nParentheses Notations:\\n\")",
            "  (display \"Folders: \")",
            "  (display folder-parentheses)",
            "  (newline)",
            "  (display \"Links: \")",
            "  (display link-parentheses)",
            "  (newline))",
            "",
            ";; Run to see output",
            ";; (show-vault)",
        ])
        
        return '\n'.join(lines)


def main():
    """CLI interface for Scheme bijection."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Convert vault structure to Scheme code'
    )
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Root path of the vault'
    )
    parser.add_argument(
        '--style',
        choices=['let', 'lambda', 'module'],
        default='let',
        help='Scheme code style (default: let)'
    )
    parser.add_argument(
        '--folders',
        action='store_true',
        help='Show folder structure as Scheme'
    )
    parser.add_argument(
        '--links',
        action='store_true',
        help='Show link graph as Scheme'
    )
    parser.add_argument(
        '--executable',
        action='store_true',
        help='Generate complete executable Scheme program'
    )
    parser.add_argument(
        '--output',
        help='Output file (default: stdout)'
    )
    
    args = parser.parse_args()
    
    # Load vault
    print(f";; Loading vault from: {args.path}", file=__import__('sys').stderr)
    vault = MarkdownVault(args.path)
    vault.scan()
    
    scheme_bijection = SchemeVaultBijection(vault)
    
    output = []
    
    # Default: show everything
    show_all = not any([args.folders, args.links, args.executable])
    
    if args.executable or show_all:
        output.append(scheme_bijection.generate_executable_vault_scheme())
    else:
        if args.folders:
            output.append(";; Folder Structure\n")
            output.append(scheme_bijection.folder_structure_to_scheme(args.style))
        
        if args.links:
            output.append("\n;; Link Graph\n")
            output.append(scheme_bijection.link_graph_to_scheme(args.style))
    
    result = '\n'.join(output)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result)
        print(f";; Scheme code written to {args.output}", file=__import__('sys').stderr)
    else:
        print(result)


if __name__ == '__main__':
    main()
