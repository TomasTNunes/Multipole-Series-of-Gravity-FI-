import os
import numpy as np
import math
import sympy as sym
import pandas as pd

# Calculate and return the Series of Spherical harmonics Matrix using the columns of the basis matrix
def get_series_SH(coeff, l_max, PHI, THETA, basis_matrix):  
    f = PHI * 0
    for l in range(l_max+1):
        for m in range(-l,l+1):
            j = l**2 + l + m
            #f = f + coeff[l][m+l] * get_spherical_harmonic(l, m, PHI, THETA).astype(complex).real
            f = f + coeff[l][m+l] * basis_matrix[:,j]
    return f


# Calculate Associated Legendre Polynomial Matrix and calculate the complex Spherical Harmonic Matrix
# Returns the complex Spherical Harmonic Matrix
def get_spherical_harmonic(l, m, PHI, THETA):
    a = np.sqrt(((2 * l + 1) / (4 * np.pi)) * (((math.factorial(l - abs(m))) / (math.factorial(l + abs(m))))))
    s = sym.Symbol('s')
    G = (s ** 2 - 1) ** l
    H = (1 - s ** 2) ** (abs(m) / 2)
    P_lm = ((-1) ** abs(m) / (math.factorial(l) * (2 ** l))) * H * sym.diff(G, s, abs(m) + l)
    P_lm = sym.lambdify(s, P_lm)
    Y_lm = a * np.exp(1j * abs(m) * PHI) * P_lm(np.cos(THETA))
    if m<0: Y_lm = (-1)**m * Y_lm.conj()
    return Y_lm


# Get and return the matrix of Vertices and matrix of Faces from data file, using body name
def get_Vertices_Faces(Body_name):
    folder = Body_name.split('-')[0]
    OBJ = pd.read_csv(f'data/Repres_BS-data/{folder}/{Body_name}.OBJ', delim_whitespace=True, \
                                    names=['TYPE', 'X1', 'X2', 'X3'])

    VERTICES = OBJ.loc[OBJ['TYPE'] == 'v'][['X1', 'X2', 'X3']].values \
                .tolist()

    FACES = OBJ.loc[OBJ['TYPE'] == 'f'][['X1', 'X2', 'X3']].values
    FACES = FACES - 1
    FACES = FACES.astype(int)
    FACES = FACES.tolist()
    return VERTICES, FACES


# Convert polar coordinates to cartesian coordinates
# Theta 0 to pi
# Return the cartesian coordinates in The VERTICES matrix
def get_cart_vertices(r, phi, theta):
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)

    VERTICES = np.zeros((len(x),3)) 
    VERTICES[:,0] = x
    VERTICES[:,1] = y
    VERTICES[:,2] = z
    return VERTICES

# Convert cartesian coordinates to polar coordinates
# Theta 0 to pi
# Phi -pi to pi
# returns polar coordinates
def get_polar_vertices(VERTICES):
    N = len(VERTICES)
    r = np.tile(0.0, N)
    theta = np.tile(0.0, N)
    phi = np.tile(0.0, N)
    for i in range(N):
        r[i] = np.sqrt(VERTICES[i][0]**2 + VERTICES[i][1]**2 + VERTICES[i][2]**2)
        theta[i] = np.arccos(VERTICES[i][2]/r[i]) # beteween 0 and PI
        phi[i] = math.atan2(VERTICES[i][1],VERTICES[i][0]) # beteween -PI and PI
    return r, theta, phi


# Calculates and returns basis_matrix using lmax selected and get_spherical_harmonic() function
def get_basis_matrix(phi, theta, l_max):
    k = (l_max+1)**2
    basis_matrix = np.zeros((len(phi),k)) # dtype=np.complex128 onde ha np.zero
    for l in range(l_max+1):
        for m in range(-l,l+1):
            j = l**2 + l + m
            basis_matrix[:,j] = get_spherical_harmonic(l, m, phi, theta).astype(complex).real
    return basis_matrix


# Apply Least Square Method and return coefficients and residual error
def get_coeff_least_square(A, f):
    f = f.reshape(len(f),1)
    B = A.T @ A
    if np.linalg.det(B) == 0:
        coeff = np.linalg.pinv(B) @ A.T @ f
    else:
        coeff = np.linalg.inv(B) @ A.T @ f
    residual_error = f - A @ coeff
    return coeff, residual_error


# Converts coefficient vector to a matrix
def vector2matrix (vector, l_max):
    k = 0
    matrix = np.zeros((l_max+1, 2*l_max+1))
    for i in range(l_max+1):
        for j in range(1+2*i):
            matrix[i][j] = vector[k]
            k = k+1
    return matrix


# saves data file with body name, lmax, VERTICES and FACES
def save_SH_file(lmax, Body_name, VERTICES, FACES):
    FACES = np.array(FACES) + 1
    f = open(f'data/Repres_BS-data/{Body_name}/{Body_name}-lmax{lmax}.OBJ', 'w')
    for i in range(len(VERTICES)):
        f.write(f'v {VERTICES[i][0]} {VERTICES[i][1]} {VERTICES[i][2]}\n')
    for i in range(len(FACES)):
        f.write(f'f {FACES[i][0]} {FACES[i][1]} {FACES[i][2]}\n')
    f.close()


# return true if data file of lmax of a body exists
def check_body_file_exists(lmax, Body_name):
    return os.path.isfile(f'data/{Body_name}/{Body_name}-lmax{lmax}.OBJ')


# Calls get_polar_vertices(), get_basis_matrix(), get_coeff_least_square(), vector2matrix(),...
# get_series_SH() and get_cart_vertices() to calculate VERT_SH
# Return VERT_SH
def get_VERT_SH(VERTICES, l_max):
    r_Ver, theta_Ver, phi_Ver = get_polar_vertices(VERTICES)
    Basis_Matrix = get_basis_matrix(phi_Ver, theta_Ver, l_max)
    coeff_LS, res_error_LS = get_coeff_least_square(Basis_Matrix, r_Ver)
    coeff_LS_matrix = vector2matrix(coeff_LS, l_max)
    f = get_series_SH(coeff_LS_matrix, l_max, phi_Ver, theta_Ver, Basis_Matrix)
    VERT_SH = get_cart_vertices(f, phi_Ver, theta_Ver)
    return VERT_SH
