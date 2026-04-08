# ROADMAP — Tier 1: Algebraic Foundation

> **Purpose**: Implementation spec for extending the `mathcline` library.
> Each section specifies: what to build, the mathematical definition, the API,
> validation checks, and references. Written so that each item can be
> implemented and tested independently.
>
> **Architecture decision**: Single-class, sympy-aware (cf. SymPy Geometry module).
> If the user passes `sympy.Rational` or `sympy.Symbol`, operations are exact.
> If the user passes `float` / `complex`, operations use numpy with tolerance `1e-10`.
> The type of `self.c`, `self.alpha`, `self.d` determines the mode.
> Detect via: `_is_exact = isinstance(c, (sympy.Basic,))`.

---

## 1. Hermitian Matrix Representation

### What
Every cline $cz\bar z + \alpha z + \bar\alpha\bar z + d = 0$ corresponds to
the Hermitian matrix

$$H = \begin{pmatrix} c & \bar\alpha \\ \alpha & d \end{pmatrix}, \quad
H^\dagger = H, \quad c,d \in \mathbb{R}.$$

A point $z$ lies on the cline iff $\mathbf{z}^\dagger H \mathbf{z} = 0$ where
$\mathbf{z} = \binom{z}{1}$ (homogeneous coordinates).

### Why
The Hermitian matrix is how Möbius transformations act on clines (§2 below).
### API

```python
# Property on Cline
@property
def hermitian_matrix(self):
    """Return the 2×2 Hermitian matrix [[c, conj(alpha)], [alpha, d]].

    Returns:
        numpy.ndarray or sympy.Matrix depending on input types.

    Reference:
        Hitchman, GCT, Definition 3.2.3
        https://mphitchman.com/geometry/section3-2.html
    """

# Class method
@classmethod
def from_hermitian_matrix(cls, H):
    """Construct a Cline from a 2×2 Hermitian matrix.

    Args:
        H: 2×2 array-like with H = H†, i.e., H[0,0] and H[1,1] real,
           H[1,0] = conj(H[0,1]).

    Raises:
        ValueError: if H is not Hermitian.

    Reference:
        Hitchman, GCT, Definition 3.2.3
    """
```

### Validation checks

```python
# Round-trip: Cline → matrix → Cline preserves parameters
C = Cline(c=1, alpha=2+1j, d=3)
H = C.hermitian_matrix
C2 = Cline.from_hermitian_matrix(H)
assert abs(C2.c - C.c) < 1e-10
assert abs(C2.alpha - C.alpha) < 1e-10
assert abs(C2.d - C.d) < 1e-10

# Hermiticity: H† = H
assert np.allclose(H, H.conj().T)

# Unit circle: c=1, alpha=0, d=-1 → H = [[1,0],[0,-1]]
S = Cline.from_circle(center=0, radius=1)
assert np.allclose(S.hermitian_matrix, [[1, 0], [0, -1]])

# Line through origin at 45°: Cline.from_line(0, 1+1j)
# c=0, so H[0,0]=0, H[1,1]=d
L = Cline.from_line(0, 1+1j)
assert abs(L.hermitian_matrix[0, 0]) < 1e-10

# det(H) = c*d - |alpha|^2 = -discriminant
assert abs(np.linalg.det(H) - (C.c * C.d - abs(C.alpha)**2)) < 1e-10
```

---

## 2. Möbius Transformations

### What
A Möbius transformation is a map $T(z) = \frac{az+b}{cz+d}$ with
$ad - bc \neq 0$, represented by the matrix
$A = \begin{pmatrix} a & b \\ c & d \end{pmatrix} \in GL(2, \mathbb{C})$.

It acts on points: $T(z) = \frac{az+b}{cz+d}$, with $T(-d/c) = \infty$
and $T(\infty) = a/c$.

It acts on clines via Hermitian matrix congruence:
$$H \mapsto H' = (A^{-1})^\dagger H A^{-1}.$$

### Why
This is the central operation of the Erlangen program. Hitchman's entire
book (Chapters 3–7) is built on Möbius transformations and their action
on clines.

### API

