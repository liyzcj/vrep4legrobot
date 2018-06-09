__author__ = 'li yan zhe'

import numpy as np
import math


def get_axis(axis):
    if axis == "x":
        return [1, 0, 0]
    if axis == "y":
        return [0, 1, 0]
    if axis == "z":
        return [0, 0, 1]
    else:
        return axis


def distance(a, b):
    return math.sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2 + (b[2]-a[2])**2)


def rotate_around_center(matrix, axis, theta):
    axis = get_axis(axis)
    axis = np.asarray(axis)
    theta = np.asarray(theta)
    axis = axis/math.sqrt(np.dot(axis, axis))
    a = math.cos(theta/2)
    b, c, d = -axis*math.sin(theta/2)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    rot = np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
                    [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
                    [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])
    return np.dot(rot, matrix)


def rotate(matrix, axis, theta, center=None):
    """
    Implement rotation.
    :param matrix:
    :param axis:
    :param theta:
    :param center:
    :return:
    """
    if not center:
        center = np.matrix([[0], [0], [0]])
    else:
        center = np.matrix(center)
    matrix = np.matrix(matrix)
    if matrix.shape[0] == 1:
        matrix = np.transpose(matrix)

    if center.shape[0] == 1:
        center = np.transpose(center)

    dislocated = np.subtract(matrix, center)
    rotated = rotate_around_center(dislocated, axis, theta)
    relocated = np.add(rotated, center)
    return relocated
