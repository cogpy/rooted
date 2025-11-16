Yes — and this is one of the *loveliest cross-domain coincidences* in combinatorics, logic, and theoretical biology:

> **P-systems (membrane systems) in their “free membrane structure” form**
> are enumerated by **OEIS A000081**,
> the number of **unlabeled rooted trees**.

Let me give you:

1. **Full derivation** (why free membrane systems are exactly the same combinatorial class as unlabeled rooted trees).
2. **Examples** (ASCII and membrane diagrams).
3. **Short intuitive summary**.

---

# 1. Full derivation:

## “Free membrane structures = unlabeled rooted trees (A000081)”

### 1.1 What a P-system membrane structure is

In classical **Păun membrane computing**, a **membrane structure** is:

* a rooted hierarchical arrangement of membranes,
* each membrane is a “region” labeled usually by integers (but labels are not mathematical identities),
* membranes may contain sub-membranes, and so on,
* everything sits inside the **skin membrane** (the outside layer).

Diagrammatically:

```
[   [ ]  [ [ ] ]  ]
```

This is literally a **tree**:

* each membrane = a node,
* containment = parent–child relation,
* the skin membrane = the root.

### 1.2 What does “free membrane structure” mean?

In “free P-systems” or “free membrane structures”:

* membrane labels carry **no identity** (unlike classical P-systems where membranes are labeled 1..m and rules refer to them),
* only the **shape** of nesting matters,
* two membrane structures are considered the same if you can rename membrane IDs bijectively.

Thus we are counting membrane structures **up to isomorphism**.

This kills labels ⇒ membranes become **unlabeled nodes**.

### 1.3 What operations are allowed?

A free membrane system allows:

* membranes containing multisets of membranes,
* order between siblings does **not** matter,
* multiplicity of identical sub-membrane patterns **does** matter.

That is exactly the **MSET(T)** construction:

> A membrane contains a **multiset** of sub-membrane structures.

And the whole system is:

> A root (skin) membrane + a multiset of sub-membranes.

This is **precisely** the combinatorial species:

[
T = X \star \operatorname{MSET}(T).
]

Passing to OGFs:

[
R(x) = x \exp\left(\sum_{k\ge 1} R(x^k)/k\right).
]

This is the canonical OGF for **unlabeled rooted trees**.
Exactly OEIS **A000081**.

### 1.4 Why exactly A000081?

Because:

* each membrane structure = an unlabeled rooted tree,
* two membrane structures are equivalent iff their trees are isomorphic,
* the skin membrane is the root,
* no left–right order ⇒ unlabeled,
* children form a multiset ⇒ the exponential formula produces the same functional equation as for unlabeled rooted trees.

Thus:

> **#free P-system membrane structures with n membranes = rₙ (A000081)**.

Values:

| n (membranes) | 1 | 2 | 3 | 4 | 5 | 6  | 7  | …     |
| ------------- | - | - | - | - | - | -- | -- | ----- |
| A000081 rₙ    | 1 | 1 | 2 | 4 | 9 | 20 | 48 | 115 … |

---

# 2. Examples (structures → trees)

### 2.1 n=4 membranes

A000081 says: **4 unlabeled rooted trees**.
Thus 4 free membrane structures.

ASCII membrane depictions and matching trees:

#### (1) Star (skin contains 3 membranes):

```
[ [ ] [ ] [ ] ]
```

Tree:

```
    o
  / | \
 o  o  o
```

#### (2) One branch shallow:

```
[ [ [ ] ] [ ] ]
```

Tree:

```
    o
   / \
  o   o
 /
o
```

#### (3) One branch deep:

```
[ [ [ [ ] ] ] ]
```

Tree:

```
o
|
o
|
o
|
o
```

#### (4) Middle branching:

```
[ [ ] [ [ ] ] ]
```

Tree:

```
    o
    |
    o
   / \
  o   o
```

Exactly r₄ = 4.

---

# 3. Why membrane computing collapses to trees

Underlying reason:

### Membrane *nesting* is a tree.

* No spatial embedding (so no plane order).
* No membrane labels with semantic identity.
* Children are simply **multisets** of membranes.

All of these remove the richer structures that lead to Catalan numbers or to unrooted counts.

Thus A000081 is the *canonical*, *unavoidable* enumeration.

---

# 4. Short intuitive summary

* A free membrane P-system is **just a hierarchy of membranes**, each containing a **multiset** of other membranes.
* This is identical to the recursive specification of **unlabeled rooted trees**.
* Therefore the number of distinct free membrane structures with n membranes is **A000081(n)**.
* The skin membrane = root.
* Sub-membranes = unordered children.
* Their multiplicities give the MSET combinatorics.

So indeed:

> **Free P-systems = unlabeled rooted trees (A000081).**

If you want, I can extend this to:

* unrooted membrane structures (sphere membranes) → A000055;
* “plane” membrane structures (ordered) → A000108;
* membrane systems with labels → labeled rooted trees (n^{n−1});
* relationship between P-system rule application and tree automorphisms.

Just tell me where you want to go.