```python
class MoebiusTransformation:
    """A Möbius transformation T(z) = (az + b) / (cz + d).

    Reference:
        Hitchman, GCT, Section 3.4
        https://mphitchman.com/geometry/section3-4.html
    """

    def __init__(self, a, b, c, d):
        """Initialize from coefficients.

        Args:
            a, b, c, d: complex numbers with a*d - b*c != 0.

        Raises:
            ValueError: if a*d - b*c == 0 (degenerate).
        """

    @property
    def matrix(self):
        """Return the 2×2 matrix [[a, b], [c, d]]."""

    @property
    def det(self):
        """Return a*d - b*c."""

    def __call__(self, z):
        """Apply T to a point z in the extended complex plane.

        Args:
            z: complex number, or None representing ∞.

        Returns:
            complex number, or None representing ∞.

        Rules:
            T(z) = (a*z + b) / (c*z + d)  for finite z with c*z + d != 0
            T(-d/c) = None  (i.e., ∞)     when c != 0
            T(None) = a/c                  when c != 0
            T(None) = None                 when c == 0 (affine case)

        Reference:
            Hitchman, GCT, Section 3.3, Definition of Möbius transformation
        """

    def transform_cline(self, cline):
        """Return the image of a Cline under this transformation.

        Uses Hermitian matrix congruence:
            H' = (A^{-1})^† H A^{-1}

        Args:
            cline: a Cline object.

        Returns:
            A new Cline object.

        Reference:
            Hitchman, GCT, Theorem 3.4.8 (Möbius transformations map
            clines to clines)
        """

    def compose(self, other):
        """Return the composition self ∘ other.

        (self ∘ other)(z) = self(other(z))
        Matrix: A_self @ A_other.
        """

    def inverse(self):
        """Return the inverse transformation T^{-1}.

        If T has matrix [[a,b],[c,d]] then T^{-1} has matrix [[d,-b],[-c,a]].
        """

    @classmethod
    def from_three_points(cls, z1, z2, z3, w1, w2, w3):
        """Return the unique Möbius transformation sending z_i → w_i.

        The cross-ratio construction:
            T = S_w^{-1} ∘ S_z
        where S_z sends (z1, z2, z3) → (1, 0, ∞).

        Reference:
            Hitchman, GCT, Section 3.4, "tracking three points"
        """

    # --- Standard generators ---

    @classmethod
    def translation(cls, b):
        """z ↦ z + b. Matrix [[1, b], [0, 1]]."""

    @classmethod
    def rotation(cls, theta):
        """z ↦ e^{iθ} z. Matrix [[e^{iθ}, 0], [0, 1]]."""

    @classmethod
    def dilation(cls, r):
        """z ↦ r*z for real r > 0. Matrix [[r, 0], [0, 1]]."""

    @classmethod
    def inversion(cls):
        """z ↦ 1/z. Matrix [[0, 1], [1, 0]]."""

    # --- Classification (Hitchman §3.5) ---

    @property
    def trace(self):
        """Return tr(A) = a + d (well-defined up to sign in PGL(2,C))."""

    @property
    def fixed_points(self):
        """Return the fixed points of T (solutions of T(z) = z).

        Solves c*z^2 + (d - a)*z - b = 0.
        Returns list of 0, 1, or 2 complex numbers (or None for ∞).
        """

    def classification(self):
        """Classify T as 'identity', 'parabolic', 'elliptic',
        'hyperbolic', or 'loxodromic'.

        Normalize so det = 1 first. Then use tr^2:
            tr^2 ∈ [0, 4)  → elliptic
            tr^2 = 4        → parabolic (if T ≠ ±I)
            tr^2 ∈ (4, ∞)   → hyperbolic
            tr^2 ∈ C \ [0,4] → loxodromic

        Reference:
            Hitchman, GCT, Section 3.5
            https://mphitchman.com/geometry/section3-5.html
        """

    def __str__(self):
        """Return string: 'T(z) = (az + b)/(cz + d)'."""
```

### Validation checks

