# Aplikasi Transformasi 2D + Windowing + Clipping Lengkap

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import cos, sin, pi
import sys

window_width, window_height = 800, 600
mode = 'point'
clicks = []
color = (0, 0, 0)
line_width = 1
selected_index = -1
objects = []

# Window
window_rect = None  # (x1, y1, x2, y2)
window_clicks = []

INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 4, 8

def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    gluOrtho2D(0, window_width, 0, window_height)

def compute_outcode(x, y, rect):
    x_min, y_min, x_max, y_max = rect
    code = INSIDE
    if x < x_min: code |= LEFT
    elif x > x_max: code |= RIGHT
    if y < y_min: code |= BOTTOM
    elif y > y_max: code |= TOP
    return code

def cohen_sutherland_clip(x1, y1, x2, y2, rect):
    outcode1 = compute_outcode(x1, y1, rect)
    outcode2 = compute_outcode(x2, y2, rect)
    while True:
        if not (outcode1 | outcode2):
            return x1, y1, x2, y2
        elif outcode1 & outcode2:
            return None
        else:
            outcode_out = outcode1 or outcode2
            x, y = 0, 0
            x_min, y_min, x_max, y_max = rect
            if outcode_out & TOP:
                x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                y = y_max
            elif outcode_out & BOTTOM:
                x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                y = y_min
            elif outcode_out & RIGHT:
                y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                x = x_max
            elif outcode_out & LEFT:
                y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                x = x_min
            if outcode_out == outcode1:
                x1, y1 = x, y
                outcode1 = compute_outcode(x1, y1, rect)
            else:
                x2, y2 = x, y
                outcode2 = compute_outcode(x2, y2, rect)

def draw_point(x, y):
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def draw_line(x1, y1, x2, y2):
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def draw_square_clipped(x1, y1, x2, y2, rect):
    xmin, ymin, xmax, ymax = rect
    x1, x2 = max(min(x1, x2), xmin), min(max(x1, x2), xmax)
    y1, y2 = max(min(y1, y2), ymin), min(max(y1, y2), ymax)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()

def draw_ellipse_clipped(x1, y1, x2, y2, rect):
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    rx = abs(x2 - x1) / 2
    ry = abs(y2 - y1) / 2
    xmin, ymin, xmax, ymax = rect
    glBegin(GL_LINE_STRIP)
    for i in range(100):
        angle = 2 * pi * i / 100
        x = cx + rx * cos(angle)
        y = cy + ry * sin(angle)
        if xmin <= x <= xmax and ymin <= y <= ymax:
            glVertex2f(x, y)
    glEnd()

def get_center(coords):
    if len(coords) == 2: return coords
    x1, y1, x2, y2 = coords
    return ((x1 + x2) / 2, (y1 + y2) / 2)

def display():
    glClear(GL_COLOR_BUFFER_BIT)

    if window_rect:
        x1, y1, x2, y2 = window_rect
        glColor3f(1, 0, 0)
        glLineWidth(1)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x1, y1)
        glVertex2f(x2, y1)
        glVertex2f(x2, y2)
        glVertex2f(x1, y2)
        glEnd()

    for obj in objects:
        glPushMatrix()
        tx, ty = obj['translate']
        glTranslatef(tx, ty, 0)
        cx, cy = get_center(obj['coords'])
        glTranslatef(cx, cy, 0)
        glRotatef(obj['rotation'], 0, 0, 1)
        sx, sy = obj['scale']
        glScalef(sx, sy, 1)
        glTranslatef(-cx, -cy, 0)

        tipe = obj['type']
        coords = obj['coords']
        glLineWidth(obj['line_width'])

        if window_rect:
            glColor3f(0, 1, 0)
            if tipe == 'point':
                x, y = coords
                if compute_outcode(x, y, window_rect) == 0:
                    draw_point(x, y)
            elif tipe == 'line':
                clipped = cohen_sutherland_clip(*coords, window_rect)
                if clipped:
                    draw_line(*clipped)
            elif tipe == 'square':
                draw_square_clipped(*coords, window_rect)
            elif tipe == 'ellipse':
                draw_ellipse_clipped(*coords, window_rect)
        else:
            glColor3f(*obj['color'])
            if tipe == 'point': draw_point(*coords)
            elif tipe == 'line': draw_line(*coords)
            elif tipe == 'square': draw_square_clipped(*coords, (0, 0, window_width, window_height))
            elif tipe == 'ellipse': draw_ellipse_clipped(*coords, (0, 0, window_width, window_height))

        glPopMatrix()

    glFlush()

