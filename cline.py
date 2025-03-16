r"""
Cline class for representing circles and lines in the complex plane.

A cline is a circle or line that can be represented by the equation:
cz\bar(z) + alpha*z + \bar(alpha)*\bar(z) + d = 0

where:
- c and d are real numbers
- alpha is a complex number
- It's a circle if |alpha|^2 > c*d and c ≠ 0
- It's a line if c = 0
- It's a point if |alpha|^2 = c*d and c ≠ 0
"""

import numpy as np


class Cline:
    r"""Class representing a circle or line in the complex plane using the general equation.

    The equation is:
    cz\bar(z) + alpha*z + \bar(alpha)*\bar(z) + d = 0

    where c and d are real numbers and alpha is complex.
    """

    def __init__(self, c=0.0, alpha=0.0 + 0.0j, d=0.0):
        r"""Initialize a cline with its equation parameters.

        Args:
            c (float): Real coefficient of z\bar(z)
            alpha (complex): Complex coefficient of z
            d (float): Real constant term
        """
        # Ensure c and d are real
        self.c = float(c)
        self.d = float(d)

        # alpha is complex
        self.alpha = complex(alpha)

        # Compute discriminant |alpha|^2 - c*d
        self.discriminant = abs(self.alpha) ** 2 - self.c * self.d

        # Determine if it's a circle, point, or line
        if abs(self.c) > 1e-10:  # c ≠ 0
            if self.discriminant > 1e-10:  # Discriminant > 0
                self.is_circle = True
                self.is_point = False
                self.is_line = False
            elif abs(self.discriminant) < 1e-10:  # Discriminant ≈ 0
                self.is_circle = False
                self.is_point = True
                self.is_line = False
            else:  # Discriminant < 0
                self.is_circle = False
                self.is_point = False
                self.is_line = False
        else:  # c = 0
            self.is_circle = False
            self.is_point = False
            self.is_line = True

        # Compute center and radius for circles
        if self.is_circle:
            # Center: z_0 = (-Re(alpha)/c, Im(alpha)/c)
            real_part = -np.real(self.alpha) / self.c
            imag_part = np.imag(self.alpha) / self.c
            self.center = complex(real_part, imag_part)

            # Radius: r = sqrt((|alpha|^2-cd) / c^2)
            self.radius = np.sqrt(self.discriminant) / abs(self.c)

        # Compute point location when discriminant = 0
        if self.is_point:
            real_part = -np.real(self.alpha) / self.c
            imag_part = np.imag(self.alpha) / self.c
            self.point = complex(real_part, imag_part)

        # Compute line properties when c = 0
        if self.is_line:
            # Extract real and imaginary parts of alpha
            self.a = np.real(self.alpha)
            self.b = np.imag(self.alpha)

            # Normal vector: alpha
            self.normal_vector = self.alpha

            # Direction vector: v = b - ia (perpendicular to alpha)
            self.direction_vector = complex(self.b, -self.a)

            # Distance from origin: |d|/(2|alpha|)
            if abs(self.alpha) > 1e-10:
                self.distance_from_origin = abs(self.d) / (2 * abs(self.alpha))
            else:
                self.distance_from_origin = float("inf")

            # Find a point on the line for parametric form
            # For the equation ax - by + d/2 = 0
            if abs(self.a) > abs(self.b):
                # If |a| > |b|, set y = 0 and solve for x
                x = -self.d / (2 * self.a)
                y = 0
            else:
                # Otherwise, set x = 0 and solve for y
                x = 0
                y = self.d / (2 * self.b)

            self.point_on_line = complex(x, y)

    def __str__(self):
        """Return a string representation of the cline."""
        equation = f"{self.c}·|z|² + {self.alpha}·z + {np.conjugate(self.alpha)}·z̄ + {self.d} = 0"

        result = f"A cline with equation: {equation}\n"
        result += f"Discriminant: |alpha|^2-c*d = {self.discriminant}\n"
        result += "The cline describes: "

        if self.is_circle:
            result += f"a circle with center {self.center} and radius {self.radius}"
        elif self.is_point:
            result += f"a point at ({self.point.real}, {self.point.imag})"
        elif self.is_line:
            a, b = self.a, self.b
            result += "a line with the following properties:\n"
            result += f"  1. Cartesian Form: {a}x - {b}y = {-self.d/2} where alpha = {a} + {b}i\n"
            result += f"  2. Normal Vector: {self.normal_vector}\n"
            result += f"  3. Direction Vector: {self.direction_vector} (perpendicular to normal)\n"
            result += f"  4. Distance from Origin: {self.distance_from_origin}\n"
            result += (
                f"  5. Parametric Form: z(t) = {self.point_on_line} + t·{self.direction_vector}"
            )
        else:
            result += "not a valid geometric object (discriminant < 0)"

        return result

    def __repr__(self):
        """Return a string representation for debugging."""
        return self.__str__()
