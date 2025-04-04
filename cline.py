r"""
Cline class for representing circles and lines in the complex plane.

A cline is a circle or line that can be represented by the equation:
cz\bar{z} + alpha*z + \bar{alpha}*\bar{z} + d = 0

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
    cz\bar{z} + alpha*z + \bar{alpha}*\bar{z} + d = 0

    where c and d are real numbers and alpha is complex.
    """

    def __init__(self, c=0.0, alpha=0.0 + 0.0j, d=0.0):
        r"""Initialize a cline with its equation parameters.

        Args:
            c (float): Real coefficient of z\bar{z}
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
            z0 (complex or tuple): First point, either complex number or tuple (real, imag)
            z1 (complex or tuple): Second point, either complex number or tuple (real, imag)
            z2 (complex or tuple): Third point, either complex number or tuple (real, imag)

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

    @classmethod
    def from_line(cls, z0, z1):
        r"""Construct a cline representing a line through two points.

        Args:
            z0 (complex or tuple): First point, either complex number or tuple (real, imag)
            z1 (complex or tuple): Second point, either complex number or tuple (real, imag)

        Returns:
            Cline: A cline representing the line through z0 and z1

        For a line, we set c = 0, and the parameters are calculated as:
            - alpha = i*(z1 - z0) (perpendicular to the line direction)
            - d = -2*Re(alpha*z0)
        """
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

        # Check if points are distinct
        if abs(z1 - z0) < 1e-10:
            raise ValueError("Points must be distinct to define a line")

        # For a line, set c = 0
        c = 0.0

        # Calculate alpha = i*(z₁ - z₀)
        alpha = 1j * (z1 - z0)

        # Calculate d = -2*Re(alpha*z0)
        d = -2 * np.real(alpha * z0)

        # Create the cline and store the points
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

        For a circle, we set c = 1, and the parameters are calculated as:
            - alpha = -center
            - d = |center|^2 - radius^2
        """
        # Convert center to complex number
        if isinstance(center, tuple):
            center = complex(center[0], center[1])
        else:
            center = complex(center)

        # Validate radius
        radius = float(radius)
        if radius <= 0:
            raise ValueError("Radius must be positive")

        # For a circle, set c = 1
        c = 1.0

        # Calculate alpha = -center
        alpha = -center

        # Calculate d = |center|^2 - radius^2
        d = abs(center) ** 2 - radius**2

        # Create the cline
        cline = cls(c=c, alpha=alpha, d=d)

        # Store the center and radius for reference
        cline.center = center
        cline.radius = radius

        return cline

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
