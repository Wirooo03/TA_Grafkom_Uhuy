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
selected_index = -1  # objek aktif untuk transformasi

# Menyimpan semua objek dan properti transformasi
objects = []

def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    gluOrtho2D(0, window_width, 0, window_height)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    for idx, obj in enumerate(objects):
        glPushMatrix()
        glColor3f(*obj['color'])
        glLineWidth(obj['line_width'])

        # Terapkan transformasi
        tx, ty = obj['translate']
        glTranslatef(tx, ty, 0)

        cx, cy = get_center(obj['coords'])
        glTranslatef(cx, cy, 0)
        glRotatef(obj['rotation'], 0, 0, 1)
        sx, sy = obj['scale']
        glScalef(sx, sy, 1)
        glTranslatef(-cx, -cy, 0)

        # Gambar bentuk
        tipe = obj['type']
        if tipe == 'point':
            draw_point(*obj['coords'])
        elif tipe == 'line':
            draw_line(*obj['coords'])
        elif tipe == 'square':
            draw_square(*obj['coords'])
        elif tipe == 'ellipse':
            draw_ellipse(*obj['coords'])

        glPopMatrix()
    glFlush()

def get_center(coords):
    if len(coords) == 2: return coords  # titik
    x1, y1, x2, y2 = coords
    return ((x1 + x2) / 2, (y1 + y2) / 2)

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

def draw_square(x1, y1, x2, y2):
    glBegin(GL_LINE_LOOP)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()

def draw_ellipse(x1, y1, x2, y2):
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    rx = abs(x2 - x1) / 2
    ry = abs(y2 - y1) / 2
    glBegin(GL_LINE_LOOP)
    for i in range(100):
        angle = 2 * pi * i / 100
        glVertex2f(cx + rx * cos(angle), cy + ry * sin(angle))
    glEnd()

def mouse_click(button, state, x, y):
    global clicks, selected_index
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        x = x
        y = window_height - y
        clicks.append((x, y))

        if mode == 'point':
            objects.append({
                'type': 'point',
                'coords': (x, y),
                'color': color,
                'line_width': line_width,
                'rotation': 0,
                'scale': (1, 1),
                'translate': (0, 0)
            })
            selected_index = len(objects) - 1
            clicks = []

        elif len(clicks) == 2:
            x1, y1 = clicks[0]
            x2, y2 = clicks[1]
            tipe = mode
            objects.append({
                'type': tipe,
                'coords': (x1, y1, x2, y2),
                'color': color,
                'line_width': line_width,
                'rotation': 0,
                'scale': (1, 1),
                'translate': (0, 0)
            })
            selected_index = len(objects) - 1
            clicks = []

        glutPostRedisplay()

def keyboard(key, x, y):
    global mode, color, line_width, selected_index, clicks
    key = key.decode('utf-8').lower()
    clicks = []

    if key == '1': mode = 'point'
    elif key == '2': mode = 'line'
    elif key == '3': mode = 'square'
    elif key == '4': mode = 'ellipse'
    elif key == 'r': color = (1, 0, 0)
    elif key == 'g': color = (0, 1, 0)
    elif key == 'b': color = (0, 0, 1)
    elif key == 'k': color = (0, 0, 0)
    elif key == '+': line_width = min(line_width + 1, 10)
    elif key == '-': line_width = max(line_width - 1, 1)
    elif key == '\t':  # tab untuk ganti objek aktif
        if objects:
            selected_index = (selected_index + 1) % len(objects)
            print(f"Objek aktif: #{selected_index+1}")

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

    print(f"Mode: {mode} | Warna: {color} | Ketebalan: {line_width}")
    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Aplikasi 2D Transformasi - PyOpenGL")
    init()
    glutDisplayFunc(display)
    glutMouseFunc(mouse_click)
    glutKeyboardFunc(keyboard)
    glutMainLoop()

if __name__ == "__main__":
    main()
