# Cline

A Python library for representing circles and lines in the complex plane using the general cline equation.

## Overview

A cline is a circle or line that can be represented by the equation:

cz\bar(z) + alpha*z + \bar(alpha)*\bar(z) + d = 0

where:
- c and d are real numbers
- alpha is a complex number
- It's a circle if |alpha|^2 > c*d and c ≠ 0
- It's a line if c = 0
- It's a point if |alpha|^2 = c*d and c ≠ 0

This unified representation allows for elegant manipulation of both circles and lines in the complex plane.

## Installation

```bash
pip install cline
```

## Usage

### Creating Clines

```python
from cline import Cline
import matplotlib.pyplot as plt

# Create a circle with center at 1+2j and radius 3
circle = Cline.from_circle(center=1+2j, radius=3)

# Create a line passing through two points
line = Cline.from_line(z0=0, z1=1+1j)

# Create a cline passing through three points
# (This will be a circle if the points are not collinear)
cline = Cline.from_three_points(z0=0, z1=1, z2=1j)

# Create a cline directly using the equation parameters
custom_cline = Cline(c=1.0, alpha=-3-4j, d=16)
```

### Accessing Cline Properties

```python
# For circles
print(f"Center: {circle.center}, Radius: {circle.radius}")

# For lines
print(f"Normal vector: {line.normal_vector}")
print(f"Direction vector: {line.direction_vector}")
print(f"Distance from origin: {line.distance_from_origin}")
```

### Visualizing Clines

```python
# Plot multiple clines on the same figure
fig, ax = plt.subplots(figsize=(8, 8))

# Plot with default settings
circle.plot(ax=ax, color='blue', label='Circle')

# Customize appearance
line.plot(
    ax=ax,
    color='red',
    label='Line',
    xlim=(-5, 5),
    ylim=(-5, 5),
    point_color='green'
)

plt.legend()
plt.show()
```

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
- Visualization using Matplotlib
- Mathematical operations (coming soon)

## Requirements

- Python 3.6+
- NumPy
- Matplotlib

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
