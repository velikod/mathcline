"""Tests for the Cline class."""

import numpy as np
import pytest
import sympy

from cline import Cline


TOL = 1e-10


class TestFromCircle:
    """Tests for Cline.from_circle."""

    def test_real_center(self):
        C = Cline.from_circle(center=3, radius=2)
        assert abs(C.center - 3) < TOL
        assert abs(C.radius - 2) < TOL
        assert C.is_circle

    def test_complex_center(self):
        C = Cline.from_circle(center=1 + 2j, radius=3)
        assert abs(C.center - (1 + 2j)) < TOL
        assert abs(C.radius - 3) < TOL

    def test_complex_center_alpha(self):
        """alpha should be -conj(center), not -center."""
        C = Cline.from_circle(center=1 + 2j, radius=3)
        assert abs(C.alpha - (-1 + 2j)) < TOL

    def test_point_on_circle_satisfies_equation(self):
        center = 1 + 2j
        radius = 3
        C = Cline.from_circle(center=center, radius=radius)
        # Test several points on the circle
        for theta in [0, np.pi / 4, np.pi / 2, np.pi, 3 * np.pi / 2]:
            z = center + radius * np.exp(1j * theta)
            val = C.c * abs(z) ** 2 + C.alpha * z + np.conj(C.alpha) * np.conj(z) + C.d
            assert abs(val) < TOL, f"Point {z} not on circle, val={val}"

    def test_point_inside_circle_does_not_satisfy(self):
        C = Cline.from_circle(center=0, radius=1)
        z = 0.5
        val = C.c * abs(z) ** 2 + C.alpha * z + np.conj(C.alpha) * np.conj(z) + C.d
        assert abs(val) > TOL

    def test_unit_circle(self):
        C = Cline.from_circle(center=0, radius=1)
        assert abs(C.c - 1) < TOL
        assert abs(C.alpha) < TOL
        assert abs(C.d - (-1)) < TOL

    def test_tuple_center(self):
        C = Cline.from_circle(center=(3, 4), radius=5)
        assert abs(C.center - (3 + 4j)) < TOL
        assert abs(C.radius - 5) < TOL

    def test_negative_radius_raises(self):
        with pytest.raises(ValueError):
            Cline.from_circle(center=0, radius=-1)

    def test_zero_radius_raises(self):
        with pytest.raises(ValueError):
            Cline.from_circle(center=0, radius=0)


class TestFromLine:
    """Tests for Cline.from_line."""

    def test_real_axis(self):
        L = Cline.from_line(-1, 1)
        assert L.is_line
        assert abs(L.c) < TOL

    def test_points_on_line_satisfy_equation(self):
        z0, z1 = 1 + 1j, 3 + 2j
        L = Cline.from_line(z0, z1)
        for z in [z0, z1]:
            val = L.c * abs(z) ** 2 + L.alpha * z + np.conj(L.alpha) * np.conj(z) + L.d
            assert abs(val) < TOL

    def test_midpoint_on_line(self):
        z0, z1 = 0, 2 + 2j
        L = Cline.from_line(z0, z1)
        mid = (z0 + z1) / 2
        val = L.c * abs(mid) ** 2 + L.alpha * mid + np.conj(L.alpha) * np.conj(mid) + L.d
        assert abs(val) < TOL

    def test_identical_points_raises(self):
        with pytest.raises(ValueError):
            Cline.from_line(1 + 1j, 1 + 1j)

    def test_imaginary_axis(self):
        L = Cline.from_line(0, 1j)
        assert L.is_line
        # Point off the imaginary axis should not satisfy the equation
        z = 1.0
        val = L.c * abs(z) ** 2 + L.alpha * z + np.conj(L.alpha) * np.conj(z) + L.d
        assert abs(val) > TOL


