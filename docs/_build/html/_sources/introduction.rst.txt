Introduction
============

What is a Cline?
---------------

A **cline** is a mathematical concept that unifies circles and lines in the complex plane under a single equation:

.. math::

   c z \bar{z} + \alpha z + \bar{\alpha} \bar{z} + d = 0

where:

- :math:`c` and :math:`d` are real numbers
- :math:`\alpha` is a complex number
- :math:`\bar{z}` and :math:`\bar{\alpha}` represent the complex conjugates of :math:`z` and :math:`\alpha`

This geometric structure represents:

- A circle if :math:`|\alpha|^2 > c \cdot d` and :math:`c \neq 0`
- A point if :math:`|\alpha|^2 = c \cdot d` and :math:`c \neq 0`
- A line if :math:`c = 0`
- No geometric object if :math:`|\alpha|^2 < c \cdot d` and :math:`c \neq 0`

Visual Representation
--------------------

Below is a visualization showing examples of clines in the complex plane:

.. plot::
    :include-source: false
    :context: close-figs

    import matplotlib.pyplot as plt
    from cline import Cline
    import numpy as np

    # Create a figure
    fig, ax = plt.subplots(figsize=(8, 6))

    # Create several clines
    circle1 = Cline.from_circle(center=0, radius=2)
    circle2 = Cline.from_circle(center=2+1j, radius=1.5)

    # For lines, we need to ensure we're using correct parameters
    line1 = Cline.from_line(z0=-3+0j, z1=3+0j)  # Horizontal line
    line2 = Cline.from_line(z0=0-3j, z1=0+3j)   # Vertical line

    # Plot all clines
    circle1.plot(ax=ax, color='royalblue', label='Circle 1')
    circle2.plot(ax=ax, color='cornflowerblue', label='Circle 2')
    line1.plot(ax=ax, color='firebrick', label='Line 1')
    line2.plot(ax=ax, color='indianred', label='Line 2')

    # Customize the plot
    ax.set_xlim(-3, 4)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.title('Examples of Clines in the Complex Plane')
    plt.legend(loc='upper right')

Features
--------

The **Cline** library provides:

1. **Unified Representation**: Represent both circles and lines with a single class
2. **Multiple Construction Methods**:
   - From three points
   - From circle center and radius
   - From two points (for a line)
   - From direct equation parameters
3. **Easy Access to Properties**:
   - Circle center and radius
   - Line normal and direction vectors
   - Distance from origin
4. **Visualization**: Plot circles and lines using Matplotlib

Mathematical Foundation
-----------------------

For a circle with center :math:`z_0` and radius :math:`r`, the cline parameters are:

- :math:`c = 1`
- :math:`\alpha = -z_0`
- :math:`d = |z_0|^2 - r^2`

For a line with normal vector :math:`n` at distance :math:`\rho` from the origin, the cline parameters are:

- :math:`c = 0`
- :math:`\alpha = i \cdot n`
- :math:`d = -2\rho |n|`

Why Use Clines?
--------------

Clines provide several advantages:

- **Unified Treatment**: Algorithms can work with both circles and lines
- **Transformation Properties**: Clines transform elegantly under Möbius transformations
- **Algebraic Simplicity**: Representing complex geometric relationships with simple equations
