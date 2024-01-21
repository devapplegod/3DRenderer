from OpenGL.GL import *
import math


class Cube:
    def __init__(self, center_x, center_y, center_z, side_length, color, camera_location):
        self.center_x = center_x
        self.center_y = center_y
        self.center_z = center_z
        self.side_length = side_length
        self.half_length = self.side_length / 2
        self.color = color
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        self.camera_location = camera_location
        self.nodes = [[-self.half_length, -self.half_length, -self.half_length],
                      [self.half_length, -self.half_length, -self.half_length],
                      [self.half_length, self.half_length, -self.half_length],
                      [-self.half_length, self.half_length, -self.half_length],

                      [-self.half_length, self.half_length, self.half_length],
                      [-self.half_length, -self.half_length, self.half_length],
                      [self.half_length, -self.half_length, self.half_length],
                      [self.half_length, self.half_length, self.half_length]]
        self.edges = [[0, 1], [1, 2], [2, 3], [3, 0],
                      [0, 5], [5, 6], [6, 7], [7, 4],
                      [4, 3], [7, 2], [6, 1], [4, 5]]

    def set_color(self, color_rgb):
        self.color = color_rgb

    def rotate_z_axis_radians(self, angle_radians):
        self.angle_z = angle_radians
        for node in self.nodes:
            x, y = node[0], node[1]
            node[0] = x * math.cos(self.angle_z) - y * math.sin(self.angle_z)
            node[1] = y * math.cos(self.angle_z) + x * math.sin(self.angle_z)

    def rotate_y_axis_radians(self, angle_radians):
        self.angle_y = angle_radians
        for node in self.nodes:
            x, z = node[0], node[2]
            node[0] = x * math.cos(self.angle_y) + z * math.sin(self.angle_y)
            node[2] = z * math.cos(self.angle_y) - x * math.sin(self.angle_y)

    def rotate_x_axis_radians(self, angle_radians):
        self.angle_x = angle_radians
        for node in self.nodes:
            y, z = node[1], node[2]
            node[1] = y * math.cos(self.angle_x) - z * math.sin(self.angle_x)
            node[2] = z * math.cos(self.angle_x) + y * math.sin(self.angle_x)

    def perspective(self, node):
        x_cam, y_cam, z_cam = self.camera_location[0], self.camera_location[1], self.camera_location[2]
        x_node, y_node, z_node = node[0], node[1], node[2]
        distance = math.sqrt((x_cam - x_node) ** 2 + (y_cam - y_node) ** 2 + (z_cam - z_node) ** 2)
        scaleFactor = z_cam / distance
        new_node = [scaleFactor * x_node, scaleFactor * y_node, z_node]
        return new_node

    def __line(self, x1, y1, z1, x2, y2, z2):
        glBegin(GL_LINES)
        glColor3f(*self.color)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
        glEnd()

    def draw(self):
        for edge in self.edges:
            n = self.edges.index(edge)
            n0 = self.edges[n][0]
            n1 = self.edges[n][1]
            node0 = self.perspective(self.nodes[n0])
            node1 = self.perspective(self.nodes[n1])
            x1, y1, z1, x2, y2, z2 = node0[0], node0[1], node0[2], node1[0], node1[1], node1[2]
            self.__line(x1 + self.center_x, y1 + self.center_y, z1 + self.center_z, x2 + self.center_x, y2 + self.center_y, z2 + self.center_z)