class TestFromThreePoints:
    """Tests for Cline.from_three_points."""

    def test_circle_through_three_points(self):
        z0, z1, z2 = 1, 1j, -1
        C = Cline.from_three_points(z0, z1, z2)
        assert C.is_circle
        assert abs(C.center) < TOL
        assert abs(C.radius - 1) < TOL

    def test_all_points_satisfy_equation(self):
        z0, z1, z2 = 1 + 1j, 3 + 0j, 0 + 3j
        C = Cline.from_three_points(z0, z1, z2)
        for z in [z0, z1, z2]:
            val = C.c * abs(z) ** 2 + C.alpha * z + np.conj(C.alpha) * np.conj(z) + C.d
            assert abs(val) < TOL

    def test_collinear_points_give_line(self):
        C = Cline.from_three_points(0, 1, 2)
        assert C.is_line

    def test_agrees_with_from_circle(self):
        """from_three_points on a known circle should match from_circle."""
        center = 2 + 3j
        radius = 4
        pts = [center + radius * np.exp(1j * t) for t in [0, 2 * np.pi / 3, 4 * np.pi / 3]]
        C1 = Cline.from_three_points(*pts)
        C2 = Cline.from_circle(center=center, radius=radius)
        assert abs(C1.center - C2.center) < TOL
        assert abs(C1.radius - C2.radius) < TOL


class TestDirectConstructor:
    """Tests for Cline.__init__ with raw parameters."""

    def test_circle_parameters(self):
        C = Cline(c=1, alpha=-1 + 2j, d=0)
        assert C.is_circle
        # center = -conj(alpha)/c = -(-1-2j)/1 = 1+2j
        assert abs(C.center - (1 + 2j)) < TOL

    def test_line_parameters(self):
        C = Cline(c=0, alpha=1 + 0j, d=0)
        assert C.is_line

    def test_point_parameters(self):
        # discriminant = |alpha|^2 - c*d = 0
        C = Cline(c=1, alpha=0, d=0)
        assert C.is_point

    def test_invalid_cline(self):
        # discriminant = |alpha|^2 - c*d = 0 - 1*1 = -1 < 0
        C = Cline(c=1, alpha=0, d=1)
        assert not C.is_circle
        assert not C.is_line
        assert not C.is_point

    def test_discriminant(self):
        C = Cline(c=2, alpha=3 + 4j, d=1)
        expected = abs(3 + 4j) ** 2 - 2 * 1  # 25 - 2 = 23
        assert abs(C.discriminant - expected) < TOL

    def test_scaled_parameters_same_circle(self):
        """Scaling (c, alpha, d) by a real factor gives the same geometric circle."""
        C1 = Cline(c=1, alpha=-1 + 2j, d=0)
        C2 = Cline(c=3, alpha=-3 + 6j, d=0)
        assert abs(C1.center - C2.center) < TOL
        assert abs(C1.radius - C2.radius) < TOL


class TestSymbolicCircle:
    """Tests for symbolic (sympy) mode with circles."""

    def test_unit_circle_exact(self):
        C = Cline.from_circle(center=sympy.Integer(0), radius=sympy.Integer(1))
        assert C._is_exact
        assert C.is_circle
        assert C.c == 1
        assert C.alpha == 0
        assert C.d == -1
        assert C.center == 0
        assert C.radius == 1

    def test_complex_center_exact(self):
        center = sympy.Integer(1) + sympy.I * sympy.Integer(2)
        C = Cline.from_circle(center=center, radius=sympy.Integer(3))
        assert C._is_exact
        assert C.is_circle
        # alpha = -conj(center) = -1 + 2i
        assert C.alpha == -1 + 2 * sympy.I
        assert sympy.simplify(C.center - center) == 0
        assert C.radius == 3

    def test_irrational_radius(self):
        """Circle with radius sqrt(2) — exact, no floating point."""
        C = Cline.from_circle(center=sympy.Integer(0), radius=sympy.sqrt(2))
        assert C._is_exact
        assert C.is_circle
        assert C.d == -2  # |0|^2 - (sqrt(2))^2 = -2
        assert C.radius == sympy.sqrt(2)

    def test_pi_coefficient(self):
        """Use pi as a real parameter."""
        C = Cline(c=sympy.pi, alpha=sympy.Integer(0), d=-sympy.pi)
        assert C._is_exact
        assert C.is_circle
        # discriminant = 0 - pi*(-pi) = pi^2 > 0
        assert sympy.simplify(C.discriminant - sympy.pi**2) == 0
        assert C.center == 0
        assert sympy.simplify(C.radius - 1) == 0

    def test_rational_center(self):
        """Exact rational arithmetic — no floating point error."""
        center = sympy.Rational(1, 3) + sympy.I * sympy.Rational(1, 7)
        C = Cline.from_circle(center=center, radius=sympy.Rational(5, 11))
        assert C._is_exact
        assert C.is_circle
        assert sympy.simplify(C.center - center) == 0
        assert C.radius == sympy.Rational(5, 11)

    def test_point_on_circle_exact(self):
        """Verify a point on the circle satisfies the equation exactly."""
        C = Cline.from_circle(center=sympy.Integer(1) + sympy.I, radius=sympy.Integer(2))
        # z = center + radius = 3 + i is on the circle
        z = sympy.Integer(3) + sympy.I
        val = C.c * z * sympy.conjugate(z) + C.alpha * z + sympy.conjugate(C.alpha) * sympy.conjugate(z) + C.d
        assert sympy.simplify(val) == 0

    def test_discriminant_exact(self):
        C = Cline(c=sympy.Integer(2), alpha=sympy.Integer(3) + 4 * sympy.I, d=sympy.Integer(1))
        # |3+4i|^2 - 2*1 = 25 - 2 = 23
        assert sympy.simplify(C.discriminant - 23) == 0


