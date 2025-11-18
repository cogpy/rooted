# Scheme Code Bijection

This module extends the Obsidian vault bijection to include **Scheme code representation**, creating a three-way mapping:

```
Folder Structure ↔ Rooted Tree ↔ Scheme Code
     ↕                 ↕              ↕
Link Graph      ↔ Rooted Tree ↔ Scheme Code
```

All three representations use **matching parentheses structure** from OEIS A000081.

## Concept

### The Triple Bijection

The Scheme bijection maps rooted trees to executable Scheme code:

1. **Folder hierarchy** → Nested `let` expressions (scopes)
2. **Files** → Variables and functions
3. **Nesting** → Nested execution contexts
4. **Branching** → Multiple bindings in same scope

### Parentheses Preservation

The key property: **parentheses structure is preserved**:

```
Rooted Tree:    ((())()()()())
Scheme Code:    (let ((a ...) (b 'x) (c 'y) (d 'z)) ...)
                     └──┘  └──────────────────┘
                     Nesting    Branching
```

## Features

### 1. Multiple Scheme Styles

**Let-binding style** (nested scopes):
```scheme
(let ((scope 'vault)
      (file1 'file)
      (folder1
        (let ((scope 'folder1)
              (nested-file 'file))
          (list scope nested-file))))
  (list scope file1 folder1))
```

**Lambda style** (functional):
```scheme
((lambda (file1 folder1)
   (list 'vault file1 folder1))
 'file1
 ((lambda (nested-file)
    (list 'folder1 nested-file))
  'nested-file))
```

**Module style** (definitions):
```scheme
(define (vault)
  (define file1 'file)
  (define (folder1)
    (define nested-file 'file)
    (list nested-file))
  (list file1 folder1))
```

### 2. Executable Programs

Generate complete Scheme programs representing your vault:

```scheme
;; Vault Structure as Scheme Code
(define vault-folders
  (let ((scope 'vault) ...)
    (list scope ...)))

(define vault-links
  ((lambda (...) ...)
   ...))

(define folder-parentheses
  '((())()()()()))

(define (show-vault)
  (display vault-folders)
  ...)
```

### 3. Direct Parentheses Conversion

Convert OEIS A000081 parentheses directly to S-expressions:

```python
gen = SchemeCodeGenerator()
scheme = gen.parentheses_to_scheme("((())())", ['a', 'b', 'c'])
# Result: (list (list 'a) 'b 'c)
```

## Installation

No additional dependencies! Uses only Python standard library.

```bash
chmod +x scheme_bijection.py
```

## Usage

### Basic Conversion

```bash
# Convert folder structure to Scheme (let style)
python3 scheme_bijection.py --folders

# Convert link graph to Scheme (lambda style)
python3 scheme_bijection.py --links --style lambda

# Generate complete executable program
python3 scheme_bijection.py --executable
```

### Output to File

```bash
# Save to file
python3 scheme_bijection.py --executable --output vault.scm

# Run in a Scheme interpreter
guile vault.scm
# or
racket vault.scm
```

### Programmatic Use

```python
from scheme_bijection import SchemeVaultBijection
from obsidian_vault import MarkdownVault

# Load vault
vault = MarkdownVault(".")
vault.scan()

# Create bijection
scheme_bij = SchemeVaultBijection(vault)

# Convert to Scheme
folder_scheme = scheme_bij.folder_structure_to_scheme('let')
link_scheme = scheme_bij.link_graph_to_scheme('lambda')

# Generate executable
program = scheme_bij.generate_executable_vault_scheme()

# Save
with open('vault.scm', 'w') as f:
    f.write(program)
```

## Examples

### Example 1: Simple Vault

Vault structure:
```
vault/
├── README.md
├── doc1.md
└── docs/
    └── guide.md
```

Generated Scheme (let style):
```scheme
(let ((scope 'vault)
      (readme 'file)
      (doc1 'file)
      (docs
        (let ((scope 'docs)
              (guide 'file))
          (list scope guide))))
  (list scope readme doc1 docs))
```

