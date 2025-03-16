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

import matplotlib.pyplot as plt
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

        # Initialize points attribute to None (will be set if created from points)
        self.points = None

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
            z0 (complex): First point
            z1 (complex): Second point
            z2 (complex): Third point

        Returns:
            Cline: A cline passing through the three points

        Algorithm:
            1. Check if the points are collinear by testing Im((z₂ - z₀)/(z₁ - z₀)) = 0
            2. If collinear:
               - Set c = 0
               - Calculate α = i(z₁ - z₀)
               - Calculate d = -2Re(αz₀)
            3. If not collinear:
               - Set c = 1
               - Calculate Δ₁ = z₁ - z₀, Δ₂ = z₂ - z₀
               - Calculate S₁ = |z₁|² - |z₀|², S₂ = |z₂|² - |z₀|²
               - Calculate α using the formula derived from the system of equations
               - Calculate d = -(|z₀|² + 2Re(αz₀))
        """
        # Convert inputs to complex numbers
        z0 = complex(z0)
        z1 = complex(z1)
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
                alpha = 1j * delta  # Perpendicular to the direction
                d = -2 * np.real(alpha * z0)
                cline = cls(c=0.0, alpha=alpha, d=d)
                cline.points = [z0, z1, z2]  # Store the points
                return cline

        # Check collinearity using the imaginary part of the ratio
        ratio = (z2 - z0) / (z1 - z0)
        if abs(np.imag(ratio)) < 1e-10:  # Points are collinear
            # Set c = 0 (line)
            c = 0.0

            # Calculate α = i(z₁ - z₀)
            alpha = 1j * (z1 - z0)

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

    def plot(
        self,
        ax=None,
        figsize=(8, 8),
        xlim=(-5, 5),
        ylim=(-5, 5),
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
            xlim (tuple, optional): x-axis limits. Defaults to (-5, 5).
            ylim (tuple, optional): y-axis limits. Defaults to (-5, 5).
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

        # Set the aspect ratio to equal and the limits
        ax.set_aspect("equal")
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

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
            # Plot a line
            # For a line with normal n at distance d from origin,
            # parametrize as z(t) = d*n + t*i*n where t is a real parameter

            # Calculate how far to go in each direction to reach the plot boundary
            max_extent = max(abs(xlim[0]), abs(xlim[1]), abs(ylim[0]), abs(ylim[1]))
            t_values = np.linspace(-2 * max_extent, 2 * max_extent, num_points)

            # Generate points along the line
            points = np.array([self.point_on_line + t * self.direction_vector for t in t_values])

            # Filter points within the plot limits
            mask = (
                (points.real >= xlim[0])
                & (points.real <= xlim[1])
                & (points.imag >= ylim[0])
                & (points.imag <= ylim[1])
            )
            filtered_points = points[mask]

            if len(filtered_points) > 0:
                x = filtered_points.real
                y = filtered_points.imag
                ax.plot(x, y, color=color, label=label, **kwargs)

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