class TestSymbolicLine:
    """Tests for symbolic (sympy) mode with lines."""

    def test_line_through_origin(self):
        L = Cline.from_line(sympy.Integer(0), sympy.Integer(1))
        assert L._is_exact
        assert L.is_line
        assert L.c == 0

    def test_points_satisfy_equation(self):
        z0 = sympy.Integer(1) + sympy.I
        z1 = sympy.Integer(3) + 2 * sympy.I
        L = Cline.from_line(z0, z1)
        for z in [z0, z1]:
            val = L.alpha * z + sympy.conjugate(L.alpha) * sympy.conjugate(z) + L.d
            assert sympy.simplify(val) == 0

    def test_direct_constructor_line(self):
        L = Cline(c=sympy.Integer(0), alpha=sympy.Integer(1) + sympy.I, d=sympy.Integer(0))
        assert L._is_exact
        assert L.is_line


class TestHermitianMatrix:
    """Tests for hermitian_matrix property and from_hermitian_matrix."""

    def test_unit_circle_matrix(self):
        S = Cline.from_circle(center=0, radius=1)
        H = S.hermitian_matrix
        assert np.allclose(H, [[1, 0], [0, -1]])

    def test_hermiticity(self):
        C = Cline(c=1, alpha=2 + 1j, d=3)
        H = C.hermitian_matrix
        assert np.allclose(H, H.conj().T)

    def test_round_trip(self):
        C = Cline(c=1, alpha=2 + 1j, d=3)
        H = C.hermitian_matrix
        C2 = Cline.from_hermitian_matrix(H)
        assert abs(C2.c - C.c) < TOL
        assert abs(C2.alpha - C.alpha) < TOL
        assert abs(C2.d - C.d) < TOL

    def test_line_matrix(self):
        L = Cline.from_line(0, 1 + 1j)
        H = L.hermitian_matrix
        assert abs(H[0, 0]) < TOL  # c=0

    def test_determinant(self):
        C = Cline(c=1, alpha=2 + 1j, d=3)
        H = C.hermitian_matrix
        det = np.linalg.det(H)
        expected = C.c * C.d - abs(C.alpha) ** 2
        assert abs(det - expected) < TOL

    def test_non_hermitian_raises(self):
        bad_H = np.array([[1, 2 + 1j], [3 + 1j, 4]])  # H[0,1] != conj(H[1,0])
        with pytest.raises(ValueError):
            Cline.from_hermitian_matrix(bad_H)

    def test_symbolic_round_trip(self):
        C = Cline(c=sympy.Integer(1), alpha=sympy.Integer(2) + sympy.I, d=sympy.Integer(3))
        H = C.hermitian_matrix
        assert isinstance(H, sympy.Matrix)
        C2 = Cline.from_hermitian_matrix(H)
        assert C2._is_exact
        assert C2.c == C.c
        assert C2.alpha == C.alpha
        assert C2.d == C.d

    def test_symbolic_hermiticity(self):
        C = Cline(c=sympy.pi, alpha=sympy.sqrt(2) + sympy.I, d=-sympy.pi)
        H = C.hermitian_matrix
        # H[0,1] should equal conj(H[1,0])
        assert sympy.simplify(H[0, 1] - sympy.conjugate(H[1, 0])) == 0


