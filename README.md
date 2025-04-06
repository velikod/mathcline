# Cline

A Python library for representing circles and lines in the complex plane using the general _cline_ equation.

The inspiration for this package comes from the open source book [Geometry with an Introduction to Cosmic Topology](https://mphitchman.com/geometry/preface.html) by Michael P. Hitchman, which is a fascinating introduction to non-Euclidean geometries following the Erlangen program. The approach in the book relies heavily on Möbius transformations and their effects on _clines_.

## Documentation

Full documentation is available at: [https://velikod.github.io/mathcline](https://velikod.github.io/mathcline)

## Overview

A cline is a circle or line that can be represented by the unified equation:

```math
cz\bar{z} + \alpha z + \bar{\alpha}\bar{z} + d = 0
```

where:
- $c$ and $d$ are real numbers
- $\alpha$ is a complex number

Based on the discriminant $\Delta = |\alpha|^2 - c \cdot d$, a cline represents:
- A circle if $\Delta > 0$ and $c \neq 0$
- A point if $\Delta = 0$ and $c \neq 0$
- A line if $c = 0$
- An invalid geometric object (no solutions) if $\Delta < 0$ and $c \neq 0$

## Mathematical Formulation

### Circle Representation
When $\Delta > 0$ and $c \neq 0$, the cline is a circle with:
- Center: $z_0 = -\frac{\alpha}{c}$
- Radius: $r = \frac{\sqrt{|\alpha|^2 - c \cdot d}}{|c|}$

### Line Representation
When $c = 0$, the cline is a line with:
- Normal vector: $\alpha = a + bi$
- Direction vector: $v = b - ai$ (perpendicular to normal)
- Cartesian form: $ax - by + \frac{d}{2} = 0$

### Three-Point Construction
The library provides a method to construct a cline from three points, automatically determining whether to create a circle or a line by checking if the points are collinear.

## Installation (not yet published as a package)


## Features

- Unified representation of circles and lines using the cline equation
- Create clines from various inputs:
  - Circle from center and radius
  - Line from two points
  - Any cline from three points
  - Directly from equation parameters (e.g., `Cline(c=1, d=1, alpha=2+1j)`)
- Easy access to geometric properties:
  - Circle center and radius
  - Line normal and direction vectors
  - Distance from origin
- Visualization using Matplotlib with automatic window calibration
- Comprehensive mathematical derivations and formulations
- Detailed documentation with LaTeX-rendered equations

## Examples

```python
from cline import Cline
import matplotlib.pyplot as plt

# Create a cline directly from parameters
c1 = Cline(c=1, alpha=2+1j, d=1)

# Create a circle from center and radius
c2 = Cline.from_circle(center=1+2j, radius=2)

# Create a line from two points
c3 = Cline.from_line(0, 1+1j)

# Create a cline from three points
c4 = Cline.from_three_points(0, 1, 2j)

# Plot the clines
fig, ax = plt.subplots(figsize=(10, 10))
c1.plot(ax=ax, color='red', label='Parameters c=1, α=2+j, d=1')
c2.plot(ax=ax, color='blue', label='Circle center=1+2j, radius=2')
c3.plot(ax=ax, color='green', label='Line through 0 and 1+j')
c4.plot(ax=ax, color='purple', label='Cline through 0, 1, and 2j')
plt.legend()
plt.show()
```

## Requirements

- Python 3.6+
- NumPy
- Matplotlib


## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
