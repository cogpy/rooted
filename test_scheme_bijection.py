#!/usr/bin/env python3
"""
Tests for Scheme Code Bijection

Tests the conversion from rooted trees to Scheme code with matching
parentheses structure.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from obsidian_vault import MarkdownVault
from vault_tree_bijection import TreeNode
from scheme_bijection import SchemeCodeGenerator, SchemeVaultBijection


class TestSchemeCodeGenerator(unittest.TestCase):
    """Test cases for SchemeCodeGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.gen = SchemeCodeGenerator()
    
    def test_sanitize_name(self):
        """Test name sanitization for Scheme identifiers."""
        # Basic cases
        self.assertEqual(self.gen._sanitize_name("file.md"), "file-md")
        self.assertEqual(self.gen._sanitize_name("my_file"), "my-file")
        self.assertEqual(self.gen._sanitize_name("folder/file"), "folder-file")
        
        # Edge cases
        self.assertEqual(self.gen._sanitize_name("123file"), "n123file")
        self.assertEqual(self.gen._sanitize_name(""), "unnamed")
        self.assertEqual(self.gen._sanitize_name("a--b"), "a-b")
    
    def test_simple_tree_to_let(self):
        """Test converting simple tree to let form."""
        tree = TreeNode("root")
        child = TreeNode("child", is_file=True)
        tree.add_child(child)
        
        result = self.gen._tree_to_let_form(tree)
        
        # Should contain let binding
        self.assertIn("(let", result)
        self.assertIn("'root", result)
        self.assertIn("child", result)
    
    def test_nested_tree_to_let(self):
        """Test converting nested tree to let form."""
        root = TreeNode("root")
        child1 = TreeNode("child1")
        child2 = TreeNode("child2", is_file=True)
        root.add_child(child1)
        child1.add_child(child2)
        
        result = self.gen._tree_to_let_form(root)
        
        # Should have nested let
        self.assertIn("(let", result)
        self.assertIn("child1", result)
        self.assertIn("child2", result)
    
    def test_tree_to_lambda(self):
        """Test converting tree to lambda form."""
        tree = TreeNode("func")
        arg1 = TreeNode("arg1", is_file=True)
        arg2 = TreeNode("arg2", is_file=True)
        tree.add_child(arg1)
        tree.add_child(arg2)
        
        result = self.gen._tree_to_lambda_form(tree)
        
        self.assertIn("(lambda", result)
        self.assertIn("arg1", result)
        self.assertIn("arg2", result)
    
    def test_tree_to_module(self):
        """Test converting tree to module form."""
        tree = TreeNode("module")
        def1 = TreeNode("def1", is_file=True)
        def2 = TreeNode("def2", is_file=True)
        tree.add_child(def1)
        tree.add_child(def2)
        
        result = self.gen._tree_to_module_form(tree)
        
        self.assertIn("(define", result)
        self.assertIn("module", result)
        self.assertIn("def1", result)
        self.assertIn("def2", result)
    
    def test_parentheses_to_scheme(self):
        """Test converting parentheses notation to Scheme."""
        # Simple case: (())
        result = self.gen.parentheses_to_scheme("(())", ["a"])
        self.assertIn("'a", result)
        
        # Multiple children: (()())
        result = self.gen.parentheses_to_scheme("(()())", ["a", "b"])
        self.assertIn("list", result)
    
    def test_parentheses_balancing(self):
        """Test that generated Scheme has balanced parentheses."""
        tree = TreeNode("root")
        for i in range(3):
            tree.add_child(TreeNode(f"child{i}", is_file=True))
        
        for style in ['let', 'lambda', 'module']:
            result = self.gen.tree_to_scheme_function(tree, style)
            
            # Count parentheses
            open_count = result.count('(')
            close_count = result.count(')')
            
            self.assertEqual(
                open_count, close_count,
                f"Unbalanced parentheses in {style} style"
            )


