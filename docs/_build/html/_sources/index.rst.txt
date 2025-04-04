Welcome to Cline's documentation!
================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   introduction
   installation
   usage
   api
   examples

Cline
=====

A Python library for representing circles and lines in the complex plane using the general cline equation.

Overview
--------

A cline is a circle or line that can be represented by the equation:

.. math::

   c z \bar{z} + \alpha z + \bar{\alpha} \bar{z} + d = 0

where:

- c and d are real numbers
- alpha is a complex number
- It's a circle if :math:`|\alpha|^2 > c \cdot d` and :math:`c \neq 0`
- It's a line if :math:`c = 0`
- It's a point if :math:`|\alpha|^2 = c \cdot d` and :math:`c \neq 0`

This unified representation allows for elegant manipulation of both circles and lines in the complex plane.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
