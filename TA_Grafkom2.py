from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

# Posisi kamera
eyeX, eyeY, eyeZ = 5.0, 3.0, 5.0

# Transformasi objek
angle_x, angle_y = 0, 0
translate_x, translate_y = 0, 0

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Pencahayaan
    ambient = [0.2, 0.2, 0.2, 1.0]
    diffuse = [0.5, 0.5, 0.5, 1.0]
    specular = [1.0, 1.0, 1.0, 1.0]
    position = [5.0, 5.0, 5.0, 1.0]

    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    glLightfv(GL_LIGHT0, GL_POSITION, position)

    glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
    glMateriali(GL_FRONT, GL_SHININESS, 50)

def draw_pyramid():
    glBegin(GL_TRIANGLES)

    # Sisi depan
    glNormal3f(0.0, 0.5, 0.5)
    glVertex3f( 0.0, 1.0, 0.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)

    # Sisi kanan
    glNormal3f(0.5, 0.5, 0.0)
    glVertex3f( 0.0, 1.0, 0.0)
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0,-1.0)

    # Sisi belakang
    glNormal3f(0.0, 0.5, -0.5)
    glVertex3f( 0.0, 1.0, 0.0)
    glVertex3f( 1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)

    # Sisi kiri
    glNormal3f(-0.5, 0.5, 0.0)
    glVertex3f( 0.0, 1.0, 0.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0, 1.0)

    glEnd()

    # Alas (quad)
    glBegin(GL_QUADS)
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(-1.0, -1.0,  1.0)
    glVertex3f( 1.0, -1.0,  1.0)
    glVertex3f( 1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glEnd()

def display():
    global eyeX, eyeY, eyeZ
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Kamera
    gluLookAt(eyeX, eyeY, eyeZ, 0, 0, 0, 0, 1, 0)

    glTranslatef(translate_x, translate_y, 0)
    glRotatef(angle_x, 1, 0, 0)
    glRotatef(angle_y, 0, 1, 0)

    draw_pyramid()

    glutSwapBuffers()

def reshape(w, h):
    if h == 0:
        h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w / h, 1, 100)
    glMatrixMode(GL_MODELVIEW)

def keyboard(key, x, y):
    global translate_x, translate_y
    global eyeX, eyeY, eyeZ

    # Translasi objek
    if key == b'w':
        translate_y += 0.1
    elif key == b's':
        translate_y -= 0.1
    elif key == b'a':
        translate_x -= 0.1
    elif key == b'd':
        translate_x += 0.1

    # Kamera manual
    elif key == b'i':  # Zoom in (mendekat)
        eyeZ -= 0.2
    elif key == b'k':  # Zoom out (menjauh)
        eyeZ += 0.2
    elif key == b'j':  # Geser kamera ke kiri
        eyeX -= 0.2
    elif key == b'l':  # Geser kamera ke kanan
        eyeX += 0.2
    elif key == b'u':  # Kamera ke atas
        eyeY += 0.2
    elif key == b'o':  # Kamera ke bawah
        eyeY -= 0.2

    glutPostRedisplay()

def special_keys(key, x, y):
    global angle_x, angle_y
    if key == GLUT_KEY_UP:
        angle_x -= 5
    elif key == GLUT_KEY_DOWN:
        angle_x += 5
    elif key == GLUT_KEY_LEFT:
        angle_y -= 5
    elif key == GLUT_KEY_RIGHT:
        angle_y += 5
    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"3D Transformasi & Kamera")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutMainLoop()

if __name__ == "__main__":
    main()
