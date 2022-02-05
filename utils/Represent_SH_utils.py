import math
import numpy as np
import sympy as sym

# Calculate Associated Legendre Polynomial Matrix and calculate the complex Spherical Harmonic Matrix
# Returns the complex Spherical Harmonic Matrix and The meshgrid of PHI and THETA (Azimuthal and polar angles)
def get_SH(l,m):
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
    return Y_lm, PHI, THETA


# Convert polar coordinates to cartesian coordinates
# Theta 0 to pi
def get_cart_vertices(r,phi,theta):
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return x, y, z


# Depending on the type returns the correspondig form oh the Spherical Harmonics Matrix
def check_type(Type, Y_lm):
    if Type == 'Abs':
        R = np.abs(Y_lm.astype(complex))
    elif Type == 'Real':
        R = Y_lm.astype(complex).real
    elif Type == 'Imag':
        R = Y_lm.astype(complex).imag
    return R

# Calls functions get_SH(), check_type() and get_cart_vertices() to return the cartesian coordinates of the mayavi mesh, depending on the type of representation selected
# Also returns the Spherical harmonic function matrix in the correct form to be used has surface color
def get_xyz(l,m,Type,Repres):
    Y_lm, PHI, THETA = get_SH(l,m)
    R = check_type(Type, Y_lm)
    if Repres == 'Y_lm':
        x, y, z = get_cart_vertices(abs(R),PHI,THETA)
    elif Repres == 'US':
        x, y, z = get_cart_vertices(1,PHI,THETA)
    elif Repres == 'Y_lm+1':
        x, y, z = get_cart_vertices(1+R,PHI,THETA)
    return x,y,z,R