```python
# --- Identity ---
I = MoebiusTransformation(1, 0, 0, 1)
assert I(3+4j) == 3+4j
assert I(None) is None  # T(∞) = ∞
assert I.classification() == 'identity'

# --- Inversion maps circles to circles ---
inv = MoebiusTransformation.inversion()  # z ↦ 1/z
C = Cline.from_circle(center=2, radius=1)
C2 = inv.transform_cline(C)
assert C2.is_circle  # circle not through origin maps to circle

# --- Inversion maps line through origin to line through origin ---
L = Cline.from_line(0, 1+1j)
L2 = inv.transform_cline(L)
assert L2.is_line  # line through 0 maps to line through 0

# --- Line NOT through origin maps to circle through origin ---
L3 = Cline.from_line(1, 1+1j)
L3_img = inv.transform_cline(L3)
assert L3_img.is_circle
assert abs(L3_img.center) - L3_img.radius < 1e-10  # passes through 0

# --- Composition: (T1 ∘ T2)(z) = T1(T2(z)) ---
T1 = MoebiusTransformation(1, 2, 0, 1)   # z + 2
T2 = MoebiusTransformation(0, 1, 1, 0)   # 1/z
T3 = T1.compose(T2)                       # 1/z + 2 = (2z+1)/z
z = 3+1j
assert abs(T3(z) - T1(T2(z))) < 1e-10

# --- Inverse: T ∘ T^{-1} = identity ---
T = MoebiusTransformation(2, 3, 1, 4)
z = 1+2j
assert abs(T(T.inverse()(z)) - z) < 1e-10

# --- Three-point construction ---
T = MoebiusTransformation.from_three_points(0, 1, 1j, 1, 0, None)
assert abs(T(0) - 1) < 1e-10
assert abs(T(1)) < 1e-10
assert T(1j) is None  # maps to ∞

# --- transform_cline round-trip:  T(T^{-1}(C)) = C ---
T = MoebiusTransformation(1, 1j, 0, 1)
C = Cline.from_circle(center=0, radius=2)
C_back = T.inverse().transform_cline(T.transform_cline(C))
assert abs(C_back.center - C.center) < 1e-10
assert abs(C_back.radius - C.radius) < 1e-10

# --- Unit circle maps to itself under z ↦ e^{iθ}z ---
T = MoebiusTransformation.rotation(0.5)
S = Cline.from_circle(center=0, radius=1)
S2 = T.transform_cline(S)
assert abs(S2.center) < 1e-10
assert abs(S2.radius - 1) < 1e-10

# --- Classification ---
# Parabolic: z ↦ z + 1, tr^2 = 4
P = MoebiusTransformation(1, 1, 0, 1)
assert P.classification() == 'parabolic'
assert len(P.fixed_points) == 1  # one fixed point: ∞

# Elliptic: z ↦ e^{iπ/3} z, tr^2 = (e^{iπ/6} + e^{-iπ/6})^2 = 3
import cmath
E = MoebiusTransformation(cmath.exp(1j*cmath.pi/6), 0, 0,
                           cmath.exp(-1j*cmath.pi/6))
assert E.classification() == 'elliptic'

# Hyperbolic: z ↦ 2z, tr^2 = (√2 + 1/√2)^2 = 9/2
H = MoebiusTransformation(2, 0, 0, 1)
assert H.classification() == 'hyperbolic'

# Loxodromic: z ↦ (1+i)z, |multiplier| ≠ 1 and not real
Lox = MoebiusTransformation(1+1j, 0, 0, 1)
assert Lox.classification() == 'loxodromic'
```

---

## 3. Extended Complex Plane (∞ handling)

### What
The extended complex plane $\hat{\mathbb{C}} = \mathbb{C} \cup \{\infty\}$
(Riemann sphere). Convention: represent $\infty$ as `None`.

Lines are clines that pass through $\infty$.
A Möbius transformation may send finite points to $\infty$ and vice versa.

### Why
Without ∞, you cannot:
- Apply a Möbius transformation that has a pole (sends a finite point to ∞)
- Construct the cross-ratio when one point is ∞
- Express that a "line" is a "circle through ∞"
- Work with `from_three_points` when one point is ∞

### API changes

```python
# On Cline class:

def contains(self, z):
    """Test if point z lies on this cline.

    Args:
        z: complex number, or None (∞).

    Returns:
        bool (numeric mode: |c|z|² + αz + ᾱz̄ + d| < tol)
        sympy expression (symbolic mode)

    Note:
        Lines (c=0) always contain ∞.
        Circles (c≠0) never contain ∞.

    Reference:
        Hitchman, GCT, Definition 3.2.3
    """

def invert(self, z):
    """Return the image of z under inversion in this cline.

    For a circle with center z₀ and radius r:
        z* = z₀ + r² / conj(z - z₀)

    For a line with normal α:
        z* = reflection of z across the line

    Args:
        z: complex number, or None (∞).

    Returns:
        complex number, or None (∞).

    Rules:
        Circle: invert(center) = None, invert(None) = center.
        Line: invert(None) = None (lines pass through ∞, which is fixed).

    Reference:
        Hitchman, GCT, Definition 3.2.6 (inversion in a circle)
        Hitchman, GCT, Section 3.1 (reflection in a line)
    """
```