class TestFromThreePointsInfinity:
    """Tests for from_three_points with sympy.zoo (∞)."""

    def test_infinity_gives_line(self):
        """Three points with one at ∞ should give a line."""
        L = Cline.from_three_points(sympy.zoo, sympy.Integer(0), sympy.Integer(1))
        assert L.is_line

    def test_infinity_last(self):
        L = Cline.from_three_points(sympy.Integer(0), sympy.Integer(1), sympy.zoo)
        assert L.is_line

    def test_infinity_middle(self):
        L = Cline.from_three_points(sympy.Integer(1), sympy.zoo, sympy.I)
        assert L.is_line

    def test_two_infinities_raises(self):
        with pytest.raises(ValueError):
            Cline.from_three_points(sympy.zoo, sympy.zoo, sympy.Integer(0))

    def test_line_contains_finite_points(self):
        z0 = sympy.Integer(1) + sympy.I
        z1 = sympy.Integer(3) + 2 * sympy.I
        L = Cline.from_three_points(z0, z1, sympy.zoo)
        assert L.contains(z0)
        assert L.contains(z1)
        assert L.contains(sympy.zoo)  # line contains ∞


class TestContains:
    """Tests for Cline.contains."""

    def test_circle_contains_point_on_circle(self):
        C = Cline.from_circle(center=0, radius=1)
        assert C.contains(1)
        assert C.contains(1j)
        assert C.contains(-1)

    def test_circle_not_contains_interior(self):
        C = Cline.from_circle(center=0, radius=1)
        assert not C.contains(0.5)
        assert not C.contains(0)

    def test_circle_not_contains_infinity(self):
        C = Cline.from_circle(center=0, radius=1)
        assert not C.contains(sympy.zoo)

    def test_line_contains_infinity(self):
        L = Cline.from_line(0, 1)
        assert L.contains(sympy.zoo)

    def test_line_contains_defining_points(self):
        L = Cline.from_line(1 + 1j, 3 + 2j)
        assert L.contains(1 + 1j)
        assert L.contains(3 + 2j)

    def test_symbolic_contains(self):
        C = Cline.from_circle(center=sympy.Integer(0), radius=sympy.Integer(1))
        assert C.contains(sympy.Integer(1))
        assert C.contains(sympy.I)
        assert not C.contains(sympy.Rational(1, 2))


class TestInvert:
    """Tests for Cline.invert."""

    def test_unit_circle_inversion(self):
        S = Cline.from_circle(center=0, radius=1)
        assert abs(S.invert(2) - 0.5) < TOL
        assert abs(S.invert(1j) - 1j) < TOL  # on circle, so fixed
        assert abs(S.invert(0.5) - 2) < TOL
        assert abs(S.invert(2j) - 0.5j) < TOL  # 1/conj(2j) = 1/(-2j) = j/2

    def test_invert_center_gives_infinity(self):
        S = Cline.from_circle(center=0, radius=1)
        assert S.invert(0) is sympy.zoo

    def test_invert_infinity_gives_center(self):
        S = Cline.from_circle(center=0, radius=1)
        assert abs(S.invert(sympy.zoo)) < TOL

    def test_involution(self):
        """Inversion is an involution: invert(invert(z)) = z."""
        C = Cline.from_circle(center=1 + 1j, radius=3)
        z = 3 + 2j
        assert abs(C.invert(C.invert(z)) - z) < TOL

    def test_points_on_circle_fixed(self):
        C = Cline.from_circle(center=0, radius=2)
        z = 2.0  # on the circle
        assert abs(C.invert(z) - z) < TOL

    def test_line_reflection(self):
        """Reflection in the real axis."""
        L = Cline.from_line(-1, 1)  # real axis
        assert abs(L.invert(1 + 2j) - (1 - 2j)) < TOL

    def test_line_invert_infinity(self):
        L = Cline.from_line(0, 1)
        assert L.invert(sympy.zoo) is sympy.zoo

    def test_line_reflection_involution(self):
        L = Cline.from_line(0, 1 + 1j)
        z = 3 + 2j
        assert abs(L.invert(L.invert(z)) - z) < TOL

    def test_symbolic_inversion(self):
        S = Cline.from_circle(center=sympy.Integer(0), radius=sympy.Integer(1))
        assert S.invert(sympy.Integer(2)) == sympy.Rational(1, 2)
        assert S.invert(sympy.Integer(0)) is sympy.zoo
        assert S.invert(sympy.zoo) == 0

    def test_symbolic_involution(self):
        C = Cline.from_circle(
            center=sympy.Rational(1, 3) + sympy.I,
            radius=sympy.Integer(2)
        )
        z = sympy.Integer(3) + 2 * sympy.I
        assert sympy.simplify(C.invert(C.invert(z)) - z) == 0