class TestSchemeVaultBijection(unittest.TestCase):
    """Test cases for SchemeVaultBijection class."""
    
    def setUp(self):
        """Create a temporary vault for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.vault_path = Path(self.temp_dir)
        
        # Create test structure
        (self.vault_path / "README.md").write_text(
            "# README\n\nSee [[doc1]].\n"
        )
        (self.vault_path / "doc1.md").write_text(
            "# Doc 1\n\nBack to [[README]].\n"
        )
        
        # Create subdirectory
        docs = self.vault_path / "docs"
        docs.mkdir()
        (docs / "guide.md").write_text(
            "# Guide\n"
        )
    
    def tearDown(self):
        """Clean up temporary vault."""
        shutil.rmtree(self.temp_dir)
    
    def test_folder_structure_to_scheme(self):
        """Test converting folder structure to Scheme."""
        vault = MarkdownVault(self.temp_dir)
        vault.scan()
        
        bijection = SchemeVaultBijection(vault)
        result = bijection.folder_structure_to_scheme('let')
        
        # Should contain vault structure
        self.assertIn("(let", result)
        self.assertIn("readme", result.lower())
        self.assertIn("doc1", result.lower())
    
    def test_link_graph_to_scheme(self):
        """Test converting link graph to Scheme."""
        vault = MarkdownVault(self.temp_dir)
        vault.scan()
        
        bijection = SchemeVaultBijection(vault)
        result = bijection.link_graph_to_scheme('lambda')
        
        # Should contain link structure
        self.assertIn("lambda", result)
    
    def test_executable_generation(self):
        """Test generating complete executable Scheme."""
        vault = MarkdownVault(self.temp_dir)
        vault.scan()
        
        bijection = SchemeVaultBijection(vault)
        result = bijection.generate_executable_vault_scheme()
        
        # Should have all components
        self.assertIn("vault-folders", result)
        self.assertIn("vault-links", result)
        self.assertIn("folder-parentheses", result)
        self.assertIn("link-parentheses", result)
        self.assertIn("show-vault", result)
    
    def test_parentheses_bijection(self):
        """Test that Scheme code preserves parentheses structure."""
        vault = MarkdownVault(self.temp_dir)
        vault.scan()
        
        bijection = SchemeVaultBijection(vault)
        
        # Get folder scheme and count parentheses
        folder_scheme = bijection.folder_structure_to_scheme('let')
        
        # Scheme should have balanced parentheses
        open_count = folder_scheme.count('(')
        close_count = folder_scheme.count(')')
        
        self.assertEqual(open_count, close_count)
    
    def test_all_styles(self):
        """Test that all Scheme styles work."""
        vault = MarkdownVault(self.temp_dir)
        vault.scan()
        
        bijection = SchemeVaultBijection(vault)
        
        for style in ['let', 'lambda', 'module']:
            # Should not raise exception
            folder_result = bijection.folder_structure_to_scheme(style)
            link_result = bijection.link_graph_to_scheme(style)
            
            # Both should have balanced parentheses
            for result in [folder_result, link_result]:
                self.assertEqual(result.count('('), result.count(')'))


class TestSchemeBijectionIntegration(unittest.TestCase):
    """Integration tests for the complete bijection."""
    
    def test_parentheses_preservation(self):
        """
        Test that the bijection preserves parentheses structure.
        
        Tree parentheses → Scheme code should maintain nesting structure.
        """
        # Create simple tree
        root = TreeNode("root")
        child1 = TreeNode("c1", is_file=True)
        child2 = TreeNode("c2", is_file=True)
        root.add_child(child1)
        root.add_child(child2)
        
        # Get parentheses
        tree_parens = root.to_parentheses()
        
        # Convert to Scheme
        gen = SchemeCodeGenerator()
        scheme_code = gen.tree_to_scheme_function(root, 'let')
        
        # Scheme should have same depth of nesting
        # Tree (()()) has 2 levels
        # Scheme should also have nested structure
        
        # Count nesting depth
        max_depth = 0
        current_depth = 0
        for char in scheme_code:
            if char == '(':
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif char == ')':
                current_depth -= 1
        
        self.assertGreater(max_depth, 0)
    
    def test_bijection_roundtrip_concept(self):
        """
        Test the concept of bijection (not actual roundtrip).
        
        While we can't parse Scheme back to trees easily,
        we can verify structural properties are preserved.
        """
        # Create tree
        root = TreeNode("root")
        for i in range(3):
            child = TreeNode(f"child{i}", is_file=True)
            root.add_child(child)
        
        # Get properties
        tree_parens = root.to_parentheses()
        tree_child_count = len(root.children)
        
        # Convert to Scheme
        gen = SchemeCodeGenerator()
        scheme_let = gen.tree_to_scheme_function(root, 'let')
        scheme_lambda = gen.tree_to_scheme_function(root, 'lambda')
        
        # Verify both have same number of child references
        for scheme in [scheme_let, scheme_lambda]:
            for i in range(tree_child_count):
                self.assertIn(f"child{i}", scheme)


def run_tests():
    """Run all tests."""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    run_tests()
