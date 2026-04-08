r"""
Cline class for representing circles and lines in the complex plane.

A cline is a circle or line that can be represented by the equation:

.. math::

   cz\bar{z} + \alpha z + \bar{\alpha}\bar{z} + d = 0

where:
- c and d are real numbers
- alpha is a complex number

Based on the parameters, we have: 
- It's a circle if :math:`|\alpha|^2 > c \cdot d` and :math:`c \neq 0`
- It's a line if :math:`c = 0`
- It's a point if :math:`|\alpha|^2 = c \cdot d` and :math:`c \neq 0`
- Is not a valid geometric object (no solutions) if $|\alpha|^2 < c \cdot d$ and $c \neq 0$
"""

import matplotlib.pyplot as plt
import numpy as np

try:
    import sympy
    _HAS_SYMPY = True
except ImportError:
    _HAS_SYMPY = False


def _is_sympy(x):
    """Check if x is a sympy expression."""
    return _HAS_SYMPY and isinstance(x, sympy.Basic)


def _conjugate(x):
    """Conjugate that works for both numeric and sympy types."""
    if _is_sympy(x):
        return sympy.conjugate(x)
    return np.conj(x)


def _abs_sq(x):
    """Compute |x|^2 for both numeric and sympy types."""
    if _is_sympy(x):
        return (x * sympy.conjugate(x)).expand()
    return abs(x) ** 2


def _real(x):
    """Real part for both numeric and sympy types."""
    if _is_sympy(x):
        return sympy.re(x)
    return np.real(x)


def _sqrt(x):
    """Square root for both numeric and sympy types."""
    if _is_sympy(x):
        return sympy.sqrt(x)
    return np.sqrt(x)


def _is_infinity(z):
    """Check if z is the point at infinity (sympy.zoo)."""
    return _HAS_SYMPY and z is sympy.zoo


