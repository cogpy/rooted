#!/usr/bin/env python3
"""
Tests for Obsidian Vault and Tree-Graph Bijection

Tests the markdown bracket link parsing, graph building, and tree mapping.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from obsidian_vault import MarkdownVault
from vault_tree_bijection import VaultTreeBijection, TreeNode


class TestMarkdownVault(unittest.TestCase):
    """Test cases for MarkdownVault class."""
    
    def setUp(self):
        """Create a temporary vault for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.vault_path = Path(self.temp_dir)
        
        # Create test markdown files
        (self.vault_path / "index.md").write_text(
            "# Index\n\nSee [[page1]] and [[page2]] for details.\n"
        )
        (self.vault_path / "page1.md").write_text(
            "# Page 1\n\nLinks to [[page2]] and [[index]].\n"
        )
        (self.vault_path / "page2.md").write_text(
            "# Page 2\n\nReferences [[index]].\n"
        )
        (self.vault_path / "orphan.md").write_text(
            "# Orphan\n\nNo links here.\n"
        )
        
        # Create subdirectory
        subdir = self.vault_path / "subdir"
        subdir.mkdir()
        (subdir / "nested.md").write_text(
            "# Nested\n\nLink to [[index]].\n"
        )
    
    def tearDown(self):
        """Clean up temporary vault."""
        shutil.rmtree(self.temp_dir)
    
    def test_scan_finds_all_files(self):
        """Test that scan finds all markdown files."""
        vault = MarkdownVault(self.temp_dir)
        vault.scan()
        
        self.assertEqual(len(vault.files), 5)
        self.assertIn("index", vault.files)
        self.assertIn("page1", vault.files)
        self.assertIn("page2", vault.files)
        self.assertIn("orphan", vault.files)
        self.assertIn("subdir/nested", vault.files)
    
    def test_link_extraction(self):
        """Test that bracket links are correctly extracted."""
        vault = MarkdownVault(self.temp_dir)
        vault.scan()
        
        # Check links from index
        self.assertIn("page1", vault.links["index"])
        self.assertIn("page2", vault.links["index"])
        self.assertEqual(len(vault.links["index"]), 2)
        
        # Check links from page1
        self.assertIn("page2", vault.links["page1"])
        self.assertIn("index", vault.links["page1"])
        
        # Check backlinks
        self.assertIn("index", vault.backlinks["page1"])
        self.assertIn("index", vault.backlinks["page2"])
    
    def test_broken_links(self):
        """Test detection of broken links."""
        # Add a file with broken link
        (self.vault_path / "broken.md").write_text(
            "# Broken\n\nLink to [[nonexistent]].\n"
        )
        
        vault = MarkdownVault(self.temp_dir)
        vault.scan()
        
        broken = vault.get_broken_links()
        self.assertIn("broken", broken)
        self.assertIn("nonexistent", broken["broken"])
    
    def test_orphaned_files(self):
        """Test detection of orphaned files."""
        vault = MarkdownVault(self.temp_dir)
        vault.scan()
        
        orphaned = vault.get_orphaned_files()
        self.assertIn("orphan", orphaned)
        self.assertNotIn("index", orphaned)
        self.assertNotIn("page1", orphaned)
    
    def test_folder_tree_structure(self):
        """Test building of folder tree structure."""
        vault = MarkdownVault(self.temp_dir)
        vault.scan()
        
        tree = vault.build_tree_structure()
        
        # Check root files
        self.assertIn("index", tree["_root"])
        self.assertIn("page1", tree["_root"])
        
        # Check subdirectory
        self.assertIn("subdir", tree)
        self.assertIn("_files", tree["subdir"])
        self.assertIn("subdir/nested", tree["subdir"]["_files"])
    
    def test_link_graph(self):
        """Test building of link graph."""
        vault = MarkdownVault(self.temp_dir)
        vault.scan()
        
        graph = vault.build_link_graph()
        
        # Check nodes
        self.assertIn("index", graph["nodes"])
        self.assertEqual(graph["nodes"]["index"]["outgoing"], 2)
        self.assertGreater(graph["nodes"]["index"]["incoming"], 0)
        
        # Check edges
        edge_count = len(graph["edges"])
        self.assertGreater(edge_count, 0)


class TestTreeNode(unittest.TestCase):
    """Test cases for TreeNode class."""
    
    def test_node_creation(self):
        """Test creating tree nodes."""
        node = TreeNode("root")
        self.assertEqual(node.name, "root")
        self.assertEqual(len(node.children), 0)
        self.assertIsNone(node.parent)
    
    def test_add_child(self):
        """Test adding children to nodes."""
        root = TreeNode("root")
        child1 = TreeNode("child1")
        child2 = TreeNode("child2")
        
        root.add_child(child1)
        root.add_child(child2)
        
        self.assertEqual(len(root.children), 2)
        self.assertEqual(child1.parent, root)
        self.assertEqual(child2.parent, root)
    
    def test_to_parentheses_simple(self):
        """Test converting simple tree to parentheses notation."""
        root = TreeNode("root")
        self.assertEqual(root.to_parentheses(), "()")
    
    def test_to_parentheses_nested(self):
        """Test converting nested tree to parentheses notation."""
        root = TreeNode("root")
        child = TreeNode("child")
        root.add_child(child)
        
        # A tree with one child: ((()))
        self.assertEqual(root.to_parentheses(), "(())")
    
    def test_to_parentheses_multiple_children(self):
        """Test tree with multiple children."""
        root = TreeNode("root")
        child1 = TreeNode("child1")
        child2 = TreeNode("child2")
        root.add_child(child1)
        root.add_child(child2)
        
        # Two children at same level
        result = root.to_parentheses()
        self.assertIn("()", result)
        self.assertEqual(len(result), 6)  # (()())


