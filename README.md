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

### Creating Clines from Equation Parameters

```python
from cline import Cline

# Create a cline directly using the equation parameters
# This represents a circle with center at 3+4j and radius 5
custom_cline = Cline(c=1.0, alpha=-3-4j, d=16)
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
- Mathematical operations (coming soon)

## Requirements

- Python 3.6+
- NumPy
- Matplotlib

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
