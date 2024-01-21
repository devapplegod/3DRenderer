import math

import pygame
from pygame.locals import *
from OpenGL.GL import *

from cube import Cube
from square import Square


def draw_point(x, y, color):
    glBegin(GL_POINTS)
    glColor3f(*color)
    glVertex2f(x, y)
    glEnd()


def draw_line(x1, y1, x2, y2, color):
    glBegin(GL_LINES)
    glColor3f(*color)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()


def draw_line_thick(x1, y1, x2, y2, line_thickness, color):
    dx = y2 - y1
    dy = x1 - x2
    length = (dx**2 + dy**2)**0.5
    dx /= length
    dy /= length

    glBegin(GL_QUADS)
    glColor3f(*color)

    glVertex2f(x1 - dx * line_thickness, y1 - dy * line_thickness)
    glVertex2f(x1 + dx * line_thickness, y1 + dy * line_thickness)
    glVertex2f(x2 + dx * line_thickness, y2 + dy * line_thickness)
    glVertex2f(x2 - dx * line_thickness, y2 - dy * line_thickness)
    glEnd()


def draw_circle(center_x, center_y, radius, num_segments, color):
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(*color)
    glVertex2f(center_x, center_y)
    for i in range(num_segments + 1):
        theta = (2 * math.pi * i) / num_segments
        x = radius * math.cos(theta) + center_x
        y = radius * math.sin(theta) + center_y
        glVertex2f(x, y)
    glEnd()


def draw_rectangle(x1, y1, x2, y2, line_thickness, color):
    draw_line_thick(x1, y1, x2, y1, line_thickness, color)
    draw_line_thick(x2, y1, x2, y2, line_thickness, color)
    draw_line_thick(x2, y2, x1, y2, line_thickness, color)
    draw_line_thick(x1, y2, x1, y1, line_thickness, color)


def draw_square_center(center_x, center_y, side_length, line_thickness, color):
    half_length = side_length / 2.0
    x1 = center_x - half_length
    x2 = center_x + half_length
    y1 = center_y - half_length
    y2 = center_y + half_length
    draw_rectangle(x1, y1, x2, y2, line_thickness, color)


SQRT_2 = 1.41421


def rotate_coords(current_x, current_y, angle_radians):
    x = current_x * math.cos(angle_radians) - current_y * math.sin(angle_radians)
    y = current_y * math.cos(angle_radians) + current_x * math.sin(angle_radians)
    return x, y


def draw_rotate_square(center_x, center_y, side_length, line_thickness, color, angle_radians):
    half_length = side_length / 2
    a_x = -half_length
    a_y = -half_length
    b_x = a_x + side_length
    b_y = a_y
    c_x = b_x
    c_y = b_y + side_length
    d_x = a_x
    d_y = c_y

    a_x, a_y = rotate_coords(a_x, a_y, angle_radians)
    b_x, b_y = rotate_coords(b_x, b_y, angle_radians)
    c_x, c_y = rotate_coords(c_x, c_y, angle_radians)
    d_x, d_y = rotate_coords(d_x, d_y, angle_radians)
    a_x, b_x, c_x, d_x = a_x+center_x, b_x+center_x, c_x+center_x, d_x+center_x
    a_y, b_y, c_y, d_y = a_y+center_y, b_y+center_y, c_y+center_y, d_y+center_y

    draw_line(a_x, a_y, b_x, b_y, color)
    draw_line(a_x, a_y, d_x, d_y, color)
    draw_line(c_x, c_y, d_x, d_y, color)
    draw_line(c_x, c_y, b_x, b_y, color)


PI_HALF_ANGLE_SIDE_LENGTH_CONST = 0.35355