### Example 2: Link Graph

Links:
- README → doc1
- doc1 → guide

Generated Scheme (lambda style):
```scheme
((lambda (readme)
   (list 'link-graph readme))
 ((lambda (doc1)
    (list 'readme doc1))
  ((lambda (guide)
     (list 'doc1 guide))
   'guide)))
```

### Example 3: Parentheses Comparison

```bash
$ python3 scheme_bijection.py --executable | grep parentheses
(define folder-parentheses
  '((())()()()()()()()()()()()()()()))
(define link-parentheses
  '((()()()()()()()()()())(())()()))
```

Both match the OEIS A000081 notation from the rooted tree algorithms!

### Example 4: Different Styles

```bash
# Let style (default)
python3 scheme_bijection.py --folders --style let

# Lambda style
python3 scheme_bijection.py --folders --style lambda

# Module style
python3 scheme_bijection.py --folders --style module
```

## API Reference

### SchemeCodeGenerator

```python
class SchemeCodeGenerator:
    """Converts rooted trees to Scheme code."""
    
    def tree_to_scheme_function(tree: TreeNode, style: str) -> str:
        """
        Convert tree to Scheme code.
        
        Args:
            tree: TreeNode to convert
            style: 'let', 'lambda', or 'module'
        
        Returns:
            Scheme code as string
        """
    
    def parentheses_to_scheme(parentheses: str, names: List[str]) -> str:
        """
        Convert parentheses notation to S-expression.
        
        Args:
            parentheses: String like "((())())"
            names: Node names
        
        Returns:
            Scheme S-expression
        """
```

### SchemeVaultBijection

```python
class SchemeVaultBijection:
    """Bijection between vault structure and Scheme code."""
    
    def folder_structure_to_scheme(style: str = 'let') -> str:
        """Convert folder structure to Scheme."""
    
    def link_graph_to_scheme(style: str = 'let') -> str:
        """Convert link graph to Scheme."""
    
    def generate_executable_vault_scheme() -> str:
        """Generate complete Scheme program."""
```

## Mathematical Foundation

### Nesting & Branching in Scheme

The Scheme bijection embodies the repository's core algebra:

| Concept | Tree | Scheme |
|---------|------|--------|
| **Nesting** | Parent-child edges | Nested `(let ...)` scopes |
| **Branching** | Siblings | Multiple bindings `(a ...) (b ...) (c ...)` |
| **Leaves** | Files | Simple values `'file` |
| **Composition** | Tree structure | S-expression structure |

### Parentheses Isomorphism

The bijection preserves the parentheses structure:

```
Tree Parentheses:    ((())()()())
                      ↓
Scheme Code:        (let ((a (let ...)) (b 'x) (c 'y) (d 'z)) ...)
                         └─────┘        └──────────────┘
                         Nesting        Branching
```

This is a **structure-preserving map** (homomorphism) between:
- Rooted trees (combinatorial objects)
- Scheme S-expressions (syntactic objects)

### Connection to OEIS A000081

The parentheses notation connects all three representations:

```python
# Get parentheses from tree
tree.to_parentheses()  # "((())()())"

# Get parentheses from Scheme
# Count nesting structure in generated code
# Same pattern as tree!

# Compare with rooted tree enumeration
from rootrees.list_rooted_trees_optimized import count_rooted_trees
# Same mathematical object!
```

## Scheme Execution

The generated Scheme code is **executable**!

### With Guile

```bash
python3 scheme_bijection.py --executable --output vault.scm
guile vault.scm
```

In Guile REPL:
```scheme
guile> (load "vault.scm")
guile> (show-vault)
Vault Folder Structure:
(vault ...)
...
```

### With Racket

```bash
racket vault.scm
```

Or in DrRacket, add at the top:
```scheme
#lang racket
;; rest of generated code
```

### With Chicken Scheme