def mouse_click(button, state, x, y):
    global clicks, selected_index, window_clicks, window_rect
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        x = x
        y = window_height - y
        if mode == 'window':
            window_clicks.append((x, y))
            if len(window_clicks) == 2:
                x1, y1 = window_clicks[0]
                x2, y2 = window_clicks[1]
                window_rect = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
                window_clicks = []
        else:
            clicks.append((x, y))
            if mode == 'point':
                objects.append({'type': 'point', 'coords': (x, y), 'color': color,
                                'line_width': line_width, 'rotation': 0,
                                'scale': (1, 1), 'translate': (0, 0)})
                selected_index = len(objects) - 1
                clicks = []
            elif len(clicks) == 2:
                x1, y1 = clicks[0]
                x2, y2 = clicks[1]
                objects.append({'type': mode, 'coords': (x1, y1, x2, y2), 'color': color,
                                'line_width': line_width, 'rotation': 0,
                                'scale': (1, 1), 'translate': (0, 0)})
                selected_index = len(objects) - 1
                clicks = []
        glutPostRedisplay()

def keyboard(key, x, y):
    global mode, color, line_width, selected_index, clicks, window_rect
    key = key.decode('utf-8').lower()
    clicks = []
    if key == '1': mode = 'point'
    elif key == '2': mode = 'line'
    elif key == '3': mode = 'square'
    elif key == '4': mode = 'ellipse'
    elif key == 'o': mode = 'window'
    elif key == 'c': window_rect = None
    elif window_rect:
        x1, y1, x2, y2 = window_rect
        if key == 'l': window_rect = (x1 + 10, y1, x2 + 10, y2)
        elif key == 'j': window_rect = (x1 - 10, y1, x2 - 10, y2)
        elif key == 'i': window_rect = (x1, y1 + 10, x2, y2 + 10)
        elif key == 'k': window_rect = (x1, y1 - 10, x2, y2 - 10)
        elif key == 'u': window_rect = (x1 + 10, y1 + 10, x2 - 10, y2 - 10)
        elif key == 'p': window_rect = (x1 - 10, y1 - 10, x2 + 10, y2 + 10)
    elif key == 'r': color = (1, 0, 0)
    elif key == 'g': color = (0, 1, 0)
    elif key == 'b': color = (0, 0, 1)
    elif key == 'k': color = (0, 0, 0)
    elif key == '+': line_width = min(line_width + 1, 10)
    elif key == '-': line_width = max(line_width - 1, 1)
    elif key == '\t':
        if objects:
            selected_index = (selected_index + 1) % len(objects)
    elif selected_index != -1:
        obj = objects[selected_index]
        if key == 'w': obj['translate'] = (obj['translate'][0], obj['translate'][1] + 10)
        elif key == 's': obj['translate'] = (obj['translate'][0], obj['translate'][1] - 10)
        elif key == 'a': obj['translate'] = (obj['translate'][0] - 10, obj['translate'][1])
        elif key == 'd': obj['translate'] = (obj['translate'][0] + 10, obj['translate'][1])
        elif key == 'q': obj['rotation'] += 10
        elif key == 'e': obj['rotation'] -= 10
        elif key == 'z': obj['scale'] = (obj['scale'][0] * 1.1, obj['scale'][1] * 1.1)
        elif key == 'x': obj['scale'] = (obj['scale'][0] * 0.9, obj['scale'][1] * 0.9)
    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Transformasi 2D + Clipping")
    init()
    glutDisplayFunc(display)
    glutMouseFunc(mouse_click)
    glutKeyboardFunc(keyboard)
    glutMainLoop()

if __name__ == "__main__":
    main()
