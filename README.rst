.. image:: https://travis-ci.org/congma/polygon-inclusion.svg?branch=master
    :target: https://travis-ci.org/congma/polygon-inclusion

Summary
-------

Polygon inclusion algorithm based on the winding number.

The module provides a class, ``PolygonRegion``, that implements the
winding-number count, based on the algorithm description by Dan Sunday. `[SUN]`_


Examples
--------

(Taken from the class docstring.)

A simple polygon with 4 vertices.

>>> import numpy as np
>>> np.set_printoptions(formatter={"bool": str, "int": str})
>>> points = np.array(((1.0, -1.0, -1.0,  1.0),
...                    (1.0,  1.0, -1.0, -1.0)))
>>> poly = PolygonRegion(points)
>>> print(poly.winding_number(np.array((0.0, 0.0))))
1
>>> print(poly.winding_number(np.array(((0.5, 1.5,  0.9),
...                                     (0.5, 0.5, -0.1)))))
... # doctest: +NORMALIZE_WHITESPACE
[1 0 1]

A self-intersecting polygon.

>>> points = np.array(((1.0, -2.0, -2.0,  2.0, 2.0, -1.0, -1.0,  1.0),
...                    (2.0,  2.0, -2.0, -2.0, 1.0,  1.0, -1.0, -1.0)))
>>> poly = PolygonRegion(points)
>>> print(poly.winding_number(np.array((0.0, 0.0))))
2
>>> print(poly.contains(np.array(((0.0, 1.5),
...                               (0.0, 1.5)))))
... # doctest: +NORMALIZE_WHITESPACE
[True False]

Reversing the orientation of the polygon.

>>> points = points[::-1, :]
>>> poly = PolygonRegion(points)
>>> print(poly.winding_number(np.array((0.0, 0.0))))
-2

A polygon with a simple hole inside.

>>> points = np.array(((2.0, -2.0, -2.0,  2.0, 1.0,  1.0, -1.0, -1.0),
...                    (2.0,  2.0, -2.0, -2.0, 1.0, -1.0, -1.0,  1.0)))
>>> poly = PolygonRegion(points)
>>> print(poly.winding_number(np.array((0.0, 0.0))))
0


Notes
-----

The current implementation is a pure-Python one utilizing ``numpy``. The
``winding_number()`` method does not use the ``if`` (branch) statement, which
is costly in the Python code.  The implementation should work reasonably well
for the usage pattern where the polygon region is fixed but the number of
points to be tested for inclusion is large.

In the context of SVG files, the definition for a point being "inside" the
polygon based on the winding number corresponds to the ``nonzero`` option for
the ``fill-rule`` attribute of ``<polygon>`` (and similar) elements.  `[MDN]`_
The other rule, ``evenodd``, is equivalent to the "crossing number" rule
described as an alternative definition in `[SUN]`_.


.. _[SUN]: https://geomalgorithms.com/a03-_inclusion.html
.. _[MDN]: https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fill-rule#nonzero