```bash
csi -s vault.scm
```

## Use Cases

### 1. Vault as Executable Code

Represent your knowledge base as runnable Scheme:
- Folders → Modules
- Files → Functions
- Links → Function calls

### 2. Structural Analysis

Use Scheme macros to analyze vault structure:
```scheme
(define-syntax analyze-structure
  (syntax-rules ()
    ((analyze-structure (let bindings body))
     (list 'scope (length bindings)))))
```

### 3. Code Generation

Generate code that mirrors your documentation:
```scheme
;; If docs/api.md exists
(define (api)
  (define endpoint-1 'function)
  (define endpoint-2 'function)
  ...)
```

### 4. Literate Programming

Bridge between documentation and code:
- Markdown files → Documentation
- Scheme code → Implementation
- Both have same structure!

### 5. Educational Tool

Teach Scheme using vault structure:
- Visual folder tree → Abstract syntax tree
- File organization → Code organization
- Links → Dependencies

## Testing

Run the test suite:

```bash
python3 test_scheme_bijection.py
```

Tests cover:
- Name sanitization for Scheme identifiers
- Tree to Scheme conversion (all styles)
- Parentheses balancing
- Structure preservation
- Executable program generation

All 14 tests passing ✓

## Advanced Features

### Custom Scheme Patterns

Extend the generator for custom patterns:

```python
class CustomSchemeGen(SchemeCodeGenerator):
    def tree_to_custom_form(self, tree):
        # Your custom Scheme pattern
        pass
```

### Scheme Macros

Use the generated code with Scheme macros:

```scheme
(define-syntax with-vault
  (syntax-rules ()
    ((with-vault vault-folders body ...)
     (let ((current-vault vault-folders))
       body ...))))
```

### Integration with Scheme Libraries

Use with existing Scheme code:

```scheme
;; Import generated vault structure
(load "vault.scm")

;; Use with your library
(import (your-library))

(process-vault vault-folders)
```

## Limitations

### Current Scope

- Names are sanitized to valid Scheme identifiers
- File content is not included (only structure)
- Links are represented structurally, not executed

### Future Enhancements

Potential additions:
- [ ] Include file content as Scheme strings
- [ ] Execute links as function calls
- [ ] Generate Scheme modules per folder
- [ ] Support for Scheme R6RS/R7RS standards
- [ ] Integration with Racket packages
- [ ] Scheme REPL with vault navigation

## Comparison with Other Representations

| Feature | Folder Tree | Link Graph | Parentheses | Scheme Code |
|---------|-------------|------------|-------------|-------------|
| **Human readable** | ✓ | ✓ | △ | ✓ |
| **Machine readable** | ✓ | ✓ | ✓ | ✓ |
| **Executable** | ✗ | ✗ | ✗ | ✓ |
| **Analyzable** | △ | ✓ | ✓ | ✓ |
| **Mathematical** | △ | ✓ | ✓ | ✓ |

The Scheme representation adds **executability** while preserving all structural properties!

## References

### Scheme Language

- [R7RS Scheme Standard](https://small.r7rs.org/)
- [The Scheme Programming Language](https://www.scheme.com/tspl4/)
- [Structure and Interpretation of Computer Programs](https://mitpress.mit.edu/sites/default/files/sicp/index.html)

### Mathematical Background

- [OEIS A000081](https://oeis.org/A000081) - Unlabeled rooted trees
- [Catalan Numbers and Trees](https://en.wikipedia.org/wiki/Catalan_number)
- [S-expressions](https://en.wikipedia.org/wiki/S-expression)

### Related Projects

- [Racket Language](https://racket-lang.org/)
- [GNU Guile](https://www.gnu.org/software/guile/)
- [Chicken Scheme](https://www.call-cc.org/)

## License

Same as the main repository. See [LICENSE](LICENSE) for details.

---

**Scheme Bijection**: Where folder structures become executable code, preserving the mathematical beauty of rooted trees in functional programming form. 🌲→λ