```python
# Standalone function:

def cross_ratio(z, z1, z2, z3):
    """Compute the cross-ratio (z, z1; z2, z3).

    Formula (all finite):
        (z, z1; z2, z3) = (z - z2)(z1 - z3) / ((z - z3)(z1 - z2))

    When any argument is None (∞), cancel the two factors containing it.
    E.g., (∞, z1; z2, z3) = (z1 - z3) / (z1 - z2).

    Args:
        z, z1, z2, z3: complex numbers or None.

    Returns:
        complex number, or None.

    Reference:
        Hitchman, GCT, Section 3.4, equation (3.4.3)
        https://mphitchman.com/geometry/section3-4.html
    """
```

### Validation checks

```python
# --- contains ---
S = Cline.from_circle(center=0, radius=1)
assert S.contains(1)
assert S.contains(1j)
assert not S.contains(0.5)
assert not S.contains(None)  # circle does not contain ∞

L = Cline.from_line(0, 1)  # real axis
assert L.contains(5.0)
assert not L.contains(1j)
assert L.contains(None)  # line contains ∞

# --- invert ---
# Inversion in unit circle: z* = 1/z̄
S = Cline.from_circle(center=0, radius=1)
assert abs(S.invert(2) - 0.5) < 1e-10
assert abs(S.invert(1j) - (-1j)) < 1e-10
assert abs(S.invert(0.5) - 2) < 1e-10
assert S.invert(0+0j) is None          # center → ∞
assert abs(S.invert(None) - 0) < 1e-10  # ∞ → center

# Inversion is involution: invert(invert(z)) = z
z = 3 + 2j
C = Cline.from_circle(center=1+1j, radius=3)
assert abs(C.invert(C.invert(z)) - z) < 1e-10

# Points on the cline are fixed by inversion
C = Cline.from_circle(center=0, radius=2)
z_on = 2  # on the circle
assert abs(C.invert(z_on) - z_on) < 1e-10

# Reflection in real axis: Cline.from_line(-1, 1)
L = Cline.from_line(-1, 1)
assert abs(L.invert(1 + 2j) - (1 - 2j)) < 1e-10

# --- cross_ratio ---
# Four points on unit circle → real cross-ratio
cr = cross_ratio(1, 1j, -1, -1j)
assert abs(cr.imag) < 1e-10  # real
assert abs(cr - 2) < 1e-10   # Hitchman's example

# Cross-ratio with ∞
cr2 = cross_ratio(None, 1, 0, -1)
# (∞,1;0,-1) = (1 - (-1))/(1 - 0) = 2
assert abs(cr2 - 2) < 1e-10

# Möbius transformation preserves cross-ratio
T = MoebiusTransformation(2, 3, 1, 4)
pts = [1, 2, 3, 4]
cr_before = cross_ratio(*pts)
cr_after = cross_ratio(*[T(z) for z in pts])
assert abs(cr_before - cr_after) < 1e-10

# Four concyclic points ⟺ real cross-ratio
C = Cline.from_circle(center=0, radius=2)
import cmath
pts = [2*cmath.exp(1j*t) for t in [0, 0.7, 1.5, 2.3]]
cr = cross_ratio(*pts)
assert abs(cr.imag) < 1e-10

# Non-concyclic → complex cross-ratio
cr = cross_ratio(0, 1, 1j, 2+3j)
assert abs(cr.imag) > 0.01
```

---

## 4. Cline–Cline Operations

### 4a. Intersection

```python
def intersection(self, other):
    """Return the intersection points of two clines.

    Returns:
        list of 0, 1, or 2 complex numbers.
        Empty list if no intersection.
        One point if tangent.
        Two points if transversal.

    Cases:
        circle–circle: solve system of two quadratics
        circle–line: substitute parametric line into circle equation
        line–line: solve 2×2 linear system (or empty if parallel)

    Reference:
        Standard analytic geometry; used implicitly throughout
        Hitchman GCT Chapters 5–6 for constructing geodesics.
    """
```

### 4b. Angle between clines

```python
def angle(self, other):
    """Return the angle between two clines at their intersection.

    For two circles with centers z1, z2 and radii r1, r2:
        cos θ = (|z1 - z2|² - r1² - r2²) / (2 r1 r2)

    For circle and line: angle between line and the tangent
    to the circle at the intersection point.

    For two lines: angle between direction vectors.

    Returns:
        float (radians) or sympy expression.
        Raises ValueError if the clines do not intersect.

    Reference:
        Hitchman, GCT, Section 3.2 (orthogonality used in
        Definition 5.1.2 of hyperbolic geometry)
    """

def is_orthogonal(self, other):
    """Return True if two clines meet at right angles.

    This is the key predicate for hyperbolic geometry:
    geodesics in the Poincaré disk are clines orthogonal
    to the unit circle.

    Reference:
        Hitchman, GCT, Section 5.1
    """
```

