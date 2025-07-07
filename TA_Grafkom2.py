from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

camera_pos = [0, 0, 10]
rotation = [0, 0]

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Lighting
    ambient = [0.2, 0.2, 0.2, 1.0]
    diffuse = [0.8, 0.8, 0.8, 1.0]
    specular = [1.0, 1.0, 1.0, 1.0]
    position = [3.0, 3.0, 3.0, 1.0]

    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    glLightfv(GL_LIGHT0, GL_POSITION, position)

    glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
    glMateriali(GL_FRONT, GL_SHININESS, 100)

    glClearColor(0.1, 0.1, 0.1, 1.0)
    glShadeModel(GL_SMOOTH)

def draw_cube():
    glColor3f(1.0, 0.6, 0.2)
    glBegin(GL_QUADS)

    # Sisi-sisi kubus dengan normal
    normals = [
        (0, 0, 1), (0, 0, -1),
        (1, 0, 0), (-1, 0, 0),
        (0, 1, 0), (0, -1, 0)
    ]
    vertices = [
        [(-1, -1,  1), ( 1, -1,  1), ( 1,  1,  1), (-1,  1,  1)],  # depan
        [(-1, -1, -1), (-1,  1, -1), ( 1,  1, -1), ( 1, -1, -1)],  # belakang
        [( 1, -1, -1), ( 1,  1, -1), ( 1,  1,  1), ( 1, -1,  1)],  # kanan
        [(-1, -1, -1), (-1, -1,  1), (-1,  1,  1), (-1,  1, -1)],  # kiri
        [(-1,  1, -1), (-1,  1,  1), ( 1,  1,  1), ( 1,  1, -1)],  # atas
        [(-1, -1, -1), ( 1, -1, -1), ( 1, -1,  1), (-1, -1,  1)]   # bawah
    ]

    for i in range(6):
        glNormal3fv(normals[i])
        for vertex in vertices[i]:
            glVertex3fv(vertex)

    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
              0, 0, 0, 0, 1, 0)

    glRotatef(rotation[0], 1, 0, 0)
    glRotatef(rotation[1], 0, 1, 0)

    draw_cube()
    glutSwapBuffers()

def reshape(w, h):
    if h == 0: h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w / h, 1, 100)
    glMatrixMode(GL_MODELVIEW)

def keyboard(key, x, y):
    global camera_pos
    step = 0.5
    if key == b'w': camera_pos[2] -= step
    if key == b's': camera_pos[2] += step
    if key == b'a': camera_pos[0] -= step
    if key == b'd': camera_pos[0] += step
    if key == b'q': camera_pos[1] += step
    if key == b'e': camera_pos[1] -= step
    glutPostRedisplay()

def special_keys(key, x, y):
    if key == GLUT_KEY_UP: rotation[0] -= 5
    if key == GLUT_KEY_DOWN: rotation[0] += 5
    if key == GLUT_KEY_LEFT: rotation[1] -= 5
    if key == GLUT_KEY_RIGHT: rotation[1] += 5
    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Kontrol Kamera + Pencahayaan 3D")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutMainLoop()

if __name__ == "__main__":
    main()
