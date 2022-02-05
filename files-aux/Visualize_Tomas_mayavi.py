from mayavi import mlab
import math
import numpy as np
import sympy as sym

def visualize(l,m):

    n = 200
    phi = np.linspace(0, 2 * np.pi, n)
    theta = np.linspace(0, np.pi, n)
    [PHI, THETA] = np.meshgrid(phi, theta)

    a = np.sqrt(((2 * l + 1) / (4 * np.pi)) * (((math.factorial(l - abs(m))) / (math.factorial(l + abs(m))))))

    s = sym.Symbol('s')

    G = (s ** 2 - 1) ** l

    H = (1 - s ** 2) ** (abs(m) / 2)
    P_lm = ((-1) ** abs(m) / (math.factorial(l) * (2 ** l))) * H * sym.diff(G, s, abs(m) + l)

    P_lm = sym.lambdify(s, P_lm)
    Y_lm = a * np.exp(1j * abs(m) * PHI) * P_lm(np.cos(THETA))
    if m<0: Y_lm = (-1)**m * Y_lm.conj()
    Y_lm_real = Y_lm.astype(complex).real
    Y_lm_imag = Y_lm.astype(complex).imag
    Y_lm_abs = np.abs(Y_lm.astype(complex))

    r = 1
    x = r*np.sin(THETA) * np.cos(PHI)
    y = r*np.sin(THETA) * np.sin(PHI)
    z = r*np.cos(THETA)

    x11 = (r+Y_lm_real) * np.sin(THETA) * np.cos(PHI)
    y11 = (r+Y_lm_real) * np.sin(THETA) * np.sin(PHI)
    z11 = (r+Y_lm_real) * np.cos(THETA)

    x22 = (r+Y_lm_imag) * np.sin(THETA) * np.cos(PHI)
    y22 = (r+Y_lm_imag) * np.sin(THETA) * np.sin(PHI)
    z22 = (r+Y_lm_imag) * np.cos(THETA)

    x33 = (r+Y_lm_abs) * np.sin(THETA) * np.cos(PHI)
    y33 = (r+Y_lm_abs) * np.sin(THETA) * np.sin(PHI)
    z33 = (r+Y_lm_abs) * np.cos(THETA)

    x1 = abs(Y_lm_real) * np.sin(THETA) * np.cos(PHI)
    y1 = abs(Y_lm_real) * np.sin(THETA) * np.sin(PHI)
    z1 = abs(Y_lm_real) * np.cos(THETA)

    x2 = abs(Y_lm_imag) * np.sin(THETA) * np.cos(PHI)
    y2 = abs(Y_lm_imag) * np.sin(THETA) * np.sin(PHI)
    z2 = abs(Y_lm_imag) * np.cos(THETA)

    x3 = Y_lm_abs * np.sin(THETA) * np.cos(PHI)
    y3 = Y_lm_abs * np.sin(THETA) * np.sin(PHI)
    z3 = Y_lm_abs * np.cos(THETA)

    #############################
    scale = 3

    dx31 = scale*x3.max() - scale*x1.min() + 1
    d = x.max() - x.min() + 1
    if d > dx31:
        dx31 = d
    d = x33.max() - x11.min() + 1
    if d > dx31:
        dx31 = d
    
    dx12 = scale*x1.max() - scale*x2.min() + 1
    d = x.max() - x.min() + 1
    if d > dx12:
        dx12 = d
    d = x11.max() - x22.min() + 1
    if d > dx12:
        dx12 = d
    
    dz1 = -scale*z3.min() + z.max() + 2
    d = -scale*z1.min() + z.max() + 2
    if d > dz1:
        dz1 = d
    d = -scale*z2.min() + z.max() + 2
    if d > dz1:
        dz1 = d
    
    dz2 = -z.min() + z33.max() + 2
    d = -z.min() + z11.max() + 2
    if d > dz2:
        dz2 = d
    d = -z.min() + z22.max() + 2
    if d > dz2:
        dz2 = d
    
    ##############################

    mlab.figure(1, bgcolor=(1, 1, 1), size=(1000, 900))
    mlab.clf()

    mlab.mesh(x3*scale, y3*scale, z3*scale, scalars=Y_lm_abs, colormap='jet')

    mlab.mesh((x1*scale+dx31), y1*scale, z1*scale, scalars=Y_lm_real, colormap='jet')

    mlab.mesh(x2*scale+dx31+dx12, y2*scale, z2*scale, scalars=Y_lm_imag, colormap='jet')

    mlab.mesh(x, y, z-dz1, scalars=Y_lm_abs, colormap='jet')

    mlab.mesh(x+dx31, y, z-dz1, scalars=Y_lm_real, colormap='jet')

    if m != 0:
        mlab.mesh(x+dx31+dx12, y, z-dz1, scalars=Y_lm_imag, colormap='jet')

    mlab.mesh(x33, y33, z33-dz1-dz2, scalars=Y_lm_abs, colormap='jet')

    mlab.mesh(x11+dx31, y11, z11-dz1-dz2, scalars=Y_lm_real, colormap='jet')
    
    if m != 0:
        mlab.mesh(x22+dx31+dx12, y22, z22-dz1-dz2, scalars=Y_lm_imag, colormap='jet')

    mlab.text3d(-0.2, 0, scale*z3.max()+1, 'Abs', scale=(0.2, 0.2, 0.2), color=(0,0,0))
    mlab.text3d(-0.2+dx31, 0, scale*z3.max()+1, 'Re', scale=(0.2, 0.2, 0.2), color=(0,0,0))
    mlab.text3d(-0.2+dx31+dx12, 0, scale*z3.max()+1, 'Im', scale=(0.2, 0.2, 0.2), color=(0,0,0))

    mlab.text3d(scale*x3.min()-2.5, 0, 0, 'R=Ylm', scale=(0.2, 0.2, 0.2), color=(0,0,0))
    mlab.text3d(scale*x3.min()-2.5, 0, -dz1, 'Unit Sphere', scale=(0.2, 0.2, 0.2), color=(0,0,0))
    mlab.text3d(scale*x3.min()-2.5, 0, -dz1-dz2, 'R=(1+Ylm)', scale=(0.2, 0.2, 0.2), color=(0,0,0))

    mlab.view(-85,85,30)
    mlab.show()


if __name__ == "__main__":
    l = 2
    m = 1
    visualize(l,m)