# Cline

A Python library for representing circles and lines in the complex plane using the general cline equation.

## Overview

A cline is a circle or line that can be represented by the equation:

```math
cz\bar{z} + \alpha z + \bar{\alpha}\bar{z} + d = 0
```

where:
- $c$ and $d$ are real numbers
- $\alpha$ is a complex number
- It's a circle if $|\alpha|^2 > c \cdot d$ and $c \neq 0$
- It's a line if $c = 0$
- It's a point if $|\alpha|^2 = c \cdot d$ and $c \neq 0$

This unified representation allows for elegant manipulation of both circles and lines in the complex plane.

## Installation

```bash
pip install cline
```

## Usage

### Creating Clines from Equation Parameters

```python
from cline import Cline

# Create a cline directly using the equation parameters
# c=1, d=1, alpha=2+1j
custom_cline = Cline(c=1.0, alpha=2+1j, d=1.0)
print(custom_cline)

# Plot the cline - automatic window calculation based on geometry
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(8, 8))
custom_cline.plot(ax=ax, color='blue', label='Circle')
plt.legend()
plt.show()
```

### Creating Circles

```python
from cline import Cline
import matplotlib.pyplot as plt

# Create a circle with center at 1+2j and radius 3
circle = Cline.from_circle(center=1+2j, radius=3)

# Access circle properties
print(f"Center: {circle.center}, Radius: {circle.radius}")
```

### Creating Lines

```python
# Create a line passing through two points
line = Cline.from_line(z0=0, z1=1+1j)

# Access line properties
print(f"Normal vector: {line.normal_vector}")
print(f"Direction vector: {line.direction_vector}")
print(f"Distance from origin: {line.distance_from_origin}")
```

### Creating Clines from Three Points

```python
# Create a cline passing through three points
# (This will be a circle if the points are not collinear)
cline = Cline.from_three_points(z0=0, z1=1, z2=1j)
```

### Visualizing Clines

```python
# Plot multiple clines on the same figure
fig, ax = plt.subplots(figsize=(8, 8))

# Plot circle and line - limits automatically calculated
circle.plot(ax=ax, color='blue', label='Circle')
line.plot(ax=ax, color='red', label='Line')

# Add legend and show
plt.legend()
plt.show()
```

## Mathematical Formulation

### Circle Representation

When $c \neq 0$ and $|\alpha|^2 > c \cdot d$, the equation represents a circle with:

```math
\text{center} = -\frac{\alpha}{c}
```

```math
\text{radius} = \frac{\sqrt{|\alpha|^2 - cd}}{|c|}
```

### Line Representation

When $c = 0$, the equation becomes:

```math
\alpha z + \bar{\alpha}\bar{z} + d = 0
```

which can be rewritten in Cartesian form as:

```math
a\cdot x - b \cdot y + \frac{d}{2} = 0
```

where $\alpha = a + bi$, and:
- Normal vector: $\alpha$
- Direction vector: $b - ia$ (perpendicular to normal)
- Distance from origin: $\frac{|d|}{2|\alpha|}$

### From Three Points

Given three points $z_0$, $z_1$, and $z_2$ in the complex plane, we can construct a cline:

1. If the points are collinear:
   - Set $c = 0$ (representing a line)
   - Calculate $\alpha = i(z_1 - z_0)$ perpendicular to the line direction
   - Solve for $d = -2\text{Re}(\alpha z_0)$

2. If the points are not collinear:
   - Set $c = 1$ (representing a circle)
   - Solve a linear system of equations for $\alpha$ and $d$

## Features

- Unified representation of circles and lines using the cline equation
- Create clines from various inputs:
  - Circle from center and radius
  - Line from two points
  - Any cline from three points
  - Directly from equation parameters
- Easy access to geometric properties:
  - Circle center and radius
  - Line normal and direction vectors
  - Distance from origin
- Visualization using Matplotlib with automatic window calculation
- Comprehensive mathematical derivations in the documentation

## Requirements

- Python 3.6+
- NumPy
- Matplotlib

## Documentation

Full documentation is available at: [https://velikod.github.io/mathcline](https://velikod.github.io/mathcline)

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