class Cline:
    r"""Class representing a circle or line in the complex plane using the general equation.

    The equation is:

    .. math::

       cz\bar{z} + \alpha z + \bar{\alpha}\bar{z} + d = 0

    where c and d are real numbers and alpha is complex.
    """

    def __init__(self, c=0.0, alpha=0.0 + 0.0j, d=0.0):
        r"""Initialize a cline with its equation parameters.

        Args:
            c (float): Real coefficient of :math:`z\bar{z}`
            alpha (complex): Complex coefficient of z
            d (float): Real constant term
            
        Mathematical Formulation:
            A cline is determined by the general equation:
            
            .. math::
            
               cz\bar{z} + \alpha z + \bar{\alpha}\bar{z} + d = 0
               
            where:
            
            * :math:`c` and :math:`d` are real numbers
            * :math:`\alpha` is a complex number
            
            The discriminant of the cline is defined as:
            
            .. math::
            
               \Delta = |\alpha|^2 - c \cdot d
               
            Based on the parameters, the cline represents:
            
            * A circle if :math:`\Delta > 0` and :math:`c \neq 0`
            * A point if :math:`\Delta = 0` and :math:`c \neq 0`
            * A line if :math:`c = 0`
            * An invalid geometric object (no solutions) if :math:`\Delta < 0` and :math:`c \neq 0`
            
            For a circle (:math:`\Delta > 0` and :math:`c \neq 0`):
            
            * Center: :math:`z_0 = -\frac{\bar{\alpha}}{c}`
            * Radius: :math:`r = \frac{\sqrt{\Delta}}{|c|} = \frac{\sqrt{|\alpha|^2 - c \cdot d}}{|c|}`
            
            For a point (:math:`\Delta = 0` and :math:`c \neq 0`):
            
            * Point location: :math:`z_0 = -\frac{\alpha}{c}`
            
            For a line (:math:`c = 0`):
            
            * Normal vector: :math:`\alpha = a + bi`
            * Direction vector: :math:`v = b - ai` (perpendicular to normal)
            * Cartesian form: :math:`ax - by + \frac{d}{2} = 0`
            * Distance from origin: :math:`\frac{|d|}{2|\alpha|}`
            * Parametric form: :math:`z(t) = z_0 + t \cdot v` where :math:`z_0` is a point on the line
            
        Algorithm:
            1. Calculate the discriminant :math:`\Delta = |\alpha|^2 - c \cdot d`
            
            2. Determine the type of cline:
               * If :math:`|c| < \epsilon` (near zero): Line
               * If :math:`|c| \geq \epsilon` and :math:`\Delta > \epsilon`: Circle
               * If :math:`|c| \geq \epsilon` and :math:`|\Delta| < \epsilon`: Point
               * If :math:`|c| \geq \epsilon` and :math:`\Delta < -\epsilon`: Invalid object
               
            3. For a circle, calculate:
               * Center: :math:`z_0 = -\frac{\bar{\alpha}}{c}`
               * Radius: :math:`r = \frac{\sqrt{\Delta}}{|c|}`
               
            4. For a point, calculate:
               * Point location: same as circle center
               
            5. For a line, calculate:
               * Normal vector: :math:`\alpha`
               * Direction vector: :math:`v = \text{Im}(\alpha) - i \cdot \text{Re}(\alpha)`
               * Distance from origin: :math:`\frac{|d|}{2|\alpha|}`
               * A point on the line by setting either x=0 or y=0 in the Cartesian form
        """
        # Detect symbolic mode
        self._is_exact = any(_is_sympy(x) for x in (c, alpha, d))

        if self._is_exact:
            self.c = sympy.sympify(c)
            self.d = sympy.sympify(d)
            self.alpha = sympy.sympify(alpha)
        else:
            self.c = float(c)
            self.d = float(d)
            self.alpha = complex(alpha)

        # Initialize points attribute to None (will be set if created from points)
        self.points = None

        # Compute discriminant |alpha|^2 - c*d
        self.discriminant = _abs_sq(self.alpha) - self.c * self.d

        # Determine if it's a circle, point, or line
        if self._is_exact:
            c_is_zero = self.c == 0
            if c_is_zero:
                self.is_circle = False
                self.is_point = False
                self.is_line = True
            else:
                disc_simplified = sympy.simplify(self.discriminant)
                if disc_simplified.is_positive:
                    self.is_circle = True
                    self.is_point = False
                    self.is_line = False
                elif disc_simplified.is_zero:
                    self.is_circle = False
                    self.is_point = True
                    self.is_line = False
                elif disc_simplified.is_negative:
                    self.is_circle = False
                    self.is_point = False
                    self.is_line = False
                else:
                    # Cannot determine sign symbolically
                    self.is_circle = None
                    self.is_point = None
                    self.is_line = None
        else:
            if abs(self.c) > 1e-10:  # c ≠ 0
                if self.discriminant > 1e-10:
                    self.is_circle = True
                    self.is_point = False
                    self.is_line = False
                elif abs(self.discriminant) < 1e-10:
                    self.is_circle = False
                    self.is_point = True
                    self.is_line = False
                else:
                    self.is_circle = False
                    self.is_point = False
                    self.is_line = False
            else:
                self.is_circle = False
                self.is_point = False
                self.is_line = True

        # Compute center and radius for circles
        if self.is_circle:
            # Center: z_0 = -conj(alpha)/c
            self.center = -_conjugate(self.alpha) / self.c

            # Radius: r = sqrt(discriminant) / |c|
            if self._is_exact:
                self.radius = _sqrt(self.discriminant) / sympy.Abs(self.c)
            else:
                self.radius = np.sqrt(self.discriminant) / abs(self.c)

        # Compute point location when discriminant = 0
        if self.is_point:
            # Point location: z_0 = -conj(alpha)/c
            self.point = -_conjugate(self.alpha) / self.c

        # Compute line properties when c = 0
        if self.is_line:
            if self._is_exact:
                self.a = sympy.re(self.alpha)
                self.b = sympy.im(self.alpha)
                self.normal_vector = self.alpha
                self.direction_vector = self.b - sympy.I * self.a
            else:
                self.a = np.real(self.alpha)
                self.b = np.imag(self.alpha)
                self.normal_vector = self.alpha
                self.direction_vector = complex(self.b, -self.a)

                # Distance from origin: |d|/(2|alpha|)
                if abs(self.alpha) > 1e-10:
                    self.distance_from_origin = abs(self.d) / (2 * abs(self.alpha))
                else:
                    self.distance_from_origin = float("inf")

                # Find a point on the line for parametric form
                if abs(self.a) > abs(self.b):
                    x = -self.d / (2 * self.a)
                    y = 0
                else:
                    x = 0
                    y = self.d / (2 * self.b)
                self.point_on_line = complex(x, y)

    def _format_complex(self, z, precision=4):
        """Format a complex number with specified precision."""
        real = round(z.real, precision)
        imag = round(z.imag, precision)

        # Remove trailing zeros
        if real == int(real):
            real = int(real)
        if imag == int(imag):
            imag = int(imag)

        if imag == 0:
            return f"{real}"
        elif imag > 0:
            return f"{real}+{imag}j"
        else:
            return f"{real}{imag}j"

    def _format_float(self, x, precision=4):
        """Format a float with specified precision."""
        rounded = round(x, precision)

        # Remove trailing zeros
        if rounded == int(rounded):
            return str(int(rounded))
        else:
            return str(rounded)

    @classmethod
    def from_three_points(cls, z0, z1, z2):
        r"""Construct a cline from three points in the complex plane.

        Args:
            z0 (complex or tuple): First point, either complex number or tuple (real, imag)
            z1 (complex or tuple): Second point, either complex number or tuple (real, imag)
            z2 (complex or tuple): Third point, either complex number or tuple (real, imag)

        Returns:
            Cline: A cline passing through the three points

        Mathematical Derivation:
            Substituting three points into the general cline equation:

            .. math::

               c|z|^2 + \alpha z + \bar{\alpha}\bar{z} + d = 0

            For each point :math:`z_i`, we get:

            .. math::

               c|z_i|^2 + \alpha z_i + \bar{\alpha}\bar{z_i} + d = 0, \qquad i=0,1,2.

            With three points, we have three equations with four unknowns
            (:math:`c`, :math:`\alpha = \alpha_1+i*\alpha_2`, and :math:`d`).

            We know already that the case :math:`c=0` represents a line, so when the three points
            are collinear we can set c=0 and solve for the rest. Otherwise since the equation
            is overdetermined, we can set :math:`c=1` and solve for the circle case.

            To determine which value of :math:`c` to use, we check if the points are collinear:

            * When the points are collinear:

              * Set :math:`c=0` (representing a line)
              * Calculate :math:`\alpha = i(z_1 - z_0)` perpendicular to the line direction
              * Solve for :math:`d = -2\text{Re}(\alpha z_0)`

            * When the points are not collinear:

              * Set :math:`c=1` (representing a circle)
              * Solve a system of linear equations for the remaining parameters

            To check collinearity, we compute:

            .. math::

               \text{Im}\left(\frac{z_2 - z_0}{z_1 - z_0}\right) = 0

            When the points are not collinear, we set :math:`c=1` and solve a system of linear
            equations.
            We can subtract the equation for :math:`z_0` from the equations for
            :math:`z_1` and :math:`z_2`:

            .. math::

               c(|z_1|^2 - |z_0|^2) + \alpha(z_1 - z_0) + \bar{\alpha}(\bar{z_1}
               - \bar{z_0}) &= 0 \\
               c(|z_2|^2 - |z_0|^2) + \alpha(z_2 - z_0) + \bar{\alpha}(\bar{z_2}
               - \bar{z_0}) &= 0

            With :math:`c=1`, :math:`\Delta_1 = z_1 - z_0`, :math:`\Delta_2 = z_2 - z_0`,
            :math:`S_1 = |z_1|^2 - |z_0|^2`, and :math:`S_2 = |z_2|^2 - |z_0|^2`, we get:

            .. math::

               S_1 + \alpha\Delta_1 + \bar{\alpha}\bar{\Delta_1} &= 0 \\
               S_2 + \alpha\Delta_2 + \bar{\alpha}\bar{\Delta_2} &= 0

            This can be rewritten as:

            .. math::

               S_1 + 2\text{Re}(\alpha\Delta_1) &= 0 \\
               S_2 + 2\text{Re}(\alpha\Delta_2) &= 0

            Leading to:

            .. math::

               \text{Re}(\alpha\Delta_1) &= -\frac{S_1}{2} \\
               \text{Re}(\alpha\Delta_2) &= -\frac{S_2}{2}

            Expanding :math:`\alpha = a + bi` and :math:`\Delta_j = x_j + y_j i`, we get:

            .. math::

               a x_1 - b y_1 &= -\frac{S_1}{2} \\
               a x_2 - b y_2 &= -\frac{S_2}{2}

            This 2×2 system is solved for :math:`a` and :math:`b` to find :math:`\alpha`.
            Finally, we compute :math:`d` using the original equation and the value of :math:`z_0`.

        Algorithm:
            1. Check if the points are collinear by testing
               :math:`\text{Im}((z_2 - z_0)/(z_1 - z_0)) = 0`

            2. If collinear:

               * Set :math:`c = 0`
               * Calculate :math:`\alpha = i(z_1 - z_0)`
               * Calculate :math:`d = -2\text{Re}(\alpha z_0)`

            3. If not collinear:

               * Set :math:`c = 1`
               * Calculate :math:`\Delta_1 = z_1 - z_0, \Delta_2 = z_2 - z_0`
               * Calculate :math:`S_1 = |z_1|^2 - |z_0|^2, S_2 = |z_2|^2 - |z_0|^2`
               * Calculate :math:`\alpha` by solving the linear system:

                 .. math::

                    \begin{pmatrix}
                    \text{Re}(\Delta_1) & -\text{Im}(\Delta_1) \\
                    \text{Re}(\Delta_2) & -\text{Im}(\Delta_2)
                    \end{pmatrix}
                    \begin{pmatrix}
                    \text{Re}(\alpha) \\
                    \text{Im}(\alpha)
                    \end{pmatrix} =
                    \begin{pmatrix}
                    -S_1/2 \\
                    -S_2/2
                    \end{pmatrix}

                 The solution is:

                 .. math::

                    \begin{pmatrix}
                    \text{Re}(\alpha) \\
                    \text{Im}(\alpha)
                    \end{pmatrix} =
                    \begin{pmatrix}
                    \text{Re}(\Delta_1) & -\text{Im}(\Delta_1) \\
                    \text{Re}(\Delta_2) & -\text{Im}(\Delta_2)
                    \end{pmatrix}^{-1}
                    \begin{pmatrix}
                    -S_1/2 \\
                    -S_2/2
                    \end{pmatrix}

               * Calculate :math:`d = -(|z_0|^2 + 2\text{Re}(\alpha z_0))`
        """
        # Handle infinity: a cline through ∞ is a line through the other two
        inf_flags = [_is_infinity(z) for z in (z0, z1, z2)]
        if sum(inf_flags) >= 2:
            raise ValueError("At most one point can be at infinity")
        if inf_flags[0]:
            cline = cls.from_line(z1, z2)
            cline.points = [z0, z1, z2]
            return cline
        if inf_flags[1]:
            cline = cls.from_line(z0, z2)
            cline.points = [z0, z1, z2]
            return cline
        if inf_flags[2]:
            cline = cls.from_line(z0, z1)
            cline.points = [z0, z1, z2]
            return cline

        # Detect symbolic mode
        exact = any(_is_sympy(x) for x in (z0, z1, z2))

        if exact:
            z0 = sympy.sympify(z0)
            z1 = sympy.sympify(z1)
            z2 = sympy.sympify(z2)
            return cls._from_three_points_exact(z0, z1, z2)

        # Convert inputs to complex numbers
        # Handle tuples as (real, imag) coordinates
        if isinstance(z0, tuple):
            z0 = complex(z0[0], z0[1])
        else:
            z0 = complex(z0)

        if isinstance(z1, tuple):
            z1 = complex(z1[0], z1[1])
        else:
            z1 = complex(z1)

        if isinstance(z2, tuple):
            z2 = complex(z2[0], z2[1])
        else:
            z2 = complex(z2)

        # Check if the points are collinear
        if abs(z1 - z0) < 1e-10:  # z0 and z1 are the same point
            if abs(z2 - z0) < 1e-10:  # All three points are the same
                # Return a point (degenerate case)
                cline = cls(c=1.0, alpha=-z0, d=abs(z0) ** 2)
                cline.points = [z0, z1, z2]  # Store the points
                return cline
            else:
                # z0 = z1 ≠ z2, so we have a line through z0 and z2
                delta = z2 - z0
                alpha = 1j * np.conj(delta)  # Perpendicular to the direction
                d = -2 * np.real(alpha * z0)
                cline = cls(c=0.0, alpha=alpha, d=d)
                cline.points = [z0, z1, z2]  # Store the points
                return cline

        # Check collinearity using the imaginary part of the ratio
        ratio = (z2 - z0) / (z1 - z0)
        if abs(np.imag(ratio)) < 1e-10:  # Points are collinear
            # Set c = 0 (line)
            c = 0.0

            # Calculate α = i*conj(z₁ - z₀)
            alpha = 1j * np.conj(z1 - z0)

            # Calculate d = -2Re(αz₀)
            d = -2 * np.real(alpha * z0)
        else:
            # Points are not collinear, so we have a circle
            # Set c = 1
            c = 1.0

            # Calculate Δ₁ = z₁ - z₀, Δ₂ = z₂ - z₀
            delta1 = z1 - z0
            delta2 = z2 - z0

            # Calculate S₁ = |z₁|² - |z₀|², S₂ = |z₂|² - |z₀|²
            S1 = abs(z1) ** 2 - abs(z0) ** 2
            S2 = abs(z2) ** 2 - abs(z0) ** 2

            # Calculate α by solving the system of equations:
            # S₁ = -2Re(αΔ₁)
            # S₂ = -2Re(αΔ₂)

            # This can be rewritten as:
            # S₁ = -(αΔ₁ + ᾱΔ̄₁)
            # S₂ = -(αΔ₂ + ᾱΔ̄₂)

            # We can solve this by setting up a 2x2 system:
            # [Re(Δ₁) -Im(Δ₁)] [Re(α)] = [-S₁/2]
            # [Re(Δ₂) -Im(Δ₂)] [Im(α)]   [-S₂/2]

            A = np.array([[np.real(delta1), -np.imag(delta1)], [np.real(delta2), -np.imag(delta2)]])

            b = np.array([-S1 / 2, -S2 / 2])

            try:
                x = np.linalg.solve(A, b)
                alpha = complex(x[0], x[1])
            except np.linalg.LinAlgError:
                # If the system is singular, the points might be collinear
                # or have some other special configuration
                # Fall back to a simpler approach
                alpha = -np.conjugate(z0)

            # Calculate d = -(|z₀|² + 2Re(αz₀))
            d = -(abs(z0) ** 2 + 2 * np.real(alpha * z0))

        # Create the cline and store the points
        cline = cls(c=c, alpha=alpha, d=d)
        cline.points = [z0, z1, z2]
        return cline

    @classmethod
    def _from_three_points_exact(cls, z0, z1, z2):
        """Symbolic path for from_three_points using sympy.

        Solves the cline equation c|z|² + αz + ᾱz̄ + d = 0 for three points
        by setting up and solving the linear system symbolically.
        """
        # Check collinearity via the determinant method
        # Three points are collinear iff Im((z2-z0)/(z1-z0)) = 0
        delta10 = z1 - z0
        if sympy.simplify(delta10) == 0:
            # z0 == z1, use z0 and z2
            return cls.from_line(z0, z2)

        delta20 = z2 - z0
        ratio = delta20 / delta10
        if sympy.simplify(sympy.im(ratio)) == 0:
            # Collinear → line
            return cls.from_line(z0, z1)

        # Not collinear → circle. Set c = 1.
        # Solve: |z_i|² + α·z_i + ᾱ·z̄_i + d = 0 for i = 0,1,2
        # Subtract eq(z0) from eq(z1) and eq(z2):
        #   (|z1|²-|z0|²) + α(z1-z0) + ᾱ(z̄1-z̄0) = 0
        #   (|z2|²-|z0|²) + α(z2-z0) + ᾱ(z̄2-z̄0) = 0
        # Let α = a + bi, expand Re parts to get 2x2 real system
        S1 = sympy.expand(z1 * sympy.conjugate(z1) - z0 * sympy.conjugate(z0))
        S2 = sympy.expand(z2 * sympy.conjugate(z2) - z0 * sympy.conjugate(z0))

        dx1 = sympy.re(delta10)
        dy1 = sympy.im(delta10)
        dx2 = sympy.re(delta20)
        dy2 = sympy.im(delta20)

        # System: [dx1, -dy1; dx2, -dy2] [a; b] = [-S1/2; -S2/2]
        det = dx1 * (-dy2) - dx2 * (-dy1)
        det = sympy.simplify(det)

        a_val = ((-S1 / 2) * (-dy2) - (-S2 / 2) * (-dy1)) / det
        b_val = (dx1 * (-S2 / 2) - dx2 * (-S1 / 2)) / det

        alpha = sympy.simplify(a_val + sympy.I * b_val)
        c = sympy.Integer(1)
        d = sympy.simplify(
            -(z0 * sympy.conjugate(z0) + alpha * z0
              + sympy.conjugate(alpha) * sympy.conjugate(z0))
        )

        cline = cls(c=c, alpha=alpha, d=d)
        cline.points = [z0, z1, z2]
        return cline

    @classmethod
    def from_line(cls, z0, z1):
        r"""Construct a cline representing a line through two points.

        Args:
            z0 (complex or tuple): First point, either complex number or tuple (real, imag)
            z1 (complex or tuple): Second point, either complex number or tuple (real, imag)

        Returns:
            Cline: A cline representing the line through z0 and z1

        For a line, we set :math:`c = 0`, and the parameters are calculated as:
            - :math:`\alpha = i \cdot \overline{(z_1 - z_0)}` (perpendicular to the line direction)
            - :math:`d = -2 \cdot \text{Re}(\alpha \cdot z_0)`
        """
        # Detect symbolic mode
        exact = any(_is_sympy(x) for x in (z0, z1))

        if exact:
            z0 = sympy.sympify(z0)
            z1 = sympy.sympify(z1)
            c = sympy.Integer(0)
            delta = z1 - z0
            alpha = sympy.I * sympy.conjugate(delta)
            d = -2 * sympy.re(alpha * z0)
        else:
            if isinstance(z0, tuple):
                z0 = complex(z0[0], z0[1])
            else:
                z0 = complex(z0)
            if isinstance(z1, tuple):
                z1 = complex(z1[0], z1[1])
            else:
                z1 = complex(z1)
            if abs(z1 - z0) < 1e-10:
                raise ValueError("Points must be distinct to define a line")
            c = 0.0
            alpha = 1j * np.conj(z1 - z0)
            d = -2 * np.real(alpha * z0)

        cline = cls(c=c, alpha=alpha, d=d)
        cline.points = [z0, z1]
        return cline

    @classmethod
    def from_circle(cls, center, radius):
        r"""Construct a cline representing a circle with specified center and radius.

        Args:
            center (complex or tuple): Center of the circle,
            either complex number or tuple (real, imag)
            radius (float): Radius of the circle (must be positive)

        Returns:
            Cline: A cline representing the circle with given center and radius

        For a circle, we set :math:`c = 1`, and the parameters are calculated as:
            - :math:`\alpha = -\overline{\text{center}}`
            - :math:`d = |\text{center}|^2 - \text{radius}^2`
        """
        # Detect symbolic mode
        exact = _is_sympy(center) or _is_sympy(radius)

        if exact:
            center = sympy.sympify(center)
            radius = sympy.sympify(radius)
            c = sympy.Integer(1)
            alpha = -sympy.conjugate(center)
            d = (center * sympy.conjugate(center) - radius**2).expand()
        else:
            if isinstance(center, tuple):
                center = complex(center[0], center[1])
            else:
                center = complex(center)
            radius = float(radius)
            if radius <= 0:
                raise ValueError("Radius must be positive")
            c = 1.0
            alpha = -np.conj(center)
            d = abs(center) ** 2 - radius**2

        # Create the cline
        cline = cls(c=c, alpha=alpha, d=d)
        return cline

    @property
    def hermitian_matrix(self):
        r"""Return the 2x2 Hermitian matrix representing this cline.

        Derivation:
            The cline equation :math:`c|z|^2 + \alpha z + \bar\alpha\bar z + d = 0`
            can be written as a Hermitian form. Define the column vector
            :math:`\mathbf{z} = \binom{z}{1}`, then:

            .. math::

                \mathbf{z}^\dagger H \mathbf{z}
                = (\bar z, 1) \begin{pmatrix} c & \bar\alpha \\ \alpha & d \end{pmatrix}
                  \binom{z}{1}
                = c|z|^2 + \bar\alpha \cdot 1 \cdot z + \alpha \cdot \bar z \cdot 1 + d

            which is zero precisely when z lies on the cline. The matrix

            .. math::

                H = \begin{pmatrix} c & \bar{\alpha} \\ \alpha & d \end{pmatrix}

            satisfies :math:`H^\dagger = H` since c, d are real and the off-diagonal
            entries are conjugates. Note :math:`\det(H) = cd - |\alpha|^2 = -\Delta`
            where :math:`\Delta` is the discriminant.

        Returns:
            sympy.Matrix (exact mode) or numpy.ndarray (numeric mode).

        Reference:
            Hitchman, *Geometry with an Introduction to Cosmic Topology*,
            Definition 3.2.3. https://mphitchman.com/geometry/section3-2.html
        """
        alpha_conj = _conjugate(self.alpha)
        if self._is_exact:
            return sympy.Matrix([[self.c, alpha_conj], [self.alpha, self.d]])
        return np.array([[self.c, alpha_conj], [self.alpha, self.d]])

    @classmethod
    def from_hermitian_matrix(cls, H):
        r"""Construct a Cline from a 2x2 Hermitian matrix.

        Args:
            H: 2x2 array-like with :math:`H = H^\dagger`, i.e.,
               H[0,0] and H[1,1] real, H[1,0] = conj(H[0,1]).

        Returns:
            Cline: the cline represented by H.

        Raises:
            ValueError: if H is not Hermitian.

        Reference:
            Hitchman, GCT, Definition 3.2.3
        """
        if _HAS_SYMPY and isinstance(H, sympy.Matrix):
            c = H[0, 0]
            alpha = H[1, 0]
            d = H[1, 1]
            if sympy.simplify(H[0, 1] - sympy.conjugate(alpha)) != 0:
                raise ValueError("Matrix is not Hermitian: H[0,1] != conj(H[1,0])")
        else:
            H = np.asarray(H)
            c = H[0, 0].real
            alpha = H[1, 0]
            d = H[1, 1].real
            if abs(H[0, 1] - np.conj(alpha)) > 1e-10:
                raise ValueError("Matrix is not Hermitian: H[0,1] != conj(H[1,0])")
        return cls(c=c, alpha=alpha, d=d)

    def contains(self, z):
        r"""Test if a point z lies on this cline.

        Derivation:
            A point z lies on the cline iff it satisfies the equation

            .. math::

                c|z|^2 + \alpha z + \bar\alpha\bar z + d = 0

            Equivalently, in homogeneous coordinates :math:`\mathbf{z} = (z,1)^T`,
            the condition is :math:`\mathbf{z}^\dagger H \mathbf{z} = 0`.

            For the point at infinity :math:`z = \infty`, use the homogeneous
            representative :math:`\mathbf{z} = (1, 0)^T`. Then
            :math:`\mathbf{z}^\dagger H \mathbf{z} = c`. So :math:`\infty` lies
            on the cline iff :math:`c = 0`, i.e., the cline is a line.

        Args:
            z: complex number, sympy expression, or sympy.zoo (∞).

        Returns:
            bool (numeric mode), or bool (symbolic mode, after simplification).

        Reference:
            Hitchman, *GCT*, Definition 3.2.3.
            https://mphitchman.com/geometry/section3-2.html
        """
        if _is_infinity(z):
            # Lines (c=0) pass through ∞; circles (c≠0) do not
            return self.is_line

        if self._is_exact:
            z = sympy.sympify(z)
            val = self.c * z * sympy.conjugate(z) + self.alpha * z + \
                sympy.conjugate(self.alpha) * sympy.conjugate(z) + self.d
            return sympy.simplify(val) == 0

        z = complex(z)
        val = self.c * abs(z) ** 2 + self.alpha * z + \
            np.conj(self.alpha) * np.conj(z) + self.d
        return abs(val) < 1e-10

    def invert(self, z):
        r"""Return the image of z under inversion in this cline.

        This method is polymorphic:

        - If z is a **point** (complex, sympy expression, or sympy.zoo),
          returns the image point under inversion/reflection.
        - If z is a **Cline**, returns the image cline. Inversion maps
          clines to clines (Hitchman, *GCT*, Theorem 3.2.12).

        Derivation (point, circle inversion):
            Given a circle with center :math:`z_0` and radius r, the inverse
            of a point z is defined by the relation

            .. math::

                |z - z_0| \cdot |z^* - z_0| = r^2

            with :math:`z^*` on the same ray from :math:`z_0` as z. Writing this
            in complex form:

            .. math::

                z^* - z_0 = \frac{r^2}{\overline{z - z_0}}

            which gives the formula :math:`z^* = z_0 + r^2 / \overline{(z - z_0)}`.

            This is an involution: :math:`(z^*)^* = z`, which follows because
            applying the formula twice yields
            :math:`z_0 + r^2 / \overline{(z^* - z_0)} = z_0 + r^2 / (r^2/(z - z_0)) = z`.

            Special cases: :math:`z_0 \mapsto \infty` (denominator zero) and
            :math:`\infty \mapsto z_0` (by continuity on the Riemann sphere).

        Derivation (point, line reflection):
            For a line :math:`\alpha z + \bar\alpha\bar z + d = 0`, the
            reflection of z across the line is

            .. math::

                z^* = -\frac{\bar\alpha\bar z + d}{\alpha}

            Proof: a reflection maps z to :math:`z^*` such that the midpoint
            :math:`(z + z^*)/2` lies on the line and :math:`z^* - z` is
            perpendicular to the line direction. Substituting the formula into
            the midpoint condition recovers the line equation for z, confirming
            the midpoint lies on the line. This is also an involution.

        Derivation (cline inversion):
            Inversion maps clines to clines (Hitchman, *GCT*, Theorem 3.2.12).
            If this cline (the inversion cline) has Hermitian matrix J, and the
            argument cline has Hermitian matrix H, then the image cline has
            Hermitian matrix

            .. math::

                H' = J \cdot H \cdot J

            Proof: a point z lies on H iff :math:`\mathbf{z}^\dagger H \mathbf{z} = 0`.
            Inversion in J acts on homogeneous coordinates as
            :math:`\mathbf{z} \mapsto J \mathbf{z}` (up to scale). So :math:`z^*`
            lies on :math:`H'` iff :math:`(J\mathbf{z})^\dagger H' (J\mathbf{z}) = 0`,
            which equals :math:`\mathbf{z}^\dagger J H' J \mathbf{z}`. For this to
            equal :math:`\mathbf{z}^\dagger H \mathbf{z}` we need :math:`J H' J = H`,
            i.e., :math:`H' = J^{-1} H J^{-1}`. Since J is Hermitian and
            :math:`J^{-1} \propto \text{adj}(J) \propto J` (for an involution),
            this simplifies to :math:`H' = J H J` (up to a real scalar).

        Args:
            z: complex number, sympy expression, sympy.zoo (∞), or Cline.

        Returns:
            complex/sympy/sympy.zoo if z is a point, or Cline if z is a Cline.

        Reference:
            Hitchman, *GCT*, Definition 3.2.6 (point inversion in a circle).
            Hitchman, *GCT*, Section 3.1 (reflection in a line).
            Hitchman, *GCT*, Theorem 3.2.12 (inversion maps clines to clines).
            https://mphitchman.com/geometry/section3-2.html
        """
        # Dispatch: if z is a Cline, invert the cline
        if isinstance(z, Cline):
            return self._invert_cline(z)

        # Otherwise, invert a point
        return self._invert_point(z)

    def _invert_point(self, z):
        """Invert a point z in this cline."""
        if self.is_circle:
            if _is_infinity(z):
                return self.center

            if self._is_exact:
                z = sympy.sympify(z)
                diff = z - self.center
                if sympy.simplify(diff) == 0:
                    return sympy.zoo
                return sympy.simplify(
                    self.center + self.radius ** 2 / sympy.conjugate(diff)
                )

            z = complex(z)
            diff = z - self.center
            if abs(diff) < 1e-15:
                return sympy.zoo
            return self.center + self.radius ** 2 / np.conj(diff)

        elif self.is_line:
            if _is_infinity(z):
                return sympy.zoo

            if self._is_exact:
                z = sympy.sympify(z)
                return sympy.simplify(
                    -(sympy.conjugate(self.alpha) * sympy.conjugate(z) + self.d)
                    / self.alpha
                )

            z = complex(z)
            return -(np.conj(self.alpha) * np.conj(z) + self.d) / self.alpha

        else:
            raise ValueError("Cannot invert in a degenerate cline (point or invalid)")

    def _invert_cline(self, other):
        r"""Invert a cline in this cline.

        Pick three points on the source cline, invert each through this cline,
        and construct the image cline from the three image points. This approach
        is always correct and avoids normalization issues with the matrix formula.
        """
        if other.is_circle:
            # Pick three points on the circle
            if other._is_exact:
                # Use center ± radius and center + i*radius
                pts = [
                    other.center + other.radius,
                    other.center - other.radius,
                    other.center + sympy.I * other.radius,
                ]
            else:
                pts = [other.center + other.radius * np.exp(1j * t)
                       for t in [0, 2 * np.pi / 3, 4 * np.pi / 3]]
        elif other.is_line:
            if other._is_exact:
                # Pick two finite points on the line and ∞
                # Solve for a point: α·z + ᾱ·z̄ + d = 0
                # Use z = -d/(2α) · (ᾱ/|α|) ... simpler: use stored points or construct
                a, b = sympy.re(other.alpha), sympy.im(other.alpha)
                if a != 0:
                    z0 = -other.d / (2 * a) + sympy.Integer(0) * sympy.I
                    z1 = z0 + other.direction_vector
                else:
                    z0 = sympy.I * other.d / (2 * b)
                    z1 = z0 + other.direction_vector
                pts = [z0, z1, sympy.zoo]
            else:
                z0 = other.point_on_line
                z1 = other.point_on_line + other.direction_vector
                pts = [z0, z1, sympy.zoo]
        else:
            raise ValueError("Cannot invert a degenerate cline")

        # Invert the three points
        img_pts = [self._invert_point(p) for p in pts]

        return Cline.from_three_points(*img_pts)

    def intersection(self, other):
        r"""Return the intersection points of two clines.

        Returns:
            list of 0, 1, or 2 complex numbers (or sympy expressions).

        Reference:
            Standard analytic geometry; used implicitly in
            Hitchman GCT Chapters 5-6.
        """
        if not isinstance(other, Cline):
            raise TypeError("Can only intersect with another Cline")

        if self.is_line and other.is_line:
            return self._intersect_line_line(other)
        elif self.is_circle and other.is_circle:
            return self._intersect_circle_circle(other)
        elif self.is_circle and other.is_line:
            return self._intersect_circle_line(other)
        elif self.is_line and other.is_circle:
            return other._intersect_circle_line(self)
        else:
            raise ValueError("Cannot intersect degenerate clines")

    def _intersect_line_line(self, other):
        """Intersect two lines. Returns 0 or 1 points."""
        # Line equations: 2*Re(α·z) + d = 0
        # In Cartesian: a₁x - b₁y + d₁/2 = 0 and a₂x - b₂y + d₂/2 = 0
        if self._is_exact or other._is_exact:
            a1, b1, d1 = sympy.re(self.alpha), sympy.im(self.alpha), self.d
            a2, b2, d2 = sympy.re(other.alpha), sympy.im(other.alpha), other.d
            det = a1 * (-b2) - a2 * (-b1)
            if sympy.simplify(det) == 0:
                return []  # parallel
            x = ((-d1 / 2) * (-b2) - (-d2 / 2) * (-b1)) / det
            y = (a1 * (-d2 / 2) - a2 * (-d1 / 2)) / det
            return [sympy.simplify(x + sympy.I * y)]

        a1, b1, d1 = self.a, self.b, self.d
        a2, b2, d2 = other.a, other.b, other.d
        # System: a₁x - b₁y = -d₁/2, a₂x - b₂y = -d₂/2
        A = np.array([[a1, -b1], [a2, -b2]])
        rhs = np.array([-d1 / 2, -d2 / 2])
        det = np.linalg.det(A)
        if abs(det) < 1e-10:
            return []  # parallel
        sol = np.linalg.solve(A, rhs)
        return [complex(sol[0], sol[1])]

    def _intersect_circle_circle(self, other):
        """Intersect two circles. Returns 0, 1, or 2 points."""
        # Subtract the two cline equations to get the radical axis
        c_diff = self.c - other.c
        alpha_diff = self.alpha - other.alpha
        d_diff = self.d - other.d

        # Check if the radical axis is degenerate
        # When c_diff=0 and alpha_diff=0, the radical equation is just d_diff=0
        # If d_diff≠0: no intersection (concentric, different radii)
        # If d_diff=0: identical circles (infinite intersections, return [])
        if self._is_exact or other._is_exact:
            if sympy.simplify(c_diff) == 0 and sympy.simplify(alpha_diff) == 0:
                return []
        else:
            if abs(c_diff) < 1e-10 and abs(alpha_diff) < 1e-10:
                return []

        radical = Cline(c=c_diff, alpha=alpha_diff, d=d_diff)
        return self._intersect_circle_line(radical)

    def _intersect_circle_line(self, line):
        """Intersect a circle (self) with a line. Returns 0, 1, or 2 points."""
        if self._is_exact or line._is_exact:
            return self._intersect_circle_line_exact(line)

        # Numeric: parametrize the line and substitute into circle equation
        # Line: a·x - b·y + d/2 = 0, direction = (b, -a) (note: not our direction_vector)
        # Actually, use the cline equation directly.
        # Line passes through point p in direction v.
        # Parametrize z = p + t*v, substitute into circle equation.
        a_l, b_l, d_l = line.a, line.b, line.d

        # Solve for parametric intersection with circle
        # Circle: c|z|² + αz + ᾱz̄ + d_c = 0
        # Line in Cartesian: a_l·x - b_l·y + d_l/2 = 0
        # From line: if |b_l| > |a_l|, y = (a_l·x + d_l/2) / b_l
        #            else x = (b_l·y - d_l/2) / a_l

        # Use the approach: solve the line for one variable, substitute
        # Line: 2*Re(α_l * z) + d_l = 0 → 2(a_l·x - b_l·y) + d_l = 0

        if abs(b_l) > abs(a_l):
            # y = (a_l·x + d_l/2) / b_l
            # Sub into |z|² = x² + y² and circle eq
            # Circle: c(x²+y²) + 2(a_c·x - b_c·y) + d_c = 0
            a_c = np.real(self.alpha)
            b_c = np.imag(self.alpha)
            # y = (a_l*x + d_l/2) / b_l = m*x + n
            m = a_l / b_l
            n = d_l / (2 * b_l)
            # x² + y² = x² + (mx+n)² = (1+m²)x² + 2mnx + n²
            A_coef = self.c * (1 + m ** 2)
            B_coef = self.c * 2 * m * n + 2 * (a_c - b_c * m)
            C_coef = self.c * n ** 2 - 2 * b_c * n + self.d
        else:
            # x = (b_l*y - d_l/2) / a_l = m*y + n
            a_c = np.real(self.alpha)
            b_c = np.imag(self.alpha)
            m = b_l / a_l
            n = -d_l / (2 * a_l)
            # x² + y² = (my+n)² + y² = (1+m²)y² + 2mny + n²
            A_coef = self.c * (1 + m ** 2)
            B_coef = self.c * 2 * m * n + 2 * (a_c * m - b_c)
            C_coef = self.c * n ** 2 + 2 * a_c * n + self.d

        disc = B_coef ** 2 - 4 * A_coef * C_coef
        if disc < -1e-10:
            return []
        if abs(disc) < 1e-10:
            disc = 0

        results = []
        for sign in [1, -1]:
            t = (-B_coef + sign * np.sqrt(disc)) / (2 * A_coef)
            if abs(b_l) > abs(a_l):
                x, y = t, m * t + n
            else:
                y, x = t, m * t + n
            results.append(complex(x, y))

        if abs(disc) < 1e-10:
            return results[:1]  # tangent — one point
        return results

    def _intersect_circle_line_exact(self, line):
        """Symbolic circle-line intersection using sympy.solve."""
        x, y = sympy.symbols('x y', real=True)
        z_expr = x + sympy.I * y
        z_conj = x - sympy.I * y

        # Circle equation
        eq1 = self.c * (x**2 + y**2) + self.alpha * z_expr + \
            sympy.conjugate(self.alpha) * z_conj + self.d

        # Line equation
        eq2 = line.c * (x**2 + y**2) + line.alpha * z_expr + \
            sympy.conjugate(line.alpha) * z_conj + line.d

        eq1 = sympy.expand(sympy.re(eq1))
        eq2 = sympy.expand(sympy.re(eq2))

        solutions = sympy.solve([eq1, eq2], [x, y])
        if isinstance(solutions, dict):
            solutions = [solutions]
        return [sympy.simplify(sol[0] + sympy.I * sol[1])
                if isinstance(sol, (list, tuple))
                else sympy.simplify(sol[x] + sympy.I * sol[y])
                for sol in solutions]

    def angle(self, other):
        r"""Return the angle between two clines at their intersection.

        For two circles with centers z1, z2 and radii r1, r2:
            :math:`\cos\theta = \frac{|z_1 - z_2|^2 - r_1^2 - r_2^2}{2 r_1 r_2}`

        For circle and line, or two lines: computed from direction vectors
        at the intersection point.

        Returns:
            float (radians) or sympy expression.

        Raises:
            ValueError: if the clines do not intersect.

        Reference:
            Hitchman, GCT, Section 3.2
        """
        if self.is_circle and other.is_circle:
            if self._is_exact or other._is_exact:
                d_sq = _abs_sq(self.center - other.center)
                cos_theta = (d_sq - self.radius**2 - other.radius**2) / \
                    (2 * self.radius * other.radius)
                return sympy.acos(sympy.simplify(cos_theta))

            d = abs(self.center - other.center)
            cos_theta = (d**2 - self.radius**2 - other.radius**2) / \
                (2 * self.radius * other.radius)
            # Clamp for numerical stability
            cos_theta = max(-1, min(1, cos_theta))
            return np.arccos(cos_theta)

        elif self.is_line and other.is_line:
            # Angle between two lines from their normal vectors
            if self._is_exact or other._is_exact:
                dot = sympy.re(self.alpha * sympy.conjugate(other.alpha))
                return sympy.acos(sympy.simplify(
                    dot / (sympy.Abs(self.alpha) * sympy.Abs(other.alpha))
                ))

            dot = np.real(self.alpha * np.conj(other.alpha))
            cos_theta = dot / (abs(self.alpha) * abs(other.alpha))
            cos_theta = max(-1, min(1, cos_theta))
            return np.arccos(abs(cos_theta))

        else:
            # Circle-line case: find intersection, compute angle there
            pts = self.intersection(other)
            if not pts:
                raise ValueError("Clines do not intersect")

            # At intersection point, angle = angle between tangent to circle
            # and the line direction. Use the formula via normals.
            if self.is_circle:
                circle, line = self, other
            else:
                circle, line = other, self

            # Tangent to circle at intersection point is perpendicular to radius
            p = pts[0]
            if circle._is_exact or line._is_exact:
                p = sympy.sympify(p)
                radius_dir = p - circle.center
                # Angle between radius direction and line normal
                dot = sympy.re(radius_dir * sympy.conjugate(line.alpha))
                cos_angle = dot / (sympy.Abs(radius_dir) * sympy.Abs(line.alpha))
                # Angle between tangent and line = pi/2 - angle between radius and line
                return sympy.simplify(sympy.Abs(sympy.asin(sympy.simplify(cos_angle))))

            radius_dir = p - circle.center
            dot = np.real(radius_dir * np.conj(line.alpha))
            cos_angle = dot / (abs(radius_dir) * abs(line.alpha))
            cos_angle = max(-1, min(1, cos_angle))
            return abs(np.arcsin(cos_angle))

    def is_orthogonal(self, other):
        r"""Return True if two clines meet at right angles.

        Derivation:
            Two clines with Hermitian matrices :math:`H_1, H_2` are orthogonal
            iff :math:`\text{tr}(H_1 \text{adj}(H_2)) = 0`. Expanding this trace
            with

            .. math::

                H_1 = \begin{pmatrix} c_1 & \bar\alpha_1 \\ \alpha_1 & d_1 \end{pmatrix},
                \quad
                H_2 = \begin{pmatrix} c_2 & \bar\alpha_2 \\ \alpha_2 & d_2 \end{pmatrix}

            and :math:`\text{adj}(H_2) = \begin{pmatrix} d_2 & -\bar\alpha_2 \\ -\alpha_2 & c_2 \end{pmatrix}`,
            we get:

            .. math::

                \text{tr}(H_1 \cdot \text{adj}(H_2))
                = c_1 d_2 - \bar\alpha_1 \alpha_2 - \alpha_1 \bar\alpha_2 + d_1 c_2
                = c_1 d_2 + c_2 d_1 - 2\text{Re}(\alpha_1 \bar\alpha_2)

            This criterion is equivalent to the angle formula giving
            :math:`\cos\theta = 0` for circles, and is computationally simpler
            as it does not require finding intersection points.

            For the Poincare disk model, geodesics are precisely the clines
            orthogonal to the unit circle (:math:`c=1, \alpha=0, d=-1`).

        Reference:
            Hitchman, *GCT*, Section 5.1 (orthogonality, Poincare disk geodesics).
            https://mphitchman.com/geometry/section5-1.html
        """
        val = self.c * other.d + other.c * self.d - \
            2 * _real(self.alpha * _conjugate(other.alpha))

        if self._is_exact or other._is_exact:
            return sympy.simplify(val) == 0
        return abs(val) < 1e-10

    def plot(
        self,
        ax=None,
        figsize=(8, 8),
        xlim=None,
        ylim=None,
        color="blue",
        point_color="red",
        label=None,
        show_points=True,
        num_points=100,
        precision=4,
        **kwargs,
    ):
        r"""Plot the cline in the complex plane.

        Args:
            ax (matplotlib.axes.Axes, optional): Axes to plot on. If None, a new figure is created.
            figsize (tuple, optional): Figure size if creating a new figure. Defaults to (8, 8).
            xlim (tuple, optional): x-axis limits. If None, automatically calculated.
            ylim (tuple, optional): y-axis limits. If None, automatically calculated.
            color (str, optional): Color of the cline. Defaults to 'blue'.
            point_color (str, optional): Color of the points. Defaults to 'red'.
            label (str, optional): Label for the cline in the legend. Defaults to None.
            show_points (bool, optional): Whether to show the points used to create the cline.
                Defaults to True.
            num_points (int, optional): Number of points to use when plotting a circle.
                Defaults to 100.
            precision (int, optional): Number of decimal places to round to. Defaults to 4.
            **kwargs: Additional keyword arguments passed to the plot function.

        Returns:
            matplotlib.axes.Axes: The axes containing the plot.
        """
        # Create a new figure if ax is not provided
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)

        # Set the aspect ratio to equal
        ax.set_aspect("equal")

        # Calculate appropriate limits if not provided
        auto_xlim = None
        auto_ylim = None

        # Auto-calculate limits based on cline type
        if self.is_circle:
            # For circles, use center and radius
            radius_margin = 1.5 * self.radius
            auto_xlim = (self.center.real - radius_margin, self.center.real + radius_margin)
            auto_ylim = (self.center.imag - radius_margin, self.center.imag + radius_margin)
        elif self.is_point:
            # For points, use a small window around the point
            auto_xlim = (self.point.real - 1, self.point.real + 1)
            auto_ylim = (self.point.imag - 1, self.point.imag + 1)
        elif self.is_line:
            if self.points is not None and len(self.points) >= 2:
                # For lines, use the points with a margin
                p1, p2 = self.points[0], self.points[1]
                x_diff = abs(p1.real - p2.real)
                y_diff = abs(p1.imag - p2.imag)
                x_margin = max(2 * x_diff, 2)
                y_margin = max(2 * y_diff, 2)

                # Handle different orderings of coordinates
                x_min = min(p1.real, p2.real) - x_margin
                x_max = max(p1.real, p2.real) + x_margin
                y_min = min(p1.imag, p2.imag) - y_margin
                y_max = max(p1.imag, p2.imag) + y_margin

                auto_xlim = (x_min, x_max)
                auto_ylim = (y_min, y_max)
            else:
                # Fallback for lines without stored points
                auto_xlim = (-5, 5)
                auto_ylim = (-5, 5)

        # Apply limits, prioritizing provided values over auto-calculated ones
        ax.set_xlim(xlim if xlim is not None else auto_xlim)
        ax.set_ylim(ylim if ylim is not None else auto_ylim)

        # Add grid
        ax.grid(True, linestyle="--", alpha=0.7)

        # Plot the cline based on its type
        if self.is_circle:
            # Plot a circle
            theta = np.linspace(0, 2 * np.pi, num_points)
            x = self.center.real + self.radius * np.cos(theta)
            y = self.center.imag + self.radius * np.sin(theta)
            ax.plot(x, y, color=color, label=label, **kwargs)

            # Mark the center
            ax.plot(self.center.real, self.center.imag, "o", color=color, markersize=5)
            center_str = self._format_complex(self.center, precision)
            ax.text(
                self.center.real,
                self.center.imag,
                f" center: {center_str}",
                color=color,
                fontsize=8,
                verticalalignment="bottom",
            )

        elif self.is_point:
            # Plot a point
            ax.plot(
                self.point.real,
                self.point.imag,
                "o",
                color=color,
                markersize=8,
                label=label,
                **kwargs,
            )
            point_str = self._format_complex(self.point, precision)
            ax.text(
                self.point.real,
                self.point.imag,
                f" point: {point_str}",
                color=color,
                fontsize=8,
                verticalalignment="bottom",
            )

        elif self.is_line:
            # Completely rewritten line plotting logic for maximum robustness
            if self.points is not None and len(self.points) >= 2:
                # Get the two points that define the line
                z0, z1 = self.points[0], self.points[1]

                # Get the current axis limits
                x_min, x_max = ax.get_xlim()
                y_min, y_max = ax.get_ylim()

                # Calculate the slope
                dx = z1.real - z0.real
                dy = z1.imag - z0.imag

                # Handle vertical lines (or nearly vertical lines)
                if abs(dx) < 1e-10:
                    # Use a vertical line at the x-coordinate
                    x_coords = [z0.real, z0.real]
                    y_coords = [y_min, y_max]
                else:
                    # For non-vertical lines, calculate y = m(x - x0) + y0
                    slope = dy / dx

                    # Calculate y-coordinates at the min and max x values
                    y_at_xmin = slope * (x_min - z0.real) + z0.imag
                    y_at_xmax = slope * (x_max - z0.real) + z0.imag

                    # Use the boundaries to create the line
                    x_coords = [x_min, x_max]
                    y_coords = [y_at_xmin, y_at_xmax]

                    # If the line runs outside the y-axis boundaries, calculate intersections
                    if (
                        y_at_xmin < y_min
                        or y_at_xmin > y_max
                        or y_at_xmax < y_min
                        or y_at_xmax > y_max
                    ):
                        points = []

                        # Calculate intersection with each boundary line
                        # Left boundary (x = x_min)
                        if y_min <= y_at_xmin <= y_max:
                            points.append((x_min, y_at_xmin))

                        # Right boundary (x = x_max)
                        if y_min <= y_at_xmax <= y_max:
                            points.append((x_max, y_at_xmax))

                        # Calculate x-coordinates at min and max y values
                        if abs(slope) > 1e-10:  # Avoid division by zero
                            # Calculate x at minimum y value
                            x_at_ymin = (y_min - z0.imag) / slope + z0.real
                            # Calculate x at maximum y value
                            x_at_ymax = (y_max - z0.imag) / slope + z0.real

                            # Bottom boundary (y = y_min)
                            if x_min <= x_at_ymin <= x_max:
                                points.append((x_at_ymin, y_min))

                            # Top boundary (y = y_max)
                            if x_min <= x_at_ymax <= x_max:
                                points.append((x_at_ymax, y_max))

                        # If we found at least 2 intersection points, use them
                        if len(points) >= 2:
                            # Sort the points by x-coordinate for consistency
                            points.sort()
                            x_coords = [p[0] for p in points[:2]]
                            y_coords = [p[1] for p in points[:2]]

                # Double-check if the line actually intersects the plot area
                if len(x_coords) >= 2:
                    # Plot the line
                    ax.plot(x_coords, y_coords, color=color, label=label, **kwargs)
            else:
                # Fallback approach if points are not available
                # Draw a line in the direction of the normal vector through the origin
                direction = self.direction_vector

                # Calculate a reasonable length for the line
                max_extent = max(
                    abs(ax.get_xlim()[0]),
                    abs(ax.get_xlim()[1]),
                    abs(ax.get_ylim()[0]),
                    abs(ax.get_ylim()[1]),
                )

                # Generate points along the line
                t_values = np.linspace(-2 * max_extent, 2 * max_extent, num_points)
                points = [self.point_on_line + t * direction for t in t_values]

                # Extract x and y coordinates
                x_coords = [p.real for p in points]
                y_coords = [p.imag for p in points]

                # Plot the line
                ax.plot(x_coords, y_coords, color=color, label=label, **kwargs)

        # Plot the points used to create the cline if available and requested
        if self.points is not None and show_points:
            for i, point in enumerate(self.points):
                ax.plot(point.real, point.imag, "o", color=point_color, markersize=8)
                point_str = self._format_complex(point, precision)
                ax.text(
                    point.real,
                    point.imag,
                    f" $z_{i}$: {point_str}",
                    color=point_color,
                    fontsize=10,
                    verticalalignment="bottom",
                )

        # Add title based on the cline type
        if label is None:
            if self.is_circle:
                center_str = self._format_complex(self.center, precision)
                radius_str = self._format_float(self.radius, precision)
                ax.set_title(f"Circle: center={center_str}, radius={radius_str}")
            elif self.is_point:
                point_str = self._format_complex(self.point, precision)
                ax.set_title(f"Point: {point_str}")
            elif self.is_line:
                normal_str = self._format_complex(self.normal_vector, precision)
                distance_str = self._format_float(self.distance_from_origin, precision)
                ax.set_title(f"Line: normal={normal_str}, distance={distance_str}")
            else:
                ax.set_title("Invalid Cline")
        else:
            ax.set_title(label)

        # Add legend if there's a label
        if label is not None:
            ax.legend()

        # Add axis labels
        ax.set_xlabel("Re(z)")
        ax.set_ylabel("Im(z)")

        return ax

    def __str__(self):
        """Return a string representation of the cline."""
        # Format the equation with rounded values
        c_str = self._format_float(self.c)
        alpha_str = self._format_complex(self.alpha)
        alpha_conj_str = self._format_complex(np.conjugate(self.alpha))
        d_str = self._format_float(self.d)

        equation = f"{c_str}·|z|² + {alpha_str}·z + {alpha_conj_str}·z̄ + {d_str} = 0"

        # Format the discriminant
        disc_str = self._format_float(self.discriminant)

        result = f"A cline with equation: {equation}\n"
        result += f"Discriminant: |alpha|^2-c*d = {disc_str}\n"
        result += "The cline describes: "

        if self.is_circle:
            center_str = self._format_complex(self.center)
            radius_str = self._format_float(self.radius)
            result += f"a circle with center {center_str} and radius {radius_str}"
        elif self.is_point:
            point_str = self._format_complex(self.point)
            result += f"a point at {point_str}"
        elif self.is_line:
            a_str = self._format_float(self.a)
            b_str = self._format_float(self.b)
            d_half_str = self._format_float(-self.d / 2)
            normal_str = self._format_complex(self.normal_vector)
            dir_str = self._format_complex(self.direction_vector)
            dist_str = self._format_float(self.distance_from_origin)
            point_str = self._format_complex(self.point_on_line)

            result += "a line with the following properties:\n"
            result += (
                f"  1. Cartesian Form: {a_str}x - {b_str}y = {d_half_str} "
                f"where alpha = {a_str} + {b_str}i\n"
            )
            result += f"  2. Normal Vector: {normal_str}\n"
            result += f"  3. Direction Vector: {dir_str} (perpendicular to normal)\n"
            result += f"  4. Distance from Origin: {dist_str}\n"
            result += f"  5. Parametric Form: z(t) = {point_str} + t·{dir_str}"
        else:
            result += "not a valid geometric object (discriminant < 0)"

        return result

    def __repr__(self):
        """Return a string representation for debugging."""
        return self.__str__()