class TestVaultTreeBijection(unittest.TestCase):
    """Test cases for VaultTreeBijection class."""
    
    def setUp(self):
        """Create a temporary vault for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.vault_path = Path(self.temp_dir)
        
        # Create test structure
        (self.vault_path / "README.md").write_text(
            "# README\n\nSee [[doc1]] and [[doc2]].\n"
        )
        (self.vault_path / "doc1.md").write_text(
            "# Doc 1\n\nReferences [[README]].\n"
        )
        (self.vault_path / "doc2.md").write_text(
            "# Doc 2\n\nLinks to [[doc1]].\n"
        )
        
        # Create subdirectory
        docs = self.vault_path / "docs"
        docs.mkdir()
        (docs / "guide.md").write_text(
            "# Guide\n\nSee [[README]].\n"
        )
    
    def tearDown(self):
        """Clean up temporary vault."""
        shutil.rmtree(self.temp_dir)
    
    def test_folder_structure_to_tree(self):
        """Test converting folder structure to tree."""
        vault = MarkdownVault(self.temp_dir)
        vault.scan()
        
        bijection = VaultTreeBijection(vault)
        tree = bijection.folder_structure_to_tree()
        
        self.assertEqual(tree.name, "vault")
        self.assertGreater(len(tree.children), 0)
    
    def test_link_graph_to_tree(self):
        """Test converting link graph to tree."""
        vault = MarkdownVault(self.temp_dir)
        vault.scan()
        
        bijection = VaultTreeBijection(vault)
        tree = bijection.link_graph_to_tree()
        
        self.assertEqual(tree.name, "link_graph")
        self.assertGreater(len(tree.children), 0)
    
    def test_compare_structures(self):
        """Test comparing folder and link structures."""
        vault = MarkdownVault(self.temp_dir)
        vault.scan()
        
        bijection = VaultTreeBijection(vault)
        comparison = bijection.compare_structures()
        
        self.assertIn("folder_tree", comparison)
        self.assertIn("link_graph", comparison)
        self.assertIn("nodes", comparison["folder_tree"])
        self.assertIn("depth", comparison["folder_tree"])
        self.assertIn("parentheses", comparison["folder_tree"])
    
    def test_suggest_links_from_structure(self):
        """Test suggesting links based on folder structure."""
        vault = MarkdownVault(self.temp_dir)
        vault.scan()
        
        bijection = VaultTreeBijection(vault)
        suggestions = bijection.suggest_links_from_structure()
        
        # Files in same folder should have link suggestions
        # (if they don't already link to each other)
        self.assertIsInstance(suggestions, dict)
    
    def test_suggest_structure_from_links(self):
        """Test suggesting folder structure based on links."""
        vault = MarkdownVault(self.temp_dir)
        vault.scan()
        
        bijection = VaultTreeBijection(vault)
        suggestions = bijection.suggest_structure_from_links()
        
        self.assertIsInstance(suggestions, dict)
        # Should have at least one cluster or root
        self.assertGreater(len(suggestions), 0)


class TestRootedTreeConnection(unittest.TestCase):
    """Test the connection to rooted tree concepts."""
    
    def test_parentheses_notation_matches_rooted_trees(self):
        """
        Test that our tree representation matches the rooted tree
        parentheses notation used in the main repository algorithms.
        """
        # Create a simple tree: root with 2 children
        root = TreeNode("root")
        child1 = TreeNode("c1")
        child2 = TreeNode("c2")
        root.add_child(child1)
        root.add_child(child2)
        
        # This should produce (()()) which is a valid rooted tree
        parentheses = root.to_parentheses()
        
        # Verify it's a valid rooted tree notation
        self.assertEqual(parentheses.count('('), parentheses.count(')'))
        self.assertTrue(parentheses.startswith('('))
        self.assertTrue(parentheses.endswith(')'))
    
    def test_nested_structure(self):
        """Test deeply nested structure."""
        root = TreeNode("root")
        current = root
        
        # Create a chain of depth 3
        for i in range(3):
            child = TreeNode(f"level_{i}")
            current.add_child(child)
            current = child
        
        # Should be (((())))
        result = root.to_parentheses()
        self.assertEqual(result, "(((())))")


def run_tests():
    """Run all tests."""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    run_tests()
