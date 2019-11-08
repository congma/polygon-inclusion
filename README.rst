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
...                                (0.0, 1.5)))))
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


.. _[SUN]: https://geomalgorithms.com/a03-_inclusion.html