class TestInvertCline:
    """Tests for inverting a cline in another cline."""

    def test_circle_inverted_in_unit_circle(self):
        """Inversion of a circle not through origin gives a circle."""
        S = Cline.from_circle(center=0, radius=1)
        C = Cline.from_circle(center=2, radius=1)
        C_img = S.invert(C)
        assert C_img.is_circle

    def test_inversion_is_involution(self):
        """Inverting twice gives back the original cline."""
        S = Cline.from_circle(center=0, radius=1)
        C = Cline.from_circle(center=2, radius=1)
        C_back = S.invert(S.invert(C))
        assert abs(C_back.center - C.center) < TOL
        assert abs(C_back.radius - C.radius) < TOL

    def test_circle_through_center_becomes_line(self):
        """A circle through the inversion center maps to a line."""
        S = Cline.from_circle(center=0, radius=1)
        # Circle through origin: center=1, radius=1 passes through 0
        C = Cline.from_circle(center=1, radius=1)
        C_img = S.invert(C)
        assert C_img.is_line

    def test_line_through_center_stays_line(self):
        """A line through the inversion center maps to itself (as a set)."""
        S = Cline.from_circle(center=0, radius=1)
        L = Cline.from_line(-1, 1)  # real axis, through origin
        L_img = S.invert(L)
        assert L_img.is_line

    def test_line_not_through_center_becomes_circle(self):
        """A line not through the inversion center maps to a circle through it."""
        S = Cline.from_circle(center=0, radius=1)
        # Vertical line x=1
        L = Cline(c=0, alpha=1 + 0j, d=-2)
        C_img = S.invert(L)
        assert C_img.is_circle
        # Image circle passes through the inversion center (origin)
        assert C_img.contains(0)

    def test_points_on_image(self):
        """Points on C map to points on invert(C)."""
        S = Cline.from_circle(center=0, radius=2)
        C = Cline.from_circle(center=3, radius=1)
        C_img = S.invert(C)
        # Take points on C, invert them, check they lie on C_img
        for theta in [0, np.pi / 2, np.pi]:
            z = 3 + np.exp(1j * theta)
            z_inv = S.invert(z)
            assert C_img.contains(z_inv)

    def test_unit_circle_fixed(self):
        """Unit circle inverted in itself gives the unit circle."""
        S = Cline.from_circle(center=0, radius=1)
        S_img = S.invert(S)
        assert S_img.is_circle
        assert abs(S_img.center) < TOL
        assert abs(S_img.radius - 1) < TOL

    def test_symbolic_cline_inversion(self):
        S = Cline.from_circle(center=sympy.Integer(0), radius=sympy.Integer(1))
        C = Cline.from_circle(center=sympy.Integer(3), radius=sympy.Integer(1))
        C_img = S.invert(C)
        assert C_img._is_exact
        assert C_img.is_circle
        # Involution
        C_back = S.invert(C_img)
        assert sympy.simplify(C_back.center - C.center) == 0
        assert sympy.simplify(C_back.radius - C.radius) == 0