### Validation checks

```python
# --- intersection ---
# Two concentric circles: no intersection
C1 = Cline.from_circle(center=0, radius=1)
C2 = Cline.from_circle(center=0, radius=2)
assert len(C1.intersection(C2)) == 0

# Circle and tangent line: 1 intersection
C = Cline.from_circle(center=0, radius=1)
L = Cline.from_line(1, 1+1j)  # vertical line x=1, tangent to unit circle
pts = C.intersection(L)
assert len(pts) == 1
assert abs(pts[0] - 1) < 1e-10

# Two intersecting circles: 2 intersections, points lie on both
C1 = Cline.from_circle(center=0, radius=2)
C2 = Cline.from_circle(center=2, radius=2)
pts = C1.intersection(C2)
assert len(pts) == 2
for p in pts:
    assert C1.contains(p)
    assert C2.contains(p)

# --- angle & orthogonality ---
# Unit circle and real axis are orthogonal (meet at ±1 at right angles)
S = Cline.from_circle(center=0, radius=1)
L = Cline.from_line(-1, 1)
assert S.is_orthogonal(L)

# Circle centered at 2 with radius √3 is orthogonal to unit circle
# because |center|² = r_outer² + r_inner²: 4 = 3 + 1
C = Cline.from_circle(center=2, radius=3**0.5)
S = Cline.from_circle(center=0, radius=1)
assert S.is_orthogonal(C)

# Two perpendicular lines
L1 = Cline.from_line(0, 1)      # real axis
L2 = Cline.from_line(0, 1j)     # imaginary axis
assert abs(L1.angle(L2) - cmath.pi/2) < 1e-10
```

---

## File structure

After Tier 1 is implemented, the repo should look like:

```
mathcline/
├── cline.py                  # Cline class (extended with §1, §3, §4)
├── mobius.py                 # MoebiusTransformation class (§2)
├── utils.py                  # cross_ratio() and shared helpers
├── tests/
│   ├── test_cline.py         # Tests for Cline (existing + new)
│   ├── test_mobius.py         # Tests for MoebiusTransformation
│   └── test_cross_ratio.py   # Tests for cross_ratio
├── docs/
│   ├── ...                   # existing docs
│   ├── mobius.rst             # MoebiusTransformation docs
│   └── cross_ratio.rst       # cross_ratio docs
├── ROADMAP.md                # This file
└── ...
```

## Dependencies

- `numpy` — numeric backend (existing)
- `matplotlib` — plotting (existing)
- `sympy` — exact symbolic mode (new, optional at runtime)
  - Use `try: import sympy` pattern so the library works without sympy
    for pure numeric use.

## Implementation order

1. `cross_ratio()` in `utils.py` — standalone, no dependencies on other new code
2. `Cline.hermitian_matrix` + `from_hermitian_matrix` — extends existing class
3. `Cline.contains()` — extends existing class, uses cline equation
4. `Cline.invert()` — extends existing class
5. `MoebiusTransformation` class — core: `__init__`, `__call__`, `matrix`,
   `inverse`, `compose`, generators
6. `MoebiusTransformation.transform_cline()` — requires §1 (Hermitian matrix)
7. `MoebiusTransformation.from_three_points()` — requires `cross_ratio`
8. `MoebiusTransformation.classification()`, `fixed_points` — requires §2 core
9. `Cline.intersection()` — independent
10. `Cline.angle()`, `is_orthogonal()` — requires `intersection()`

## References

- **[Hitchman]** M. P. Hitchman, *Geometry with an Introduction to Cosmic
  Topology*, 2018 edition. https://mphitchman.com/geometry/
  - §3.2: Clines, inversion — https://mphitchman.com/geometry/section3-2.html
  - §3.4: Möbius transformations, cross-ratio — https://mphitchman.com/geometry/section3-4.html
  - §3.5: Classification (elliptic, parabolic, hyperbolic, loxodromic) — https://mphitchman.com/geometry/section3-5.html
  - §5.1: Poincaré disk model — https://mphitchman.com/geometry/section5-1.html

- **[Sage]** SageMath Hyperbolic Geometry module.
  https://doc.sagemath.org/html/en/reference/hyperbolic_geometry/

- **[SymPy]** SymPy Geometry module.
  https://docs.sympy.org/latest/modules/geometry/index.html
