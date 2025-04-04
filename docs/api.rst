API Reference
==============

Cline Module
-----------

.. automodule:: cline
   :members:
   :undoc-members:
   :show-inheritance:
   :noindex:

Cline Class
~~~~~~~~~~~

.. autoclass:: cline.Cline
   :members:
   :undoc-members:
   :special-members: __init__
   :exclude-members: _format_complex, _format_float
   :noindex:

Mathematical Formulation
~~~~~~~~~~~~~~~~~~~~~~~

A cline is represented by the equation:

.. math::

   c z \bar{z} + \alpha z + \bar{\alpha} \bar{z} + d = 0

where:

- :math:`c` and :math:`d` are real numbers
- :math:`\alpha` is a complex number
- :math:`\bar{z}` and :math:`\bar{\alpha}` represent complex conjugates

The cline represents:

- A circle if :math:`|\alpha|^2 > c \cdot d` and :math:`c \neq 0`
- A point if :math:`|\alpha|^2 = c \cdot d` and :math:`c \neq 0`
- A line if :math:`c = 0`
- Not a geometric object if :math:`|\alpha|^2 < c \cdot d` and :math:`c \neq 0`
