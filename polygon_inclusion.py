"""Polygon inclusion algorithm based on the winding number.

Reference:
    Dan Sunday, "Inclusion of a point in a polygon".
    <https://geomalgorithms.com/a03-_inclusion.html>
"""


import numpy as np


class PolygonRegion:
    """Fixed polygon region constructed from a sequence of points.

    Attributes
    ----------
        v
            Two-dimensional array of vertices, shaped (2, N), where each column
            is a vertex point, and either row a dimension.

        lb, ub
            Lower- and upper-bounding box coordinates. Each of ``lb`` or ``ub``
            is a (2, 1) array where the first row contains the minimum and the
            last row the maximum.

        e
            Array for edges, shaped (2, N). The edges are arranged in the order
            of the vertices' appearance as specified when the polygon is
            constructed.

    Public methods
    --------------
        winding_number(points)
            Calculates the winding number of the polygon with respect to the
            input points.

        contains(points)
            Polygon inclusion test based on the winding number.

    Examples
    --------
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
    """
    def __init__(self, vertices):
        """Initialize polygon with sequence of vertices.

        Arguments
        ---------
            vertices
                Array of vertices in the shape (2, N), where each column refers
                to a vertex and either row a spatial (planar) dimension.
        """
        assert np.ndim(vertices) == 2
        sh = np.shape(vertices)
        assert sh[0] == 2
        assert sh[1] >= 3
        xmin, ymin = np.min(vertices, axis=1)
        xmax, ymax = np.max(vertices, axis=1)
        # Array of vertices; each column is a vertex and each row a dimension.
        self.v = np.hstack((vertices, vertices[:, 0].reshape(2, 1)))
        # Bounding box.
        self.lb = np.array([[xmin], [ymin]])    # "lower left"
        self.ub = np.array([[xmax], [ymax]])    # "upper right"
        # Edge vectors in the order specified by the input vertex sequence.
        self.e = np.diff(self.v)    # shaped (2, __len__)
        # Edge vectors with y-coordinates reversed and (x, y)-order flipped.
        ie = self.e.copy()
        ie[1] *= -1.0
        self._ie = np.ascontiguousarray(ie[::-1, :])
        # Set the internal data arrays read-only.
        for array in (self.v, self.lb, self.ub, self.e, self._ie):
            array.flags.writeable = False

    def __len__(self):
        return self.e.shape[-1]

    def winding_number(self, points):
        """Calculates the winding numbers of the polygon with respect to the
        input points.

        Arguments
        ---------
            points
                Input array representing N points, i. e. ndarray shaped (2, N),
                where each column refers to an input point and each row is a
                planar dimension.

        Return value
        ------------
            wn
                One-dimensional array of integers with length N, where the i-th
                element is the winding number of the i-th input point.
                Counter-clockwise winding is positive.

                The type of ``wn`` degenerates to a zero-dimensional array if
                the input is a single point specified as one-dimensinal,
                length-two array.
        """
        pp = np.atleast_2d(points).reshape(2, -1)
        del_tails = pp.T[:, None] - self.v[:, :-1].T  # shaped (n, m, 2)
        b1 = del_tails[:, :, 1] >= 0.0
        b2 = np.less.outer(pp[1], self.v[1, 1:])
        sides = np.sign(np.einsum("ijk, kj -> ij", del_tails, self._ie))
        wn_pos = (b1 & b2 & (sides > 0)).sum(axis=1, dtype=int)
        wn_neg = (~b1 & ~b2 & (sides < 0)).sum(axis=1, dtype=int)
        wn = wn_pos - wn_neg
        if len(wn) == 1:
            return wn[0]
        return wn

    def contains(self, points):
        """Polygon inclusion test.

        Arguments
        ---------
            points
                Input array representing N points, i. e. ndarray shaped (2, N),
                where each column refers to an input point and each row is a
                planar dimension.

        Return value
        ------------
            mask
                One-dimensional array of booleans with length N, where the i-th
                element is the truth value of the i-th input point's inclusion
                in the polygon.

                The type of ``mask`` degenerates to a zero-dimensional array if
                the input is a single point specified as one-dimensinal,
                length-two array.
        """
        p = np.asarray(points, dtype=np.float64)
        return self.winding_number(p) != 0


__all__ = ["PolygonRegion"]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
