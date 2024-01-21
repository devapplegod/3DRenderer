import math


# 15.14
def get_ellipse_points(center_x, center_y, major_axis, minor_axis, rotation_degrees, n_points):
    rotation_angle_radians = math.radians(rotation_degrees)
    points = []

    for i in range(n_points):
        theta = 2 * math.pi * i / n_points  # Current angle in radians
        x = major_axis * math.cos(theta)
        y = minor_axis * math.sin(theta)

        # Rotation transformation
        x_rotated = x * math.cos(rotation_angle_radians) - y * math.sin(rotation_angle_radians)
        y_rotated = x * math.sin(rotation_angle_radians) + y * math.cos(rotation_angle_radians)

        # Translate the point to the ellipse's center
        x_rotated += center_x
        y_rotated += center_y

        points.append([x_rotated, y_rotated])

    return points