def draw_cube_origin(origin_x, origin_y, side_length, line_thickness, color):
    back_point_offset = side_length * PI_HALF_ANGLE_SIDE_LENGTH_CONST
    a_x = origin_x
    a_y = origin_y
    b_x = a_x + side_length
    b_y = a_y
    c_x = b_x
    c_y = b_y + side_length
    d_x = a_x
    d_y = c_y

    a2_x = a_x + back_point_offset
    a2_y = a_y + back_point_offset
    b2_x = a2_x + side_length
    b2_y = a2_y
    c2_x = b2_x
    c2_y = b2_y + side_length
    d2_x = a2_x
    d2_y = c2_y

    draw_rectangle(a_x, a_y, c_x, c_y, line_thickness, color)
    draw_rectangle(a2_x, a2_y, c2_x, c2_y, line_thickness, color)

    draw_line_thick(a_x, a_y, a2_x, a2_y, line_thickness, color)
    draw_line_thick(b_x, b_y, b2_x, b2_y, line_thickness, color)
    draw_line_thick(c_x, c_y, c2_x, c2_y, line_thickness, color)
    draw_line_thick(d_x, d_y, d2_x, d2_y, line_thickness, color)


def draw_cube_center(center_x, center_y, side_length, line_thickness, color, should_draw_center):
    half_length = side_length / 2.0
    front_back_point_offset = side_length * PI_HALF_ANGLE_SIDE_LENGTH_CONST * 1/2
    # OFFSET_FROM_CENTER_CLOSER = (half_length) * (1 + PI_HALF_ANGLE_SIDE_LENGTH_CONST)
    # OFFSET_FROM_CENTER_FARTHER = (half_length) * (1 - PI_HALF_ANGLE_SIDE_LENGTH_CONST)
    a_x = center_x - half_length - front_back_point_offset
    a_y = center_y - half_length - front_back_point_offset
    b_x = a_x + side_length
    b_y = a_y
    c_x = b_x
    c_y = b_y + side_length
    d_x = a_x
    d_y = c_y

    a2_x = center_x - half_length + front_back_point_offset
    a2_y = center_y - half_length + front_back_point_offset
    b2_x = a2_x + side_length
    b2_y = a2_y
    c2_x = b2_x
    c2_y = b2_y + side_length
    d2_x = a2_x
    d2_y = c2_y

    draw_rectangle(a_x, a_y, c_x, c_y, line_thickness, color)
    draw_rectangle(a2_x, a2_y, c2_x, c2_y, line_thickness, color)

    draw_line_thick(a_x, a_y, a2_x, a2_y, line_thickness, color)
    draw_line_thick(b_x, b_y, b2_x, b2_y, line_thickness, color)
    draw_line_thick(c_x, c_y, c2_x, c2_y, line_thickness, color)
    draw_line_thick(d_x, d_y, d2_x, d2_y, line_thickness, color)

    if should_draw_center:
        # draw_circle(center_x, center_y, 3, 100, [60, 214, 63])
        draw_cube_center(center_x, center_y - half_length, 15, 1, [63/255, 214/255, 60/255], False)


def draw_ellipse(center_x, center_y, a, b, num_segments, color):
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(*color)
    for i in range(num_segments):
        theta = 2 * math.pi * i / num_segments
        x = a * math.cos(theta) + center_x
        y = b * math.sin(theta) + center_y
        glVertex2f(x, y)
    glEnd()


def draw_all_points(points, color):
    for point in points:
        draw_point(int(point[0]), int(point[1]), color)


pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

glClearColor(0.0, 0.0, 0.0, 1.0)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, display[0], 0, display[1], -1, 1)
glMatrixMode(GL_MODELVIEW)

paused = False
last_frame = None

major_const = 1.39897
minor_const = 0.55681

square = Square(400, 300, 0, 200, [1, 0, 0], [0, 0, 300])
cube = Cube(400, 300, 0, 200, [0, 0, 1], [0, 0, 300])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    if not paused:
        cube.rotate_y_axis_radians(2 * math.pi / 360)
        cube.draw()
        square.rotate_y_axis_radians(2 * math.pi / 360)
        square.draw()
    else:
        cube.draw()
        square.draw()

    pygame.display.flip()
    pygame.time.wait(10)