class TestIntersection:
    """Tests for Cline.intersection."""

    def test_two_concentric_circles_no_intersection(self):
        C1 = Cline.from_circle(center=0, radius=1)
        C2 = Cline.from_circle(center=0, radius=2)
        assert len(C1.intersection(C2)) == 0

    def test_tangent_circles_one_point(self):
        C1 = Cline.from_circle(center=0, radius=1)
        C2 = Cline.from_circle(center=2, radius=1)
        pts = C1.intersection(C2)
        assert len(pts) == 1
        assert abs(pts[0] - 1) < TOL

    def test_two_intersecting_circles(self):
        C1 = Cline.from_circle(center=0, radius=2)
        C2 = Cline.from_circle(center=2, radius=2)
        pts = C1.intersection(C2)
        assert len(pts) == 2
        for p in pts:
            assert C1.contains(p)
            assert C2.contains(p)

    def test_circle_tangent_line(self):
        C = Cline.from_circle(center=0, radius=1)
        # Vertical line x=1, tangent to unit circle
        L = Cline(c=0, alpha=1 + 0j, d=-2)  # 2*Re(z) - 2 = 0 → x = 1
        pts = C.intersection(L)
        assert len(pts) == 1
        assert abs(pts[0] - 1) < TOL

    def test_two_lines_intersect(self):
        L1 = Cline.from_line(0, 1)       # real axis
        L2 = Cline.from_line(0, 1j)      # imaginary axis
        pts = L1.intersection(L2)
        assert len(pts) == 1
        assert abs(pts[0]) < TOL  # intersect at origin

    def test_parallel_lines_no_intersection(self):
        L1 = Cline(c=0, alpha=1j, d=0)    # y = 0 (real axis)
        L2 = Cline(c=0, alpha=1j, d=-2)   # y = 1
        assert len(L1.intersection(L2)) == 0

    def test_symbolic_intersection(self):
        C1 = Cline.from_circle(center=sympy.Integer(0), radius=sympy.Integer(2))
        C2 = Cline.from_circle(center=sympy.Integer(2), radius=sympy.Integer(2))
        pts = C1.intersection(C2)
        assert len(pts) == 2
        for p in pts:
            assert C1.contains(p)
            assert C2.contains(p)


class TestAngleAndOrthogonality:
    """Tests for angle and is_orthogonal."""

    def test_orthogonal_circle_and_real_axis(self):
        S = Cline.from_circle(center=0, radius=1)
        L = Cline.from_line(-1, 1)  # real axis
        assert S.is_orthogonal(L)

    def test_orthogonal_circles(self):
        # Circle centered at 2, radius sqrt(3) is orthogonal to unit circle
        # because |2|^2 = 1 + 3 = 4
        S = Cline.from_circle(center=0, radius=1)
        C = Cline.from_circle(center=2, radius=3 ** 0.5)
        assert S.is_orthogonal(C)

    def test_perpendicular_lines(self):
        L1 = Cline.from_line(0, 1)      # real axis
        L2 = Cline.from_line(0, 1j)     # imaginary axis
        assert abs(L1.angle(L2) - np.pi / 2) < TOL

    def test_non_orthogonal(self):
        C1 = Cline.from_circle(center=0, radius=1)
        C2 = Cline.from_circle(center=1, radius=1)
        assert not C1.is_orthogonal(C2)

    def test_symbolic_orthogonality(self):
        S = Cline.from_circle(center=sympy.Integer(0), radius=sympy.Integer(1))
        C = Cline.from_circle(center=sympy.Integer(2), radius=sympy.sqrt(3))
        assert S.is_orthogonal(C)

    def test_angle_between_circles(self):
        # Two unit circles centered at 0 and 1
        C1 = Cline.from_circle(center=0, radius=1)
        C2 = Cline.from_circle(center=1, radius=1)
        theta = C1.angle(C2)
        # cos(theta) = (1 - 1 - 1) / (2*1*1) = -1/2, so theta = 2pi/3
        assert abs(theta - 2 * np.pi / 3) < TOL
