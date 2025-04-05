# Cline

A Python library for representing circles and lines in the complex plane using the general _cline_ equation.

The inspiration for this package comes from the open source book [Geometry with an Introduction to Cosmic Topology](https://mphitchman.com/geometry/preface.html) by Michael P. Hitchman, which is a fascinating introduction to non-Euclidean geometries following the Erlangen program. The approach in the book relies heavily on Möbius transformations and their effects on _clines_.

## Documentation

Full documentation is available at: [https://velikod.github.io/mathcline](https://velikod.github.io/mathcline)

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

## Installation (not yet published as a package)



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


## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
